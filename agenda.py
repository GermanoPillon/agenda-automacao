print("=== INÍCIO DO SCRIPT ===")

import requests
import pandas as pd
from io import BytesIO
import os
import datetime as dt

# API KEY
API_KEY = os.environ.get("API_KEY")

print("API_KEY existe?", bool(API_KEY))

if not API_KEY:
    raise Exception("API_KEY NÃO ENCONTRADA")

# URL
url = "https://metabase.laqus.com.br/api/card/1282/query/xlsx?format_rows=false"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

print("Chamando API...")
response = requests.post(url, headers=headers)

print("Status da resposta:", response.status_code)

if response.status_code != 200:
    print("Erro na API:", response.text)
    raise Exception("Falha na API")

print("Lendo Excel...")

excel_file = BytesIO(response.content)

try:
    df = pd.read_excel(excel_file)
    print("DataFrame carregado")
    print("Quantidade de linhas:", len(df))
except Exception as e:
    print("Erro ao ler Excel:", e)
    raise

if df.empty:
    raise Exception("DataFrame vazio — nada para salvar")

# gerar parquet
hoje = dt.datetime.now().strftime("%Y-%m-%d")
file_name = f"Permanencia_{hoje}.parquet"

print("Salvando parquet...")
df.to_parquet(file_name, index=False)

print("Arquivo criado:", file_name)
print("=== FIM DO SCRIPT ===")
