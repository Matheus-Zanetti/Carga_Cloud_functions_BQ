import requests  # Biblioteca para realizar requisições HTTP
from requests.exceptions import HTTPError, Timeout, RequestException
import pandas as pd
from google.cloud import bigquery  # Biblioteca do Google Cloud BigQuery
import functions_framework  # Biblioteca para criar funções HTTP no Google Cloud Functions


# Função para obter dados da API
def get_api_data(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}")
    except RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except ValueError as json_err:
        print(f"Error parsing JSON response: {json_err}")
    return None

@functions_framework.http
def extract_and_save_data(request):
    # URL da API
    url = 'https://fakestoreapi.com/products'
    
    # Extrai dados da API
    api_data = get_api_data(url)
    if api_data is None:
        return 'Falha na extração de dados da API.', 500
    
    # Converte dados da API para DataFrame
    df = pd.DataFrame(api_data)
    
    # Configure o cliente BigQuery
    client = bigquery.Client()
    
    # Defina o nome do dataset e da tabela no BigQuery
    dataset_id = 'dados_teste'  # Substitua por seu ID de dataset
    table_id = 'api_dados'
    
    # Crie o dataset se ele não existir
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)  # Verifica se o dataset já existe
    except Exception:
        client.create_dataset(dataset_ref)
    
    # Crie a tabela se ela não existir
    table_ref = dataset_ref.table(table_id)
    try:
        client.get_table(table_ref)  # Verifica se a tabela já existe
    except Exception:
        schema = [
            bigquery.SchemaField("id", "INTEGER"),
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("price", "FLOAT"),
            bigquery.SchemaField("description", "STRING"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("image", "STRING"),
            bigquery.SchemaField("rating", "RECORD", fields=[
                bigquery.SchemaField("rate", "FLOAT"),
                bigquery.SchemaField("count", "INTEGER"),
            ]),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
    
    # Carregue os dados extraídos na tabela
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  # Adicione novos dados (ou substitua)
    
    load_job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    load_job.result()  # Aguarda a conclusão do carregamento dos dados
    
    # Retorna um texto indicando o sucesso da operação
    return f'Dados extraídos da API e salvos na tabela {table_id} do dataset {dataset_id} com sucesso.', 200

# Exemplo de uso
if __name__ == "__main__":
    result = extract_and_save_data(None)
    print(result)
