const { spawn } = require('child_process');
const fs = require('fs');

async function run() {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const port = 9333;
  const chrome = spawn(chromePath, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
  ]);

  try {
    // Wait for Chrome CDP to be available
    let connected = false;
    let versionData = null;
    for (let i = 0; i < 30; i++) {
      await new Promise(r => setTimeout(r, 200));
      try {
        const res = await fetch(`http://localhost:${port}/json/version`);
        if (res.ok) {
          versionData = await res.json();
          connected = true;
          break;
        }
      } catch (e) {}
    }

    if (!connected) {
      console.error('Failed to connect to Chrome CDP');
      return;
    }

    console.log('Chrome connected. Browser version:', versionData.Browser);

    // Create a new target/tab
    const newTabRes = await fetch(`http://localhost:${port}/json/new?http://localhost:5173/servicio/voz_pasiva`, { method: 'PUT' });
    const tabData = await newTabRes.json();
    const wsUrl = tabData.webSocketDebuggerUrl;
    console.log('Tab opened, connecting WebSocket:', wsUrl);

    const ws = new WebSocket(wsUrl);

    await new Promise((resolve, reject) => {
      ws.onopen = resolve;
      ws.onerror = reject;
    });

    let id = 1;
    function send(method, params = {}) {
      return new Promise((resolve) => {
        const msgId = id++;
        const handler = (event) => {
          const data = JSON.parse(event.data);
          if (data.id === msgId) {
            ws.removeEventListener('message', handler);
            resolve(data.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: msgId, method, params }));
      });
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.method === 'Runtime.consoleAPICalled') {
        console.log(`[BROWSER CONSOLE ${data.params.type}]`, ...data.params.args.map(a => a.value || a.description));
      } else if (data.method === 'Runtime.exceptionThrown') {
        console.error('[BROWSER EXCEPTION]', data.params.exceptionDetails);
      } else if (data.method === 'Network.responseReceived') {
        const resp = data.params.response;
        if (resp.status >= 400) {
          console.warn(`[BROWSER NETWORK ${resp.status}]`, resp.url);
        }
      }
    };

    await send('Runtime.enable');
    await send('Network.enable');
    await send('Page.enable');

    // Wait for React to render
    for (let i = 0; i < 40; i++) {
      await new Promise(r => setTimeout(r, 250));
      const check = await send('Runtime.evaluate', {
        expression: 'Boolean(document.querySelector(".markdown-body"))'
      });
      if (check?.result?.value) {
        console.log(`React rendered after ${(i + 1) * 250}ms`);
        break;
      }
    }

    // Get document HTML
    const evalRes = await send('Runtime.evaluate', {
      expression: 'document.documentElement.outerHTML'
    });
    console.log('Document outerHTML length:', evalRes?.result?.value?.length);
    console.log('Document outerHTML snippet:', evalRes?.result?.value?.slice(0, 500));

    // Capture full page screenshot
    const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
    if (shot && shot.data) {
      fs.writeFileSync('C:\\Users\\Juliana\\.gemini\\antigravity-ide\\brain\\f5a3ef6e-fb68-42d5-a063-6d6d74c437e5\\scratch\\browser_shot.png', Buffer.from(shot.data, 'base64'));
      console.log('Saved screenshot to scratch/browser_shot.png');
    }

    ws.close();
  } finally {
    chrome.kill('SIGKILL');
  }
}

run().catch(console.error);
