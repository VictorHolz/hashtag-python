import pandas as pd
from tqdm import tqdm

vendas_df = pd.read_csv('Contoso - Vendas - 2017.csv', sep=';')
lojas_df = pd.read_csv('Contoso - Lojas.csv', sep=';')
clientes_df = pd.read_csv('Contoso - Clientes.csv', sep=';')
produtos_df = pd.read_csv('Contoso - Cadastro Produtos.csv', sep=';')

lojas_df = lojas_df[['ID Loja', 'Nome da Loja']]
clientes_df = clientes_df[['ID Cliente', 'E-mail']]
produtos_df = produtos_df[['ID Produto', 'Nome do Produto']]

vendas_df = vendas_df.merge(lojas_df, on='ID Loja')
vendas_df = vendas_df.merge(clientes_df, on='ID Cliente').rename(columns={'E-mail': 'E-mail do Cliente'})
vendas_df = vendas_df.merge(produtos_df, on='ID Produto')

print(vendas_df)
