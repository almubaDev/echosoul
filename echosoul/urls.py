from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    # Ruta para cambiar idioma (debe ir fuera del i18n_patterns)
    path('set-language/', set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    # Ruta para la landing y vistas públicas
    path('', include('client.urls')),
    # Ruta para el admin de Django
    path('admin/', admin.site.urls),
)
