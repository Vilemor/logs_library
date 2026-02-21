# 📦 Structured JSON Logging Library

Biblioteca de logging estruturado em JSON com suporte a:

- ✅ Logs padronizados em JSON (JSON Lines)
- ✅ Decorators versionados para observabilidade automática
- ✅ Tratamento estruturado de exceções
- ✅ Suporte a campos personalizados (`extra`)
- ✅ Arquitetura extensível e pronta para produção
- ✅ Compatível com ELK, Datadog, CloudWatch

---

# 🏗 Arquitetura do Projeto
```
json_log_library/
    ├── init.py
    ├── formatter.py # Responsável por estruturar o JSON final
    ├── logger.py # Configuração do logger
    └── decorators/
        ├── init.py # Factory de versionamento
        ├── base.py # Classe base abstrata
        └── v1.py # Implementação do decorator v1
```
---


# 🎯 Objetivo

Padronizar logs da aplicação com:

- Estrutura previsível
- Observabilidade automática
- Separação de responsabilidades
- Extensibilidade via versionamento

---

# 📄 Estrutura do Log (Contrato Oficial)

Todos os logs seguem o seguinte formato:

```json
{
  "id_execucao": "uuid",
  "data_hora": "YYYY-MM-DD HH:MM:SS",
  "nivel": "INFO | ERROR | DEBUG | WARNING",
  "mensagem": "string",
  "funcao": "nome_funcao",
  "linha": 123,
  "tempo_execucao": 0.0004,
  "erro": {
      "tipo": "ZeroDivisionError",
      "mensagem": "division by zero",
      "traceback": "stack trace"
  }
}
```

🔹Campos obrigatórios

- id_execucao
- data_hora
- nivel
- mensagem
- funcao
- linha

🔹 Campos opcionais

- tempo_execucao
- erro
- Qualquer campo adicional via extra={}

🚀 Como Usar
1️⃣ Configurar o Logger

```python
from json_log_library.logger import configurar_logger
logger = configurar_logger()
```


2️⃣ Usar o Decorator de Execução
```python
from json_log_library.decorators import log_execucao

@log_execucao(logger)
def dividir(a: int, b: int) -> float:
    return a / b
```

Executando:
```python
dividir(10, 2)
dividir(10, 0)
```

3️⃣ Criar Logs Personalizados

```python
logger.info(
    "Processamento iniciado",
    extra={
        "evento": "startup",
        "ambiente": "dev",
        "versao_app": "1.0.0"
    }
)
```

Saída:

```json
{
  "id_execucao": "...",
  "data_hora": "...",
  "nivel": "INFO",
  "mensagem": "Processamento iniciado",
  "funcao": "main",
  "linha": 12,
  "evento": "startup",
  "ambiente": "dev",
  "versao_app": "1.0.0"
}
```

🧠 Boas Práticas
❌ Evite

```python
logger.info(f"Usuário {user} iniciou processo")
```

✅ Prefira

```python
logger.info(
    "Usuário iniciou processo",
    extra={"usuario": user}
)
```

Motivo

- Melhor indexação em ferramentas de observabilidade
- Evita parsing de string
- Estrutura mais limpa
- Compatível com ElasticSearch e DataDog

---
🔄 Versionamento de Decorators
- A biblioteca suporta versionamento de decorators.

```python
@log_execucao(logger, versao="v1")
```

Por que versionar?

Permite evoluir sem quebrar código legado:

- v1 → logging básico
- v2 → tracing distribuído
- v3 → métricas automáticas
- v4 → integração OpenTelemetry

🧩 Design Principles Aplicados
✅ SRP (Single Responsibility Principle)

- Formatter → só formata
- Logger → só configura
 Decorator → só trata execução
- Factory → controla versões

✅ Extensibilidade

Novas versões podem ser adicionadas sem alterar código existente.
---
📊 Compatibilidade

Funciona com:

- ELK Stack
- DataDog
- AWS CloudWatch
- Splunk
- Grafana Loki

Formato utilizado: JSON Lines (1 log por linha)
---

⚙️ Requisitos

Python 3.9+

---
🔒 Produção & Observabilidade

A estrutura atual permite evoluir para:

- Correlation ID automático
- Contextvars
- Async support
- Mascaramento de dados sensíveis
- OpenTelemetry
---

📌 Roadmap Futuro

-  Suporte a async functions
-  Correlation ID automático
-  Middleware para FastAPI
- Integração com OpenTelemetry
- Testes unitários com pytest
- Publicação como package (pyproject.toml)
---

👨‍💻 Autor (Guilherme Vilela Moreira)

Biblioteca desenvolvida para padronização de logs estruturados em ambientes críticos.
---
