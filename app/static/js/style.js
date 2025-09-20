document.addEventListener('DOMContentLoaded', function () {
  const optionCreate = document.getElementById('option_create');
  const optionExisting = document.getElementById('option_existing');
  const sqlGroup = document.getElementById('sql_file_group');
  const hostGroup = document.getElementById('host_db_group');
  const fileSql = document.getElementById('file_sql');
  const sourceZipRadio = document.getElementById('source_type_zip');
  const sourceGithubRadio = document.getElementById('source_type_github');
  const zipGroup = document.getElementById('zip_file_group');
  const githubGroup = document.getElementById('github_link_group');
  const zipInput = document.getElementById('file_zip');
  const githubUrlInput = document.getElementById('github_url');


  function toggleFields() {
    if (!optionCreate || !optionExisting || !sqlGroup || !hostGroup) return;
    const create = optionCreate.checked;
    sqlGroup.style.display = create ? 'block' : 'none';
    hostGroup.style.display = create ? 'none' : 'block';
    if (fileSql) {
      if (create) fileSql.setAttribute('required', 'required');
      else fileSql.removeAttribute('required');
    }
  }
  if (optionCreate && optionExisting) {
    optionCreate.addEventListener('change', toggleFields);
    optionExisting.addEventListener('change', toggleFields);
    toggleFields();
  }

  // nút "Deploy" nhưng yêu cầu đăng nhập
  const newDeployBtn = document.getElementById('deploy-btn-login');
  const modalEl = document.getElementById('loginRequiredModal1');
  if (newDeployBtn && modalEl && window.bootstrap?.Modal) {
    const loginModal = new bootstrap.Modal(modalEl);
    newDeployBtn.addEventListener('click', function (e) {
      e.preventDefault();
      loginModal.show();
    });
  }

  // hiện loading modal khi submit
  const deployForm = document.getElementById('deploy-form');
  const loadingModal = document.getElementById('loadingModal');
  if (deployForm && loadingModal && window.bootstrap?.Modal) {
    const loadingModalInstance = new bootstrap.Modal(loadingModal, {
      backdrop: 'static',
      keyboard: false
    });
    deployForm.addEventListener('submit', function () {
      loadingModalInstance.show();
    });
  }

  const toggleBtn = document.getElementById('toggle-passwd'); // <button id="toggle-passwd"><i class="fa-regular fa-eye-slash"></i></button>
  const passwdInput = document.getElementById('passwd');
  if (toggleBtn && passwdInput) {
    toggleBtn.addEventListener('click', function () {
      const show = passwdInput.type === 'password'; // đang ẩn → chuẩn bị hiện
      passwdInput.type = show ? 'text' : 'password';
      const icon = toggleBtn.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-eye', show);
        icon.classList.toggle('fa-eye-slash', !show);
      }
      toggleBtn.setAttribute('aria-pressed', show ? 'true' : 'false');
    });
  }




        function handleSourceChange() {
            if (sourceGithubRadio.checked) {
                githubGroup.style.display = 'block';
                zipGroup.style.display = 'none';
                githubUrlInput.required = true;
                zipInput.required = false;
            } else { // ZIP is selected
                githubGroup.style.display = 'none';
                zipGroup.style.display = 'block';
                githubUrlInput.required = false;
                zipInput.required = true;
            }
        }
        sourceZipRadio.addEventListener('change', handleSourceChange);
        sourceGithubRadio.addEventListener('change', handleSourceChange);

        dbExistingRadio.addEventListener('change', handleDbOptionChange);
        dbCreateRadio.addEventListener('change', handleDbOptionChange);

  setInterval(function () {
    const frame = document.getElementById('jenkins-frame');
    if (frame) frame.src = frame.src;
  }, 10000);
});

