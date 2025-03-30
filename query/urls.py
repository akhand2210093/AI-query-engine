from django.urls import path
from .views import QueryAPIView, ExplainAPIView, ValidateAPIView

urlpatterns = [
    path("query/", QueryAPIView.as_view(), name="query"),
    path("explain/", ExplainAPIView.as_view(), name="explain"),
    path("validate/", ValidateAPIView.as_view(), name="validate"),
]
