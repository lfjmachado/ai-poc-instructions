---
description: Validação RÍGIDA de Arquivos de Orquestração (Data Platform) - Garante formato, estrutura, agendamento CRON, tipo de query e conformidade com a sintaxe DQDL.
applyTo: "src/pricing/**/orchestration/**/*.*"
---

# 🛑 REVISÃO OBRIGATÓRIA DE ORQUESTRAÇÃO (ALTA PRECISÃO E RIGOR)

O revisor (GitHub Copilot) deve executar uma validação estrita e de alta precisão em **todos os arquivos JSON** de orquestração modificados ou adicionados. A não conformidade com qualquer regra listada na Seção 1 resultará em um comentário de **BLOQUEIO OBRIGATÓRIO**.

## SEÇÃO 1: VALIDAÇÃO TÉCNICA E SINTAXE (STRICTLY REQUIRED)

### 1.1. Conformidade de Formato JSON (MANDATÓRIO)
* **Verificar:** O arquivo deve ser um JSON válido e bem-formado.
* **Sintaxe:** Não deve haver erros de sintaxe ou formatação (ex: vírgulas perdidas, chaves/colchetes desbalanceados, aspas incorretas).
* **Ação:** Emitir um comentário de bloqueio/obrigatório imediatamente se a sintaxe JSON for inválida.

### 1.2. Validação de Estrutura e Agendamento (MANDATÓRIO)
* **Estrutura:** O JSON deve aderir à estrutura do modelo: `domain`, `sub-domain`, `dataset`, `tipo`, `table-name`, `schedule`, `dependencias`, e `GdqRules`.
* **Agendamento (Cron):** O valor do campo `"schedule"` deve ser uma **expressão CRON válida** (ex: `0 2 * * *`).

### 1.3. Regras de Qualidade (AWS Glue DQDL)
* **Sintaxe DQDL:** O array `GdqRules.Rules` deve conter regras que sigam estritamente a sintaxe do **AWS Glue Data Quality Definition Language (DQDL)** (ex: `Rowcount >0`, `IsPrimaryKey 'coluna'`).
* **Conexão de String (Crucial):** O revisor deve inspecionar os itens dentro do array `Rules` e garantir que, ao serem concatenados com vírgulas (`,`) para formar a string de regras final, o resultado seja uma string DQDL **sintaticamente correta** e sem vírgulas ou pontuações duplas ou ausentes que quebrariam a execução.

## SEÇÃO 2: VALIDAÇÃO DE NEGÓCIO E CONSISTÊNCIA (ALTA PRIORIDADE)

### 2.1. Consistência de Caminho (`zone`) (MANDATÓRIO)
* **Zona Permitida:** O revisor deve inferir a "zona" pelo nome do subdiretório do arquivo (ex: `.../orchestration/sor/job.json` implica zona `sor`).
* A zona inferida **deve ser** uma das seguintes: `sor`, `sot`, `spec`, `temp` ou `stage`.

### 2.2. Validação de Tipo de Query (MANDATÓRIO)
* **Tipo Permitido:** O campo `"tipo"` é obrigatório e deve ser **estritamente** `sparksql` ou `athena`.
* **Validação Condicional (SparkSql):** Se o campo `"tipo"` for `sparksql`, o revisor deve **obrigatoriamente** verificar a existência do array `"SparkSql"`. Este array deve conter **pelo menos uma** entrada (objeto) que defina uma tabela ou passo de execução.

## SEÇÃO 3: VERIFICAÇÃO DE COEXISTÊNCIA (INTEGRIDADE DO PIPELINE)

### 3.1. Arquivo de Metadados Correspondente (OBRIGATÓRIO)
* **Ação:** O revisor deve verificar a existência de um arquivo de Metadados correspondente com o **nome exato** no mesmo subdiretório relativo, mas na pasta `metadata` (e.g., para `.../orchestration/sor/job_x.json`, esperar `.../metadata/sor/job_x.json`).
* **Alerte:** Se o arquivo de Metadados estiver ausente, emita um **comentário obrigatório** destacando a falha de integridade do pipeline e solicitando a inclusão do metadado.