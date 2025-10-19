---
description: Revisão de SINTAXE e Otimização de CUSTO/PERFORMANCE para Queries AWS ATHENA / Presto.
applyTo: "**/scripts/athena/**/*.sql"
---

# 💰 REVISÃO DE ATHENA/PRESTO (PRIORIDADE: SINTAXE > DADOS LIDOS)

O revisor (GitHub Copilot) deve focar em minimizar a quantidade de dados escaneados (lidos do S3), que é o fator primário de custo e latência do AWS Athena. A validação de sintaxe é a primeira etapa obrigatória.

## FASE 1: VALIDAÇÃO DE SINTAXE E PADRÕES (MÁXIMA PRIORIDADE - BLOQUEIO)

### 1.1. Sintaxe e Conformidade (MANDATÓRIO)
* **Verificar:** A sintaxe SQL deve ser **100% válida e compatível** com o dialeto Presto/Trino (que é o motor do Athena). Preste atenção especial a funções e tipos de dados que podem divergir do Spark ou de outros dialetos.
* **Alerte:** Se houver um erro de sintaxe, o Copilot deve bloquear a revisão com um comentário obrigatório, sugerindo a correção exata.

### 1.2. Padrões de Qualidade (MANDATÓRIO)
* Garantir o uso correto de variáveis/parâmetros (se aplicável ao ambiente de execução do Athena).
* Garantir que o script siga os padrões de nomenclatura e formatação da equipe.

## FASE 2: OTIMIZAÇÃO DE CUSTO E PERFORMANCE (ALTA PRIORIDADE)

Otimizações de Athena focam em reduzir I/O do S3 e uso de recursos do motor Presto.

### 2.1. Minimizar Dados Escaneados (REGRA DE OURO)
* **Projection Pushdown (SELECT *):** Proibir estritamente o uso de `SELECT *`. O revisor deve garantir que **apenas as colunas estritamente necessárias** sejam explicitamente selecionadas.
* **Partition Pruning (Poda de Partição):** Garantir que a query utilize filtros nas colunas de partição (`WHERE coluna_particao = valor`) para que o Athena possa ignorar pastas inteiras no S3, reduzindo drasticamente os dados lidos.
* **Predicado Pushdown:** Garantir que todos os filtros (`WHERE`) e projeções sejam empurrados para a fonte o máximo possível, aproveitando metadados de formatos como Parquet (e.g., *row group statistics*).

### 2.2. Tipos de Dados e Formatos
* **Formatos:** Se a query estiver interagindo com tabelas, o Copilot deve lembrar que o uso de formatos otimizados para colunas (como Parquet ou ORC) é crucial. Alertar caso a query pareça forçar a leitura de formatos não otimizados (e.g., CSV não compactado).
* **Tipos Otimizados:** Sugerir que tipos de dados como `VARCHAR` e `DECIMAL` sejam utilizados com o menor tamanho possível para a necessidade (e.g., `DECIMAL(8,2)` em vez de `DECIMAL(38,10)`).

### 2.3. Operações Complexas
* **Agregações:** Sugerir o uso de funções aproximadas (e.g., `approx_distinct`, `approx_percentile`) em vez de exatas, quando a precisão total não for necessária, para reduzir o uso de memória do Presto.
* **LIMITs:** Se um `LIMIT` estiver presente sem um `ORDER BY` anterior, alertar que o `LIMIT` pode não ser eficiente ou garantir resultados determinísticos. Se for apenas para amostragem, sugira o uso de cláusulas de amostragem (se disponíveis).

## 3. Qualidade da Revisão (ENHANCEMENT)
* **Tom:** Foco em custo-benefício. Para cada sugestão, o Copilot deve quantificar o ganho potencial em termos de redução de I/O de dados. Por exemplo, "Ao evitar `SELECT *`, você pode reduzir os dados lidos em até 80% se apenas 2 de 10 colunas forem necessárias."