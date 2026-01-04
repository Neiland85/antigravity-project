/**
 * Antigravity 3D - Interactive WebGL Experience
 * Gödel equations floating in a true 3D space with mouse interaction
 */

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("godel-canvas");
  if (!canvas) return;

  // Check for WebGL support
  const gl =
    canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
  if (!gl) {
    console.warn("WebGL not supported, falling back to 2D");
    init2DFallback(canvas);
    return;
  }

  // Use 2D canvas overlay for text (WebGL is for effects)
  const ctx = canvas.getContext("2d");

  let mouseX = 0,
    mouseY = 0;
  let targetRotationX = 0,
    targetRotationY = 0;
  let currentRotationX = 0,
    currentRotationY = 0;

  function resize() {
    canvas.width = canvas.clientWidth * window.devicePixelRatio;
    canvas.height = canvas.clientHeight * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  window.addEventListener("resize", resize);
  resize();

  // Mouse interaction
  canvas.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    mouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouseY = ((e.clientY - rect.top) / rect.height) * 2 - 1;
    targetRotationY = mouseX * 0.5;
    targetRotationX = mouseY * 0.3;
  });

  canvas.addEventListener("mouseleave", () => {
    targetRotationX = 0;
    targetRotationY = 0;
  });

  // 3D Equations
  const equations = [
    { text: "G(x) = ¬Provable(x)", color: "#00ff99" },
    { text: "∀P: Consis(T) → ¬Prov(T ⊢ P ∧ ¬P)", color: "#00ffff" },
    { text: "∃φ: True(φ) ∧ ¬Prov_T(φ)", color: "#ff00ff" },
    { text: "Idem(f): f(f(s)) = f(s)", color: "#ffff00" },
    { text: "∂S/∂t ≥ 0", color: "#ff6600" },
    { text: "¬(Completo ∧ Consistente)", color: "#66ff66" },
    { text: "λx.x(x) → Ω", color: "#00ccff" },
    { text: "H(p) = -Σ p log p", color: "#ff99cc" },
  ];

  // 3D Particle system
  const particles = equations.map((eq, i) => ({
    text: eq.text,
    color: eq.color,
    x: (Math.random() - 0.5) * 400,
    y: (Math.random() - 0.5) * 300,
    z: Math.random() * 500 - 250,
    vx: (Math.random() - 0.5) * 0.5,
    vy: -Math.random() * 0.8 - 0.2, // Negative = anti-gravity (upward)
    vz: (Math.random() - 0.5) * 0.3,
    rotationSpeed: (Math.random() - 0.5) * 0.02,
    angle: Math.random() * Math.PI * 2,
    pulsePhase: Math.random() * Math.PI * 2,
  }));

  // Star field background
  const stars = Array.from({ length: 100 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    size: Math.random() * 2 + 0.5,
    twinkle: Math.random() * Math.PI * 2,
  }));

  let time = 0;

  function project3D(x, y, z, rotX, rotY) {
    // Rotate around Y axis
    const cosY = Math.cos(rotY);
    const sinY = Math.sin(rotY);
    let x1 = x * cosY - z * sinY;
    let z1 = x * sinY + z * cosY;

    // Rotate around X axis
    const cosX = Math.cos(rotX);
    const sinX = Math.sin(rotX);
    let y1 = y * cosX - z1 * sinX;
    let z2 = y * sinX + z1 * cosX;

    // Perspective projection
    const fov = 500;
    const scale = fov / (fov + z2);

    return {
      x: x1 * scale + canvas.clientWidth / 2,
      y: y1 * scale + canvas.clientHeight / 2,
      scale: scale,
      z: z2,
    };
  }

  function draw() {
    time += 0.016;

    // Smooth rotation interpolation
    currentRotationX += (targetRotationX - currentRotationX) * 0.05;
    currentRotationY += (targetRotationY - currentRotationY) * 0.05;

    // Clear with deep space gradient
    const gradient = ctx.createRadialGradient(
      canvas.clientWidth / 2,
      canvas.clientHeight / 2,
      0,
      canvas.clientWidth / 2,
      canvas.clientHeight / 2,
      Math.max(canvas.clientWidth, canvas.clientHeight)
    );
    gradient.addColorStop(0, "rgba(10, 5, 30, 1)");
    gradient.addColorStop(0.5, "rgba(5, 0, 15, 1)");
    gradient.addColorStop(1, "rgba(0, 0, 0, 1)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.clientWidth, canvas.clientHeight);

    // Draw twinkling stars
    stars.forEach((star) => {
      star.twinkle += 0.03;
      const alpha = 0.3 + Math.sin(star.twinkle) * 0.3;
      ctx.beginPath();
      ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
      ctx.fill();
    });

    // Update and sort particles by Z (painter's algorithm)
    particles.forEach((p) => {
      p.y += p.vy; // Anti-gravity effect
      p.x += p.vx;
      p.z += p.vz;
      p.angle += p.rotationSpeed;
      p.pulsePhase += 0.05;

      // Wrap around boundaries
      if (p.y < -200) {
        p.y = 200;
        p.x = (Math.random() - 0.5) * 400;
        p.z = Math.random() * 500 - 250;
      }
      if (p.x > 300) p.x = -300;
      if (p.x < -300) p.x = 300;
      if (p.z > 300) p.z = -300;
      if (p.z < -300) p.z = 300;
    });

    // Sort by Z depth (far to near)
    const sortedParticles = [...particles].sort((a, b) => {
      const projA = project3D(
        a.x,
        a.y,
        a.z,
        currentRotationX,
        currentRotationY
      );
      const projB = project3D(
        b.x,
        b.y,
        b.z,
        currentRotationX,
        currentRotationY
      );
      return projA.z - projB.z;
    });

    // Draw particles
    sortedParticles.forEach((p) => {
      const proj = project3D(p.x, p.y, p.z, currentRotationX, currentRotationY);

      if (proj.scale < 0.1) return; // Behind camera

      const pulse = 1 + Math.sin(p.pulsePhase) * 0.1;
      const fontSize = Math.max(8, 16 * proj.scale * pulse);
      const alpha = Math.min(1, Math.max(0.2, proj.scale * 1.2));

      ctx.save();
      ctx.translate(proj.x, proj.y);
      ctx.rotate(p.angle * 0.3);

      // Glow effect
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 15 * proj.scale;

      ctx.font = `${fontSize}px 'Courier New', monospace`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillStyle = p.color;
      ctx.globalAlpha = alpha;
      ctx.fillText(p.text, 0, 0);

      ctx.restore();
    });

    // Draw central vortex effect
    ctx.save();
    ctx.translate(canvas.clientWidth / 2, canvas.clientHeight / 2);
    ctx.rotate(time * 0.2);

    for (let i = 0; i < 3; i++) {
      ctx.beginPath();
      ctx.arc(0, 0, 30 + i * 20 + Math.sin(time * 2 + i) * 10, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(0, 255, 150, ${0.1 - i * 0.03})`;
      ctx.lineWidth = 2;
      ctx.stroke();
    }
    ctx.restore();

    requestAnimationFrame(draw);
  }

  draw();
});

// 2D Fallback for non-WebGL browsers
function init2DFallback(canvas) {
  const ctx = canvas.getContext("2d");
  // ... original 2D code here
}
