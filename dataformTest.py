import time
from google.cloud import dataform_v1beta1 as dataform


"""
    Faz upload de um arquivo SQLX para o repositório Dataform em uma workspace específica.

    Parâmetros:
        project_id (str): O ID do projeto do Google Cloud.
        repository_id (str): O ID do repositório no Dataform.
        workspace (str): O nome da workspace onde o arquivo será carregado.
        file_path_local (str): Caminho local do arquivo SQLX.
        file_path_repo (str): Caminho no repositório Dataform onde o arquivo será salvo.

    Funcionalidade:
        - Carrega um arquivo local (SQLX) para o workspace de um repositório Dataform.
        - Codifica o conteúdo do arquivo em UTF-8.
    """
def upload_sqlx_file(project_id, repository_id, workspace, file_path_local, file_path_repo):
    """
    Faz upload de um arquivo SQLX para o repositório Dataform em uma workspace específica.
    """
    try:
        # Inicializa o cliente do Dataform
        client = dataform.DataformClient()

        # Definindo o caminho correto do repositório
        repository_name = client.repository_path(project_id, "us-central1", repository_id)

        # Lendo o conteúdo do arquivo local
        with open(file_path_local, "r") as file:
            file_content = file.read()

        # Definindo o caminho do arquivo no repositório
        file_name = f"definitions/{file_path_repo}"

        # Preparando o nome do workspace
        workspace_name = f"{repository_name}/workspaces/{workspace}"

        # Montando o request para escrever o arquivo no workspace
        request = dataform.WriteFileRequest(
            workspace=workspace_name,
            path=file_name,
            contents=file_content.encode("utf-8")  # Certifique-se de codificar o conteúdo do arquivo
        )

        # Enviando o arquivo para o workspace
        client.write_file(request=request)

        print(f"Arquivo {file_name} enviado com sucesso para o workspace {workspace}.")

    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")


"""
    Cria um resultado de compilação para um repositório Dataform.

    Parâmetros:
        project_id (str): O ID do projeto do Google Cloud.
        repository_id (str): O ID do repositório no Dataform.
        workspace (str): A branch ou workspace que está sendo compilada.

    Funcionalidade:
        - Gera um resultado de compilação para os arquivos carregados no workspace.
        - Retorna a resposta da API com o resultado da compilação.
    """
def sample_create_compilation_result(project_id, repository_id, workspace):
    # Cria um cliente para o Dataform
    client = dataform.DataformClient()

    # Inicialize os argumentos da solicitação
    compilation_result = dataform.CompilationResult()
    # Substitua por seu branch, tag ou commit
    compilation_result.workspace = f"projects/{project_id}/locations/us-central1/repositories/{repository_id}/workspaces/{workspace}"    

    # Defina o parent corretamente com o caminho para o repositório
    request = dataform.CreateCompilationResultRequest(
        parent=f"projects/{project_id}/locations/us-central1/repositories/{repository_id}",
        compilation_result=compilation_result,
    )

    # Faz a solicitação para criar o resultado de compilação
    response = client.create_compilation_result(request=request)

    print(response)
    # Manipula a resposta
    return response
# sample_create_compilation_result()


"""
    Executa um job completo no Dataform, desde a compilação dos arquivos até a execução de um workflow.

    Parâmetros:
        project_id (str): O ID do projeto do Google Cloud.
        repository_id (str): O ID do repositório no Dataform.
        workspace (str): A branch ou workspace que será compilada e executada.
        dataset_id (str): O dataset no BigQuery que será alvo da execução.
        file_name (str): O nome do arquivo que será executado.

    Funcionalidade:
        - Compila os arquivos no repositório Dataform.
        - Executa o workflow correspondente e retorna o resultado da execução.
    """
def create_workflow_invocation(compilation_result, project_id, repository_id, dataset_id, file_name):
    # Cria um cliente para o Dataform
    client = dataform.DataformClient()

    # Inicialize os argumentos da invocação do workflow
    workflow_invocation = dataform.WorkflowInvocation()

    # Define o compilation result a partir do valor obtido
    workflow_invocation.compilation_result = compilation_result

    workflow_invocation.invocation_config.included_targets.extend([
        dataform.Target(
            database=project_id,   
            schema=dataset_id,   
            name=file_name
        )
    ])

    # Crie o request de invocação
    request = dataform.CreateWorkflowInvocationRequest(
        parent=f"projects/{project_id}/locations/us-central1/repositories/{repository_id}",
        workflow_invocation=workflow_invocation,
    )

    # Faz a solicitação para criar o workflow invocation
    response = client.create_workflow_invocation(request=request)

    print(response)
    # Manipula a resposta
    return response
#create_workflow_invocation()

"""
    Executa um job completo no Dataform, desde a compilação dos arquivos até a execução de um workflow.

    Parâmetros:
        project_id (str): O ID do projeto do Google Cloud.
        repository_id (str): O ID do repositório no Dataform.
        workspace (str): A branch ou workspace que será compilada e executada.
        dataset_id (str): O dataset no BigQuery que será alvo da execução.
        file_name (str): O nome do arquivo que será executado.

    Funcionalidade:
        - Compila os arquivos no repositório Dataform.
        - Executa o workflow correspondente e retorna o resultado da execução.
    """
def execute_job(project_id, repository_id, workspace, dataset_id, file_name):

    compilation_result = sample_create_compilation_result(project_id=project_id, repository_id=repository_id, workspace=workspace)

    workflow_invocation = create_workflow_invocation(compilation_result=compilation_result.name, project_id=project_id, repository_id=repository_id, dataset_id=dataset_id, file_name=file_name)

    return workflow_invocation