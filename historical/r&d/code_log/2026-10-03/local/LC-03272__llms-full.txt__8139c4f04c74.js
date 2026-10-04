import * as THREE from 'three';
import { simplexNoise } from 'tsl-textures';

material.colorNode = simplexNoise ( {
	scale: 2,
	balance: 0,
	contrast: 0,
	color: new THREE.Color(16777215),
	background: new THREE.Color(0),
	seed: 0
} );

