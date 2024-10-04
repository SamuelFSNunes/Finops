from google.cloud import secretmanager
import os
import json

def get_credentials_from_secret_manager(secret_id, project_id):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    # Acessa o secret
    response = client.access_secret_version(name=secret_name)
    secret_payload = response.payload.data.decode('UTF-8')
    
    # Salva as credenciais temporariamente em um arquivo
    credentials_path = "temp_credentialsBQ.json"
    with open(credentials_path, "w") as f:
        f.write(secret_payload)
    
    # Define a variável de ambiente com o caminho do arquivo de credenciais
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Chame a função passando o nome do secret e o projeto
get_credentials_from_secret_manager(secret_id="bigquery-key", project_id="499926906409")

# Agora suas credenciais já estão configuradas, e você pode usar o BigQuery normalmente.
