import pandas as pd
from ofxparse import OfxParser
from pandas import DataFrame
from datetime import datetime


def formatar_arquivo_para_db(arquivo:str) -> DataFrame:
    """Formata os dados de um .ofx e transforma em um DataFrame

    Args:
        arquivo (str): path do arquivo

    Returns:
        DataFrame: DF formatado
    """

    # Abrindo arquivo .ofx (modelo NuBank)
    with open(rf'{arquivo}', 'rb') as fileObj:
        ofx = OfxParser.parse(fileObj)

    # Acessando e formatando dados das faturas/transações
    account = ofx.account
    statement = account.statement
    transactions = statement.transactions

    lista_transacoes = []
    for transaction in transactions:
        lista_transacoes.append({
            'start_date_fatura': statement.start_date, 
            'end_date_fatura': statement.end_date,

            'date': transaction.date,
            'amount': transaction.amount,
            'memo': transaction.memo,
            'id': transaction.id,
            'type': transaction.type,

            'status': "Aberta" if datetime.now() < statement.end_date and datetime.now() > statement.start_date else "Fechada",

            'model' : "Parcelado" if 'Parcela' in transaction.memo else "A Vista",
            'total_parcelas' : transaction.memo[-1] if 'Parcela' in transaction.memo else 0,
            'parcela_atual' : transaction.memo[-3] if 'Parcela' in transaction.memo else 0,
        })

    # Criando e ajustando DF para retorno final
    df = pd.DataFrame(lista_transacoes)

    df['date'] = pd.to_datetime(df['date'])
    df['start_date_fatura'] = pd.to_datetime(df['start_date_fatura'])
    df['end_date_fatura'] = pd.to_datetime(df['end_date_fatura'])
    df['amount'] = df['amount'].astype(float)

    return df

if __name__ == "__main__":
    df = formatar_arquivo_para_db(arquivo=r'C:\0 - Desenvolvimento\gerenciamento-financeiro\Nubank_2026-03-09.ofx')
    print(df.head())

    ...