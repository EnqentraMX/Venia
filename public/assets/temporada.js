/* Temporada navideña LicLink: activa del 25 nov al 6 ene. Para verla apagada: ?sin-temporada */
(function () {
  var d = new Date(), m = d.getMonth() + 1, dia = d.getDate();
  var on = (m === 11 && dia >= 25) || m === 12 || (m === 1 && dia <= 6);
  if (!on || /[?&]sin-temporada/.test(location.search)) return;
  var html = document.documentElement; html.classList.add("navidad");
  function listo(fn) { if (document.body) fn(); else document.addEventListener("DOMContentLoaded", fn); }
  listo(function () {
    var c = document.createElement("div"); c.className = "nv-cinta"; c.setAttribute("role", "note");
    c.innerHTML = "<span>✦</span> Felices fiestas · En LicLink te acompañamos también en estas fechas <span>✦</span>";
    if (innerWidth < 420) c.innerHTML = "<span>✦</span> Felices fiestas · Te acompañamos en estas fechas <span>✦</span>";
    document.body.insertBefore(c, document.body.firstChild);
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var cv = document.createElement("canvas"); cv.className = "nv-nieve"; cv.setAttribute("aria-hidden", "true");
    document.body.appendChild(cv);
    var x = cv.getContext("2d"), W, H, R = Math.min(devicePixelRatio || 1, 2), P = [];
    function tam() { W = innerWidth; H = innerHeight; cv.width = W * R; cv.height = H * R; x.setTransform(R, 0, 0, R, 0, 0); }
    tam(); addEventListener("resize", tam);
    var n = W < 600 ? 22 : 40;
    for (var i = 0; i < n; i++) P.push({ x: Math.random() * W, y: Math.random() * H, r: 1 + Math.random() * 2.2, v: .25 + Math.random() * .55, f: Math.random() * 6.28, a: .35 + Math.random() * .45, e: Math.random() < .22 });
    function estrella(p) {
      var s = p.r * 2.6; x.beginPath();
      x.moveTo(p.x, p.y - s); x.quadraticCurveTo(p.x, p.y, p.x + s, p.y); x.quadraticCurveTo(p.x, p.y, p.x, p.y + s); x.quadraticCurveTo(p.x, p.y, p.x - s, p.y); x.quadraticCurveTo(p.x, p.y, p.x, p.y - s); x.fill();
    }
    function cuadro() {
      if (!document.hidden) {
        x.clearRect(0, 0, W, H);
        for (var i = 0; i < P.length; i++) {
          var p = P[i]; p.y += p.v; p.f += .012; p.x += Math.sin(p.f) * .35;
          if (p.y > H + 10) { p.y = -10; p.x = Math.random() * W; }
          x.globalAlpha = p.a * (p.e ? (.55 + .45 * Math.sin(p.f * 3)) : 1);
          x.fillStyle = p.e ? "#ffe39a" : "#e6c77e";
          x.shadowColor = "rgba(255,215,120,.9)"; x.shadowBlur = p.e ? 10 : 6;
          if (p.e) estrella(p); else { x.beginPath(); x.arc(p.x, p.y, p.r, 0, 6.283); x.fill(); }
        }
      }
      requestAnimationFrame(cuadro);
    }
    requestAnimationFrame(cuadro);
  });
})();
