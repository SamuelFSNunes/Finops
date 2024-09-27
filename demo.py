from google.cloud import bigquery

client = bigquery.Client()

def select_bq(query_sql):

    return client.query(query_sql)
