---
description: Validação RÍGIDA de Integridade Cross-File (Orquestração, Metadados e SQL) para garantir a compatibilidade do pipeline Data Platform.
applyTo: "src/teste/**/orchestration/**/*.*"
---

# 🔗 VALIDAÇÃO DE INTEGRIDADE CROSS-FILE (BLOQUEIO OBRIGATÓRIO)

O revisor (GitHub Copilot) deve executar uma inspeção crítica em todos os arquivos relacionados ao pipeline (Orquestração, Metadados e Scripts SQL) dentro do Pull Request. O objetivo é garantir que todas as referências entre arquivos sejam consistentes e que o schema de dados esteja sincronizado.

## SEÇÃO 1: CONSISTÊNCIA E LOCALIZAÇÃO DE ARQUIVOS (HIGH PRIORITY)

### 1.1. Compatibilidade de Localização (MANDATÓRIO)
* **Verificar:** Garantir que o arquivo de Metadados correspondente (mesmo nome, mesma zona, na pasta `metadata`) **exista** no PR ou no repositório.
* **Verificar:** Garantir que um arquivo SQL correspondente (assumindo o mesmo nome base, na pasta `scripts` do mesmo `tipo` de query, ex: `sparksql`) **exista** no PR ou no repositório, ou que seja referenciado explicitamente dentro do JSON de Orquestração, se a estrutura for mais complexa.
* **Ação:** Se qualquer um dos arquivos ligados estiver ausente, emita um comentário de BLOQUEIO OBRIGATÓRIO.

### 1.2. Identificação de Alteração (Novo vs. Existente)
* **Diagnóstico:** Determinar se o PR está criando um **Novo Pipeline** (se Orquestração, Metadados e SQL forem arquivos ADDED) ou **Alterando um Existente** (se forem MODIFIED). Use essa informação para priorizar a revisão do schema (Se for novo, o schema deve ser perfeito).

## SEÇÃO 2: COMPATIBILIDADE SQL E METADADOS (CRITICAL)

### 2.1. Sincronização de Schema (MÁXIMA PRECISÃO)
* **Extração SQL:** Analisar o script SQL correspondente para determinar o **Schema de Saída (Output Schema)**. O revisor deve listar os **nomes** e **tipos de dados** (inferidos) de todas as colunas no `SELECT` final da query.
* **Comparação com Metadados:** Comparar a lista de colunas extraída do SQL com o array `"Columns"` no arquivo de Metadados correspondente.
    * **Nomes e Tipos:** Todos os nomes de campos e seus tipos de dados devem ser **IDÊNTICOS** entre o output do SQL e o Metadado.
    * **Ordem (Se Aplicável):** Se a ordem dos campos no SQL for crucial para a escrita (ex: `INSERT INTO` sem lista de colunas), a ordem no Metadado deve refletir a ordem do `SELECT`.

* **Ação:** Se houver qualquer divergência (coluna faltando, nome diferente, tipo de dado incompatível), emita um comentário de BLOQUEIO OBRIGATÓRIO citando a linha no SQL e a linha no Metadado que precisam ser corrigidas.

### 2.2. Verificação de Colunas nas Regras de Qualidade (GDQ)
* **Extração GDQ:** Inspecionar o array `GdqRules.Rules` no JSON de Orquestração.
* **Verificação:** Para cada regra (ex: `IsPrimaryKey 'id_transacao'`, `Completeness 'valor'`), o nome da coluna referenciada (`id_transacao`, `valor`) **deve existir** como um `"campo"` no array `Columns` do arquivo de Metadados correspondente.
* **Ação:** Se uma regra de qualidade referenciar uma coluna inexistente no Metadado, emita um BLOQUEIO obrigatório.

## SEÇÃO 3: VALIDAÇÃO DE PARÂMETROS E REGRAS DE NEGÓCIO

### 3.1. Consistência de Zonas (Cross-File)
* Verificar se a zona inferida do caminho do arquivo (Seção 1.1) é **igual** à zona declarada no campo `zone` do arquivo de Metadados.

### 3.2. Referência de Query (SparkSql/Athena)
* Se o `"tipo"` for `sparksql` ou `athena`, garantir que a estrutura `SparkSql` ou `Athena` referencie corretamente os recursos necessários para a execução, e que o arquivo SQL correspondente (se existir) esteja no subdiretório correto (e.g., `sparksql` ou `athena` dentro de `scripts/`).