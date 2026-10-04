// Range values node example

const randomColor = range( new THREE.Color( 0x000000 ), new THREE.Color( 0xFFFFFF ) );

material.colorNode = randomColor;

//...

const mesh = new THREE.InstancedMesh( geometry, material, count );
