from django.contrib import admin
from .models import *

admin.site.register(Faturas)
admin.site.register(Transacoes)
admin.site.register(TipoTransacao)
admin.site.register(ModeloTransacao)