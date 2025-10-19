---
description: Revisão de SINTAXE e Performance de Alto Nível para Scripts SPARK SQL.
applyTo: "**/scripts/sparksql/**/*.sql"
---

# 🔎 REVISÃO DE SPARK SQL (PRIORIDADE: SINTAXE > PERFORMANCE)

O revisor (GitHub Copilot) deve executar uma validação em duas fases. A prioridade máxima é a validação da sintaxe, seguida pela análise profunda de otimização de performance para o ambiente distribuído Spark.

## FASE 1: VALIDAÇÃO DE SINTAXE E PADRÕES (MÁXIMA PRIORIDADE - BLOQUEIO)

### 1.1. Sintaxe e Conformidade (MANDATÓRIO)
* **Verificar:** A sintaxe SQL deve ser **100% válida e compatível** com o dialeto Spark SQL (incluindo funções, tipos e operadores específicos).
* **Alerte:** Se houver um erro de sintaxe, o Copilot deve bloquear a revisão com um comentário obrigatório, sugerindo a correção exata.

### 1.2. Padrões de Qualidade (MANDATÓRIO)
* Garantir que o script siga os padrões de nomenclatura do TIME-DATA-PLATFORM (e.g., `snake_case` para identificadores, palavras-chave em **MAIÚSCULAS**).
* Garantir o uso correto de variáveis/parâmetros (e.g., sintaxe `${nome_da_variavel}`).
* Garantir que os comentários sejam em português.

## FASE 2: OTIMIZAÇÃO DE PERFORMANCE DISTRIBUÍDA (ALTA PRIORIDADE)

Otimizações de Spark SQL são críticas para o custo e a escalabilidade, conforme o requisito global do TIME-DATA-PLATFORM.

### 2.1. Otimização Estrutural (CTEs e Complexidade)
* **CTEs (Common Table Expressions):** Identificar subqueries complexas, aninhadas ou repetidas e sugerir ativamente a refatoração para o uso de cláusulas `WITH` (CTEs).
* **Encadeamento:** Recomendar a simplificação de operações longas em etapas intermediárias para melhor gerenciamento de *DAG* (Directed Acyclic Graph) do Spark.

### 2.2. Gerenciamento de Dados e JOINs
* **Predicado Pushdown / Filtro Inicial:** Garantir que as cláusulas `WHERE` (filtros) sejam aplicadas o mais cedo possível na query para reduzir o volume de dados a serem lidos e processados *antes* de qualquer `JOIN` ou agregação.
* **Otimização de JOINs:**
    * Alertar sobre `JOIN`s que não usem colunas particionadas/indexadas de forma eficiente.
    * Sugira o uso de `BROADCAST JOIN` (ou o hint `/*+ BROADCAST(tabela_menor) */`) se uma das tabelas for significativamente menor (idealmente <= 10GB), promovendo otimização máxima.
* **Data Skew (Dados Enviesados):** Se a query executar uma agregação (`GROUP BY`) ou `JOIN` em uma coluna de alta cardinalidade onde se espera desbalanceamento de dados, sugerir técnicas de prevenção de *Skew*, como *salting* ou o uso de hints de otimização de Skew do Spark (se aplicável à versão em uso).

### 2.3. Controle de Particionamento (Partition Pruning)
* **Partição:** Verificar se a query está utilizando colunas de partição no `WHERE` (e.g., `data_processamento = '2023-01-01'`) para garantir que o Spark leia apenas os arquivos de dados necessários, evitando a varredura completa (`full scan`).

## 3. Qualidade da Revisão (ENHANCEMENT)
* **Tom:** Mantenha um tom profissional e de alto nível de engenharia. Para cada sugestão de otimização, justifique o ganho de performance esperado (e.g., "Usar CTE reduz a recomputação" ou "Broadcast Join evita o Shuffle de dados").