import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import re

"""
    Gera um conteúdo com base na mensagem de entrada usando um modelo generativo do Vertex AI.

    Parâmetros:
        message (str): A mensagem de entrada para o modelo generativo.

    Retorno:
        response (str): A resposta gerada pelo modelo.

    Funcionalidade:
        - Inicializa o cliente Vertex AI no projeto especificado.
        - Configura o modelo generativo com as instruções de sistema e parâmetros de geração.
        - Chama o modelo para gerar uma resposta baseada na mensagem de entrada.
    """
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
    print(response.text)
    return response

# Define parâmetros como o número máximo de tokens de saída e outros ajustes de geração.
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Define parâmetros de segurança para bloquear conteúdo prejudicial ou ofensivo.
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

"""
    Extrai uma consulta SQL da resposta gerada pelo modelo.

    Parâmetros:
        response (str): A resposta gerada pelo modelo, que pode conter uma consulta SQL.

    Retorno:
        sql_query (str ou None): A query SQL extraída, ou None se não for encontrada.

    Funcionalidade:
        - Utiliza expressões regulares para buscar uma consulta SQL específica dentro da resposta.
        - Retorna a consulta encontrada ou uma mensagem de erro caso não encontre.
    """
def get_query_in_response(response):
    match = re.search(r'CREATE\s+OR\s+REPLACE\s+VIEW([\s\S]*?)FROM\s+(`?squadcalouros\.dataform\.\w+`?)', response)
    if match:
        sql_query = match.group(0).strip()  # Obtemos a parte capturada e removemos espaços em branco
        print(sql_query)
        return sql_query
    else:
        print("Query não encontrada.")
        print(match)
        return

"""
    Cria um arquivo `.sqlx` com a consulta SQL fornecida.

    Parâmetros:
        query (str): A query SQL que será gravada no arquivo.
        file_name (str): O nome base do arquivo sem extensão.

    Funcionalidade:
        - Gera um arquivo com a extensão `.sqlx` e escreve a consulta SQL no arquivo.
        - Exibe uma mensagem de sucesso após a criação do arquivo.
    """
def create_sqlx(query, file_name):
    file_name = f"{file_name}.sqlx"
    with open(file_name, "w") as file:
    # Escreve o conteúdo do SQLX no arquivo
        file.write(query)
    print(f"Arquivo {file_name} criado com sucesso.")