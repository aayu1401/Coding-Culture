from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path("mine",views.mine,name='mine'),
    path("competitions",views.competitions,name='competitions'),
    path("progress",views.progress,name='progress'),
    path("submitquery",views.submitquery, name='submitquery'),
    path("details",views.details, name='details'),
    path("contest",views.contest, name='contest')
]