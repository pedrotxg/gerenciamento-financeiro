import pandas as pd
from ofxparse import OfxParser

with open(r'C:\0 - Desenvolvimento\gerenciamento-financeiro\Nubank_2026-03-09.ofx', 'rb') as fileObj:
    ofx = OfxParser.parse(fileObj)

account = ofx.account
statement = account.statement
transactions = statement.transactions

lista_transacoes = []
for transaction in transactions:
    lista_transacoes.append({
        'date': transaction.date,
        'amount': transaction.amount,
        'memo': transaction.memo,
        'id': transaction.id,
        'type': transaction.type
    })

df = pd.DataFrame(lista_transacoes)

# 4. Ajustes finos (Converter data e valor para tipos corretos)
df['date'] = pd.to_datetime(df['date'])
df['amount'] = df['amount'].astype(float)

# Exibir as primeiras linhas
print(df.head())

...