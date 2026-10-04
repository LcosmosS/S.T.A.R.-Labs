import { overrideNode, overrideNodes, positionLocal, positionView, vec3 } from 'three/tsl';

// Override a single node through the material context
material.contextNode = overrideNode( positionLocal, () => positionLocal.add( vec3( 1, 0, 0 ) ) );

// Override multiple nodes at once
material.contextNode = overrideNodes( [
	[ positionView, customPositionView ], // You can use a node directly like customPositionView.
	[ positionLocal, ( builder ) => positionLocal.add( vec3( 1, 0, 0 ) ) ]
] );

// Method chaining is also supported
node.overrideNode( positionLocal, () => positionLocal.add( vec3( 1, 0, 0 ) ) );
