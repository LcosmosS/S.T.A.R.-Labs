function radialDeadzone(x, y, dz = 0.15) {
  const m = Math.hypot(x, y);
  if (m < dz) return { x: 0, y: 0 };
  const scale = ((m - dz) / (1 - dz)) / m; // re-normalize
  return { x: x * scale, y: y * scale };
}
