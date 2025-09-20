
function changeTypePassword() {
  let password = document.getElementById('passwordField');
  let eyeIcon = document.querySelector('.fa-regular');

  if (password.type === 'text') {
      password.type = 'password';
      eyeIcon.classList.remove('fa-eye-slash');
      eyeIcon.classList.add('fa-eye');
  } else {
      password.type = 'text';
      eyeIcon.classList.remove('fa-eye');
      eyeIcon.classList.add('fa-eye-slash');
  }
}
function cofirmPassword() {
  let passwords = document.getElementById('passwordFields');
  let eyeIcon = document.querySelector('.fa-solid');
  if (passwords.type === 'text') {
      passwords.type = 'password';
      eyeIcon.classList.remove('fa-lock-open');
      eyeIcon.classList.add('fa-lock');
  } else {
      passwords.type = 'text';
      eyeIcon.classList.remove('fa-lock');
      eyeIcon.classList.add('fa-lock-open');
  }
}