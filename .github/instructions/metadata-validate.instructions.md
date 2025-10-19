---
description: Validação RÍGIDA de Metadados (Data Platform) - Garante conformidade de formato, estrutura, regras de negócio e coexistência.
applyTo: "src/teste/**/metadata/**/*.*"
---

# 🚨 REVISÃO OBRIGATÓRIA DE METADADOS (TIME-DATA-PLATFORM)

O revisor (GitHub Copilot) deve executar uma validação estrita e de alta precisão em **todos os arquivos JSON** que se enquadram no escopo. O foco é a conformidade técnica e a aderência total às regras de negócio da Plataforma de Dados para garantir escalabilidade.

## 1. Conformidade de Formato e Estrutura (STRICTLY REQUIRED)

### 1.1. Validação de Sintaxe JSON (MANDATÓRIO)
* **Verificar:** O arquivo deve ser um JSON válido e bem-formado. Não deve haver erros de sintaxe (como vírgulas perdidas ou chaves/valores sem aspas).
* **Ação:** Emitir um comentário de bloqueio/obrigatório se a sintaxe JSON for inválida.

### 1.2. Aderência ao Modelo de Estrutura (MANDATÓRIO)
O JSON deve conter os seguintes campos de estrutura (modelo de dados obrigatório):
* `domain`, `sub-domain`, `dataset`, `write-mode`, `zone`, `table-name`, `description`, `DataControl`, `PartitionColumn`, `Columns`.

### 1.3. Regras de Conteúdo e Nomenclatura (MANDATÓRIO)
* **Nome do Arquivo vs. `table-name`:** O valor do campo `"table-name"` deve ser **IDÊNTICO** ao nome do arquivo (sem a extensão `.json`).
* **Validação de `write-mode`:** O campo `"write-mode"` só pode aceitar os valores: `overwrite`, `append` ou `overwrite-append`.
* **Validação da `zone`:** O campo `"zone"` deve ser um dos valores permitidos: `sor`, `sot`, `spec`, `temp` ou `stage`.
    * **Consistência de Caminho:** O valor de `zone` deve corresponder ao nome do subdiretório onde o arquivo está localizado (ex: `.../sor/job.json` deve ter `"zone": "sor"`).

### 1.4. Regras de Validação do Array `Columns` (MANDATÓRIO)
* **Mínimo de Colunas:** O array `"Columns"` é **obrigatório** e deve conter **pelo menos 1** entrada.
* **Coluna Temporal:** O array `Columns` deve conter pelo menos uma coluna com `tipo: "date"` ou `tipo: "timestamp"`.
* **`PartitionColumn` e `DataControl` na Lista:**
    * O valor de `"PartitionColumn"` deve corresponder exatamente a um `"campo"` existente no array `Columns`.
    * O valor de `"DataControl"` deve corresponder exatamente a um `"campo"` existente no array `Columns`.
    * **Tipo da Partição:** O tipo (`tipo`) da coluna especificada em `PartitionColumn` deve ser estritamente `"date"` ou `"timestamp"`.

## 2. Validação de Coexistência (HIGH PRIORITY)

### 2.1. Arquivo de Orquestração (OBRIGATÓRIO)
* **Ação:** O revisor deve **verificar estritamente** a existência de um arquivo de Orquestração correspondente.
* **Caminho Esperado:** O arquivo deve existir no mesmo subdiretório relativo, mas na pasta `orchestration` (e.g., para `.../metadata/sor/job_x.json`, esperar `.../orchestration/sor/job_x.json`).
* **Consistência de Chaves:** Se o arquivo de Orquestração for encontrado, o `job_id` dentro dele deve corresponder ao `table-name` do metadado.
* **Alerte:** Se o arquivo de orquestração estiver ausente, ou as chaves não corresponderem, emita um **comentário obrigatório** destacando a necessidade da criação/correção.

### 2.2. Script SQL (RECOMENDADO)
* **Ação:** Verificar se o arquivo de Orquestração encontrado no item 2.1 referencia um script SQL (geralmente via campo `script_path`).
* **Caminho Esperado:** Verifique se o script SQL existe no repositório.
* **Alerte:** Se o script for referenciado no JSON de Orquestração, mas o arquivo SQL estiver **ausente** na PR ou no repositório, emita um **alerta de alta prioridade** solicitando a inclusão ou a confirmação de que o script já existe.

## 3. Qualidade da Revisão (ENHANCEMENT)
* **Tom:** Mantenha um tom profissional, educativo e focado em soluções imediatas. Sugira a linha de código exata para a correção sempre que possível.