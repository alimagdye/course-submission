from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.popular_course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('submit/<int:course_id>/', views.submit, name='submit'),
    path('exam_result/<int:submission_id>/', views.show_exam_result, name='show_exam_result'),
]
