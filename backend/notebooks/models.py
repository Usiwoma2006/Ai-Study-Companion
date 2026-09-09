from django.conf import settings
from django.db import models
from pgvector.django import VectorField
import uuid


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Notebook(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notebooks',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class Document(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        READY = 'ready', 'Ready'
        FAILED = 'failed', 'Failed'

    notebook = models.ForeignKey(
        Notebook,
        on_delete=models.CASCADE,
        related_name='documents',
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=50, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class Chunk(TimeStampedModel):
    notebook = models.ForeignKey(
        Notebook,
        on_delete=models.CASCADE,
        related_name='chunks',
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='chunks',
    )
    content = models.TextField()
    embedding = VectorField(dimensions=1024)
    page_number = models.PositiveIntegerField(null=True, blank=True)
    chunk_index = models.PositiveIntegerField()
    section_title = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['document', 'chunk_index']
        indexes = [
            models.Index(fields=['notebook', 'document']),
            models.Index(fields=['document', 'chunk_index']),
        ]

    def __str__(self):
        return f'Chunk {self.chunk_index} of {self.document.title}'


class Quiz(models.Model):
    """One generated quiz — created when quiz_agent runs, read back later
    when the student submits answers."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name="quizzes")
    query = models.TextField()  # the original request that generated this quiz
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz {self.id} for notebook {self.notebook_id}"


class QuizQuestion(models.Model):
    """One question within a Quiz, with the correct answer + citation kept
    server-side only — never sent to the student until they've answered."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveIntegerField()  # question number within the quiz, 1-indexed

    question_text = models.TextField()
    options = models.JSONField()  # list[str]
    correct_answer = models.TextField()
    citation = models.TextField(blank=True, default="")

    # filled in once the student answers
    student_answer = models.TextField(blank=True, null=True)
    answered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order} of quiz {self.quiz_id}"

    @property
    def is_correct(self) -> bool | None:
        if self.student_answer is None:
            return None
        return self.student_answer.strip() == self.correct_answer.strip()

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "user"),
        ("assistant", "assistant"),
    ]

    notebook = models.ForeignKey(
        Notebook,
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role} message in Notebook {self.notebook_id} at {self.created_at}"