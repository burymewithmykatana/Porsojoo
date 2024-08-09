from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from analytics.mixins import UserActivityMixin
from .mixins import CachedListMixin, ThrottleMixin
from .models import Form, ProcessForm, Process, Question
from .serializers import FormSerializer, ProcessFormSerializer, ProcessSerializer, QuestionSerializer


class FormViewSet(CachedListMixin, ThrottleMixin, UserActivityMixin, viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    cache_key = "form_list"

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    # ensure the view passes the request to the serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ProcessFormViewSet(CachedListMixin, ThrottleMixin, UserActivityMixin, viewsets.ModelViewSet):
    queryset = ProcessForm.objects.all()
    serializer_class = ProcessFormSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "processform_list"


class ProcessViewSet(CachedListMixin, ThrottleMixin, UserActivityMixin, viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "process_list"

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
    # ensure the view passes the request to the serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class QuestionViewSet(CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "question_list"
