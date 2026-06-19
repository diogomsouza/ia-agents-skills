# IA Agents Skills

Colecao de agents e skills para uso com Codex. O projeto organiza instrucoes reutilizaveis em `.codex/agents` e `.codex/skills`, junto com diretrizes globais em `.codex/AGENTS.md`.

## Agents

- `code-reviewer`: revisa codigo alterado contra as diretrizes do projeto, padroes de estilo, bugs relevantes e problemas de qualidade antes de commits ou pull requests.
- `code-reviewer-max`: revisa mudancas complexas com foco avancado em arquitetura, manutenibilidade, branching, abstracoes, contratos e qualidade estrutural.
- `code-reviewer-security`: revisa mudancas de alto risco com foco em seguranca, autorizacao, privacidade, integridade de dados, feature gates e regressoes criticas.
- `code-simplifier`: simplifica codigo recem-escrito ou modificado, preservando comportamento e priorizando clareza, consistencia e manutencao.
- `code-worker`: executa implementacoes, correcoes, refatoracoes e migracoes com foco rigoroso em clareza, limites arquiteturais e baixa complexidade incidental.
- `comment-analyzer`: analisa comentarios, docstrings e documentacao tecnica para verificar precisao, completude e risco de ficarem desatualizados.
- `csharp-expert`: apoia desenvolvimento .NET/C# com foco em convencoes da plataforma, design limpo, seguranca, testes, performance e manutencao.
- `optimizing-dotnet-performance`: analisa codigo .NET em busca de gargalos, recomenda otimizacoes concretas e orienta validacao com benchmarks.
- `pr-test-analyzer`: avalia a qualidade da cobertura de testes em pull requests, focando caminhos criticos, casos de borda e testes que previnem regressao real.
- `silent-failure-hunter`: audita tratamento de erros, fallbacks e blocos `catch` para encontrar falhas silenciosas, logs insuficientes e mensagens pouco acionaveis.
- `type-design-analyzer`: revisa o desenho de tipos, invariantes, encapsulamento e validacao para melhorar robustez e clareza do modelo de dominio.
- `win-forms-expert`: apoia criacao e manutencao de apps WinForms compativeis com o Designer, incluindo layout, binding, DPI, dark mode e regras para arquivos `.designer`.

## Skills

- `agent-hive`: coordena trabalhos maiores com planejamento persistente, delegacao para subagents, verificadores independentes, commits condicionais de checkpoint e acompanhamento em arquivo de progresso.
- `analyzing-dotnet-performance`: escaneia codigo .NET em busca de antipadroes de performance em async, memoria, strings, colecoes, LINQ, regex, serializacao e I/O.
- `architecture-blueprint-generator`: gera blueprint arquitetural a partir da analise do codebase, documentando stack, padroes, componentes, dependencias e diagramas.
- `angular-developer`: orienta e gera codigo Angular seguindo boas praticas modernas para componentes, servicos, reatividade, formularios, roteamento, acessibilidade, testes e CLI.
- `angular-new-app`: cria novas aplicacoes Angular com Angular CLI, incluindo checagem de CLI, flags apropriadas e configuracao de assistente de IA.
- `code-planner`: conduz um modo de planejamento conversacional para trabalho de implementacao antes de editar codigo, com exploracao sem mutacao, perguntas obrigatorias e plano final completo.
- `dotnet-webapi`: orienta criacao e modificacao de endpoints ASP.NET Core Web API com semantica HTTP, OpenAPI, DTOs e tratamento de erros.
- `gpt-image-2`: gera ou edita imagens bitmap com a API de Images da OpenAI usando o modelo `gpt-image-2`, salvando assets prontos para projetos.
- `grill-code`: conduz uma entrevista tecnica sobre um plano usando contexto, ADRs e documentos versionados, sem implementar codigo ate haver aprovacao explicita.
- `grill-me`: entrevista o usuario sobre um plano ou desenho, uma pergunta por vez, ate resolver ambiguidades e dependencias de decisao.
- `optimizing-ef-core-queries`: orienta otimizacao de consultas Entity Framework Core, cobrindo N+1, tracking, queries compiladas e armadilhas comuns de carga no banco.
- `thermo-nuclear-code-quality-review`: executa uma revisao extremamente rigorosa de manutenibilidade, abstracoes, arquivos grandes e crescimento de condicionais complexas.
- `thermo-nuclear-review`: executa uma auditoria profunda de seguranca e corretude em mudancas de branch, focando bugs, quebras, regressao de devex e vazamento de feature gates.

## Estrutura

```text
.codex/
  AGENTS.md
  agents/
  skills/
```

## Fluxo Operacional Recomendado

Use as skills quando o trabalho tem risco de decisao, dominio ou implementacao:

```text
grill-code -> code-planner -> agent-hive
```

- `grill-code`: valida entendimento, termos, limites de dominio e decisoes arquiteturais.
- `code-planner`: transforma o entendimento em um plano de implementacao fechado.
- `agent-hive`: executa o plano com subagents, checkpoints e verificacao independente.

Nem todo caso precisa das tres. Para mudancas simples, normalmente basta execucao direta com revisao. Para mudancas complexas, use o fluxo completo.

## code-planner

Use quando voce quer planejar antes de editar codigo.

Casos ideais:

- feature nao trivial;
- bug com causa incerta;
- mudanca que afeta APIs, contratos, schemas, permissoes ou persistencia;
- refactor com risco de regressao;
- migracao entre padroes ou bibliotecas;
- quando voce quer um plano implementavel por outro agent sem replanejamento.

Workflow:

1. Explorar o codigo sem modificar arquivos.
2. Identificar comportamento atual, padroes locais e riscos.
3. Fazer perguntas apenas sobre ambiguidades materiais.
4. Definir escopo, fora de escopo e sucesso esperado.
5. Produzir plano final com resumo, mudancas principais, plano de testes e premissas.

Quando nao usar:

- correcao obvia de uma linha;
- alteracao puramente textual;
- tarefa onde o usuario ja forneceu um plano fechado e pediu execucao direta.

## grill-code

Use quando o problema precisa ser questionado antes de virar codigo.

Casos ideais:

- dominio mal definido;
- nomes ambiguos como `account`, `order`, `cancellation` ou `session`;
- regra de negocio com excecoes;
- mudanca que pode gerar ADR;
- plano que parece correto, mas depende de invariantes nao documentadas;
- antes de implementar algo que altera responsabilidades entre modulos.

Workflow:

1. Explorar o codigo e documentacao existente.
2. Fazer exatamente uma pergunta por vez.
3. Recomendar uma resposta, mas esperar confirmacao.
4. Quando um termo, limite ou invariant for resolvido, registrar em `docs/CONTEXT-{context-id}.md`.
5. Quando houver decisao arquitetural relevante, criar ADR em `docs/adr/`.
6. Ao fim, perguntar se pode iniciar implementacao.

Quando nao usar:

- quando o dominio ja esta claro;
- quando o usuario quer apenas uma revisao;
- quando a mudanca e puramente mecanica.

## agent-hive

Use quando o trabalho precisa ser orquestrado com subagents, progresso persistente e verificacao independente.

Casos ideais:

- implementacao longa ou multi-etapas;
- migracao grande;
- refactor em varios modulos;
- feature que cruza camadas;
- correcao com alto risco de regressao;
- trabalho que pode ser dividido entre agents;
- quando voce quer execucao com checkpoint, revisao e validacao por fase.

Workflow:

1. Criar ou reutilizar um goal.
2. Criar `.agent-hive/PLAN-PROGRESS-{context-id}.md`.
3. Descobrir agents disponiveis.
4. Registrar pedido original, escopo, riscos, plano de execucao, validacoes e fila de atividades.
5. Delegar exploracao, se necessario.
6. Delegar execucao para `code-worker`.
7. Coletar resultado.
8. Delegar verificacao para reviewer separado.
9. Se aprovado, rodar validacao.
10. Para trabalho multi-etapas, tentar checkpoint commit.
11. Repetir ate todas as fases serem aceitas.
12. Registrar riscos residuais e finalizar.

Uso dos agents:

- `code-worker`: agent executor. Implementa codigo, corrige bugs, faz refactors e roda validacoes proporcionais.
- `code-reviewer`: verificacao padrao para mudancas pequenas ou medias, com foco em guidelines, bugs obvios e manutencao comum.
- `code-reviewer-max`: verificacao avancada para arquitetura, complexidade, branching, abstracoes, contratos e manutenibilidade.
- `code-reviewer-security`: verificacao focada em seguranca, autorizacao, privacidade, integridade de dados, feature gates e regressoes criticas.

## Escolha Rapida

- Quero pensar antes de codar: `code-planner`
- Quero ser questionado sobre o dominio ou plano: `grill-code`
- Quero executar um plano complexo com agents: `agent-hive`

## Fluxos Recomendados

Para feature com dominio incerto:

```text
grill-code
-> agent-hive
   -> code-worker
   -> code-reviewer-max
```

Para mudanca em autenticacao, autorizacao, billing ou feature flags:

```text
code-planner
-> agent-hive
   -> code-worker
   -> code-reviewer-security
   -> code-reviewer-max se tambem houver risco estrutural
```

Para refactor grande:

```text
code-planner
-> agent-hive
   -> multiplos code-worker por modulo
   -> code-reviewer-max por batch
```

Para plano ja escrito, mas suspeito:

```text
grill-code
-> agent-hive se a execucao for grande
```

## Uso

Copie ou mantenha a pasta `.codex` na raiz de um workspace que deve carregar esses agents e skills. Ajuste as instrucoes conforme a necessidade de cada projeto.
