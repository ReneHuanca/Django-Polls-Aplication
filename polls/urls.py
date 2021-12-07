from django.urls import path

from . import views

app_name = 'polls'  # the namespace 'polls' is used when call the name in {% url 'polls:detail' question.id %}
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
