from django.urls import path
from . import views

urlpatterns = [
	path('', views.home),
	path('index/', views.index, name='index'),
	path('register/', views.register_view, name='register'),
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('github/callback/', views.github_callback, name='github_callback'),
	path('api/save-credential/', views.save_credential, name='save_credential'),
	path('api/delete-credential/<int:credential_id>/', views.delete_credential, name='delete_credential'),
	path('api/get-credentials/', views.get_credentials, name='get_credentials'),
]