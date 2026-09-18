# Check Point 01 — Coding for Security

**Aluno:** Enzo Parada Seixas (RM 572294)
**Professor:** Fabio Bara
**Conteúdo avaliado:** Aulas 1 a 4 — SQL vs NoSQL, MongoDB (PyMongo), MySQL (mysql-connector-python), Machine Learning (scikit-learn)

## Estrutura

```
cp01-coding-security-fiap/
├── docker-compose.yml       # sobe MySQL e MongoDB para o laboratório
├── requirements.txt
├── data/
│   └── auth.log             # log de autenticação usado no Exercício 10 (arquivo
│                             # original de fabioBaraDev/coding_for_security,
│                             # GS_1Semestre/securaPy/logs/auth.log)
├── ex1_sql_crud.py          # Ex 1  - Modelagem e CRUD SQL (tabela ativos)
├── ex2_mongo_crud.py        # Ex 2  - CRUD com PyMongo (vulnerabilidades)
├── ex3_mongo_agg.py         # Ex 3  - Agregação: Top IPs
├── ex4_sql_injection.py     # Ex 4  - Query insegura vs parametrizada
├── ex5_transacao.py         # Ex 5  - Transação com rollback
├── ex6_indice.py            # Ex 6  - Índice e desempenho (MongoDB)
├── ex7_classificador.py     # Ex 7  - RandomForest: tráfego normal vs malicioso
├── ex8_anomalias.py         # Ex 8  - IsolationForest: detecção de anomalias
├── ex9_metricas.py          # Ex 9  - Métricas honestas (matriz de confusão etc.)
└── ex10_siem_pipeline.py    # Ex 10 - Mini-pipeline SIEM: log -> MongoDB -> ML
```

## Ambiente

### 1. Subir os bancos com Docker

```bash
docker-compose up -d
```

Isso sobe:
- **MySQL** em `localhost:3306` (usuário `root`, senha `root`, banco `cp01_security`)
- **MongoDB** em `localhost:27017` (banco `cp01_security`)

Aguarde alguns segundos até os containers ficarem saudáveis (`docker ps`).

### 2. Instalar dependências Python

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Variáveis de ambiente (opcional)

Os scripts já usam os valores padrão do `docker-compose.yml`. Para customizar:

| Variável | Padrão |
|---|---|
| `MYSQL_HOST` | `localhost` |
| `MYSQL_PORT` | `3306` |
| `MYSQL_USER` | `root` |
| `MYSQL_PASSWORD` | `root` |
| `MYSQL_DATABASE` | `cp01_security` |
| `MONGO_URI` | `mongodb://localhost:27017` |
| `MONGO_DATABASE` | `cp01_security` |

## Executando cada exercício

```bash
python ex1_sql_crud.py
python ex2_mongo_crud.py
python ex3_mongo_agg.py
python ex4_sql_injection.py
python ex5_transacao.py
python ex6_indice.py
python ex7_classificador.py
python ex8_anomalias.py
python ex9_metricas.py
python ex10_siem_pipeline.py
```

Cada script é independente, cria/recria suas próprias tabelas ou coleções e imprime a saída esperada no enunciado.

## Observação de segurança (Exercício 4)

O `ex4_sql_injection.py` contém propositalmente uma função vulnerável a SQL Injection (`busca_insegura`) para fins didáticos, comparando-a com a versão segura e parametrizada (`busca_segura`). Rode apenas no banco local de laboratório, nunca em produção.
