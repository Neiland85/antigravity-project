document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("godel-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  function resize() {
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
  }

  window.addEventListener("resize", resize);
  resize();

  const equations = [
    "G(x) = ¬Provable(x)",
    "∀P: Consis(T) → ¬Prov(T ⊢ P ∧ ¬P)",
    "∃φ: True(φ) ∧ ¬Prov_T(φ)",
    "Idem(f): f(f(s)) = f(s)",
    "∂S/∂t ≥ 0",
    "¬(Completo ∧ Consistente)"
  ];

  const particles = [];

  for (let i = 0; i < equations.length; i++) {
    particles.push({
      text: equations[i],
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      z: Math.random() * 1.5 + 0.5,   // “profundidad”
      angle: Math.random() * Math.PI * 2,
      speed: (Math.random() * 0.4 + 0.2) * (Math.random() < 0.5 ? 1 : -1),
      drift: Math.random() * 0.4 + 0.1
    });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Fondo ligero “espacial”
    const gradient = ctx.createRadialGradient(
      canvas.width / 2,
      canvas.height / 2,
      10,
      canvas.width / 2,
      canvas.height / 2,
      Math.max(canvas.width, canvas.height)
    );
    gradient.addColorStop(0, "rgba(0, 255, 150, 0.08)");
    gradient.addColorStop(1, "rgba(0, 0, 0, 1)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {
      p.y -= p.drift * p.z;          // subir (gravedad negativa)
      p.angle += 0.01 * p.speed;     // rotación

      // reaparecer por abajo
      if (p.y < -20) {
        p.y = canvas.height + 20;
        p.x = Math.random() * canvas.width;
        p.z = Math.random() * 1.5 + 0.5;
      }

      const scale = p.z;
      const alpha = 0.3 + 0.5 * scale;

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.angle);
      ctx.scale(scale, scale);
      ctx.globalAlpha = alpha;

      ctx.fillStyle = "#00ff99";
      ctx.font = "14px monospace";
      ctx.textAlign = "center";
      ctx.fillText(p.text, 0, 0);

      ctx.restore();
    });

    requestAnimationFrame(draw);
  }

  draw();
});
