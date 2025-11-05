from django.db import models
from django.utils import timezone


class Story(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Question(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.story.title} - {self.text}"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, null=True)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user} - {self.question}"
