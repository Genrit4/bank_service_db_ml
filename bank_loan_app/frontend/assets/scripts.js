const API = 'http://127.0.0.1:8000';

// Модалки
function openModal(id){ document.getElementById(id).style.display = 'flex'; }
function closeModal(id){ document.getElementById(id).style.display = 'none'; }

// Навигация по модалкам
function showLogin() {
  closeModal('authModal');
  openModal('loginModal');
}
function showRegister() {
  closeModal('authModal');
  openModal('registerModal');
}

// Регистрация
async function register() {
  const payload = {
    login: document.getElementById('reg-login').value,
    password: document.getElementById('reg-password').value,
    email: document.getElementById('reg-mail').value,
    phone: document.getElementById('reg-phone').value
  };
  const res = await fetch(`${API}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (res.ok) {
    alert('Успешно зарегистрированы');
    closeModal('registerModal');
  } else {
    const err = await res.text();
    alert('Ошибка регистрации: ' + err);
  }
}

// Вход
async function login() {
  const form = new URLSearchParams();
  form.append('username', document.getElementById('login-login').value);
  form.append('password', document.getElementById('login-password').value);

  const res = await fetch(`${API}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form
  });

  if (res.ok) {
    const data = await res.json();
    // Сохраняем токен в localStorage
    localStorage.setItem('access_token', data.access_token);
    alert('Вход выполнен');
    closeModal('loginModal');
    window.location.href = 'prediction.html';
  } else {
    const err = await res.text();
    alert('Ошибка входа: ' + err);
  }
}

// Предсказание (prediction.html)
async function predictLoan(event) {
  // Если событие передано, подавляем дефолтное поведение
  if (event) event.preventDefault();

  const token = localStorage.getItem('access_token');
  if (!token) {
    alert('Сначала войдите в систему');
    window.location.href = 'index.html';
    return;
  }

  const fields = ['dependents','income_annum','loan_amount','loan_term','cibil_score'];
  const payload = {};
  for (let f of fields) {
    payload[f] = parseFloat(document.getElementById(f).value);
  }
  payload.self_employed = document.getElementById('self_employed').checked;
  payload.education = document.getElementById('education').checked;

  const res = await fetch(`${API}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    const { loan_status } = await res.json();
    document.getElementById('result').innerText = loan_status
      ? 'Вероятнее всего — кредит одобрят!'
      : 'К сожалению, отказ.';
  } else if (res.status === 401) {
    alert('Токен недействителен. Пожалуйста, войдите заново.');
    window.location.href = 'index.html';
  } else {
    document.getElementById('result').innerText = 'Ошибка предсказания';
  }
}
