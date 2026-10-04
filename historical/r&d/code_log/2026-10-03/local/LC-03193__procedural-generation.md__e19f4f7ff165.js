  import { createNoise2D } from 'simplex-noise';
  const noise2D = createNoise2D(mulberry32(12345)); // returns ~[-1, 1]
  const v = noise2D(x * 0.01, y * 0.01);            // scale coords = "frequency"
