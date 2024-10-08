from demo import select_bq, get_schemas
from demoAI import generate, get_query_in_response, create_sqlx
from dataformTest import upload_sqlx_file, execute_job

print("Iniciando aplicação!\n")

project_id = "squadcalouros" # ID do projeto
dataset_id = "dataform" # ID do dataset
table_name = "eventos_oficial" # Nome da tabela
repository_id = "teste"  # Nome simples do repositório
workspace = "testDataform"  # A branch onde você quer fazer o upload
file_name = "eventos_view" # Nome do arquivo
file_path_local = "eventos_data.sqlx"  # Caminho do arquivo local
file_path_repo = file_name + ".sqlx"  # Nome do arquivo dentro do repositório

table_observed = f"{project_id}.{dataset_id}.{table_name}" # squadcalouros.dataform.eventos_oficial

query = f"""SELECT * FROM `{table_observed}`""" # selecionando todos os dados da tabela eventos
schema = get_schemas(table_path=table_observed)
print("Schemas coletados!\n")


select_return = select_bq(query)
print("Query concluída com sucesso! \n")

for row in select_return:
    print("Enviando mensagem para o VERTEX AI... \n")
    message = f"""Tenho uma tabela no Big Query chamada {table_observed} que possui o seguinte esquema {schema}.Meu objetivo é criar uma VIEW com o nome {row['attributes']['event']} a partir de um SQLX apenas com os valores que estão na coluna "data" e quero que esses dados estejam no mesmo tipos que estão no JSON,  como ela está em um formato JSON será necessário usar a função JSON_VALUE. {row["data"]}, Me retorne apenas a query SQLX"""

    response_chat = generate(message)

    querysql = get_query_in_response(response_chat.text)

    create_sqlx(querysql, "eventos_data")
    
    upload_sqlx_file(project_id, repository_id, workspace, file_path_local, file_path_repo)
    execute_job(project_id, repository_id, workspace, dataset_id, file_name)

print("Deu tudo certo")
    