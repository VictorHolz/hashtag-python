import pandas as pd
from pathlib import Path
import win32com.client as win32

vendas_df = pd.read_excel('Bases de Dados/Vendas.xlsx')
lojas_df = pd.read_csv('Bases de Dados/Lojas.csv', sep=';', encoding='latin1')
emails_df = pd.read_excel('Bases de Dados/Emails.xlsx')
vendas_df = vendas_df.merge(lojas_df, on='ID Loja')
vendas_df = vendas_df.merge(emails_df, on='Loja')

ano_dict = {'Loja': [], 'Faturamento': []}
dia_dict = {'Loja': [], 'Faturamento': []}

outlook = win32.Dispatch('outlook.application')

caminho = Path('/home/victor/Área de Trabalho/projeto1/Backup Arquivos Lojas')

for loja in lojas_df['Loja']:
    temp_df = vendas_df[vendas_df['Loja'] == loja]
    dia_indicador = temp_df['Data'].max()
    
    #Salvar a planilha na pasta de backup
    if not (caminho / loja).exists():
        Path.mkdir(caminho / loja)
    nome_arquivo = f'{dia_indicador.day}_{dia_indicador.month}_{loja}'
    temp_df.to_excel(caminho / loja / f'{nome_arquivo}.xlsx')
    
    #Calcular Indicadores
    #ano
    faturamento_ano = temp_df['Valor Final'].sum()
    diversidade_ano = len(temp_df['Produto'].unique())
    valor_venda = temp_df.groupby('Código Venda').sum()
    ticket_medio_ano = valor_venda['Valor Final'].mean()
    #dia
    temp_dia_df = temp_df[temp_df['Data'] == dia_indicador]
    faturamento_dia = temp_dia_df['Valor Final'].sum()
    diversidade_dia = len(temp_dia_df['Produto'].unique())
    valor_venda = temp_dia_df.groupby('Código Venda').sum()
    ticket_medio_dia = valor_venda['Valor Final'].mean()
    
    faturamento_meta_ano = 1650000
    diversidade_meta_ano = 120
    ticket_medio_meta_ano = 500
    
    faturamento_meta_dia = 1000
    diversidade_meta_dia = 4
    ticket_medio_meta_dia = 500
    
    #Enviar Emails
    indi_faturamento_ano = 'green' if faturamento_ano >= faturamento_meta_ano else 'red'
    indi_diversidade_ano = 'green' if diversidade_ano >= diversidade_meta_ano else 'red'
    indi_ticket_medio_ano = 'green' if ticket_medio_ano >= ticket_medio_meta_ano else 'red'
    
    indi_faturamento_dia = 'green' if faturamento_dia >= faturamento_meta_dia else 'red'
    indi_diversidade_dia = 'green' if diversidade_dia >= diversidade_meta_dia else 'red'
    indi_ticket_medio_dia = 'green' if ticket_medio_dia >= ticket_medio_meta_dia else 'red'
    
    nome = emails_df[emails_df['Loja'] == loja]['Gerente']
    mail = outlook.CreateItem(0)
    mail.To = emails_df[emails_df['Loja'] == loja]['Gerente']
    mail.Subject = f'OnePage dia {dia_indicador.day}/{dia_indicador.month} - Loja {loja}'
    mail.HTMLBody = f'''
Bom dia, {nome}

O resultado de ontem (dia {dia_indicador.day}/{dia_indicador.month}) da Loja {loja} foi:
      <table>
      <tr>
        <th>Valor Dia</th>
        <th>Meta Dia</th>
        <th>Cenário Dia</th>
      </tr>
      <tr>
        <td>Faturamento</td>
        <td>1000</td>
        <td style="color: {indi_faturamento_dia};">◙</td>
      </tr>
      <tr>
        <td>Diversidade</td>
        <td>4</td>
        <td style="color: {indi_diversidade_dia};">◙</td>
      </tr>
      <tr>
        <td>Ticket Médio</td>
        <td>500</td>
        <td style="color: {indi_ticket_medio_dia};">◙</td>
      </tr>
    </table>
    <table>
      <tr>
        <th>Valor Ano</th>
        <th>Meta Ano</th>
        <th>Cenário Ano</th>
      </tr>
      <tr>
        <td>Faturamento</td>
        <td>1.650.000</td>
        <td style="color: {indi_faturamento_ano};">◙</td>
      </tr>
      <tr>
        <td>Diversidade</td>
        <td>120</td>
        <td style="color: {indi_diversidade_ano};">◙</td>
      </tr>
      <tr>
        <td>Ticket Médio</td>
        <td>500</td>
        <td style="color: {indi_ticket_medio_ano};">◙</td>
      </tr>
    </table>

Segue em anexo a planilha com todos os dados para mais detalhes.
Qualquer dúvida, estou à disposição.

Att,
Fulano
    '''
    #Criar ranking para a diretoria
    ano_dict['Loja'].append(loja)
    ano_dict['Faturamento'].append(faturamento_ano)
    dia_dict['Loja'].append(loja)
    dia_dict['Faturamento'].append(faturamento_dia)

ano_df = pd.DataFrame.from_dict(ano_dict)
dia_df = pd.DataFrame.from_dict(dia_dict)
