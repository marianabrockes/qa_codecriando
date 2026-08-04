describe('Fluxo da estudante', () => {

  beforeEach(() => {
    cy.loginComoEstudante();
  });

  it('exibe a lista de projetos publicados disponíveis', () => {
    cy.get('#view-student-list').should('be.visible');
    cy.get('#student-projects-grid .project-card').should('have.length.greaterThan', 0);
    cy.get('.project-card').first().within(() => {
      cy.get('.card-title').should('not.be.empty');
      cy.get('.badge-nivel').should('exist');
    });
  });

  it('abre o detalhe de um projeto a partir da lista', () => {
    cy.get('.project-card').first().find('button').click();

    cy.get('#view-student-detail').should('be.visible');
    cy.get('#student-detail-title').should('not.be.empty');
  });

  it('volta para a lista a partir do detalhe do projeto', () => {
    cy.get('.project-card').first().find('button').click();
    cy.get('#back-from-student-detail').click();

    cy.get('#view-student-list').should('be.visible');
    cy.get('#view-student-detail').should('not.be.visible');
  });

  it('exibe as etapas e o formulário de envio em projeto matriculado', () => {
    cy.get('.project-card').contains('.badge-publicado', 'Matriculada')
      .parents('.project-card')
      .find('button')
      .first()
      .click();

    cy.get('#view-student-detail').should('be.visible');
    cy.get('.stage-student-card').should('have.length.greaterThan', 0);
    cy.get('.stage-student-card').first().within(() => {
      cy.get('.stage-num').should('be.visible');
      cy.get('.stage-student-name').should('not.be.empty');
      cy.get('textarea').should('be.visible');
      cy.get('button[type="submit"]').should('contain', 'Enviar solução');
    });
  });

  it('envia uma solução para a primeira etapa de um projeto matriculado', () => {
    cy.get('.project-card').contains('.badge-publicado', 'Matriculada')
      .parents('.project-card')
      .find('button')
      .first()
      .click();

    cy.get('.stage-student-card').first().within(() => {
      cy.get('textarea').type('Solução enviada durante teste automatizado E2E');
      cy.get('button[type="submit"]').click();
    });

    cy.get('.stage-student-card').first().within(() => {
      cy.get('.submission-status').should('be.visible');
      cy.get('.badge-pendente').should('exist');
    });
  });

  it('impede o envio de solução com campo vazio', () => {
    cy.get('.project-card').contains('.badge-publicado', 'Matriculada')
      .parents('.project-card')
      .find('button')
      .first()
      .click();

    cy.get('.stage-student-card').first().within(() => {
      cy.get('button[type="submit"]').click();
      cy.get('textarea:invalid').should('exist');
    });
  });

});