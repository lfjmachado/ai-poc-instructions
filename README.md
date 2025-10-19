## **PoC: Automação de Code Review e Qualidade de Código com GitHub Copilot**

Este repositório serve como uma Prova de Conceito (PoC) para demonstrar a aplicação de Inteligência Artificial, via **GitHub Copilot**, na automação e padronização do processo de *Code Review* para a Plataforma de Dados (Data Platform).

O foco é validar a arquitetura de *commits* e arquivos de configuração (Orquestração, Metadados e Scripts SQL) antes que o código seja mesclado às *branches* principais.

### 💡 Objetivo da PoC

O objetivo principal é codificar o conhecimento de engenharia de dados em **Instruções Personalizadas do Copilot** (`.instructions.md`) para garantir:

1.  **Conformidade de Configuração:** Validação do formato JSON em arquivos de orquestração e metadados.
2.  **Integridade do Pipeline:** Garantia de que cada job de orquestração tenha seu arquivo de metadados correspondente.
3.  **Qualidade do Código Spark SQL:** Revisão automatizada da sintaxe, padrões e otimização de performance em scripts SQL.

### 📁 Estrutura do Projeto

A arquitetura de arquivos foi projetada para simular um ambiente real de Data Platform, onde a lógica de execução é separada dos metadados e dos scripts.

```
/
├── .github/
│   ├── copilot-instructions.md     # Contexto global para o Copilot (Ex: Nome do Time, Padrões gerais)
│   └── instructions/
│       ├── review-validation.instructions.md # Regras para JSON e Coexistência de arquivos
│       └── spark-sql-review.instructions.md  # Regras para otimização e sintaxe SQL
├── scripts/                      # Contém os scripts Spark SQL
│   └── processar_dados.sql
├── orchestration/                # Contém os arquivos de orquestração (JSON)
│   └── processar_dados.json
└── metadata/                     # Contém os arquivos de metadados correspondentes (JSON)
    └── processar_dados.json
```

### ⚙️ Como a Revisão de IA Funciona

O GitHub Copilot Code Review é configurado para ser executado automaticamente em *Pull Requests* (PRs) abertas, utilizando as seguintes regras:

| Arquivo de Instrução | Escopo (`applyTo`) | Foco da Revisão |
| :--- | :--- | :--- |
| `review-validation.instructions.md` | `**/metadata/*.json`, `**/orchestration/*.json` | **Formato:** Valida sintaxe JSON. **Integridade:** Verifica se todo arquivo em `orchestration` tem um par em `metadata`. |
| `spark-sql-review.instructions.md` | `**/scripts/*.sql` | **Performance:** Sugere o uso de CTEs, eficiência de `JOIN`s. **Qualidade:** Valida a sintaxe Spark SQL e o uso de variáveis. |
| `.github/copilot-instructions.md` | Global (`**`) | Define o **TIME-DATA-PLATFORM** como proprietário e reforça a prioridade máxima em *Otimização de Performance*. |

### 🛠️ Configuração de Revisão Automática

A execução automática do Copilot nas PRs é garantida via **GitHub Rulesets** (Conjuntos de Regras).

O *Ruleset* está configurado para:

1.  **Target branches:** Aplicar a regra a *branches* de desenvolvimento (Ex: `develop`) ou de *feature* (`feature/*`).
2.  **Branch rule:** Habilitar **Automatically request Copilot code review**.
3.  **Gatilho:** Executar a revisão tanto na criação da PR quanto em novos *pushes* de *commit* (dependendo da configuração do *Ruleset*).

### 🚀 Exemplo de Uso

Ao abrir um *Pull Request* que inclua um novo job de orquestração:

1.  O desenvolvedor envia `orchestration/novo_job.json` e `scripts/novo_job.sql`.
2.  Se o arquivo `metadata/novo_job.json` **não** for incluído, o Copilot, acionado pelo `review-validation.instructions.md`, emitirá um **comentário obrigatório** solicitando o arquivo de metadados ausente.
3.  Se o `novo_job.sql` tiver uma subconsulta ineficiente, o Copilot, acionado pelo `spark-sql-review.instructions.md` (e o contexto global de otimização), sugerirá a refatoração para **CTEs** para atender ao padrão do time.

-----

**Desenvolvido para:** Prova de Conceito (PoC)
**Tecnologia Principal:** GitHub Copilot Code Review (Custom Instructions)
**Domínio:** Plataforma de Dados (Data Platform)