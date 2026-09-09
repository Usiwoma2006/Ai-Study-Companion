from xmlrpc.client import FastParser


from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from agents.services.tutor_service import run_tutor
from agents.services.quiz_service import run_quiz
from agents.services.study_planner_service import run_study_planner
from agents.services.research_service import run_research
from agents.services.progress_analysis_service import run_progress_analysis
from retrieval.services.retrieve_rerank_compress import retrieve_rerank_compress

from .models import ChatMessage, Notebook, Document, Quiz
from .serializers import NotebookSerializer
from .permissions import IsNotebookOwner
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
 
from notebooks.models import QuizQuestion
from notebooks.serializers import AnswerSubmissionSerializer, DocumentSerializer
from ingestion.services.pipeline import process_document


def _summarize_quiz_performance(questions):
    total = questions.count()
    answered = questions.exclude(student_answer__isnull=True).exclude(student_answer="")
    answered_count = answered.count()
    correct = sum(1 for question in answered if question.is_correct)

    return {
        "total_questions": total,
        "answered_questions": answered_count,
        "unanswered_questions": total - answered_count,
        "correct_answers": correct,
        "incorrect_answers": answered_count - correct,
        "accuracy_percentage": round(correct / answered_count * 100, 2)
        if answered_count else 0,
    }


class NotebookViewSet(viewsets.ModelViewSet):
    serializer_class = NotebookSerializer
    permission_classes = [IsAuthenticated, IsNotebookOwner]

    def get_queryset(self):
        return Notebook.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AnswerSubmissionView(APIView):
    """
    POST /api/quizzes/<quiz_id>/questions/<question_id>/answer/
 
    Handles ONE student answering ONE question, exactly once.
    """
 
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id, question_id):
        question = get_object_or_404(
            QuizQuestion,
            id=question_id,
            quiz_id=quiz_id,
        )

        if question.quiz.notebook.owner != request.user:
            return Response(
                {"detail": "You do not have permission to answer this question."},
                status=status.HTTP_403_FORBIDDEN,
        )

        if question.student_answer:
            return Response(
                {"detail": "This question has already been answered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AnswerSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submitted_answer = serializer.validated_data["answer"]

        if submitted_answer not in question.options:
            return Response(
                {"detail": "Submitted answer is not a valid option for this question."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        question.student_answer = submitted_answer
        question.answered_at = timezone.now()
        question.save()

        return Response(
            {
                "question_id": str(question.id),
                "your_answer": question.student_answer,
                "is_correct": question.is_correct,
                "correct_answer": question.correct_answer,
                "citation": question.citation,
            },
            status=status.HTTP_200_OK,
        )

class DocumentListDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, notebook_id):
        notebook = get_object_or_404(
            Notebook,
            id=notebook_id,
            owner=request.user,
        )
        documents = notebook.documents.all()
        return Response(DocumentSerializer(documents, many=True).data)

    def post(self, request, notebook_id):
        # DEBUG: Print the notebook_id and user info
        print("DEBUG notebook_id:", notebook_id, type(notebook_id))
        print("DEBUG request.user:", request.user, request.user.id)
        
        notebook = get_object_or_404(
            Notebook,
            id=notebook_id,
            owner=request.user,
        )
        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save(notebook=notebook)

        process_document(document.id)

        return Response(
            DocumentSerializer(document).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, notebook_id, document_id):
        notebook = get_object_or_404(
            Notebook,
            id=notebook_id,
            owner=request.user,
        )
        document = get_object_or_404(
            Document,
            id=document_id,
            notebook=notebook,
        )
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, notebook_id):
        notebook = get_object_or_404(
            Notebook,
            id=notebook_id,
            owner=request.user,
        )
        messages = notebook.chat_messages.order_by("created_at")
        return Response(
            [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
        )

    def post(self, request, notebook_id):
        notebook = get_object_or_404(
            Notebook,
            id=notebook_id,
            owner=request.user,
        )

        query = request.data.get("query", "").strip()
        if not query:
            return Response(
                {"error": "query is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # pull recent history, oldest → newest, shaped for run_tutor
        recent_messages = notebook.chat_messages.order_by("-created_at")[:20]
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(recent_messages)
        ]

        retrieved_context = retrieve_rerank_compress(query, notebook_id)

        answer = run_tutor(query, chat_history, retrieved_context)

        ChatMessage.objects.create(notebook=notebook, role="user", content=query)
        ChatMessage.objects.create(notebook=notebook, role="assistant", content=answer)

        return Response({"answer": answer}, status=status.HTTP_200_OK)


class QuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notebook_id):
        notebook = get_object_or_404(Notebook, id=notebook_id, owner=request.user)

        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)

        recent_messages = notebook.chat_messages.order_by("-created_at")[:20]
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(recent_messages)
        ]

        retrieved_context = retrieve_rerank_compress(query, notebook_id)
        questions_string, answer_key = run_quiz(query, chat_history, retrieved_context)

        if answer_key is None:
            return Response({"error": questions_string}, status=status.HTTP_502_BAD_GATEWAY)

        if not answer_key:
            return Response(
                {"error": "No quiz questions could be generated from the available context."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        quiz = Quiz.objects.create(notebook=notebook, query=query)
        for i, q in enumerate(answer_key, start=1):
            QuizQuestion.objects.create(
                quiz=quiz,
                order=i,
                question_text=q["question"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                citation=q.get("citation", ""),
            )

        return Response(
            {
                "quiz_id": str(quiz.id),
                "questions": [
                    {
                        "id": str(q.id),
                        "order": q.order,
                        "question_text": q.question_text,
                        "options": q.options,
                    }
                    for q in quiz.questions.order_by("order")
                ],
            },
            status=status.HTTP_201_CREATED,
        )

class StudyPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notebook_id):
        notebook = get_object_or_404(Notebook, id=notebook_id, owner=request.user)

        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)

        recent_messages = notebook.chat_messages.order_by("-created_at")[:20]
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(recent_messages)
        ]

        retrieved_context = retrieve_rerank_compress(query, notebook_id)
        plan = run_study_planner(query, chat_history, retrieved_context)

        return Response({"plan": plan}, status=status.HTTP_200_OK)

class ResearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notebook_id):
        notebook = get_object_or_404(Notebook, id=notebook_id, owner=request.user)

        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)

        recent_messages = notebook.chat_messages.order_by("-created_at")[:20]
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(recent_messages)
        ]

        retrieved_context = retrieve_rerank_compress(query, notebook_id)
        answer = run_research(query, chat_history, retrieved_context)

        return Response({"answer": answer}, status=status.HTTP_200_OK)

class ProgressAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notebook_id):
        notebook = get_object_or_404(Notebook, id=notebook_id, owner=request.user)

        recent_messages = notebook.chat_messages.order_by("-created_at")[:40]
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(recent_messages)
        ]

        questions = QuizQuestion.objects.filter(quiz__notebook=notebook)
        quiz_summary = _summarize_quiz_performance(questions)

        analysis = run_progress_analysis(
            query="Analyze my learning progress based on our conversation history and quiz performance.",
            chat_history=chat_history,
            retrieved_context=[],
            quiz_summary=quiz_summary,
        )

        return Response({"analysis": analysis}, status=status.HTTP_200_OK)