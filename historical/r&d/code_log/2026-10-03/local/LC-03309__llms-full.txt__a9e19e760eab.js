import { grayscale, pass } from 'three/tsl';
import { gaussianBlur } from 'three/addons/tsl/display/GaussianBlurNode.js';

// Post-processing
const scenePass = pass( scene, camera );
const output = scenePass.getTextureNode(); // default parameter is 'output'

renderPipeline.outputNode = grayscale( gaussianBlur( output, 4 ) );
