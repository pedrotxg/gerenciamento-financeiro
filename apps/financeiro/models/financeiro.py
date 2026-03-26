from django.db import models

class Faturas(models.Model):
    class Meta:
        db_table="tb_faturas"
        verbose_name="Fatura"
        verbose_name_plural="Faturas"

    data_inicio = models.DateField(help_text="Data Inicio da fatura")
    data_fim = models.DateField(help_text="Data Fim da fatura")
    status = models.CharField(max_length=10, choices=[('aberta', 'Aberta'), ('fechada', 'Fechada'),], help_text='"Aberta" ou "Fechada"')

    def __str__(self):
        return self.status

class TipoTransacao(models.Model):
    class Meta:
        db_table="tb_tipo_transacao"
        verbose_name="Tipo de Transação"
        verbose_name_plural="Tipos de Transações"

    tipo_transacao = models.CharField(max_length=10, null=False, blank=False, help_text='"Débito" ou "Crédito"')

    def __str__(self):
        return self.tipo_transacao

class ModeloTransacao(models.Model):
    class Meta:
        db_table="tb_modelo_transacao"
        verbose_name="Modelo de Trasação"
        verbose_name_plural="Modelos de Transações"

    modelo_transacao = models.CharField(max_length=15, null=False, blank=False, help_text='"A Vista" ou "Parcelado"')

    def __str__(self):
        return self.modelo_transacao

class Transacoes(models.Model):
    class Meta:
        db_table="tb_transacoes"
        verbose_name="Transação"
        verbose_name_plural="Transações"

    data_compra = models.DateField(help_text="Data da transação")
    valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor da transação")
    descricao = models.CharField(max_length=70, null=False, blank=False, help_text='Descrição da transação/estabelecimento/banco')
    id_externo = models.CharField(max_length=100, null=True, blank=True, help_text='Id de itentificação da transação (origem banco)')

    fatura = models.ForeignKey(Faturas, on_delete=models.CASCADE) # apaga todos as transações se a fatura por apagada
    tipo = models.ForeignKey(TipoTransacao, on_delete=models.PROTECT) # bloqueia a exclusão se o tipo for apagado
    modelo = models.ForeignKey(ModeloTransacao, on_delete=models.PROTECT) # bloqueia a exclusão se o tipo for apagado

    def __str__(self):
        return f"{self.data_compra} - {self.descricao} - {self.valor}"