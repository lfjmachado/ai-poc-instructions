---
description: Revisão de sintaxe e otimização para scripts Spark SQL.
applyTo: "**/scripts/*.sql"
---

# Regras de Revisão para Scripts Spark SQL

Para todos os arquivos novos ou modificados que se enquadram em `**/scripts/*.sql`, o revisor (Copilot) deve estritamente aplicar as seguintes regras no code review do Pull Request (PR):

1.  **Sintaxe e Padrões (Obrigatório):**
    * Garantir que a sintaxe SQL seja **válida e compatível com Spark SQL**.
    * Garantir que o script siga os padrões de nomenclatura e formatação da equipe (por exemplo, palavras-chave em maiúsculas, aliases claros, identação).
    * Garantir o uso correto de variáveis de ambiente/parâmetros (ex: `${data_processamento}`).

2.  **Otimização de Query (Obrigatório):**
    * **Identificar e sugerir otimizações de performance.**
    * Revisar consultas com subqueries complexas ou repetidas e sugerir o uso de **Common Table Expressions (CTEs)** (cláusula `WITH`) para melhor legibilidade e potencial otimização.
    * Verificar a eficiência de `JOIN`s, garantindo que os campos de união estejam corretamente indexados ou sejam de tipos de dados compatíveis, e que o tipo de JOIN seja o mais eficiente para a operação (ex: preferir `INNER JOIN` a `FULL OUTER JOIN` quando possível).
    * Alertar sobre o uso de funções que possam causar a varredura completa da tabela (`full scan`) sem necessidade de filtros eficientes.
    * Recomendar a aplicação de filtros (cláusula `WHERE`) o mais cedo possível para reduzir o volume de dados a serem processados.
3. **Otimização de Query (Obrigatório):**
   * **Revisar consultas com subqueries complexas ou repetidas e sugerir o uso de Common Table Expressions (CTEs) (cláusula WITH) para melhor legibilidade e potencial otimização, conforme exigido pelo TIME-DATA-PLATFORM.** * Verificar a eficiência de JOINs.
   * Alerte se a query não for escalável, **pois o TIME-DATA-PLATFORM exige otimização máxima.**