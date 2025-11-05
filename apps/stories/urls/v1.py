from django.urls import path
from apps.stories.views import ActiveStoriesListView, SubmitAnswersView

app_name = 'stories'

urlpatterns = [
    path('', ActiveStoriesListView.as_view(), name='list'),
    path('submit/', SubmitAnswersView.as_view(), name='submit'),
]
