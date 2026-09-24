const { spawn } = require('child_process');

async function test() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', ['--headless=new', '--remote-debugging-port=9335']);
  await new Promise(r => setTimeout(r, 1500));
  const tab = await (await fetch('http://localhost:9335/json/new?http://localhost:5173/servicio/voz_pasiva', { method: 'PUT' })).json();
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

  // Wait for React rendering
  for (let i = 0; i < 20; i++) {
    await new Promise(r => setTimeout(r, 300));
    const chk = await send('Runtime.evaluate', { expression: 'Boolean(document.querySelector(".process-simulator"))' });
    if (chk?.result?.value) {
      break;
    }
  }

  const r = await send('Runtime.evaluate', { expression: 'Boolean(document.querySelector(".process-simulator"))' });
  const title = await send('Runtime.evaluate', { expression: 'document.querySelector(".sim-title")?.textContent' });
  const stepCount = await send('Runtime.evaluate', { expression: 'document.querySelectorAll(".sim-step-node").length' });
  const activeToken = await send('Runtime.evaluate', { expression: 'document.querySelector(".sim-token-chip")?.textContent' });

  console.log('SIMULATOR_EXISTS:', r?.result?.value);
  console.log('SIMULATOR_TITLE:', title?.result?.value);
  console.log('STEP_NODES_COUNT:', stepCount?.result?.value);
  console.log('FIRST_TOKEN:', activeToken?.result?.value);

  ws.close();
  chrome.kill('SIGKILL');
}

test().catch(e => {
  console.error(e);
  process.exit(1);
});
