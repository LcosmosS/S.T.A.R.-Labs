import { pass, mrt, output, emissive } from 'three/tsl';

const scenePass = pass( scene, camera );

// Setup MRT
scenePass.setMRT( mrt( {
	output: output,
	emissive: emissive
} ) );

const outputNode = scenePass.getTextureNode( 'output' );
const emissiveNode = scenePass.getTextureNode( 'emissive' );
