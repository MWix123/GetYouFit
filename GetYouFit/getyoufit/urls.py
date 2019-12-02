from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('profile', views.profile, name="profile"),
    path('diet', views.diet, name="diet"),
    path('create-diet-entry', views.create_diet, name="create_diet"),
    path('workouts', views.workouts, name="workouts"),
    path('create-workout-entry', views.create_workout, name="create_workout")
]
