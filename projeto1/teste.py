import pandas as pd
import smtplib
from email.message import EmailMessage

vendas_df = pd.read_excel('Bases de Dados/Vendas.xlsx')
lojas_df = pd.read_csv('Bases de Dados/Lojas.csv', sep=';', encoding='latin1')
emails_df = pd.read_excel('Bases de Dados/Emails.xlsx')

EMAIL_ADRESS = 'victormholz@gmail.com'
EMAIL_PASSWORD = 'sK5387417MAo#81tE2wyK81@'
msg = EmailMessage()

lojas = [loja for loja in lojas_df['Loja']]

for i in range(1, 26):
    # ano
    df_temp = vendas_df[vendas_df['ID Loja'] == i]
    faturamento_ano = df_temp['Valor Final'].sum()
    diversidade_ano = len(df_temp['Produto'].value_counts())
    ticket_ano = df_temp['Valor Final'].mean()
    # dia
    df_temp = df_temp[vendas_df['Data'] == df_temp['Data'].max()]
    faturamento_dia = df_temp['Valor Final'].sum()
    diversidade_dia = len(df_temp['Produto'].value_counts())
    ticket_dia = df_temp['Valor Final'].mean()
    dia = df_temp['Data'].dt.day
    mes = df_temp['Data'].dt.month
    # email
    email = mails_df['E-mail'][i - 1]
    gerente = mails_df['Gerente'][i - 1]

    msg['From'] = 'victormholz@gmail.com'
    msg['To'] = emails
    msg['Subject'] = f'''Bom dia, {gerente}

O resultado de ontem (dia {dia}/{mes}) da loja {lojas[i - 1]} foi:

Segue em anexo a planilha com todos os dados para mais detalhes.
Qualquer dúvida, estou à disposição.

Att,
Fulano
'''
    msg.set_content()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        df.to_excel(f'Backup Arquivos Lojas/{lojas[i - 1]}.xlsx')

