const API = 'http://localhost:5001';

// === ESTADO ===
let state = {
  token: null,
  user: null,
  currentProject: null,
  currentSubmissaoId: null,
  enrollments: [],
};

// === UTILS ===
async function api(method, path, body) {
  const headers = { 'Content-Type': 'application/json' };
  if (state.token) headers['Authorization'] = `Bearer ${state.token}`;
  const res = await fetch(`${API}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

function showView(id) {
  document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
}

function showError(id, msg) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.classList.remove('hidden');
}

function clearError(id) {
  const el = document.getElementById(id);
  if (el) { el.textContent = ''; el.classList.add('hidden'); }
}

function badge(cls, label) {
  return `<span class="badge badge-${cls}">${label}</span>`;
}

function nivelBadge(nivel) {
  const labels = { iniciante: 'Iniciante', intermediario: 'Intermediário', avancado: 'Avançado' };
  return `<span class="badge badge-nivel">${labels[nivel] || nivel}</span>`;
}

function stageNum(ordem) {
  return `<span class="stage-num">${String(ordem).padStart(2, '0')}</span>`;
}

function formatDate(iso) {
  if (!iso) return '';
  return new Date(iso).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' });
}

// === LOGIN ===
document.getElementById('form-login').addEventListener('submit', async (e) => {
  e.preventDefault();
  clearError('login-error');
  const btn = document.getElementById('btn-login');
  btn.disabled = true;
  btn.textContent = 'Entrando...';

  const { ok, data } = await api('POST', '/login', {
    email: document.getElementById('login-email').value,
    senha: document.getElementById('login-senha').value,
  });

  btn.disabled = false;
  btn.textContent = 'Entrar';

  if (!ok) {
    showError('login-error', data.erro || 'Erro ao fazer login.');
    return;
  }

  state.token = data.token;
  state.user = data.usuario;

  document.getElementById('page-login').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  document.getElementById('nav-username').textContent = state.user.nome;

  if (state.user.perfil === 'professor') {
    loadProfList();
  } else {
    loadStudentList();
  }
});

document.getElementById('btn-logout').addEventListener('click', () => {
  state = { token: null, user: null, currentProject: null, currentSubmissaoId: null, enrollments: [] };
  document.getElementById('app').classList.add('hidden');
  document.getElementById('page-login').classList.remove('hidden');
  document.getElementById('form-login').reset();
  clearError('login-error');
});

// === PROFESSOR: LISTA DE PROJETOS ===
async function loadProfList() {
  showView('view-prof-list');
  const grid = document.getElementById('prof-projects-grid');
  const empty = document.getElementById('prof-projects-empty');
  grid.innerHTML = '<p style="color:var(--muted);font-size:14px">Carregando...</p>';
  empty.classList.add('hidden');

  const { ok, data } = await api('GET', '/projetos');
  grid.innerHTML = '';

  if (!ok || data.length === 0) {
    empty.classList.remove('hidden');
    return;
  }

  data.forEach(p => grid.appendChild(buildProfCard(p)));
}

function buildProfCard(p) {
  const card = document.createElement('div');
  card.className = 'project-card';
  card.innerHTML = `
    <div class="card-title">${p.titulo}</div>
    <p class="card-desc">${p.descricao}</p>
    <div class="card-footer">
      <div class="card-meta">
        ${badge('publicado', 'Publicado')}
        ${nivelBadge(p.nivel)}
        <span class="meta-count">${p.total_etapas} etapa${p.total_etapas !== 1 ? 's' : ''}</span>
      </div>
      <div class="card-actions">
        <button class="btn btn-sm btn-outline" data-id="${p.id}">Ver projeto</button>
      </div>
    </div>
  `;
  card.querySelector('[data-id]').addEventListener('click', () => loadProfDetail(p.id));
  return card;
}

// === PROFESSOR: CRIAR PROJETO ===
document.getElementById('btn-new-project').addEventListener('click', () => {
  showView('view-prof-create');
  document.getElementById('form-create-project').reset();
  clearError('create-proj-error');
});

document.getElementById('back-from-create').addEventListener('click', loadProfList);

document.getElementById('form-create-project').addEventListener('submit', async (e) => {
  e.preventDefault();
  clearError('create-proj-error');

  const { ok, data } = await api('POST', '/projetos', {
    titulo: document.getElementById('proj-titulo').value,
    descricao: document.getElementById('proj-descricao').value,
    nivel: document.getElementById('proj-nivel').value,
  });

  if (!ok) { showError('create-proj-error', data.erro || 'Erro ao criar projeto.'); return; }
  loadProfDetail(data.projeto.id);
});

// === PROFESSOR: DETALHE DO PROJETO ===
async function loadProfDetail(projectId) {
  showView('view-prof-detail');

  const { ok, data } = await api('GET', `/projetos/${projectId}`);
  if (!ok) return;

  state.currentProject = data;
  document.getElementById('detail-title').textContent = data.titulo;
  document.getElementById('detail-meta').innerHTML = `
    ${badge(data.status, data.status)}
    ${nivelBadge(data.nivel)}
    <span class="meta-count">${data.total_etapas} etapa${data.total_etapas !== 1 ? 's' : ''}</span>
  `;

  const publishBtn = document.getElementById('btn-publish');
  const addBlock = document.getElementById('add-stage-block');

  if (data.status === 'publicado') {
    publishBtn.disabled = true;
    publishBtn.textContent = 'Publicado';
    addBlock.classList.add('hidden');
  } else {
    publishBtn.disabled = false;
    publishBtn.textContent = 'Publicar projeto';
    addBlock.classList.remove('hidden');
  }

  renderStages(data.etapas || []);
  loadProfSubmissions(projectId);

  const ordemField = document.getElementById('stage-ordem');
  ordemField.value = (data.etapas || []).length + 1;
}

function renderStages(stages) {
  const list = document.getElementById('stages-list');
  const empty = document.getElementById('stages-empty');
  list.innerHTML = '';

  if (stages.length === 0) { empty.classList.remove('hidden'); return; }
  empty.classList.add('hidden');

  [...stages].sort((a, b) => a.ordem - b.ordem).forEach(s => {
    const el = document.createElement('div');
    el.className = 'stage-item';
    el.innerHTML = `
      ${stageNum(s.ordem)}
      <div class="stage-body">
        <div class="stage-title">${s.titulo}</div>
        <div class="stage-instrucao">${s.instrucao}</div>
      </div>
    `;
    list.appendChild(el);
  });
}

async function loadProfSubmissions(projectId) {
  const list = document.getElementById('subs-list');
  const empty = document.getElementById('subs-empty');
  list.innerHTML = '<p style="color:var(--muted);font-size:13px">Carregando...</p>';
  empty.classList.add('hidden');

  const { ok, data } = await api('GET', `/projetos/${projectId}/submissoes`);
  list.innerHTML = '';

  if (!ok || data.length === 0) { empty.classList.remove('hidden'); return; }

  data.forEach(s => {
    const el = document.createElement('div');
    el.className = 'sub-item';
    const feedbackHtml = s.feedback
      ? `<div class="${s.status === 'aprovado' ? 'sub-feedback' : 'sub-feedback-error'}">"${s.feedback}"</div>`
      : '';
    const evalBtn = s.status === 'pendente'
      ? `<button class="btn btn-sm btn-secondary" style="margin-top:8px" data-sub="${s.id}" data-content="${encodeURIComponent(s.conteudo)}">Avaliar</button>`
      : '';
    el.innerHTML = `
      <div class="sub-item-head">
        ${badge(s.status, s.status)}
        <span class="sub-date">${formatDate(s.enviado_em)}</span>
      </div>
      <div class="sub-text">${s.conteudo}</div>
      ${feedbackHtml}
      ${evalBtn}
    `;
    const btn = el.querySelector('[data-sub]');
    if (btn) btn.addEventListener('click', () => openModal(s.id, s.conteudo));
    list.appendChild(el);
  });
}

document.getElementById('back-from-detail').addEventListener('click', loadProfList);

document.getElementById('btn-publish').addEventListener('click', async () => {
  const { ok, data } = await api('PATCH', `/projetos/${state.currentProject.id}/publicar`);
  if (!ok) { alert(data.erro || 'Erro ao publicar.'); return; }
  loadProfDetail(state.currentProject.id);
});

document.getElementById('form-add-stage').addEventListener('submit', async (e) => {
  e.preventDefault();
  clearError('add-stage-error');

  const { ok, data } = await api('POST', `/projetos/${state.currentProject.id}/etapas`, {
    titulo: document.getElementById('stage-titulo').value,
    instrucao: document.getElementById('stage-instrucao').value,
    ordem: parseInt(document.getElementById('stage-ordem').value),
  });

  if (!ok) { showError('add-stage-error', data.erro || 'Erro ao adicionar etapa.'); return; }
  document.getElementById('form-add-stage').reset();
  loadProfDetail(state.currentProject.id);
});

// === MODAL DE AVALIAÇÃO ===
function openModal(submissaoId, content) {
  state.currentSubmissaoId = submissaoId;
  document.getElementById('modal-content').textContent = content;
  document.getElementById('eval-feedback').value = '';
  clearError('eval-error');
  document.getElementById('modal-eval').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('modal-eval').classList.add('hidden');
}

document.getElementById('close-modal').addEventListener('click', closeModal);

document.getElementById('modal-eval').addEventListener('click', (e) => {
  if (e.target === document.getElementById('modal-eval')) closeModal();
});

async function evaluate(status) {
  const feedback = document.getElementById('eval-feedback').value;
  const { ok, data } = await api('PATCH', `/submissoes/${state.currentSubmissaoId}/avaliar`, { status, feedback });
  if (!ok) { showError('eval-error', data.erro || 'Erro ao avaliar.'); return; }
  closeModal();
  loadProfSubmissions(state.currentProject.id);
}

document.getElementById('btn-approve').addEventListener('click', () => evaluate('aprovado'));
document.getElementById('btn-reject').addEventListener('click', () => evaluate('reprovado'));

// === ESTUDANTE: LISTA DE PROJETOS ===
async function loadStudentList() {
  showView('view-student-list');
  const grid = document.getElementById('student-projects-grid');
  const empty = document.getElementById('student-projects-empty');
  grid.innerHTML = '<p style="color:var(--muted);font-size:14px">Carregando...</p>';
  empty.classList.add('hidden');

  const [projRes, matRes] = await Promise.all([
    api('GET', '/projetos'),
    api('GET', '/matriculas'),
  ]);

  grid.innerHTML = '';
  state.enrollments = matRes.ok ? matRes.data : [];

  if (!projRes.ok || projRes.data.length === 0) {
    empty.classList.remove('hidden');
    return;
  }

  const enrolledIds = state.enrollments.map(m => m.projeto_id);
  projRes.data.forEach(p => {
    const enrolled = enrolledIds.includes(p.id);
    grid.appendChild(buildStudentCard(p, enrolled));
  });
}

function buildStudentCard(p, enrolled) {
  const card = document.createElement('div');
  card.className = 'project-card';
  card.innerHTML = `
    <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px">
      <div class="card-title">${p.titulo}</div>
      ${enrolled ? badge('publicado', 'Matriculada') : ''}
    </div>
    <p class="card-desc">${p.descricao}</p>
    <div class="card-footer">
      <div class="card-meta">
        ${nivelBadge(p.nivel)}
        <span class="meta-count">${p.total_etapas} etapa${p.total_etapas !== 1 ? 's' : ''}</span>
      </div>
      <div class="card-actions">
        <button class="btn btn-sm ${enrolled ? 'btn-outline' : 'btn-primary'}" data-id="${p.id}">
          ${enrolled ? 'Ver projeto' : 'Saiba mais'}
        </button>
      </div>
    </div>
  `;
  card.querySelector('[data-id]').addEventListener('click', () => loadStudentDetail(p, enrolled));
  return card;
}

// === ESTUDANTE: DETALHE DO PROJETO ===
async function loadStudentDetail(project, enrolled) {
  showView('view-student-detail');
  document.getElementById('student-detail-title').textContent = project.titulo;
  document.getElementById('student-detail-meta').innerHTML = `
    ${nivelBadge(project.nivel)}
    <span class="meta-count">${project.total_etapas} etapa${project.total_etapas !== 1 ? 's' : ''}</span>
  `;

  const content = document.getElementById('student-detail-content');
  content.innerHTML = '<p style="color:var(--muted);font-size:14px">Carregando...</p>';

  const { ok, data } = await api('GET', `/projetos/${project.id}`);
  if (!ok) return;

  state.currentProject = data;

  if (!enrolled) {
    content.innerHTML = `
      <div class="enroll-cta">
        <p>${data.descricao}</p>
        <button class="btn btn-primary" id="btn-enroll">Matricular-se</button>
      </div>
    `;
    document.getElementById('btn-enroll').addEventListener('click', async () => {
      const { ok: eOk, data: eData } = await api('POST', '/matriculas', { projeto_id: data.id });
      if (!eOk) { alert(eData.erro || 'Erro ao se matricular.'); return; }
      state.enrollments.push(eData.matricula);
      loadStudentDetail(project, true);
    });
    return;
  }

  const enrollment = state.enrollments.find(m => m.projeto_id === project.id);
  renderStudentStages(data, enrollment);
}

function renderStudentStages(project, enrollment) {
  const content = document.getElementById('student-detail-content');
  const stages = [...(project.etapas || [])].sort((a, b) => a.ordem - b.ordem);

  let html = `
    <div class="project-info-card">
      <p class="project-info-desc">${project.descricao}</p>
    </div>
    <div class="stages-student">
  `;

  stages.forEach(stage => {
    html += `
      <div class="stage-student-card">
        <div class="stage-student-head">
          ${stageNum(stage.ordem)}
          <span class="stage-student-name">${stage.titulo}</span>
        </div>
        <p class="stage-student-instrucao">${stage.instrucao}</p>
        <div class="stage-submit-area">
          <div id="submit-area-${stage.id}">
            <form class="submit-form" id="form-${stage.id}">
              <div class="field">
                <label for="content-${stage.id}">Sua solução</label>
                <textarea id="content-${stage.id}" rows="3" placeholder="Cole ou descreva sua solução aqui..." required></textarea>
              </div>
              <div id="submit-error-${stage.id}" class="alert alert-error hidden"></div>
              <button type="submit" class="btn btn-primary btn-sm">Enviar solução</button>
            </form>
          </div>
        </div>
      </div>
    `;
  });

  html += '</div>';
  content.innerHTML = html;

  stages.forEach(stage => {
    const form = document.getElementById(`form-${stage.id}`);
    if (!form) return;
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      clearError(`submit-error-${stage.id}`);
      const conteudo = document.getElementById(`content-${stage.id}`).value;

      const { ok, data } = await api('POST', '/submissoes', {
        matricula_id: enrollment.id,
        etapa_id: stage.id,
        conteudo,
      });

      if (!ok) { showError(`submit-error-${stage.id}`, data.erro || 'Erro ao enviar.'); return; }

      const area = document.getElementById(`submit-area-${stage.id}`);
      area.innerHTML = `
        <div class="submission-status">
          ${badge(data.submissao.status, data.submissao.status)}
          <span class="submission-status-feedback">Enviado em ${formatDate(data.submissao.enviado_em)}</span>
        </div>
      `;
    });
  });
}

document.getElementById('back-from-student-detail').addEventListener('click', loadStudentList);