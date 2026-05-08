# Primeiro teste real: Codex, VS Code e o momento em que DoneSpec deixou de ser teoria

Este documento regista a primeira experi?ncia real em que o DoneSpec foi usado como ferramenta de valida??o operacional por um agente de IA ? neste caso, o Codex a trabalhar no VS Code ? para detectar, orientar e confirmar a resolu??o de uma falha concreta.

N?o foi uma demonstra??o controlada.

N?o foi um exemplo artificial.

Foi uma falha real, num reposit?rio real, num workflow real, com consequ?ncias reais para a maturidade do projecto.

## Contexto

O DoneSpec estava a evoluir rapidamente para se afirmar como uma camada determin?stica de conclus?o para agentes de programa??o com IA.

A premissa era simples:

```text
AI agents say tasks are done.
DoneSpec verifies they actually are.
```

At? este momento, essa frase era uma promessa arquitect?nica.

Depois deste teste, passou a ser uma evid?ncia pr?tica.

O reposit?rio j? continha valida??es extensas, documenta??o de integra??o, guias de release, templates, checks de seguran?a, workflows de CI e um contrato `done.json` cada vez mais rigoroso.

A ferramenta j? n?o estava apenas a validar ficheiros.

Estava a validar confian?a.

## A falha

Durante a execu??o do workflow cross-platform no GitHub Actions, o job de Windows falhou.

O Linux passou.

O macOS passou.

Mas o Windows falhou.

A causa n?o estava na l?gica principal do DoneSpec.

Estava no ponto exacto onde muitos projectos parecem s?lidos at? encontrarem a realidade: o terminal.

O erro veio de uma superf?cie aparentemente pequena, mas cr?tica:

```text
UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'
```

O DoneSpec imprimia s?mbolos Unicode como `?` e `?` atrav?s do Rich.

Em ambientes Windows com encoding legado `cp1252`, esses s?mbolos podiam falhar antes de a valida??o terminar.

A ferramenta que tinha sido criada para validar conclus?o estava agora a ser testada pelo pr?prio mundo onde teria de operar: ambientes imperfeitos, runners diferentes, shells diferentes, codifica??es diferentes, limita??es antigas ainda presentes em infraestruturas modernas.

Foi o tipo de falha que separa uma ideia elegante de uma ferramenta confi?vel.

## O momento decisivo

O Codex n?o tratou o problema como um erro isolado.

Tratou-o como uma falha de contrato.

Primeiro inspeccionou o `done.json`.

Depois analisou o c?digo de output.

Depois encontrou as superf?cies afectadas:

- `validate`, atrav?s de `output.py`
- `explain`, atrav?s de `explain.py`
- comandos de CLI em `cli.py`, incluindo `init`, `templates` e `doctor`

A leitura foi cir?rgica: j? existia um helper de fallback para escrita segura, mas o caminho que passava por `console.print` do Rich ainda deixava os s?mbolos Unicode chegarem directamente ao terminal.

O problema n?o era a filosofia.

Era a fronteira entre inten??o e sistema operativo.

## A correc??o

A solu??o foi transformar os s?mbolos de estado numa decis?o consciente.

O DoneSpec passou a escolher entre:

```text
? / ?
```

e:

```text
+ / x
```

conforme o encoding real do console.

Em terminais modernos, mant?m a clareza visual dos s?mbolos Unicode.

Em terminais legados, recua para ASCII previs?vel.

N?o h? ru?do.

N?o h? magia.

N?o h? depend?ncia de IA.

H? apenas comportamento determin?stico adaptado ao ambiente.

## O teste que tornou a correc??o s?ria

A parte mais importante n?o foi apenas corrigir o c?digo.

Foi provar que a correc??o protegia o cen?rio real.

Foi adicionado um teste com um stream falso `cp1252`, concebido para falhar caso recebesse texto fora dessa codifica??o.

Esse teste cobriu precisamente o caminho que tinha explodido no GitHub Actions:

```text
print_human_report -> Rich console.print -> encoding cp1252
```

Este detalhe ? importante.

Porque a correc??o n?o foi baseada em esperan?a.

Foi baseada numa reprodu??o controlada da falha.

O bug deixou de ser uma anomalia.

Passou a ser uma especifica??o.

## O DoneSpec como juiz

Depois da correc??o, o pr?prio DoneSpec foi usado para validar o resultado.

As valida??es passaram:

```text
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
```

O contrato evoluiu para proteger explicitamente este comportamento.

O DoneSpec passou a verificar que o fallback `cp1252` existe, que est? testado, e que a altera??o ficou registada.

O agente corrigiu.

Mas n?o foi o agente que declarou a conclus?o.

Foi o contrato.

Foi o DoneSpec.

## Resultado

A correc??o foi commitada e enviada para `main`.

Commit:

```text
4ec2f9d fix: fallback to ASCII status symbols on legacy Windows output
```

O resultado validado foi:

```text
215 checks passed
Exit code: 0
```

A falha que come?ou como um problema de Unicode no Windows tornou-se a primeira prova pr?tica de que o DoneSpec consegue funcionar como uma camada de confian?a entre um agente de IA e um reposit?rio real.

## O significado deste teste

Este epis?dio mostrou algo maior do que uma correc??o t?cnica.

Mostrou que um agente de IA pode ser r?pido, mas precisa de uma fronteira de verdade.

Mostrou que um agente pode propor, editar, testar e explicar.

Mas a conclus?o deve ser verificada por um sistema que n?o elogia, n?o assume, n?o acredita e n?o se impressiona.

O DoneSpec n?o interpretou inten??o.

N?o avaliou estilo.

N?o confiou no tom seguro do agente.

Apenas executou o contrato.

E, quando o contrato passou, a conclus?o deixou de ser uma afirma??o.

Passou a ser um facto operacional.

## Porque isto importa

O primeiro teste real do DoneSpec com Codex no VS Code n?o foi importante por ter corrido tudo bem.

Foi importante porque falhou.

E porque, ao falhar, revelou exactamente onde a ferramenta precisava de ser mais robusta.

A partir da?, o ciclo ficou completo:

```text
falha real
an?lise por agente
correc??o cir?rgica
teste reproduz?vel
contrato actualizado
valida??o determin?stica
push para main
```

Este ? o cora??o do DoneSpec.

N?o substituir o programador.

N?o substituir os testes.

N?o substituir revis?o humana.

Mas criar uma camada onde a palavra ?feito? deixa de depender de confian?a subjectiva.

## Primeira conclus?o real

Neste primeiro uso real com Codex no VS Code, o DoneSpec demonstrou a sua fun??o mais importante:

```text
o agente pode trabalhar
mas a conclus?o pertence ao contrato
```

A partir deste momento, DoneSpec deixou de ser apenas uma ferramenta em desenvolvimento.

Passou a ser uma pe?a de infra-estrutura testada contra a realidade.

Pequena.

Local.

Determin?stica.

Incomodamente honesta.

E exactamente por isso, necess?ria.

## Frase final

A IA disse que corrigiu.

O GitHub Actions testou o mundo real.

O DoneSpec confirmou.

E, pela primeira vez, ?feito? significou exactamente isso.

## Deterministic anchor

This field note records the first real Codex VS Code usage where DoneSpec turned an agent claim into deterministic validation.

