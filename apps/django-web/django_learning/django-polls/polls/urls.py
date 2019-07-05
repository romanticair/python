from django.urls import path

from . import views

app_name = 'polls'  # 命名空间, 应用多了的时候, url搜索就不会出错了
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/                       - -  改良 URLconf 减少冗余
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),            # changed
    # ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),  # changed
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),                # not changed
]
