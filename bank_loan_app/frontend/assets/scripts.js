const API = 'http://127.0.0.1:8000';

// Модалки
function openModal(id) {
  document.getElementById(id).style.display = 'flex';
}
function closeModal(id) {
  document.getElementById(id).style.display = 'none';
}

// Навигация
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
    headers: {'Content-Type': 'application/json'},
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
  const usernameInput = document.getElementById('login-login').value;
  const passwordInput = document.getElementById('login-password').value;
  console.log('login start:', usernameInput);

  const form = new URLSearchParams();
  form.append('username', usernameInput);
  form.append('password', passwordInput);

  const res = await fetch(`${API}/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: form
  });

  console.log('login response status:', res.status);
  if (res.ok) {
    const data = await res.json();
    console.log('response token:', data.access_token);

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('username', usernameInput);
    console.log('saved username:', localStorage.getItem('username'));

    alert('Вход выполнен');
    window.location.href = 'prediction.html';
  } else {
    const err = await res.text();
    alert('Ошибка входа: ' + err);
  }
}

// Предсказание
async function predictLoan(event) {
  if (event) event.preventDefault();

  const token = localStorage.getItem('access_token');
  if (!token) {
    alert('Сначала войдите в систему');
    window.location.href = 'index.html';
    return;
  }

  const storedUser = localStorage.getItem('username');
  console.log('username on predict page:', storedUser);
  if (storedUser) {
    const userElem = document.getElementById('username');
    if (userElem) userElem.innerText = storedUser;
  }

  const fields = ['dependents', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score'];
  const payload = {};
  fields.forEach(f => payload[f] = parseFloat(document.getElementById(f).value));
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
