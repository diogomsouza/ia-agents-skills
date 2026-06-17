# IA Agents Skills

Colecao de agents e skills para uso com Codex. O projeto organiza instrucoes reutilizaveis em `.codex/agents` e `.codex/skills`, junto com diretrizes globais em `.codex/AGENTS.md`.

## Agents

- `code-reviewer`: revisa codigo alterado contra as diretrizes do projeto, padroes de estilo, bugs relevantes e problemas de qualidade antes de commits ou pull requests.
- `code-simplifier`: simplifica codigo recem-escrito ou modificado, preservando comportamento e priorizando clareza, consistencia e manutencao.
- `comment-analyzer`: analisa comentarios, docstrings e documentacao tecnica para verificar precisao, completude e risco de ficarem desatualizados.
- `csharp-expert`: apoia desenvolvimento .NET/C# com foco em convencoes da plataforma, design limpo, seguranca, testes, performance e manutencao.
- `optimizing-dotnet-performance`: analisa codigo .NET em busca de gargalos, recomenda otimizacoes concretas e orienta validacao com benchmarks.
- `pr-test-analyzer`: avalia a qualidade da cobertura de testes em pull requests, focando caminhos criticos, casos de borda e testes que previnem regressao real.
- `silent-failure-hunter`: audita tratamento de erros, fallbacks e blocos `catch` para encontrar falhas silenciosas, logs insuficientes e mensagens pouco acionaveis.
- `type-design-analyzer`: revisa o desenho de tipos, invariantes, encapsulamento e validacao para melhorar robustez e clareza do modelo de dominio.
- `win-forms-expert`: apoia criacao e manutencao de apps WinForms compativeis com o Designer, incluindo layout, binding, DPI, dark mode e regras para arquivos `.designer`.

## Skills

- `agent-hive`: coordena trabalhos maiores com planejamento persistente, delegacao para subagents, verificadores independentes e acompanhamento em arquivo de progresso.
- `analyzing-dotnet-performance`: escaneia codigo .NET em busca de antipadroes de performance em async, memoria, strings, colecoes, LINQ, regex, serializacao e I/O.
- `architecture-blueprint-generator`: gera blueprint arquitetural a partir da analise do codebase, documentando stack, padroes, componentes, dependencias e diagramas.
- `angular-developer`: orienta e gera codigo Angular seguindo boas praticas modernas para componentes, servicos, reatividade, formularios, roteamento, acessibilidade, testes e CLI.
- `angular-new-app`: cria novas aplicacoes Angular com Angular CLI, incluindo checagem de CLI, flags apropriadas e configuracao de assistente de IA.
- `gpt-image-2`: gera ou edita imagens bitmap com a API de Images da OpenAI usando o modelo `gpt-image-2`, salvando assets prontos para projetos.
- `grill-code`: conduz uma entrevista tecnica sobre um plano usando contexto, ADRs e documentos versionados, sem implementar codigo ate haver aprovacao explicita.
- `grill-me`: entrevista o usuario sobre um plano ou desenho, uma pergunta por vez, ate resolver ambiguidades e dependencias de decisao.
- `optimizing-ef-core-queries`: orienta otimizacao de consultas Entity Framework Core, cobrindo N+1, tracking, queries compiladas e armadilhas comuns de carga no banco.

## Estrutura

```text
.codex/
  AGENTS.md
  agents/
  skills/
```

## Uso

Copie ou mantenha a pasta `.codex` na raiz de um workspace que deve carregar esses agents e skills. Ajuste as instrucoes conforme a necessidade de cada projeto.
