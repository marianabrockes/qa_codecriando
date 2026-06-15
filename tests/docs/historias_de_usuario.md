# Histórias de Usuário — CodeCriando

## Personas

**Manu** — professora(a) que cria e gerencia projetos guiados de programação para crianças.  
**Lua** — estudante que segue os projetos, envia etapas e recebe feedback.

---

## EPIC-1 — Autenticação

### US-01 — Cadastro de pessoa usuária

Como pessoa usuária,  
quero me cadastrar na plataforma informando nome, email, senha e perfil,  
para ter acesso às funcionalidades do CodeCriando.

**Critérios de aceitação**

- DADO que acesso a página de cadastro, QUANDO preencho todos os campos corretamente e envio, ENTÃO minha conta é criada e recebo confirmação.
- DADO que tento me cadastrar com um email já existente, QUANDO envio o formulário, ENTÃO recebo uma mensagem de erro informando que o email já está cadastrado.
- DADO que tento me cadastrar sem preencher todos os campos obrigatórios, QUANDO envio o formulário, ENTÃO recebo uma mensagem de erro informando os campos faltantes.
- DADO que tento me cadastrar com um perfil inválido, QUANDO envio o formulário, ENTÃO recebo uma mensagem de erro informando os valores aceitos.

---

### US-02 — Login

Como pessoa usuária cadastrada,  
quero fazer login com meu email e senha,  
para acessar a plataforma com minha conta.

**Critérios de aceitação**

- DADO que tenho uma conta cadastrada, QUANDO faço login com email e senha corretos, ENTÃO recebo um token JWT e sou redirecionada para a plataforma.
- DADO que tento fazer login com senha incorreta, QUANDO envio o formulário, ENTÃO recebo uma mensagem de erro informando credenciais inválidas.
- DADO que tento fazer login sem preencher email ou senha, QUANDO envio o formulário, ENTÃO recebo uma mensagem de erro informando os campos obrigatórios.

---

## EPIC-2 — Projetos

### US-03 — Criar projeto

Como Manu (professora),  
quero criar um projeto guiado informando título, descrição e nível,  
para disponibilizar conteúdo para as estudantes.

**Critérios de aceitação**

- DADO que estou autenticada como professora, QUANDO crio um projeto com todos os campos preenchidos, ENTÃO o projeto é criado com status rascunho.
- DADO que estou autenticada como estudante, QUANDO tento criar um projeto, ENTÃO recebo um erro informando que apenas professor(a) pode criar projetos.
- DADO que estou autenticada como professora, QUANDO crio um projeto sem preencher todos os campos obrigatórios, ENTÃO recebo uma mensagem de erro.
- DADO que tento criar um projeto sem estar autenticada, QUANDO envio a requisição, ENTÃO recebo erro 401.

---

### US-04 — Publicar projeto

Como Manu (professora),  
quero publicar um projeto depois de adicionar as etapas,  
para que as estudantes possam se matricular.

**Critérios de aceitação**

- DADO que tenho um projeto com pelo menos uma etapa, QUANDO publico o projeto, ENTÃO o status muda para publicado.
- DADO que tenho um projeto sem etapas, QUANDO tento publicar, ENTÃO recebo um erro informando que o projeto precisa ter pelo menos uma etapa.
- DADO que o projeto já está publicado, QUANDO tento publicar novamente, ENTÃO recebo um erro informando que o projeto já está publicado.
- DADO que sou professora de outro projeto, QUANDO tento publicar um projeto que não é meu, ENTÃO recebo erro 403.

---

### US-05 — Editar projeto

Como Manu (professora),  
quero editar as informações de um projeto em rascunho,  
para corrigir ou atualizar o conteúdo antes de publicar.

**Critérios de aceitação**

- DADO que tenho um projeto em rascunho, QUANDO edito os dados e salvo, ENTÃO as informações são atualizadas.
- DADO que o projeto está publicado, QUANDO tento editá-lo, ENTÃO recebo um erro informando que projetos publicados não podem ser editados.
- DADO que sou professora de outro projeto, QUANDO tento editar um projeto que não é meu, ENTÃO recebo erro 403.

---

### US-06 — Deletar projeto

Como Manu (professora),  
quero deletar um projeto,  
para remover conteúdo desatualizado da plataforma.

**Critérios de aceitação**

- DADO que tenho um projeto sem matrículas ativas, QUANDO deleto o projeto, ENTÃO ele é removido da plataforma.
- DADO que o projeto tem matrículas ativas, QUANDO tento deletar, ENTÃO recebo um erro informando que não é possível deletar projeto com matrículas ativas.
- DADO que sou professora de outro projeto, QUANDO tento deletar um projeto que não é meu, ENTÃO recebo erro 403.

---

## EPIC-3 — Etapas

### US-07 — Criar etapa

Como Manu (professora),  
quero adicionar etapas a um projeto em rascunho,  
para estruturar o conteúdo de forma sequencial.

**Critérios de aceitação**

- DADO que tenho um projeto em rascunho, QUANDO adiciono uma etapa com todos os campos preenchidos, ENTÃO a etapa é criada e vinculada ao projeto.
- DADO que o projeto está publicado, QUANDO tento adicionar uma etapa, ENTÃO recebo um erro informando que projetos publicados não aceitam novas etapas.
- DADO que sou professora de outro projeto, QUANDO tento adicionar uma etapa em projeto que não é meu, ENTÃO recebo erro 403.

---

### US-08 — Editar e deletar etapa

Como Manu (professora),  
quero editar ou deletar etapas de um projeto em rascunho,  
para ajustar o conteúdo antes de publicar.

**Critérios de aceitação**

- DADO que tenho uma etapa em projeto rascunho, QUANDO edito os dados, ENTÃO as informações são atualizadas.
- DADO que o projeto está publicado, QUANDO tento editar ou deletar uma etapa, ENTÃO recebo um erro informando que não é possível modificar etapas de projeto publicado.

---

## EPIC-4 — Matrículas

### US-09 — Matricular em projeto

Como Lua (estudante),  
quero me matricular em um projeto publicado,  
para acessar as etapas e começar a aprender.

**Critérios de aceitação**

- DADO que estou autenticada como estudante, QUANDO me matriculo em um projeto publicado, ENTÃO a matrícula é criada com sucesso.
- DADO que já estou matriculada em um projeto, QUANDO tento me matricular novamente, ENTÃO recebo um erro informando que já estou matriculada.
- DADO que o projeto está em rascunho, QUANDO tento me matricular, ENTÃO recebo um erro informando que o projeto não está disponível.
- DADO que estou autenticada como professora, QUANDO tento me matricular em um projeto, ENTÃO recebo erro 403.

---

### US-10 — Cancelar matrícula

Como Lua (estudante),  
quero cancelar minha matrícula em um projeto,  
para remover projetos que não quero mais fazer.

**Critérios de aceitação**

- DADO que estou matriculada em um projeto, QUANDO cancelo a matrícula, ENTÃO ela é removida.
- DADO que tento cancelar a matrícula de outra estudante, QUANDO envio a requisição, ENTÃO recebo erro 403.

---

## EPIC-5 — Submissões

### US-11 — Submeter etapa

Como Lua (estudante),  
quero enviar minha solução para uma etapa,  
para receber feedback da professora e avançar no projeto.

**Critérios de aceitação**

- DADO que estou matriculada e a etapa anterior foi aprovada, QUANDO submeto a etapa com conteúdo, ENTÃO a submissão é criada com status pendente.
- DADO que a etapa anterior ainda não foi aprovada, QUANDO tento submeter a próxima etapa, ENTÃO recebo um erro informando que preciso ter a etapa anterior aprovada.
- DADO que não estou matriculada no projeto, QUANDO tento submeter uma etapa, ENTÃO recebo erro 403.
- DADO que a etapa não pertence ao projeto da minha matrícula, QUANDO tento submeter, ENTÃO recebo erro 400.

---

### US-12 — Avaliar submissão

Como Manu (professora),  
quero aprovar ou reprovar a submissão de uma estudante com feedback,  
para orientar o aprendizado e permitir o avanço nas etapas.

**Critérios de aceitação**

- DADO que sou professora do projeto, QUANDO avalio uma submissão como aprovada, ENTÃO o status muda para aprovado e a data de avaliação é registrada.
- DADO que sou professora do projeto, QUANDO avalio uma submissão como reprovada com feedback, ENTÃO o status muda para reprovado e o feedback é salvo.
- DADO que sou professora de outro projeto, QUANDO tento avaliar uma submissão, ENTÃO recebo erro 403.
- DADO que envio um status inválido, QUANDO tento avaliar, ENTÃO recebo erro 400.
