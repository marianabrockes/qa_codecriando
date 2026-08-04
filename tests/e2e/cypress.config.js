const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:8080',
    supportFile: 'cypress/support/e2e.js',
    specPattern: 'cypress/e2e/**/*.cy.js',
    viewportWidth: 1280,
    viewportHeight: 800,
    video: false,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 8000,
    env: {
      apiUrl: 'http://localhost:5001',
      professorEmail: 'manu@email.com',
      professorSenha: '123456',
      estudanteEmail: 'lua@email.com',
      estudanteSenha: '123456',
    },
  },
});