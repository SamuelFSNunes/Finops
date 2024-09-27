import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import re


def generate(message):
    vertexai.init(project="squadcalouros", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        system_instruction=["""Você é um especialista em Big Query"""]
    )
    response = model.generate_content(
        [message],
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    return response

text1 = """Tenho uma tabela no Big Query chamada \"squadcalouros.dataform.eventos\" que possui o seguinte esquema [{\"name\": \"subscription_name\", \"mode\": \"\", \"type\": \"STRING\", \"description\": \"\", \"fields\": []}, {\"name\": \"message_id\", \"mode\": \"\", \"type\": \"STRING\", \"description\": \"\", \"fields\": []}, {\"name\": \"publish_time\", \"mode\": \"\", \"type\": \"TIMESTAMP\", \"description\": \"\", \"fields\": []}, {\"name\": \"data\", \"mode\": \"\", \"type\": \"JSON\", \"description\": \"\", \"fields\": []}, {\"name\": \"attributes\", \"mode\": \"\", \"type\": \"STRING\", \"description\": \"\", \"fields\": []}]. 
Meu objetivo é criar uma VIEW apenas com os valores que estão na coluna \"data\" e quero que esses dados estejam no mesmo tipos que estão no JSON,  como ela está em um formato JSON será necessário usar a função JSON_VALUE.
{\"account\":{\"account_number\":\"1234567890123456\",\"account_type\":\"Checking\",\"bank\":{\"address\":{\"city\":\"New York\",\"state\":\"NY\",\"street\":\"123 Main Street\",\"zip_code\":\"10001\"},\"branch\":\"Main Street\",\"name\":\"Global Bank\"},\"currency\":\"USD\"},\"recipient\":{\"account_number\":\"6543210987654321\",\"bank\":{\"address\":{\"city\":\"Los Angeles\",\"state\":\"CA\",\"street\":\"456 Broadway\",\"zip_code\":\"90001\"},\"branch\":\"Downtown\",\"name\":\"World Trust Bank\"},\"name\":\"John Doe\"},\"sender\":{\"account_number\":\"1111222233334444\",\"bank\":{\"address\":{\"city\":\"Chicago\",\"state\":\"IL\",\"street\":\"789 Business Lane\",\"zip_code\":\"60601\"},\"branch\":\"Corporate Plaza\",\"name\":\"Enterprise Bank\"},\"name\":\"ABC Corp\"},\"transaction_details\":{\"amount\":1500.75,\"description\":\"Salary for September 2024\",\"fees\":{\"amount\":15,\"currency\":\"USD\"},\"method\":\"Wire Transfer\",\"reference_number\":\"REF987654321\",\"status\":\"Completed\",\"timestamp\":\"2024-09-17T10:30:00Z\",\"type\":\"Credit\"},\"transaction_id\":\"TX123456789\"}.
Me retorne apenas a query"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
]

def get_query_in_response(response):
    match = re.search(r'CREATE\s+OR\s+REPLACE\s+VIEW\s+`[^`]+`\s+AS[\s\S]*?FROM\s+`([^`]+)`', response)

    if match:
        sql_query = match.group(0).strip()  # Obtemos a parte capturada e removemos espaços em branco
        print(sql_query)
        return sql_query
    else:
        print("Query não encontrada.")
        return

def create_sqlx(query, file_name):
    file_name = f"{file_name}.sqlx"
    with open(file_name, "w") as file:
    # Escreve o conteúdo do SQLX no arquivo
        file.write(query)
    print(f"Arquivo {file_name} criado com sucesso.")