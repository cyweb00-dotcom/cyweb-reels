// Phone screens = the kind of websites CYWEB builds for local businesses (built in code).
// If assets/screens/1..4.png exist, render.js passes them in and they replace these.
// Layout units: the screen is 2112 px wide before the 0.5 scale (≈ 5.4 px per iOS point).
(() => {
  const css = `
  .site{position:absolute;left:0;top:0;width:200%;height:200%;transform:scale(.5);transform-origin:0 0;font-family:Inter;color:#111;background:#fbfbfa;font-size:84px;line-height:1.2}
  .site .sb{display:flex;justify-content:space-between;align-items:center;padding:56px 130px 0;font-weight:600;font-size:76px}
  .site .isl{width:600px;height:170px;border-radius:90px;background:#000}
  .site .nav{display:flex;justify-content:space-between;align-items:center;padding:70px 110px 40px}
  .site .nav b{font-size:120px;font-weight:700;letter-spacing:-.02em}
  .site .nav i{font-style:normal;font-size:110px;color:#444}
  .site .photo{margin:20px 90px;height:900px;border-radius:90px;position:relative;overflow:hidden;display:flex;align-items:flex-end;padding:90px}
  .site .photo h1{font-size:170px;line-height:1.02;color:#fff;font-weight:700;letter-spacing:-.02em;position:relative;text-shadow:0 6px 40px rgba(0,0,0,.35)}
  .site .row{display:flex;gap:50px;padding:60px 90px 10px}
  .site .btn{flex:1;text-align:center;font-weight:600;font-size:84px;padding:70px 0;border-radius:200px;background:#111;color:#fff}
  .site .btn.wa{background:#25a35a}
  .site .btn.blue{background:#1f6fe0}
  .site .btn.ghost{background:#eceef0;color:#111}
  .site h2{font-size:104px;font-weight:700;padding:90px 110px 30px;letter-spacing:-.01em}
  .site .li{display:flex;align-items:center;gap:60px;padding:56px 110px;border-bottom:4px solid #ececec;font-size:88px}
  .site .li .ic{width:120px;height:120px;border-radius:34px;flex:none}
  .site .li em{margin-left:auto;font-style:normal;color:#8a8a8a;font-size:76px}
  .site .stars{padding:40px 110px;font-size:84px;color:#444}.site .stars b{color:#f2a700;letter-spacing:.08em}
  .site .map{margin:20px 90px;height:600px;border-radius:80px;position:relative;overflow:hidden;
    background:linear-gradient(90deg,transparent 47%,#fff 47% 53%,transparent 53%),linear-gradient(0deg,transparent 60%,#fff 60% 64%,transparent 64%),linear-gradient(32deg,#dfe9df 0 50%,#e7eee6 50%)}
  .site .map:after{content:"";position:absolute;left:50%;top:40%;width:110px;height:110px;margin:-55px;border-radius:50% 50% 50% 0;background:#e24c3b;transform:rotate(-45deg)}
  .site .tiles{display:grid;grid-template-columns:1fr 1fr;gap:56px;padding:20px 90px}
  .site .tile{height:620px;border-radius:80px;position:relative;overflow:hidden;display:flex;align-items:flex-end;padding:60px;color:#fff;font-weight:700;font-size:100px}
  .site .chips{display:flex;gap:40px;padding:20px 90px;flex-wrap:wrap}
  .site .chip2{padding:46px 70px;border-radius:120px;background:#eceef0;font-weight:600;font-size:84px}
  .site .chip2.on{background:#111;color:#fff}
  .site .cal{padding:10px 90px}
  .site .cal .mh{display:flex;justify-content:space-between;align-items:center;font-size:110px;font-weight:700;padding:40px 20px}
  .site .cal .dw,.site .cal .gd{display:grid;grid-template-columns:repeat(7,1fr);text-align:center}
  .site .cal .dw{font-size:64px;color:#999;font-weight:600;padding:20px 0}
  .site .cal .gd i{font-style:normal;font-size:86px;font-weight:500;height:200px;line-height:200px;margin:8px;border-radius:100px}
  .site .cal .gd i.off{color:#c8c8c8}.site .cal .gd i.sel{background:#111;color:#fff;font-weight:700}
  `;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const sb = t => `<div class="sb"><span>${t}</span><span class="isl"></span><span>●●● ▮</span></div>`;
  const photo = (bg, art) => `background:${bg}`;
  window.SCREENS = {
    // 1 — left wall: café website (book a table, WhatsApp, menu, map, reviews)
    cafe: `<div class="site">${sb('9:41')}
      <div class="nav"><b>Your Café</b><i>☰</i></div>
      <div class="photo" style="${photo('radial-gradient(circle at 70% 38%,#f5e3c8 0 9%,#c98b4e 9.5% 15%,#5a341b 15.5% 19%,transparent 19.5%),radial-gradient(circle at 70% 40%,rgba(0,0,0,.25) 0 24%,transparent 26%),linear-gradient(160deg,#d9a56d,#8a5630 55%,#3d2516)')}"><h1>Fresh coffee<br>by the sea</h1></div>
      <div class="row"><div class="btn">Book a table</div><div class="btn wa">WhatsApp us</div></div>
      <div class="stars"><b>★★★★★</b> on Google</div>
      <h2>Menu</h2>
      <div class="li"><span class="ic" style="background:#c98b4e"></span>Flat white<em>Hot</em></div>
      <div class="li"><span class="ic" style="background:#e8c15a"></span>Halloumi toast<em>Brunch</em></div>
      <div class="li"><span class="ic" style="background:#6fb3d9"></span>Iced latte<em>Cold</em></div>
      <h2>Find us</h2><div class="map"></div></div>`,
    // 2 — top wall: salon booking site
    salon: `<div class="site">${sb('10:03')}
      <div class="nav"><b>Your Salon</b><i>☰</i></div>
      <h2 style="padding-top:20px">Book online</h2>
      <div class="tiles">
        <div class="tile" style="background:linear-gradient(160deg,#c9a6a0,#7c4e4a)">Cut</div>
        <div class="tile" style="background:linear-gradient(160deg,#b7a3d6,#5d4a86)">Colour</div>
        <div class="tile" style="background:linear-gradient(160deg,#f0b5a8,#b0574a)">Nails</div>
        <div class="tile" style="background:linear-gradient(160deg,#a8c6b8,#3f6b5a)">Brows</div></div>
      <h2>Free today</h2>
      <div class="chips"><span class="chip2">10:30</span><span class="chip2 on">12:00</span><span class="chip2">15:15</span><span class="chip2">17:45</span></div>
      <div class="row"><div class="btn">Book now</div></div></div>`,
    // 3 — right wall: clinic site (call now, book, services, hours)
    clinic: `<div class="site">${sb('9:58')}
      <div class="nav"><b>Your Clinic</b><i>☰</i></div>
      <div class="photo" style="height:760px;${photo('radial-gradient(circle at 75% 30%,rgba(255,255,255,.55) 0 14%,transparent 15%),linear-gradient(160deg,#9cc7ec,#2f6fb4)')}"><h1>Care close<br>to home</h1></div>
      <div class="row"><div class="btn blue">Call now</div><div class="btn ghost">Book a visit</div></div>
      <h2>Services</h2>
      <div class="li"><span class="ic" style="background:#dbe9f8"></span>Check-ups<em>›</em></div>
      <div class="li"><span class="ic" style="background:#dbe9f8"></span>Physiotherapy<em>›</em></div>
      <div class="li"><span class="ic" style="background:#dbe9f8"></span>Home visits<em>›</em></div>
      <h2>Open today</h2>
      <div class="li" style="border:0">8:00 – 18:00<em>Mon – Sat</em></div></div>`,
    // 4 — bottom wall + whip: booking calendar
    calendar: (() => {
      let g = ''; for (let i = 0; i < 3; i++) g += `<i class="off">${28 + i}</i>`;
      for (let d = 1; d <= 31; d++) g += `<i class="${d === 18 ? 'sel' : (d < 9 ? 'off' : '')}">${d}</i>`;
      return `<div class="site">${sb('10:04')}
      <div class="nav"><b>Book your visit</b><i>✕</i></div>
      <div class="cal"><div class="mh"><span>March</span><span style="color:#999">‹ ›</span></div>
        <div class="dw"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span></div>
        <div class="gd">${g}</div></div>
      <div class="chips" style="padding-top:60px"><span class="chip2">09:00</span><span class="chip2 on">11:30</span><span class="chip2">14:00</span></div>
      <div class="row"><div class="btn">Confirm booking</div></div></div>`;
    })(),
  };
})();
