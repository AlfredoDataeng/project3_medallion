
---

# 🏅 Arquitectura Medallion com dbt e PostgreSQL

Pipeline de dados ELT completo com arquitectura em camadas Bronze → Silver → Gold, construído com Python, dbt e Docker.

---

## 📋 Sobre o Projecto

Este projecto implementa uma arquitectura Medallion num warehouse PostgreSQL local, integrando dados de transacções bancárias angolanas com taxas de câmbio em tempo real da ExchangeRate API.

O objectivo é demonstrar como organizar dados em camadas progressivas de qualidade, aplicando boas práticas de engenharia de dados como testes automáticos, documentação e separação de responsabilidades entre ferramentas.

---

## 🏗️ Arquitectura

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────────────────────────────┐
│   FONTES        │     │  INGESTÃO    │     │          WAREHOUSE (PostgreSQL)          │
│                 │     │              │     │                                          │
│  CSV locais     │────►│   Python     │────►│  BRONZE  →  SILVER  →  GOLD             │
│  Exchange API   │     │  (ELT)       │     │  (raw)      (clean)    (metrics)        │
└─────────────────┘     └──────────────┘     └─────────────────────────────────────────┘
                                                              ▲
                                                             dbt
```

### Camadas

|Camada|Tipo|Descrição|
|---|---|---|
|**Bronze**|Tabelas|Dados brutos sem transformação|
|**Silver**|Views|Dados limpos e padronizados com dbt|
|**Gold**|Tabelas|Métricas de negócio prontas para análise|

---

## 🛠️ Stack Tecnológica

|Ferramenta|Versão|Papel|
|---|---|---|
|Python|3.x|Ingestão de dados (ELT)|
|dbt-postgres|1.7.4|Transformações dentro do warehouse|
|PostgreSQL|16.1|Data Warehouse|
|Docker|-|Containerização do ambiente|
|pandas|-|Manipulação de dados|
|sqlalchemy|-|Ligação ao PostgreSQL|

---

## 📁 Estrutura do Projecto

```
project3_medallion/
│
├── ingest/
│   ├── extract.py          # Extracção de CSVs e API
│   └── load_bronze.py      # Carregamento na camada Bronze
│
├── dbt_project/
│   └── medallion/
│       ├── models/
│       │   ├── bronze/
│       │   │   └── sources.yml          # Declaração das fontes Bronze
│       │   ├── silver/
│       │   │   ├── stg_transacoes.sql   # Transacções limpas
│       │   │   ├── stg_clientes.sql     # Clientes limpos
│       │   │   ├── stg_taxa_cambio.sql  # Taxas filtradas (AOA, EUR)
│       │   │   └── schema.yml           # Testes Silver
│       │   └── gold/
│       │       ├── mart_transacoes_por_provincia.sql
│       │       ├── mart_churn_clientes.sql
│       │       ├── mart_resumo_cambio.sql
│       │       └── schema.yml           # Testes Gold
│       ├── macros/
│       │   └── generate_schema_name.sql # Schema correcto por camada
│       └── dbt_project.yml
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🗄️ Modelos dbt

### Bronze — Dados Brutos

|Tabela|Linhas|Descrição|
|---|---|---|
|`bronze.transacoes_raw`|5.080|Transacções bancárias com problemas reais|
|`bronze.clientes_raw`|200|Dados de clientes do banco|
|`bronze.taxas_cambio_raw`|166|Todas as taxas de câmbio face ao USD|

### Silver — Dados Limpos

|View|Descrição|
|---|---|
|`silver.stg_transacoes`|Duplicados removidos, IDs normalizados, datas tratadas|
|`silver.stg_clientes`|Booleanos convertidos, datas normalizadas|
|`silver.stg_taxa_cambio`|Filtrado apenas AOA e EUR|

### Gold — Métricas de Negócio

|Tabela|Descrição|
|---|---|
|`gold.mart_transacoes_por_provincia`|Volume e valor total por província|
|`gold.mart_churn_clientes`|Clientes com conta inactiva e histórico de transacções|
|`gold.mart_resumo_cambio`|Taxa actual do AOA e EUR face ao USD|

---

## ✅ Testes de Qualidade

12 testes dbt nativos — todos passaram:

```
PASS=12 WARN=0 ERROR=0 SKIP=0
```

Testes aplicados:

- `unique` — sem valores duplicados nas chaves primárias
- `not_null` — sem valores nulos em colunas críticas

---

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Conta gratuita na [ExchangeRate API](https://www.exchangerate-api.com/)

### 1. Clonar o repositório

```bash
git clone https://github.com/teu-usuario/project3_medallion.git
cd project3_medallion
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edita o .env com a tua API_KEY
```

### 3. Subir os containers

```bash
docker-compose up -d
```

### 4. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 5. Carregar dados na camada Bronze

```bash
python ingest/load_bronze.py
```

### 6. Executar transformações dbt (Silver + Gold)

```bash
docker exec -it dbt dbt run --project-dir /usr/app/dbt/medallion
```

### 7. Correr os testes

```bash
docker exec -it dbt dbt test --project-dir /usr/app/dbt/medallion
```

### 8. Ver a documentação

```bash
docker exec -it dbt dbt docs generate --project-dir /usr/app/dbt/medallion
docker exec -it dbt dbt docs serve --project-dir /usr/app/dbt/medallion --port 8081
```

Abre **http://localhost:8081**

---

## 📚 Conceitos Demonstrados

- **Arquitectura Medallion** — organização de dados em Bronze, Silver e Gold
- **ELT vs ETL** — transformação dentro do warehouse em vez de fora
- **dbt** — modelagem, testes e documentação de dados com SQL
- **Data Lineage** — rastreabilidade do fluxo de dados entre camadas
- **Qualidade de Dados** — testes automáticos em cada camada
- **Docker** — ambiente reproduzível e isolado

---

## 👤 Autor

**Alfredo** **Francisco**— Engenheiro de Dados em formação  
[LinkedIn](https://www.linkedin.com/in/alfredo-francisco-721b6a34a/) 