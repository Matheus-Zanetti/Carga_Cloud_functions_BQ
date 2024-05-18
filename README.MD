# Cloud Functions API Data Extraction to BigQuery

<p align ='center'>
    <img width="470" src="Pessoal - Quadro 1.jpg">
</p>

Este projeto usa Google Cloud Functions para extrair dados de uma API, salvar os dados em uma tabela no BigQuery e é agendado para execução periódica pelo Google Cloud Scheduler.

## Visão Geral

1. **Cloud Functions:** Implementa uma função HTTP que extrai dados de uma API e os salva em uma tabela do BigQuery.
2. **BigQuery:** Armazena os dados extraídos da API.
3. **Cloud Scheduler:** Agendador de tarefas que dispara a execução da Cloud Function em intervalos regulares.

## Estrutura do Projeto


## Pré-requisitos

- Conta no Google Cloud Platform (GCP)
- Projeto no GCP
- BigQuery habilitado no projeto
- Cloud Functions habilitado no projeto
- Cloud Scheduler habilitado no projeto

## Configuração

### 1. Configurar o BigQuery
Crie um dataset e uma tabela no BigQuery para armazenar os dados extraídos. Por exemplo:

- Dataset ID: `seu_dataset_id`
- Table ID: `sua_tabela`

### 2. Configurar o Cloud Functions

#### Código da Função (main.py)

### 3. Implementar a Cloud Function
No Google Cloud Console, navegue até Cloud Functions e crie uma nova função com as seguintes configurações:

 - Runtime: Python 3.9
 - Trigger: HTTP
 - Autenticação: Allow unauthenticated invocations (Permitir invocações não autenticadas)
 - Faça o upload do arquivo main.py e requirements.txt. Defina o entrypoint como extract_and_save_data.

### 4. Configurar o Cloud Scheduler
No Google Cloud Console, navegue até Cloud Scheduler e crie um novo job com as seguintes configurações:

 - Frequência: Defina a frequência desejada (por exemplo, 0 8 * * * para executar todos os dias às 8h)
 - URL do alvo: A URL da sua Cloud Function
 - Método HTTP: POST
