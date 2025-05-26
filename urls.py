from django.urls import path
from . import views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.homepage, name='homepage'),  # Landing page
    path('home/', views.home, name='home'),        # Set home.html as the landing page
    path('student-login/', views.login_page, name='login_page'),  # Student login page
    path('login/', views.login_user, name='login_user'),
    path('signup/', views.signup_user, name='signup_user'),
    path('signup-page/', lambda request: render(request, 'signup.html'), name='signup_page'),
    path('dashboard/', views.dashboard, name='dash'),
 path('alumni-jobboard/', views.alumni_jobboard, name='alumni_jobboard'),
    path('alumni-login/', views.alumni_login_page, name='alumni_login_page'),
    path('alumni-login-post/', views.alumni_login, name='alumni_login'),
    path('alumni-signup/', views.alumni_signup_page, name='alumni_signup_page'),
    path('alumni-signup-post/', views.alumni_signup, name='alumni_signup'),
    path('alumni-dashboard/', views.alumni_dashboard, name='alumni_dashboard'),
     path('profile/<str:user_id>/', views.user_profile, name='user_profile'),
    path('profile/', views.profile_page, name='profile_page'),
    path('save_profile/', views.save_profile, name='save_profile'),
    path('get_profile/', views.get_profile, name='get_profile'),
    path('alumni/profile/', views.alumni_profile_view, name='alumni_profile'),
path('get_alumni_profile/', views.get_alumni_profile, name='get_alumni_profile'),
path('save_alumni_profile/', views.save_alumni_profile, name='save_alumni_profile'),
path('jobs/', views.job_opportunities, name='job_opportunities'),
path('post-job/', views.post_job, name='post_job'),
   path('alumni-network/', views.alumni_network_view, name='alumni_network'),
     path('search-alumni/', views.search_alumni, name='search_alumni'),
path('mentorship/', views.alumni_mentorship, name='alumni_mentorship'),
path('logout/', views.logout_view, name='logout'),

 path('ask/', views.ask_question, name='ask_question'),
     path('answer/<str:question_id>/', views.answer_question, name='answer_question'),
path('applyme/', views.applyme, name='applyme'),
path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('submit_contact/', views.submit_contact, name='submit_contact'),
 path('search/', views.search, name='search'),

    path('alumni/chat/', views.alumni_chat_view, name='alumni_chat'),
path('alumni-awards/', views.alumni_awards_view, name='alumni_awards'),
path('psg-college/', views.psg_college_view, name='psg_college'),

    path('student-chat/', views.student_chat_view, name='student_chat'),
    path('alumni-announcements/', views.alumni_announcements_view, name='alumni_announcements'),
    path('alumni_meetup/register/', views.alumni_meetup_register, name='alumni_meetup_register'),
    path('mylswamy', views.mylswamy, name='mylswamy'),
path('shiv', views.shiv, name='shiv'),
path('pandia', views.pandia, name='pandia'),
path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('forgot-password/', views.forgot_password_view, name='password_reset_request'),
    path('password_reset/', views.password_reset_page, name='password_reset'),
     path('announcements/', views.announcements_view, name='announcements'),
      path('add-announcement/', views.add_announcement_view, name='add_announcement'),
      path('reply/', views.reply_to_student, name='reply'),
  path('ask/', views.ask_question, name='ask_question'),
    path('answer/<str:qid>/', views.answer_question, name='answer_question'),
    path('edit_question/<str:qid>/', views.edit_question, name='edit_question'),
    path('delete_question/<str:qid>/', views.delete_question, name='delete_question'),
    path('edit_answer/<str:qid>/<str:aid>/', views.edit_answer, name='edit_answer'),
    path('delete_answer/<str:qid>/<str:aid>/', views.delete_answer, name='delete_answer'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)