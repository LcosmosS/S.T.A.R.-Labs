import { Fn, instancedArray, instanceIndex, deltaTime } from 'three/tsl';

const count = 1000;
const positionArray = instancedArray( count, 'vec3' );

// create a compute function

const computeShader = Fn( () => {

	const position = positionArray.element( instanceIndex );

	position.x.addAssign( deltaTime );

} )().compute( count );

//

renderer.compute( computeShader );
