// 사용법: node render.js <promo|s1|s2|s3> <출력.mp4> [미리보기 초들...]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

(async () => {
  const [v, out, ...stills] = process.argv.slice(2);
  const tall = v !== 'promo';
  const W = tall ? 1080 : 1920, H = tall ? 1920 : 1080, DUR = tall ? 15 : 30, FPS = 30;
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: W, height: H } });
  await page.goto('file://' + path.join(__dirname, 'film.html') + '?v=' + v);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);

  if (stills.length) {
    for (const t of stills) {
      await page.evaluate(t => seek(t), parseFloat(t));
      await page.screenshot({ path: `${out}-${v}-${t}.jpg`, type: 'jpeg', quality: 80 });
    }
    await b.close(); return;
  }

  const tmp = out.replace(/\.mp4$/, '.part.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', tmp],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = DUR * FPS;
  for (let i = 0; i < total; i++) {
    await page.evaluate(t => seek(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code === 0) { fs.renameSync(tmp, out); console.log('done', out); }
  else { console.error('ffmpeg failed', code); process.exit(1); }
})();
