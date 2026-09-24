const { spawn } = require('child_process');

async function test() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', ['--headless=new', '--remote-debugging-port=9336']);
  await new Promise(r => setTimeout(r, 1500));
  const tab = await (await fetch('http://localhost:9336/json/new?http://localhost:5173/servicio/voz_pasiva', { method: 'PUT' })).json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);

  let id = 1;
  function send(method, params = {}) {
    return new Promise(res => {
      const mid = id++;
      ws.addEventListener('message', function h(e) {
        const d = JSON.parse(e.data);
        if (d.id === mid) {
          ws.removeEventListener('message', h);
          res(d.result);
        }
      });
      ws.send(JSON.stringify({ id: mid, method, params }));
    });
  }

  for (let i = 0; i < 20; i++) {
    await new Promise(r => setTimeout(r, 300));
    const chk = await send('Runtime.evaluate', { expression: 'Boolean(document.querySelector(".markdown-body"))' });
    if (chk?.result?.value) break;
  }

  const orderCheck = await send('Runtime.evaluate', {
    expression: `
      (() => {
        const sim = document.querySelector('.process-simulator');
        const h2s = Array.from(document.querySelectorAll('.markdown-body h2'));
        const defH2 = h2s.find(h => h.textContent.toLowerCase().includes('definici'));
        if (!sim || !defH2) return 'missing elements';
        const simPos = sim.compareDocumentPosition(defH2);
        // Node.DOCUMENT_POSITION_FOLLOWING is 4, meaning defH2 is after sim
        return (simPos & Node.DOCUMENT_POSITION_FOLLOWING) !== 0 ? 'SIM_BEFORE_DEFINITION' : 'SIM_AFTER_DEFINITION';
      })()
    `
  });

  console.log('ORDER_RESULT:', orderCheck?.result?.value);
  ws.close();
  chrome.kill('SIGKILL');
}

test().catch(e => {
  console.error(e);
  process.exit(1);
});
