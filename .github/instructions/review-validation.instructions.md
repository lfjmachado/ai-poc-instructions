---
description: Validação de formato e coexistência para arquivos de Metadados e Orquestração.
applyTo: "**/metadata/*.json, **/orchestration/*.json"
---

# Regras de Revisão para Metadados e Orquestração

Para todos os arquivos novos ou modificados que se enquadram em `**/metadata/*.json` ou `**/orchestration/*.json`, o revisor (Copilot) deve estritamente aplicar as seguintes regras no code review do Pull Request (PR):

1.  **Validação de Formato JSON (Obrigatório):**
    * Verificar se o arquivo é um **JSON válido e bem-formado**. Não deve haver erros de sintaxe JSON.

2.  **Validação de Coexistência (Obrigatório):**
    * Se um arquivo for adicionado/modificado no caminho `**/orchestration/`, o revisor deve garantir que **existe um arquivo correspondente com o mesmo nome exato** na pasta `**/metadata/`.
    * Exemplo: Se `orchestration/job_x.json` existe, `metadata/job_x.json` deve existir na PR.

3.  **Validação de Conteúdo (Recomendado):**
    * Para arquivos em `**/metadata/*.json`, garantir que campos críticos como `schema` e `versao` estejam presentes.
    * Para arquivos em `**/orchestration/*.json`, garantir que o campo `job_id` corresponda ao nome do arquivo (ex: `job_id: "job_x"` para `job_x.json`).