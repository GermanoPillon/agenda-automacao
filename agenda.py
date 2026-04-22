import requests
import pandas as pd
from io import BytesIO
import os
import datetime as dt

API_KEY = os.environ["API_KEY"]

url = "https://metabase.laqus.com.br/api/card/1282/query/xlsx?format_rows=false"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

print("Baixando arquivo...")

response = requests.post(url, headers=headers)

if response.status_code != 200:
    raise Exception(f"Erro: {response.status_code} - {response.text}")

excel_file = BytesIO(response.content)
df = pd.read_excel(excel_file)

hoje = dt.datetime.now().strftime("%Y-%m-%d")
file_name = f"Permanencia_{hoje}.parquet"

df.to_parquet(file_name, index=False)

print(f"Arquivo gerado: {file_name}")
