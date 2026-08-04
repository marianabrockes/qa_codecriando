# language: pt
Funcionalidade: Submissões
  Como estudante do CodeCriando
  Quero enviar e receber avaliação das minhas etapas
  Para progredir nos projetos

  Cenário: Submeter etapa fora de ordem
    Dado que estou autenticada como estudante
    E existe uma matrícula em projeto com duas etapas
    Quando eu tento submeter a segunda etapa sem aprovar a primeira
    Então a resposta deve ter status 400
    E a resposta deve conter erro "A etapa anterior precisa ser aprovada antes de continuar"

  Cenário: Estudante tentando avaliar submissão
    Dado que estou autenticada como estudante
    E existe uma submissão pendente
    Quando eu tento avaliar essa submissão como estudante
    Então a resposta deve ter status 403
    E a resposta deve conter erro "Sem permissão para avaliar esta submissão"

  Cenário: Avaliar submissão com status inválido
    Dado que estou autenticada como professor(a)
    E existe uma submissão pendente
    Quando eu avalio essa submissão com status inválido
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Status deve ser aprovado ou reprovado"

  Cenário: Aprovar submissão com feedback
    Dado que estou autenticada como professor(a)
    E existe uma submissão pendente
    Quando eu aprovo essa submissão com feedback
    Então a resposta deve ter status 200
    E a submissão deve ter status "aprovado"

  Cenário: Reprovar submissão com feedback
    Dado que estou autenticada como professor(a)
    E existe uma submissão pendente
    Quando eu reprovo essa submissão com feedback
    Então a resposta deve ter status 200
    E a submissão deve ter status "reprovado"