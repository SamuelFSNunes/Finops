# README: Automação de Criação de View no BigQuery com Vertex AI e Dataform

Este projeto automatiza a criação de uma **VIEW** no BigQuery a partir de uma tabela que contém dados em formato **JSON**. Utilizando o poder do **Vertex AI** para gerar a consulta SQL e a integração com o **Dataform** para realizar o upload e execução do arquivo `.sqlx`, o pipeline é capaz de processar a tabela e gerar a view desejada com base nos dados JSON.

## Funcionalidades

1. **Consulta ao BigQuery**: Realiza uma consulta SQL em uma tabela do BigQuery e retorna os dados necessários para gerar a VIEW.
2. **Geração de Query SQL com Vertex AI**: Usa um modelo generativo no Vertex AI para criar automaticamente uma consulta SQL (em formato SQLX) com base nas informações da tabela do BigQuery.
3. **Criação de Arquivo SQLX**: Cria um arquivo `.sqlx` com a query gerada.
4. **Upload para o Dataform**: Faz upload do arquivo `.sqlx` para um workspace no Dataform.
5. **Execução de Job no Dataform**: Inicia o job que executa a SQLX no Dataform para criar a view no BigQuery.

## Arquitetura do Projeto

O projeto é dividido em três principais módulos:

- **demo.py**: Contém a função para realizar consultas SQL ao BigQuery.
- **demoAI.py**: Gerencia a integração com o Vertex AI para gerar a consulta SQL a partir de uma descrição, extrair a query da resposta e criar o arquivo `.sqlx`.
- **dataformTest.py**: Cuida do upload do arquivo SQLX para o Dataform e executa o job para compilar e rodar a SQLX.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `google-cloud-bigquery`: Para interagir com o BigQuery.
  - `vertexai`: Para usar o modelo generativo do Vertex AI.
  - `google-cloud-dataform`: Para interagir com o Dataform.
  - Outras dependências podem ser instaladas com `pip install -r requirements.txt`

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu_usuario/seu_projeto.git
cd seu_projeto
```

2. Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Autentique-se no Google Cloud:

```bash
gcloud auth application-default login
```
ou
```bash
$env:GOOGLE_APPLICATION_CREDENTIALS="credenciais_de_sua_conta_de_serviço"
```

5. Certifique-se de ter o **BigQuery**, **Vertex AI** e **Dataform** habilitados no seu projeto Google Cloud.

## Como Usar

### 1. Configurando Variáveis

No arquivo principal, preencha as variáveis com os valores do seu projeto:

```python
project_id = "squadcalouros"
repository_id = "teste"
workspace = "testDataform"
file_path_local = "eventos_data.sqlx"
file_path_repo = "eventos_view.sqlx"
```

- **project_id**: ID do seu projeto no Google Cloud.
- **repository_id**: Nome do repositório no Dataform.
- **workspace**: Branch no Dataform onde o arquivo SQLX será enviado.
- **file_path_local**: Caminho do arquivo `.sqlx` gerado.
- **file_path_repo**: Nome do arquivo dentro do repositório Dataform.

### 2. Executando o Pipeline

A função principal já contém todas as etapas. Basta executá-la para que todo o pipeline seja realizado:

```bash
python integrations.py
```

A execução faz o seguinte:

1. **Consulta ao BigQuery**: Extrai os dados da tabela `squadcalouros.dataform.eventos`.
2. **Geração de SQLX**: Gera uma query SQL usando o modelo generativo do Vertex AI e cria um arquivo `.sqlx`.
3. **Upload para Dataform**: Realiza o upload do arquivo SQLX para um workspace no Dataform.
4. **Execução do Job**: Executa o job no Dataform para processar e compilar o arquivo SQLX, criando a view desejada no BigQuery.

### 3. Monitoramento e Logs

Durante a execução, o sistema imprime logs no console para que você possa acompanhar o progresso e verificar eventuais erros.

### Exemplo de Uso

Este exemplo faz a seguinte consulta no BigQuery e gera uma view que contém apenas os valores da coluna `data`, convertendo-os a partir de JSON:

```sql
SELECT JSON_VALUE(data, "$.campo_especifico") as campo_especifico FROM `squadcalouros.dataform.eventos`
```

Essa query é gerada automaticamente pelo Vertex AI com base na descrição fornecida.

## Dependências Adicionais

O projeto também utiliza o Vertex AI para garantir que as queries SQL sejam geradas de forma inteligente e otimizada, assim como a integração com o Dataform para facilitar a compilação e execução do pipeline diretamente no BigQuery.

## Conclusão

Este pipeline automatiza a criação de views no BigQuery a partir de dados JSON, utilizando o poder de inteligência artificial e a flexibilidade do Dataform para manter a infraestrutura de dados organizada e automatizada.