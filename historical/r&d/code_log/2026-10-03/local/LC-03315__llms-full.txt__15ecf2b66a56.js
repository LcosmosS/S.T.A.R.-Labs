import { fog, rangeFogFactor, densityFogFactor, color } from 'three/tsl';

// Linear fog (starts at 10 units, fully opaque at 100 units)
scene.fogNode = fog( color( 0x000000 ), rangeFogFactor( 10, 100 ) );

// Exponential fog (density-based)
scene.fogNode = fog( color( 0xcccccc ), densityFogFactor( 0.02 ) );
