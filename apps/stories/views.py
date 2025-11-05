from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.stories.models import Story
from apps.stories.serializers import StorySerializer, UserAnswerSerializer


class ActiveStoriesListView(generics.ListAPIView):
    queryset = Story.objects.filter(is_active=True)
    serializer_class = StorySerializer
    permission_classes = [AllowAny]


class SubmitAnswersView(generics.CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        answers = request.data.get('answers', [])
        user = request.user

        for answer in answers:
            serializer = self.get_serializer(data=answer)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

        return Response({"message": "Javoblar muvaffaqiyatli saqlandi"}, status=status.HTTP_201_CREATED)
