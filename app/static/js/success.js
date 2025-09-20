  const tbody = document.querySelector('#deployTable tbody');
  const refreshBtn = document.getElementById('refreshBtn');
  const logModal = new bootstrap.Modal(document.getElementById('logModal'));

  function badge(status){
    const s = (status||'pending').toLowerCase();
    if (s === 'success') return '<span class="badge badge-success">SUCCESS</span>';
    if (s === 'failed' || s === 'failure') return '<span class="badge badge-failed">FAILED</span>';
    return '<span class="badge badge-pending">PENDING</span>';
  }
  function fmtTime(iso){
    if(!iso) return '';
    const d = new Date(iso);
    return d.toLocaleString();
  }
  function fmtBuildTime(v){
    if (v == null) return '';
    const s = Number(v);
    if (Number.isNaN(s)) return v;
    return s < 1 ? Math.round(s*1000)+' ms' : s.toFixed(1)+' s';
  }

  async function fetchDeployments(){
    const r = await fetch('/api/my_deployments?limit=50', {cache:'no-store'});
    const data = await r.json();
    renderTable(data);
  }

  function renderTable(items){
    tbody.innerHTML = items.map(it => `
      <tr>
        <td>#${it.id}</td>
        <td>${it.project_name || it.project_id}</td>
        <td class="mono small">${it.zip_filename || ''}</td>
        <td>${badge(it.status)}</td>
        <td class="small">${fmtTime(it.created_at)}</td>
        <td class="small">${fmtBuildTime(it.build_time)}</td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-primary" onclick="openLogs(${it.id})">Xem log</button>
          <span id="logs-${it.id}" class="d-none">${(it.logs || '').replace(/</g,'&lt;')}</span>
        </td>
      </tr>
    `).join('');
  }

  function openLogs(id){
    document.getElementById('logTitle').textContent = `#${id}`;
    const raw = document.getElementById(`logs-${id}`)?.textContent || '';
    document.getElementById('logContent').textContent = raw || '(chưa có log)';
    logModal.show();
  }

  refreshBtn.addEventListener('click', fetchDeployments);
  fetchDeployments();
  setInterval(fetchDeployments, 2000);