const { spawn } = require('child_process');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const port = 9555;
const edge = spawn(edgePath, [
  '--headless=new',
  `--remote-debugging-port=${port}`,
  '--disable-gpu',
  '--no-first-run'
]);

async function test() {
  await new Promise(r => setTimeout(r, 2000));
  const res = await fetch(`http://localhost:${port}/json/new?http://localhost:5173/`, { method: 'PUT' });
  const tab = await res.json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);

  let id = 1;
  function send(method, params = {}) {
    return new Promise((resolve) => {
      const msgId = id++;
      const handler = (e) => {
        const d = JSON.parse(e.data);
        if (d.id === msgId) {
          ws.removeEventListener('message', handler);
          resolve(d.result);
        }
      };
      ws.addEventListener('message', handler);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  }

  ws.onmessage = (e) => {
    const d = JSON.parse(e.data);
    if (d.method === 'Runtime.consoleAPICalled') {
      console.log('[CONSOLE]', d.params.type, ...d.params.args.map(a => a.value || a.description));
    }
    if (d.method === 'Runtime.exceptionThrown') {
      console.error('[EXCEPTION]', d.params.exceptionDetails);
    }
  };

  await send('Runtime.enable');
  await send('Network.enable');

  await new Promise(r => setTimeout(r, 2000));

  // Now click on the first link
  console.log('Clicking on first link...');
  const clickRes = await send('Runtime.evaluate', {
    expression: `
      const link = document.querySelector('a[href="/servicio/deteccion_conectores_logicos"]');
      if (link) {
        link.click();
        'clicked';
      } else {
        'link not found';
      }
    `
  });
  console.log('Click eval result:', clickRes);

  await new Promise(r => setTimeout(r, 2000));

  const contentRes = await send('Runtime.evaluate', {
    expression: 'document.querySelector(".main-content")?.innerHTML'
  });
  console.log('Main content length after click:', contentRes?.result?.value?.length);
  console.log('Main content preview:', contentRes?.result?.value?.slice(0, 300));

  ws.close();
  edge.kill('SIGKILL');
  process.exit(0);
}

test().catch(e => {
  console.error(e);
  edge.kill('SIGKILL');
  process.exit(1);
});
