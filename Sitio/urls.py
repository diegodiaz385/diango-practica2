from django.urls import path
from . import views

urlpatterns = [
	path('', views.home),
	path('index/', views.index, name='index'),
	path('pagina2/', views.pagina2, name='pagina2'),
	path('api/save-credentials/', views.save_credentials, name='save_credentials'),
	path('github/callback/', views.github_callback, name='github_callback'),
	path('api/users/', views.get_users, name='get_users'),
]