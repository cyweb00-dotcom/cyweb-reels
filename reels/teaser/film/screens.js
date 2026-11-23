// Stand-in phone screens (built in code). If assets/screens/1..4.png exist,
// render.js passes them in and they replace these.
window.SCREENS = {
  // 1: left wall — café website
  cafe: `
  <div class="scr light">
    <div class="sb"><span>9:41</span><span class="isl"></span><span>●●●</span></div>
    <div class="nav"><b>Your Café</b><span>☰</span></div>
    <div class="hero cafe"><div class="ht">Fresh coffee<br>by the sea</div><div class="btn">Book a table</div></div>
    <div class="sec">Today's menu</div>
    <div class="li"><span class="dot o"></span>Flat white<em>Hot</em></div>
    <div class="li"><span class="dot g"></span>Halloumi toast<em>Brunch</em></div>
    <div class="li"><span class="dot b"></span>Iced latte<em>Cold</em></div>
    <div class="li"><span class="dot o"></span>Carob cake<em>Sweet</em></div>
    <div class="li"><span class="dot g"></span>Village salad<em>Lunch</em></div>
    <div class="sec">Find us</div>
    <div class="map"></div>
    <div class="li"><span class="dot b"></span>Open 8:00 – 20:00<em>Daily</em></div>
  </div>`,
  // 2: top wall — salon booking
  salon: `
  <div class="scr light">
    <div class="sb"><span>10:03</span><span class="isl"></span><span>●●●</span></div>
    <div class="nav"><b>Your Salon</b><span>＋</span></div>
    <div class="tiles">
      <div class="tile t1">Cut</div><div class="tile t2">Colour</div><div class="tile t3">Nails</div>
      <div class="tile t4">Brows</div><div class="tile t5">Spa</div><div class="tile t6">Gift</div>
    </div>
    <div class="sec">Next free slots</div>
    <div class="li"><span class="dot b"></span>Today 14:30<em>Book</em></div>
    <div class="li"><span class="dot b"></span>Today 16:00<em>Book</em></div>
    <div class="li"><span class="dot b"></span>Tomorrow 10:15<em>Book</em></div>
    <div class="li"><span class="dot g"></span>Reviews 4.9<em>See all</em></div>
  </div>`,
  // 3: right wall — clinic site
  clinic: `
  <div class="scr light">
    <div class="sb"><span>9:58</span><span class="isl"></span><span>●●●</span></div>
    <div class="nav"><b>Your Clinic</b><span>☰</span></div>
    <div class="hero clinic"><div class="ht">Care close<br>to home</div><div class="btn">Call now</div></div>
    <div class="sec">Services</div>
    <div class="li"><span class="dot b"></span>Check-ups<em>›</em></div>
    <div class="li"><span class="dot b"></span>Physio<em>›</em></div>
    <div class="li"><span class="dot b"></span>Dental<em>›</em></div>
    <div class="li"><span class="dot b"></span>Home visits<em>›</em></div>
    <div class="sec">Folders</div>
    <div class="li"><span class="dot g"></span>Forms<em>›</em></div>
    <div class="li"><span class="dot g"></span>Insurance<em>›</em></div>
  </div>`,
  // 4: bottom wall + whip — booking calendar
  calendar: (() => {
    const month = (name, start, days) => {
      let c = '';
      for (let i = 0; i < start; i++) c += '<i></i>';
      for (let d = 1; d <= days; d++) c += `<i class="${d === 21 && name === 'Feb' ? 'sel' : ''}">${d}</i>`;
      return `<div class="mo"><div class="mn">${name}</div><div class="grid">${c}</div></div>`;
    };
    return `
  <div class="scr light">
    <div class="sb"><span>10:04</span><span class="isl"></span><span>●●●</span></div>
    <div class="nav cal"><b>2027</b><span>⌕ ＋</span></div>
    <div class="months">${month('Jan', 4, 31)}${month('Feb', 0, 28)}${month('Mar', 0, 31)}${month('Apr', 3, 30)}${month('May', 5, 31)}${month('Jun', 1, 30)}</div>
  </div>`;
  })(),
};
