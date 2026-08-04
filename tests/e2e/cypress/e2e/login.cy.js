describe('Autenticação', () => {

  beforeEach(() => {
    cy.visit('/');
  });

  it('exibe a tela de login ao acessar a aplicação', () => {
    cy.get('#page-login').should('be.visible');
    cy.get('.login-brand').should('contain', 'CodeCriando');
    cy.get('#login-email').should('be.visible');
    cy.get('#login-senha').should('be.visible');
    cy.get('#app').should('not.be.visible');
  });

  it('faz login como professora e exibe o painel de projetos', () => {
    cy.get('#login-email').type(Cypress.env('professorEmail'));
    cy.get('#login-senha').type(Cypress.env('professorSenha'));
    cy.get('#btn-login').click();

    cy.get('#app').should('be.visible');
    cy.get('#page-login').should('not.be.visible');
    cy.get('#nav-username').should('contain', 'Manu');
    cy.get('#view-prof-list').should('be.visible');
    cy.get('.view-title').should('contain', 'Meus projetos');
    cy.get('#btn-new-project').should('be.visible');
  });

  it('faz login como estudante e exibe a lista de projetos disponíveis', () => {
    cy.get('#login-email').type(Cypress.env('estudanteEmail'));
    cy.get('#login-senha').type(Cypress.env('estudanteSenha'));
    cy.get('#btn-login').click();

    cy.get('#app').should('be.visible');
    cy.get('#nav-username').should('contain', 'Lua');
    cy.get('#view-student-list').should('be.visible');
    cy.get('.view-title').should('contain', 'Projetos disponíveis');
  });

  it('exibe mensagem de erro ao usar senha incorreta', () => {
    cy.get('#login-email').type(Cypress.env('professorEmail'));
    cy.get('#login-senha').type('senhaerrada');
    cy.get('#btn-login').click();

    cy.get('#login-error')
      .should('be.visible')
      .and('contain', 'Email ou senha incorretos');
    cy.get('#app').should('not.be.visible');
  });

  it('exibe mensagem de erro ao usar email não cadastrado', () => {
    cy.get('#login-email').type('naoexiste@email.com');
    cy.get('#login-senha').type('123456');
    cy.get('#btn-login').click();

    cy.get('#login-error')
      .should('be.visible')
      .and('contain', 'Email ou senha incorretos');
  });

  it('retorna à tela de login ao sair da aplicação', () => {
    cy.loginComoProfessora();
    cy.get('#btn-logout').click();

    cy.get('#page-login').should('be.visible');
    cy.get('#app').should('not.be.visible');
    cy.get('#login-email').should('have.value', '');
  });

});