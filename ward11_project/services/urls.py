from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('report-issue/', views.report_issue_view, name='report'),
    path('track-status/', views.track_status_view, name='track'),
]
