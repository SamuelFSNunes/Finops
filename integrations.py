from demo import select_bq, get_schemas
from demoAI import generate, get_query_in_response, create_sqlx
from dataformTest import upload_sqlx_file, execute_job

table_observed = "squadcalouros.dataform.eventos"

query = f"""SELECT * FROM `{table_observed}`"""
select_return = select_bq(query)
for row in select_return:
    select_return = row["data"]

schema = get_schemas(table_path=table_observed)

message = f"""Tenho uma tabela no Big Query chamada {table_observed} que possui o seguinte esquema {schema}.
Meu objetivo é criar uma VIEW a partir de um SQLX apenas com os valores que estão na coluna "data" e quero que esses dados estejam no mesmo tipos que estão no JSON,  como ela está em um formato JSON será necessário usar a função JSON_VALUE. {select_return}, Me retorne apenas a query SQLX"""

response_chat = generate(message)

querysql = get_query_in_response(response_chat.text)

create_sqlx(querysql, "eventos_data")

project_id = "squadcalouros" # ID do projeto
dataset_id = "dataform" # ID do dataset
repository_id = "teste"  # Nome simples do repositório
workspace = "testDataform"  # A branch onde você quer fazer o upload
file_name = "eventos_view" # Nome do arquivo
file_path_local = "eventos_data.sqlx"  # Caminho do arquivo local
file_path_repo = file_name + ".sqlx"  # Nome do arquivo dentro do repositório


upload_sqlx_file(project_id, repository_id, workspace, file_path_local, file_path_repo)
execute_job(project_id, repository_id, workspace, dataset_id, file_name)