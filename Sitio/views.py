from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import requests
from .models import UserProfile, SavedCredential

# Create your views here.

def home(request):
    return HttpResponse("<BR>Hola desde Django!<BR>")

def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'register.html')
        
        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        
        messages.success(request, 'Usuario creado exitosamente')
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('index')

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    saved_credentials = SavedCredential.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'user_profile': user_profile,
        'saved_credentials': saved_credentials,
    }
    return render(request, 'dashboard.html', context)

@login_required
def github_callback(request):
    code = request.GET.get('code')
    
    if code:
        # Configuración de GitHub OAuth (necesitarás configurar esto en GitHub)
        client_id = 'TU_GITHUB_CLIENT_ID'  # Configurar en settings
        client_secret = 'TU_GITHUB_CLIENT_SECRET'  # Configurar en settings
        
        # Intercambiar código por token
        token_url = 'https://github.com/login/oauth/access_token'
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code
        }
        
        response = requests.post(token_url, data=token_data, headers={'Accept': 'application/json'})
        
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info.get('access_token')
            
            if access_token:
                # Obtener información del usuario de GitHub
                user_url = 'https://api.github.com/user'
                headers = {'Authorization': f'token {access_token}'}
                
                user_response = requests.get(user_url, headers=headers)
                
                if user_response.status_code == 200:
                    github_user = user_response.json()
                    
                    # Actualizar perfil del usuario
                    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
                    user_profile.github_username = github_user.get('login')
                    user_profile.github_access_token = access_token
                    user_profile.github_avatar_url = github_user.get('avatar_url')
                    user_profile.bio = github_user.get('bio', '')
                    user_profile.save()
                    
                    messages.success(request, 'Cuenta de GitHub conectada exitosamente')
                    return redirect('dashboard')
    
    messages.error(request, 'Error al conectar con GitHub')
    return redirect('dashboard')

@login_required
@csrf_exempt
def save_credential(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            service_name = data.get('service_name')
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            notes = data.get('notes', '')
            
            credential = SavedCredential.objects.create(
                user=request.user,
                service_name=service_name,
                username=username,
                email=email,
                password=password,
                notes=notes
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Credencial guardada exitosamente',
                'credential_id': credential.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@csrf_exempt
def delete_credential(request, credential_id):
    try:
        credential = SavedCredential.objects.get(id=credential_id, user=request.user)
        credential.delete()
        return JsonResponse({'success': True, 'message': 'Credencial eliminada exitosamente'})
    except SavedCredential.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Credencial no encontrada'})

@login_required
def get_credentials(request):
    credentials = SavedCredential.objects.filter(user=request.user).values(
        'id', 'service_name', 'username', 'email', 'notes', 'created_at'
    )
    return JsonResponse({'credentials': list(credentials)})