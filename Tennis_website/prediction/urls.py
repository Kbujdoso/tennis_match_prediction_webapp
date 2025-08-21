from django.urls import path
from . import views
urlpatterns = [
    path('', views.show_markdown, name="index"),
    path('prediction/', views.prediction, name="prediction"),
    path('prediction_view/', views.prediction_view, name="prediction_view"),
    path('autocomplete_player/', views.autocomplete_player, name="prediction_autocomplete")
]


