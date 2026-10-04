import * as THREE from 'three/webgpu';
import { pass } from 'three/tsl';

// Create the render pipeline
const renderPipeline = new THREE.RenderPipeline( renderer );

// Create a scene pass
const scenePass = pass( scene, camera );

// Set the output
renderPipeline.outputNode = scenePass;

// In the animation loop
function animate() {

	renderPipeline.render();

}
