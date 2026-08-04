# language: pt
Funcionalidade: Autenticação
  Como pessoa usuária do CodeCriando
  Quero me cadastrar e fazer login na plataforma
  Para acessar as funcionalidades disponíveis

  Cenário: Login com credenciais válidas
    Dado que a API está rodando
    Quando eu envio POST para "/login" com credenciais válidas da professora
    Então a resposta deve ter status 200
    E a resposta deve conter o campo "token"

  Cenário: Login com senha incorreta
    Dado que a API está rodando
    Quando eu envio POST para "/login" com senha incorreta
    Então a resposta deve ter status 401
    E a resposta deve conter erro "Email ou senha incorretos"

  Cenário: Login com email não cadastrado
    Dado que a API está rodando
    Quando eu envio POST para "/login" com email não cadastrado
    Então a resposta deve ter status 401
    E a resposta deve conter erro "Email ou senha incorretos"

  Cenário: Acesso a rota protegida sem token
    Dado que a API está rodando
    Quando eu envio GET para "/projetos" sem token
    Então a resposta deve ter status 401
    E a resposta deve conter erro "Token de acesso ausente"

  Cenário: Cadastro com email já existente
    Dado que a API está rodando
    Quando eu envio POST para "/register" com email já cadastrado
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Email já cadastrado"

  Cenário: Cadastro sem campos obrigatórios
    Dado que a API está rodando
    Quando eu envio POST para "/register" sem campos obrigatórios
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Todos os campos são obrigatórios"

  Cenário: Cadastro com perfil inválido
    Dado que a API está rodando
    Quando eu envio POST para "/register" com perfil inválido
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Perfil deve ser professor ou estudante"

  Cenário: Cadastro sem corpo na requisição
    Dado que a API está rodando
    Quando eu envio POST para "/register" sem corpo
    Então a resposta deve ter status 400
    E a resposta deve conter erro "Nenhum dado enviado"