const { spawn } = require('child_process');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const port = 9444;
const edge = spawn(edgePath, [
  '--headless=new',
  `--remote-debugging-port=${port}`,
  '--disable-gpu',
  '--no-first-run'
]);

async function test() {
  await new Promise(r => setTimeout(r, 2000));
  const res = await fetch(`http://localhost:${port}/json/new?http://localhost:5173/servicio/deteccion_conectores_logicos`, { method: 'PUT' });
  const tab = await res.json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);

  ws.onmessage = (e) => {
    const d = JSON.parse(e.data);
    if (d.method === 'Runtime.consoleAPICalled') {
      console.log('[EDGE CONSOLE]', d.params.args.map(a => a.value || a.description));
    }
    if (d.method === 'Runtime.exceptionThrown') {
      console.error('[EDGE EXCEPTION]', JSON.stringify(d.params.exceptionDetails, null, 2));
    }
    if (d.id === 3) {
      console.log('EDGE innerHTML length:', d.result?.result?.value?.length);
      console.log('EDGE innerHTML:', d.result?.result?.value?.slice(0, 300));
      ws.close();
      edge.kill('SIGKILL');
      process.exit(0);
    }
  };

  ws.send(JSON.stringify({ id: 1, method: 'Runtime.enable' }));
  ws.send(JSON.stringify({ id: 2, method: 'Network.enable' }));
  await new Promise(r => setTimeout(r, 4000));
  const bodyRes = await new Promise(resolve => {
    const msgId = 100;
    const handler = (e) => {
      const d = JSON.parse(e.data);
      if (d.id === msgId) {
        ws.removeEventListener('message', handler);
        resolve(d.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify({ id: msgId, method: 'Runtime.evaluate', params: { expression: 'document.body.innerHTML' } }));
  });
  console.log('EDGE body innerHTML:', bodyRes?.result?.value);
  ws.close();
  edge.kill('SIGKILL');
  process.exit(0);
}

test().catch(e => {
  console.error(e);
  edge.kill('SIGKILL');
  process.exit(1);
});
