document.addEventListener('DOMContentLoaded', () => {
  const loadButton = document.getElementById('loadButton');
  const output = document.getElementById('output');
  const tableContainer = document.getElementById('tableContainer');
  const summary = document.getElementById('summary');

  function showMessage(text) {
    summary.textContent = text;
  }

  function showOutput(data) {
    output.textContent = JSON.stringify(data, null, 2);
  }

  function renderTable(columns, rows) {
    if (!rows || rows.length === 0) {
      tableContainer.innerHTML = '<p>当前没有用户数据。</p>';
      return;
    }

    const thead = columns.map(col => `<th>${col}</th>`).join('');
    const bodyRows = rows.map(row => {
      const cells = row.map(value => `<td>${value === null ? '' : String(value)}</td>`).join('');
      return `<tr>${cells}</tr>`;
    }).join('');

    tableContainer.innerHTML = `
      <table>
        <thead><tr>${thead}</tr></thead>
        <tbody>${bodyRows}</tbody>
      </table>
    `;
  }

  function normalizeData(data) {
    if (!Array.isArray(data)) return { columns: [], rows: [] };
    if (data.length === 0) return { columns: [], rows: [] };

    const first = data[0];
    if (first && typeof first === 'object' && !Array.isArray(first)) {
      const columns = Object.keys(first);
      const rows = data.map(item => columns.map(col => item[col]));
      return { columns, rows };
    }

    if (Array.isArray(first)) {
      const columns = first.map((_, index) => `列${index + 1}`);
      return { columns, rows: data };
    }

    return { columns: ['value'], rows: data.map(item => [item]) };
  }

  loadButton.addEventListener('click', async () => {
    loadButton.disabled = true;
    showMessage('正在加载用户数据...');
    showOutput({ status: 'loading' });
    tableContainer.innerHTML = '';

    try {
      const response = await fetch('/api/admin/get_all_users');
      const body = await response.json().catch(() => null);

      if (!response.ok) {
        showMessage(`请求失败：${response.status}`);
        showOutput({ status: response.status, body });
        return;
      }

      showMessage(`已获取 ${Array.isArray(body) ? body.length : 0} 条用户记录。`);
      showOutput(body);
      const normalized = normalizeData(body);
      renderTable(normalized.columns, normalized.rows);
    } catch (error) {
      showMessage('请求出错，请检查后台是否可用。');
      showOutput({ error: error.message });
    } finally {
      loadButton.disabled = false;
    }
  });
});
