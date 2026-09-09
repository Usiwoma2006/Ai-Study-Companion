from django.urls import path, include
from rest_framework.routers import DefaultRouter

from notebooks.views import AnswerSubmissionView, ChatView, DocumentListDeleteView, NotebookViewSet, ProgressAnalysisView, QuizView, ResearchView, StudyPlanView

router = DefaultRouter()
router.register(r'', NotebookViewSet, basename='notebook')

urlpatterns = [
    path(
        'quizzes/<uuid:quiz_id>/questions/<uuid:question_id>/answer/',
        AnswerSubmissionView.as_view(),
        name='submit-answer',
    ),
    path(
        '<int:notebook_id>/documents/',
        DocumentListDeleteView.as_view(),
        name='document-list',
    ),
    path(
        '<int:notebook_id>/documents/<int:document_id>/',
        DocumentListDeleteView.as_view(),
        name='document-delete',
    ),
    path("<int:notebook_id>/chat/", ChatView.as_view(), name="notebook-chat"),
    path("<int:notebook_id>/quiz/", QuizView.as_view(), name="notebook-quiz"),
    path("<int:notebook_id>/study-plan/", StudyPlanView.as_view(), name="notebook-study-plan"),
    path("<int:notebook_id>/research/", ResearchView.as_view(), name="notebook-research"),
    path("<int:notebook_id>/progress/", ProgressAnalysisView.as_view(), name="notebook-progress"),
    path('', include(router.urls)),
]