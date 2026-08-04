# Queries SQL de Validação — CodeCriando

## Identificação

**Projeto:** CodeCriando  
**Banco de dados:** PostgreSQL 15  
**Data:** agosto/2026  
**Responsável:** Mariana Brockes

---

## Objetivo

Validar diretamente no banco de dados que as operações realizadas pela API gravaram os dados corretamente, complementando os testes funcionais com uma camada de verificação na camada de persistência.

---

## Q-001 — Verificar que senhas não são armazenadas em texto puro

```sql
SELECT id, nome, email,
       CASE
           WHEN senha LIKE 'scrypt:%' THEN 'hash seguro'
           ELSE 'ALERTA: senha em texto puro'
       END AS situacao_senha
FROM usuarios;
```

**Resultado esperado:** Todas as linhas devem exibir `hash seguro` na coluna `situacao_senha`.

---

## Q-002 — Listar pessoas usuárias por perfil

```sql
SELECT perfil, COUNT(*) AS total
FROM usuarios
GROUP BY perfil
ORDER BY perfil;
```

**Resultado esperado:** Duas linhas, uma para `estudante` e uma para `professor`.

---

## Q-003 — Verificar que apenas estudantes possuem matrículas

```sql
SELECT u.nome, u.perfil, COUNT(m.id) AS total_matriculas
FROM usuarios u
LEFT JOIN matriculas m ON m.estudante_id = u.id
GROUP BY u.id, u.nome, u.perfil
ORDER BY u.perfil;
```

**Resultado esperado:** Apenas pessoas com perfil `estudante` devem ter `total_matriculas` maior que zero.

---

## Q-004 — Verificar que matrículas só existem em projetos publicados

```sql
SELECT m.id AS matricula_id, p.titulo, p.status
FROM matriculas m
JOIN projetos p ON p.id = m.projeto_id
WHERE p.status != 'publicado';
```

**Resultado esperado:** Nenhuma linha retornada. Toda matrícula deve estar vinculada a um projeto publicado.

---

## Q-005 — Listar projetos com total de matrículas e submissões

```sql
SELECT
    p.id,
    p.titulo,
    p.status,
    COUNT(DISTINCT m.id) AS total_matriculas,
    COUNT(DISTINCT s.id) AS total_submissoes
FROM projetos p
LEFT JOIN matriculas m ON m.projeto_id = p.id
LEFT JOIN submissoes s ON s.matricula_id = m.id
GROUP BY p.id, p.titulo, p.status
ORDER BY p.id;
```

**Resultado esperado:** Cada projeto exibe o total correto de matrículas e submissões vinculadas.

---

## Q-006 — Verificar que submissões avaliadas têm avaliado_em preenchido

```sql
SELECT id, status, avaliado_em,
       CASE
           WHEN status IN ('aprovado', 'reprovado') AND avaliado_em IS NULL
               THEN 'ALERTA: avaliada sem data'
           WHEN status = 'pendente' AND avaliado_em IS NOT NULL
               THEN 'ALERTA: pendente com data de avaliação'
           ELSE 'ok'
       END AS consistencia
FROM submissoes;
```

**Resultado esperado:** Todas as linhas devem exibir `ok` na coluna `consistencia`.

---

## Q-007 — Rastrear o ciclo completo de uma matrícula

```sql
SELECT
    u.nome AS estudante,
    p.titulo AS projeto,
    e.titulo AS etapa,
    e.ordem,
    s.status AS status_submissao,
    s.feedback,
    s.enviado_em,
    s.avaliado_em
FROM matriculas m
JOIN usuarios u ON u.id = m.estudante_id
JOIN projetos p ON p.id = m.projeto_id
JOIN submissoes s ON s.matricula_id = m.id
JOIN etapas e ON e.id = s.etapa_id
WHERE m.id = 1
ORDER BY e.ordem;
```

**Resultado esperado:** O ciclo completo da matrícula 1 exibindo estudante, projeto, etapas submetidas e seus status.

---

## Q-008 — Verificar integridade referencial entre submissões e matrículas

```sql
SELECT s.id AS submissao_id, s.matricula_id, s.etapa_id
FROM submissoes s
LEFT JOIN matriculas m ON m.id = s.matricula_id
WHERE m.id IS NULL;
```

**Resultado esperado:** Nenhuma linha retornada. Toda submissão deve estar vinculada a uma matrícula válida.

---

## Q-009 — Listar submissões pendentes por projeto

```sql
SELECT
    p.titulo AS projeto,
    u.nome AS estudante,
    e.titulo AS etapa,
    s.enviado_em
FROM submissoes s
JOIN matriculas m ON m.id = s.matricula_id
JOIN projetos p ON p.id = m.projeto_id
JOIN usuarios u ON u.id = m.estudante_id
JOIN etapas e ON e.id = s.etapa_id
WHERE s.status = 'pendente'
ORDER BY s.enviado_em;
```

**Resultado esperado:** Lista de todas as submissões aguardando avaliação, com os dados necessários para a professora identificar e avaliar cada uma.

---

## Q-010 — Verificar que projetos publicados têm pelo menos uma etapa

```sql
SELECT p.id, p.titulo, p.status, COUNT(e.id) AS total_etapas
FROM projetos p
LEFT JOIN etapas e ON e.projeto_id = p.id
WHERE p.status = 'publicado'
GROUP BY p.id, p.titulo, p.status
HAVING COUNT(e.id) = 0;
```

**Resultado esperado:** Nenhuma linha retornada. A regra de negócio impede publicar projetos sem etapas.
