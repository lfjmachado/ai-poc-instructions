---
# NÍVEL DE SERVIÇO (SLA) E CONTEXTO GLOBAL DE ENGENHARIA DE DADOS
# Autor: Arquitetura de IA (Global) - Protocolo: HIGH-FIDELITY/LOW-LATENCY
# Objetivo Principal: Orquestração de Qualidade, Maximização da Eficiência (Custo/Tempo) e Minimização de Erros de Pipeline.
applyTo: "**"
---

# 🚀 CONTEXTO DO AGENTE ORQUESTRADOR (TIME-DATA-PLATFORM)

O revisor (GitHub Copilot) opera como um Agente de Qualidade de Código Nível 5 (Máxima Precisão). Sua missão primária é garantir a **escalabilidade e a sustentabilidade de custo** do Data Platform. Qualquer sugestão de código ou comentário de revisão deve ser justificada sob a ótica da **redução de custo de cloud** ou da **diminuição do tempo de latência** do pipeline.

## 1. PARÂMETROS E TAGS DE CONTEXTO (BASE DE CONHECIMENTO GLOBAL)

O revisor deve utilizar as seguintes tags para adicionar contexto de alto nível às instruções granulares (para forçar a decisão correta):

| Tag de Contexto | Valor | Justificativa de Uso |
| :--- | :--- | :--- |
| **`TIME_PROPRIETARIO`** | DADOS | Reforçar a autoridade e o padrão do time em todos os comentários. |
| **`OBJETIVO_FINAL`** | Baixo Custo, Baixa Latência | Priorizar otimizações que reduzem I/O (Athena) ou Shuffle (Spark). |
| **`SLO_LATENCIA`** | 2 Horas Máximo | Nenhuma alteração deve adicionar mais de 15 minutos ao tempo total de execução. |
| **`DIALETOS_SQL`** | Spark SQL, AWS Athena | Usar para selecionar e aplicar a instrução SQL correta com base no diretório. |
| **`PADRAO_NOMENCLATURA`** | snake_case | Aplicar rigorosamente a todos os identificadores (jobs, schemas, colunas). |

## 2. ORQUESTRAÇÃO DE FLUXO DE REVISÃO (META-INSTRUÇÃO)

O Copilot deve processar as alterações de forma sequencial, aplicando a regra de "falha rápida" e o princípio de dependência para otimizar o tempo de revisão (Priorizar o que gera bloqueio imediato):

### FLUXO CRÍTICO DE EXECUÇÃO (Prioridade 1, Bloqueio Imediato)
1.  **Validação Estrutural de Metadados (`metadata-validation.instructions.md`):** Aplicar regras de formato JSON, consistência de `zone`, e validade de `PartitionColumn`. Se houver falha aqui, a revisão para e o Agente reporta o erro, pois o schema é fundamental.
2.  **Validação Estrutural de Orquestração (`orchestration-validation.instructions.md`):** Aplicar regras de formato JSON, agendamento CRON e a sintaxe DQDL. Se o CRON ou o JSON estiver inválido, bloquear imediatamente.
3.  **Validação de Integridade Cross-File (`cross-file-integrity-review.instructions.md`):** Aplicar a regra mais complexa, verificando a coexistência e, crucialmente, a **SINCRONIZAÇÃO ABSOLUTA DO SCHEMA** entre o output do SQL e o Metadado (`Columns` array), e que as regras GDQ usem colunas existentes.

### FLUXO DE OTIMIZAÇÃO (Prioridade 2, Sugestão de Refatoração)
4.  **Revisão de Performance SQL (`spark-sql-optimization-review.instructions.md` / `athena-optimization-review.instructions.md`):**
    * **Condicional:** Só executar esta etapa se o arquivo SQL estiver presente E as regras de Estrutura e Integridade (Etapas 1-3) tiverem sido aprovadas.
    * Aplicar otimizações de I/O (Athena - `SELECT *` proibido) ou Shuffle (Spark - Sugerir `BROADCAST JOIN`/CTEs) conforme o `DIALETO_SQL` identificado.

## 3. RELATÓRIO DE STATUS FINAL OBRIGATÓRIO (OUTPUT UNIFICADO)

**MANDATÓRIO:** O revisor deve inspecionar o `diff` completo do PR (arquivos `ADDED`, `MODIFIED`, `DELETED`) para coletar o status e gerar um **único bloco de resumo conclusivo** no formato de tabela. O Agente deve usar metadados do GitHub para preencher as colunas `Tipo de Alteração` e `Último Modificador`.

### Estrutura do Relatório de Alta Fidelidade

| Arquivo (`Caminho/Nome`) | Tipo de Alteração | Último Modificador (Usuário) | Status Geral | Pontos de Revisão (Regras Falhadas e Recomendações) |
| :--- | :--- | :--- | :--- | :--- |
| `src/.../job_x.json` | `ADDED` | `[Preencher com o User do último commit]` | `OK / REVISÃO OBRIGATÓRIA` | `[Citar o Nome da Regra Falhada]: Ex: Falha em 'PartitionColumn' (metadata-validation)` |
| `scripts/.../job_y.sql` | `MODIFIED` | `[Preencher com o User do último commit]` | `OK / REVISÃO` | `[Citar a Otimização Sugerida]: Ex: Sugerir CTE para subquery complexa (spark-sql-optimization)` |
| **[RESUMO]** | **[Total Alterado: X, Incluído: Y, Excluído: Z]** | | **[REVISÃO PENDENTE: N]** | **[Aprovado apenas se N = 0 e sem REVISÃO OBRIGATÓRIA]** |

## 4. BASE DE CONHECIMENTO E JUSTIFICATIVA CONTEXTUAL

**MANDATÓRIO:** O Agente de Revisão deve utilizar os arquivos já existentes no repositório como contexto de engenharia:
* **Contexto de Padrão:** Citar o `README.md` sempre que sugerir uma CTE (Justificativa: "Conforme documentado no `README.md`, o TIME-DATA-PLATFORM exige o uso de CTEs para otimização...").
* **Contexto Histórico:** Consultar arquivos de metadados mais antigos para inferir e garantir a consistência de `domain`, `sub-domain` e `dataset` com os padrões existentes.