import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();

loader.load(
  'model.glb',
  ( gltf ) => {
    scene.add( gltf.scene );
  },
  ( progress ) => {
    console.log( ( progress.loaded / progress.total * 100 ) + '% loaded' );
  },
  ( error ) => {
    console.error( 'Error loading model:', error );
  }
);
