from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # ── Public pages ──
    path('', views.home, name='home'),
    path('works/', views.works, name='works'),
    path('works/<int:pk>/', views.work_detail, name='work_detail'),
    path('works/category/<slug:slug>/', views.category_works, name='category_works'),
    path('poster-design/', views.poster_design, name='poster_design'),
    path('thumbnail-design/', views.thumbnail_design, name='thumbnail_design'),
    path('logo-design/', views.logo_design, name='logo_design'),
    path('video-editing/', views.video_editing, name='video_editing'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('download-cv/', views.download_cv, name='download_cv'),

    # ── Custom Dashboard ──
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/profile/', views.dashboard_profile, name='dashboard_profile'),

    # Works
    path('dashboard/works/', views.dashboard_works, name='dashboard_works'),
    path('dashboard/works/add/', views.dashboard_work_add, name='dashboard_work_add'),
    path('dashboard/works/<int:pk>/edit/', views.dashboard_work_edit, name='dashboard_work_edit'),
    path('dashboard/works/<int:pk>/delete/', views.dashboard_work_delete, name='dashboard_work_delete'),
    path('dashboard/works/<int:pk>/toggle/', views.dashboard_work_toggle, name='dashboard_work_toggle'),

    # Messages
    path('dashboard/messages/', views.dashboard_messages, name='dashboard_messages'),
    path('dashboard/messages/<int:pk>/', views.dashboard_message_detail, name='dashboard_message_detail'),
    path('dashboard/messages/<int:pk>/action/', views.dashboard_message_action, name='dashboard_message_action'),

    # Other sections
    path('dashboard/skills/', views.dashboard_skills, name='dashboard_skills'),
    path('dashboard/testimonials/', views.dashboard_testimonials, name='dashboard_testimonials'),
    path('dashboard/announcements/', views.dashboard_announcements, name='dashboard_announcements'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('dashboard/services/', views.dashboard_services, name='dashboard_services'),
    path('dashboard/experience/', views.dashboard_experience, name='dashboard_experience'),
    path('dashboard/social/', views.dashboard_social, name='dashboard_social'),
    path('dashboard/contact-info/', views.dashboard_contact_info, name='dashboard_contact_info'),
]
