from django.conf.urls import url

from . import views




urlpatterns = [
    url(r'^email/', views.email, name='email'),
    url(r'^imports/', views.imports, name='import'),
    url(r'^temp/', views.temp, name='temp'),
    url(r'^imports2/', views.importclient, name='import2'),
    url(r'^pdf/', views.pdf, name='pdf'),
]