import { billboarding } from 'three/tsl';

// Default: Horizontal only (like trees) - rotates around Y axis only
material.vertexNode = billboarding();

// Full billboarding (like particles) - faces camera in all directions
material.vertexNode = billboarding( { horizontal: true, vertical: true } );
