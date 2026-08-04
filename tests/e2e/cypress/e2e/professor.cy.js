describe('Fluxo da professora', () => {

  beforeEach(() => {
    cy.loginComoProfessora();
  });

  it('exibe a lista de projetos publicados', () => {
    cy.get('#view-prof-list').should('be.visible');
    cy.get('#prof-projects-grid .project-card').should('have.length.greaterThan', 0);
    cy.get('.project-card').first().within(() => {
      cy.get('.card-title').should('not.be.empty');
      cy.get('.badge-publicado').should('exist');
    });
  });

  it('abre o formulário de criação de projeto', () => {
    cy.get('#btn-new-project').click();

    cy.get('#view-prof-create').should('be.visible');
    cy.get('#proj-titulo').should('be.visible');
    cy.get('#proj-descricao').should('be.visible');
    cy.get('#proj-nivel').should('be.visible');
  });

  it('volta para a lista ao cancelar a criação de projeto', () => {
    cy.get('#btn-new-project').click();
    cy.get('#back-from-create').click();

    cy.get('#view-prof-list').should('be.visible');
    cy.get('#view-prof-create').should('not.be.visible');
  });

  it('cria um projeto e é levada para a tela de detalhe', () => {
    const titulo = `Projeto E2E ${Date.now()}`;

    cy.get('#btn-new-project').click();
    cy.get('#proj-titulo').type(titulo);
    cy.get('#proj-descricao').type('Projeto criado durante teste automatizado E2E');
    cy.get('#proj-nivel').select('iniciante');
    cy.get('#form-create-project button[type="submit"]').click();

    cy.get('#view-prof-detail').should('be.visible');
    cy.get('#detail-title').should('contain', titulo);
    cy.get('#detail-meta .badge-rascunho').should('exist');
    cy.get('#stages-empty').should('be.visible');
  });

  it('adiciona uma etapa a um projeto em rascunho', () => {
    const titulo = `Projeto com etapa ${Date.now()}`;

    cy.get('#btn-new-project').click();
    cy.get('#proj-titulo').type(titulo);
    cy.get('#proj-descricao').type('Projeto para teste de criação de etapa');
    cy.get('#proj-nivel').select('iniciante');
    cy.get('#form-create-project button[type="submit"]').click();

    cy.get('#view-prof-detail').should('be.visible');
    cy.get('#stage-titulo').type('Etapa criada no teste E2E');
    cy.get('#stage-instrucao').type('Instrução da etapa de teste');
    cy.get('#form-add-stage button[type="submit"]').click();

    cy.get('#stages-list .stage-item').should('have.length', 1);
    cy.get('.stage-num').should('contain', '01');
    cy.get('.stage-title').should('contain', 'Etapa criada no teste E2E');
  });

  it('publica um projeto que tem pelo menos uma etapa', () => {
    const titulo = `Projeto publicável ${Date.now()}`;

    cy.get('#btn-new-project').click();
    cy.get('#proj-titulo').type(titulo);
    cy.get('#proj-descricao').type('Projeto para teste de publicação');
    cy.get('#proj-nivel').select('intermediario');
    cy.get('#form-create-project button[type="submit"]').click();

    cy.get('#stage-titulo').type('Etapa obrigatória');
    cy.get('#stage-instrucao').type('Instrução da etapa obrigatória');
    cy.get('#form-add-stage button[type="submit"]').click();
    cy.get('#stages-list .stage-item').should('have.length', 1);

    cy.get('#btn-publish').click();

    cy.get('#detail-meta .badge-publicado').should('exist');
    cy.get('#btn-publish').should('be.disabled').and('contain', 'Publicado');
    cy.get('#add-stage-block').should('not.be.visible');
  });

  it('exibe erro ao tentar publicar projeto sem etapas', () => {
    const titulo = `Projeto sem etapas ${Date.now()}`;

    cy.get('#btn-new-project').click();
    cy.get('#proj-titulo').type(titulo);
    cy.get('#proj-descricao').type('Projeto que não pode ser publicado');
    cy.get('#proj-nivel').select('iniciante');
    cy.get('#form-create-project button[type="submit"]').click();

    cy.on('window:alert', (msg) => {
      expect(msg).to.contain('Não é possível publicar projeto sem etapas');
    });

    cy.get('#btn-publish').click();
    cy.get('#detail-meta .badge-rascunho').should('exist');
  });

  it('abre o detalhe de um projeto a partir da lista', () => {
    cy.get('.project-card').first().find('button').click();

    cy.get('#view-prof-detail').should('be.visible');
    cy.get('#detail-title').should('not.be.empty');
    cy.get('.section-title').should('contain', 'Etapas');
  });

  it('volta para a lista a partir do detalhe do projeto', () => {
    cy.get('.project-card').first().find('button').click();
    cy.get('#back-from-detail').click();

    cy.get('#view-prof-list').should('be.visible');
    cy.get('#view-prof-detail').should('not.be.visible');
  });

});