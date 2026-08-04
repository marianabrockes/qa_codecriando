# language: pt
Funcionalidade: Matrículas
  Como estudante do CodeCriando
  Quero me matricular em projetos publicados
  Para acessar as etapas e começar a aprender

  Cenário: Professora tentando se matricular
    Dado que estou autenticada como professor(a)
    Quando eu envio POST para "/matriculas" com projeto_id 1
    Então a resposta deve ter status 403
    E a resposta deve conter erro "Apenas estudante pode se matricular em projetos"

  Cenário: Matricular duas vezes no mesmo projeto
    Dado que estou autenticada como estudante
    Quando eu envio POST para "/matriculas" com projeto_id 1
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Estudante já matriculada neste projeto"

  Cenário: Matricular em projeto publicado
    Dado que estou autenticada como estudante
    E existe um projeto publicado disponível para nova matrícula
    Quando eu me matriculo nesse projeto
    Então a resposta deve ter status 201
    E a resposta deve conter o campo "matricula"