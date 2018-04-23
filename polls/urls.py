from django.urls import path
from .views import IndexView
from .views import DetailView
from .views import ResultsView
from . import views

app_name = 'polls'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('<int:pk>/Results', ResultsView.as_view(), name='results'),
]
