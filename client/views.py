import base64
import os
import qrcode
import hashlib

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings
from weasyprint import HTML
from core.utils import generate_user_id, generate_user_hash
from core.models import IdentidadAnonima
from io import BytesIO

from .forms import SecretoForm
from .models import Secreto


def crear_secreto(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, _("You must be logged in anonymously."))
        return redirect('login_anonimo')

    if request.method == 'POST':
        form = SecretoForm(request.POST, request.FILES)
        if form.is_valid():
            secreto = form.save(commit=False)
            secreto.id_usuario = user_id
            secreto.save()
            messages.success(request, _("Secret successfully created."))
            return redirect('dashboard_anonimo')  # o donde quieras
    else:
        form = SecretoForm()

    return render(request, 'client/crear_secreto.html', {'form': form})




def dashboard_anonimo(request):
    user_id = request.session.get("user_id")  # <-- corregido
    if not user_id:
        return redirect('login_anonimo')
    return render(request, "client/dashboard_anonimo.html", {"user_id": user_id})



def login_anonimo(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '').strip()
        user_hash = request.POST.get('user_hash', '').strip()

        if not user_id or not user_hash:
            return render(request, 'client/login_anonimo.html', {'error': _("All fields are required.")})

        try:
            identidad = IdentidadAnonima.objects.get(user_id=user_id, user_hash=user_hash)
            request.session['user_id'] = str(identidad.user_id)
            request.session.modified = True
            return redirect('dashboard_anonimo')
        except IdentidadAnonima.DoesNotExist:
            return render(request, 'client/login_anonimo.html', {'error': _("Invalid credentials.")})

    return render(request, 'client/login_anonimo.html')





def generar_identidad(request):
    user_id = None
    user_hash = None
    secret_phrase = None
    ya_existente = False

    if request.method == 'POST':
        secret_phrase = request.POST.get('secret_phrase', '').strip()

        if secret_phrase:
            user_id = generate_user_id()
            user_hash = generate_user_hash(user_id, secret_phrase)

            if not IdentidadAnonima.objects.filter(user_id=user_id).exists():
                IdentidadAnonima.objects.create(
                    user_id=user_id,
                    user_hash=user_hash,
                    creditos=0
                )
            else:
                ya_existente = True

    return render(request, 'client/generar_identidad.html', {
        'user_id': user_id,
        'user_hash': user_hash,
        'secret_phrase': secret_phrase,
        'ya_existente': ya_existente
    })

def descargar_credenciales(request):
    user_id = request.GET.get("uid")
    user_hash = request.GET.get("hash")
    secret_phrase = request.GET.get("secret")

    if not user_id or not user_hash:
        return HttpResponse("Missing data", status=400)

    # Generar el QR con URL interna personalizada
    qr_url = f"echosoul://login?uid={user_id}&secret={secret_phrase or ''}"
    qr_img = qrcode.make(qr_url)
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    qr_data_uri = f"data:image/png;base64,{qr_base64}"

    # Logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_echosoul.png')

    # Render template
    html_string = render_to_string('client/credenciales_pdf.html', {
        'user_id': user_id,
        'user_hash': user_hash,
        'secret_phrase': secret_phrase,
        'logo_url': logo_path,
        'qr_image': qr_data_uri,
    })

    pdf = HTML(string=html_string).write_pdf()
    return HttpResponse(pdf, content_type='application/pdf', headers={
        'Content-Disposition': 'attachment; filename="echosoul_identity.pdf"'
    })

def landing_view(request):
    return render(request, 'client/landing.html')