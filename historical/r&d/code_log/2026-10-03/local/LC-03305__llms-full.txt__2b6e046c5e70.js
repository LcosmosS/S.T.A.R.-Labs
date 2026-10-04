import { pass, mrt, output, normalView, velocity, packNormalToRGB } from 'three/tsl';

const scenePass = pass( scene, camera );

scenePass.setMRT( mrt( {
	output: output,                          // Final color output
	normal: packNormalToRGB( normalView ),   // View-space normals encoded as colors
	velocity: velocity                       // Motion vectors for temporal effects
} ) );
