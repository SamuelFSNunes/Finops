from google.cloud import bigquery

"""
    Executa uma consulta SQL no BigQuery.

    Parâmetros:
        query_sql (str): A string contendo a consulta SQL a ser executada.

    Retorno:
        google.cloud.bigquery.table.RowIterator: Retorna um iterador com as linhas resultantes da consulta.

    Funcionalidade:
        - Inicializa um cliente do BigQuery.
        - Executa a consulta SQL fornecida e retorna os resultados como um iterador.
    """
def select_bq(query_sql):
    client = bigquery.Client()
    return client.query(query_sql)


"""
    Obtém o esquema de uma tabela no BigQuery.

    Parâmetros:
        table_path (str): O caminho completo da tabela no formato 'projeto.dataset.tabela'.

    Retorno:
        list: Retorna uma lista de dicionários contendo as informações de esquema da tabela.
              Cada dicionário possui as seguintes chaves:
              - "name" (str): O nome do campo.
              - "type" (str): O tipo do campo (ex: STRING, INTEGER, etc.).
              - "mode" (str): O modo do campo (ex: NULLABLE, REQUIRED, REPEATED).

    Funcionalidade:
        - Inicializa um cliente do BigQuery.
        - Obtém o esquema da tabela especificada.
        - Retorna as informações do esquema da tabela como uma lista de dicionários.
"""
def get_schemas(table_path):
    client = bigquery.Client()
    
    # Obtém a tabela
    table = client.get_table(table_path)
    
    # Armazena os esquemas em uma lista de dicionários
    schema_list = []
    for schema_field in table.schema:
        schema_list.append({
            "name": schema_field.name,
            "type": schema_field.field_type,
            "mode": schema_field.mode
        })
    
    # Retorna a lista com o esquema da tabela
    return schema_list
