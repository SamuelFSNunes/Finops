from google.cloud import bigquery

client = bigquery.Client()
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

    return client.query(query_sql)
