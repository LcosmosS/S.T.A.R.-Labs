import { texture, saturation, hue, posterize } from 'three/tsl';

// Increase saturation
material.colorNode = saturation( texture( map ), 1.5 );

// Rotate hue by 90 degrees
material.colorNode = hue( texture( map ), Math.PI / 2 );

// Posterize to 4 color levels
material.colorNode = posterize( texture( map ), 4 );
