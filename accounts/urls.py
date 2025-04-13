from django.urls import path
from .views import auth_callback, SaveProfileView, set_session, get_user_data,complete_profile , supabase_auth
from .api import profile_view

urlpatterns = [
    path("auth/callback/", auth_callback, name="auth_callback"),
    # path("complete-profile/", complete_profile, name="complete_profile"),
    path("save-profile/", SaveProfileView.as_view(), name="save_profile"),
    path("set-session/", set_session, name="set_session"),
    path("get-user-data/", get_user_data, name="get_user_data"),
    # Single endpoint for both GET and POST operations
    path("api/profile/<str:email>/", profile_view, name="profile_view"),
    path('complete-profile/',complete_profile,name='complete_profile'),
    path("supabase-auth/", supabase_auth, name="supabase-auth"),
]
