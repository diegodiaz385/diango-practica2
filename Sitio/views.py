from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
# import requests  # Comentado temporalmente
from .models import UserCredential

# Create your views here.

def home(request):
    return HttpResponse("<BR>Hola desde Django!<BR>")

def index(request):
    return render(request, 'index.html')

def pagina2(request):
    return render(request, 'pagina2.html')

def save_credentials(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # Verificar si el email ya existe
            if UserCredential.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Este email ya está registrado'
                })
            
            # Crear nueva credencial
            credential = UserCredential.objects.create(
                email=email,
                password=password
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Credenciales guardadas exitosamente',
                'redirect_url': '/pagina2/'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def check_credentials(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # Verificar si las credenciales existen
            try:
                credential = UserCredential.objects.get(email=email, password=password)
                return JsonResponse({
                    'success': True,
                    'message': 'Inicio de sesión exitoso',
                    'user_data': {
                        'email': credential.email,
                        'github_connected': credential.github_connected,
                        'github_username': credential.github_username
                    }
                })
            except UserCredential.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Correo o contraseña incorrectos'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def github_callback(request):
    code = request.GET.get('code')
    email = request.GET.get('state')  # Usamos state para pasar el email
    
    if code and email:
        try:
            # Simular conexión exitosa con GitHub (sin hacer llamadas HTTP)
            try:
                credential = UserCredential.objects.get(email=email)
                credential.github_connected = True
                credential.github_username = f"user_{credential.id}"  # Username simulado
                credential.save()
                
                messages.success(request, 'Cuenta de GitHub conectada exitosamente (simulado)')
            except UserCredential.DoesNotExist:
                # Si no existe el usuario, lo creamos
                credential = UserCredential.objects.create(
                    email=email,
                    password='github_auth',
                    github_connected=True,
                    github_username=f"github_user_{email.split('@')[0]}"
                )
                messages.success(request, 'Cuenta de GitHub conectada exitosamente')
            
            return redirect('pagina2')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('index')
    
    messages.error(request, 'Código de autorización no válido')
    return redirect('index')

def get_users(request):
    """Vista para obtener lista de usuarios (solo para desarrollo)"""
    users = UserCredential.objects.all().values('email', 'github_connected', 'github_username', 'created_at')
    return JsonResponse({'users': list(users)})