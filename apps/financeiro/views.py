from django.shortcuts import render, redirect

from .forms import *
from .models import *
from .automacao.leitor_documentos import formatar_arquivo_para_db

import pandas as pd
from datetime import datetime

def upload_fatura(request):
    if request.method == "POST":
        form = UploadFaturaForm(request.POST, request.FILES)

        if form.is_valid():
            arquivo = request.FILES['arquivo']

            df = formatar_arquivo_para_db(arquivo=arquivo)

            fatura = Faturas.objects.create(
                data_inicio = df['start_date_fatura'].min(),
                data_fim = df['end_date_fatura'].max(),
                status=df['status'].max()
            )

            for _, linha in df.iterrows():

                tipo_transacao, _ = TipoTransacao.objects.get_or_create(
                    nome=linha['type']
                )

                modelo_transacao, _ = ModeloTransacao.objects.get_or_create(
                    nome=linha['model']
                )

                Transacoes.objects.get_or_create(
                    data_compra = linha['date'],
                    valor = linha['amount'],
                    descricao = linha['memo'],
                    id_externo = linha['id'],
                    total_parcelas = linha['total_parcelas'],
                    parcela_atual = linha['parcela_atual'],

                    fatura = fatura,
                    tipo = tipo_transacao,
                    modelo = modelo_transacao,
                )

            return redirect('admin')

    else:
        form = UploadFaturaForm()

...