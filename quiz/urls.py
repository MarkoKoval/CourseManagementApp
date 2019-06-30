from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

   path("", views.enter, name = 'enter'),
path('haha', views.list, name='list'),
path('quiz', views.load_quiz, name='quiz'),
    path('home', views.enter_quiz_app, name="enter-quiz-app"),


    path('possible-course-subscriptions/<str:username>', views.get_possible_course_subscriptions, name="get_possible_course_subscriptions"),
    path('course-subscriptions/<str:username>', views.get_my_course_subscriptions, name="get_my_course_subscriptions"),
    path('create/course-subscription/<str:username>/<str:coursename>', views.create_course_subscription, name="create_course_subscription"),
    path('delete/course-subscription/<str:coursename>/<str:username>', views.delete_course_subscription, name="delete_course_subscription"),

#path("pass-test-for/course/<str:coursename>/lesson/<str:lessonname>",views.pass_test,name='pass_lesson_test'),
    path('created-courses/<str:username>', views.get_my_created_courses, name="get_my_created_courses"),
    path('create/course/by/<str:username>', views.create_course, name="create_course"),
    path('create-tests/for-course/<str:coursename>/for-lesson/<str:lessonname>', views.create_course_tests_for_lesson, name='create_course_tests_for_lesson'),
   path('delete/course/<int:id>', views.delete_course, name="delete_course"),
path('show/course-lessons-of/<str:coursename>/for-user/<str:username>', views.show_course_lessons,name = 'show_course_lessons'),
path('show/course/<str:coursename>/lesson/<str:lessonname>/files', views.show_lesson_files_,name = 'show_lesson_files'),
 path('update/course/<int:id>', views.update_course, name="update_course"),
#path('edit/<str:coursename>/<str:lessonname>/by/<str:username>', views.edit_lesson_content, name="edit_lesson_content"),
path('update/course-content-of/<str:coursename>', views.edit_course_content, name="edit_course_content"),
path('update/course-content-of/<str:coursename>/lesson/<str:lessonname>/created-by/<str:username>', views.edit_lesson_content, name="tyy"),
path('update/course-content-of/<str:coursename>/lesson/<str:lessonname>/created-by/<str:username>/resourse/<str:media>/'
     '<str:doc>/<str:year>/<str:day>/<str:month>/<str:name>', views.delete_lesson_content, name="tyyyy"),

path('chat-for/<str:coursename>/user/<str:username>',  views.show_chat ,name = 'show_course_chat'),

    path('load-quiz-info', views.load_quiz_info, name="quiz_info"),
    path('create', views.create_quiz, name="create"),
    path('load-test-pass-info',views.load_test_pass_info,name = "load"),
    path('clear', views.clear),
    path('statistic/<str:username>',views.statistic),
    path('pass-test-for/course/<str:coursename>/lesson/<str:lessonname>/by-username/<str:username>',views.pass_tests_forlesson,name = "pass_tests_for_lesson"),
    path('about',views.about, name="about")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)