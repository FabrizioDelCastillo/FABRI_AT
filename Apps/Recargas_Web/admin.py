from django.contrib import admin
from .models import Calimaco
from .models import GestionRW
from .models import Skype
from .models import TicketsPagadosDeTienda

admin.site.register(Calimaco)
admin.site.register(GestionRW)
admin.site.register(Skype)
admin.site.register(TicketsPagadosDeTienda)

# Register your models here.
