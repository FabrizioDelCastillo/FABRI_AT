# Importa los modelos de Django
from django.db import models

class Calimaco(models.Model):
    identifer_cal = models.CharField(max_length=20, default="Unknown")
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=20, default="Pending")
    fecha_de_modificacion = models.DateTimeField()
    usuario = models.CharField(max_length=20, default="Unknown")
    email = models.EmailField(default="example@example.com")
    cantidad = models.IntegerField(default=0)
    id_externo = models.CharField(max_length=20, default="Unknown")
    metodo = models.TextField(default="N/A")
    respuesta = models.TextField(default="N/A")
    agente = models.IntegerField(default=0)
    fecha_de_registro_del_jugador = models.DateTimeField()

    class Meta:
        db_table = "CALIMACO"  # Nombre de la tabla en la base de datos

    def fecha_formateada(self):
        return self.fecha.strftime('%d/%m/%Y %H:%M:%S')

    def fecha_de_modificacion_formateada(self):
        return self.fecha_de_modificacion.strftime('%d/%m/%Y %H:%M:%S')

    def fecha_de_registro_formateada(self):
        return self.fecha_de_registro_del_jugador.strftime('%d/%m/%Y %H:%M:%S')


class GestionRW(models.Model):
    identifier = models.IntegerField()
    local = models.CharField(max_length=100)
    registro = models.DateTimeField()
    tipo = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=100)
    bono = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    tipo_documento = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=20)
    web_id = models.IntegerField()
    cliente = models.CharField(max_length=255)
    recarga = models.IntegerField()
    bono_5_por_ciento = models.IntegerField()
    promotor = models.CharField(max_length=100)

    class Meta:
        db_table = "GESTION_RW"  # Nombre de la tabla en la base de datos

    def registro_formateado(self):
        return self.registro.strftime('%d/%m/%Y %H:%M:%S')

class Skype(models.Model):
    mes = models.CharField(max_length=20)
    fecha = models.DateField()
    monto = models.CharField(max_length=20)
    tx = models.BigIntegerField(default=0)
    id_web = models.BigIntegerField()
    promotor = models.CharField(max_length=100)
    cliente = models.CharField(max_length=255)
    teleservicios = models.CharField(max_length=50)
    soporte = models.CharField(max_length=50)
    calimaco = models.CharField(max_length=50)

    class Meta:
        db_table = "SKYPE"  # Nombre de la tabla en la base de datos

    def fecha_formateada(self):
        return self.fecha.strftime('%d/%m/%Y')
class TicketsPagadosDeTienda(models.Model):
    ticket = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField()
    zona_creadora = models.CharField(max_length=100)
    caja_creadora = models.CharField(max_length=100)
    usuario_creador = models.CharField(max_length=100)
    razon_social_creador = models.CharField(max_length=255)
    fecha_calculo = models.DateTimeField()
    fecha_pago = models.DateTimeField()
    caja_pagadora = models.CharField(max_length=100)
    usuario_pagador = models.CharField(max_length=100)
    razon_social_pagador = models.CharField(max_length=255)
    monto_apostado = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    num_doc_cliente = models.CharField(max_length=50)
    proveedor = models.CharField(max_length=255)

    class Meta:
        db_table = 'TICKETS_PAGADOS_DE_TIENDA'