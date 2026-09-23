const { spawn } = require('child_process');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const port = 9333;
const chrome = spawn(chromePath, ['--headless=new', `--remote-debugging-port=${port}`, '--disable-gpu']);

setTimeout(async () => {
  try {
    const tabRes = await fetch(`http://localhost:${port}/json/new?http://localhost:5173/servicio/deteccion_conectores_logicos`, { method: 'PUT' });
    const tab = await tabRes.json();
    const ws = new WebSocket(tab.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);
    ws.send(JSON.stringify({ id: 1, method: 'Runtime.enable' }));
    await new Promise(r => setTimeout(r, 3000));

    const msgId = 2;
    ws.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if (d.id === msgId) {
        console.log('Images info:', JSON.stringify(d.result?.result?.value, null, 2));
        ws.close();
        chrome.kill('SIGKILL');
        process.exit(0);
      }
    };

    ws.send(JSON.stringify({
      id: msgId,
      method: 'Runtime.evaluate',
      params: {
        expression: `
          Array.from(document.querySelectorAll('img')).map(img => ({
            src: img.src,
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
            clientWidth: img.clientWidth,
            clientHeight: img.clientHeight,
            complete: img.complete
          }))
        `,
        returnByValue: true
      }
    }));
  } catch (err) {
    console.error(err);
    chrome.kill('SIGKILL');
    process.exit(1);
  }
}, 1500);
