// Comandos customizados reutilizados nos testes E2E

Cypress.Commands.add('login', (email, senha) => {
  cy.visit('/');

  cy.get('#page-login').should('be.visible');

  cy.get('#login-email')
    .should('be.visible')
    .and('not.be.disabled')
    .clear()
    .type(email);

  cy.get('#login-senha')
    .should('be.visible')
    .and('not.be.disabled')
    .clear()
    .type(senha, { force: true });

  cy.get('#btn-login').should('not.be.disabled').click();

  cy.get('#app').should('be.visible');
  cy.get('#nav-username').should('not.be.empty');
});

Cypress.Commands.add('loginComoProfessora', () => {
  cy.login(Cypress.env('professorEmail'), Cypress.env('professorSenha'));
});

Cypress.Commands.add('loginComoEstudante', () => {
  cy.login(Cypress.env('estudanteEmail'), Cypress.env('estudanteSenha'));
});