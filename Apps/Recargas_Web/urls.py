from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('cargar_calimaco/', views.cargar_calimaco, name='cargar_calimaco'),
    path('subir-data-xlsx', views.cargar_archivo, name='cargar_archivo'),
    path('subir-data-xlsx-rw/', views.cargar_archivo_gestionrw, name='cargar_archivo_gestionrw'),
    path('subir-data-xlsx-skype/', views.cargar_db_skype, name='cargar_db_skype'),
    path('subir-data-xlsx-tickets/', views.cargar_tickets_pagados_de_tienda, name='cargar_tickets_pagados_de_tienda'),
]