// Shared the same uniform with various materials

const sharedColor = uniform( new THREE.Color() );

materialA.colorNode = sharedColor.div( 2 );
materialB.colorNode = sharedColor.mul( .5 );
materialC.colorNode = sharedColor.add( .5 );
