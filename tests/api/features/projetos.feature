# language: pt
Funcionalidade: Projetos
  Como professor(a) do CodeCriando
  Quero criar e gerenciar projetos
  Para disponibilizar conteúdo para as estudantes

  Cenário: Criar projeto com dados válidos
    Dado que estou autenticada como professor(a)
    Quando eu envio POST para "/projetos" com dados válidos
    Então a resposta deve ter status 201
    E o projeto deve ter status "rascunho"

  Cenário: Criar projeto como estudante
    Dado que estou autenticada como estudante
    Quando eu envio POST para "/projetos" com dados válidos
    Então a resposta deve ter status 403
    E a resposta deve conter erro "Apenas professor(a) pode criar projetos"

  Cenário: Criar projeto sem campos obrigatórios
    Dado que estou autenticada como professor(a)
    Quando eu envio POST para "/projetos" sem campos obrigatórios
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Todos os campos são obrigatórios"

  Cenário: Publicar projeto sem etapas
    Dado que estou autenticada como professor(a)
    E existe um projeto em rascunho sem etapas
    Quando eu publico esse projeto
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Não é possível publicar projeto sem etapas"

  Cenário: Publicar projeto com etapas
    Dado que estou autenticada como professor(a)
    E existe um projeto em rascunho com pelo menos uma etapa
    Quando eu publico esse projeto
    Então a resposta deve ter status 200
    E o projeto deve ter status "publicado"

  Cenário: Publicar projeto já publicado
    Dado que estou autenticada como professor(a)
    E existe um projeto em rascunho com pelo menos uma etapa
    E esse projeto já foi publicado
    Quando eu publico esse projeto
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Projeto já está publicado"