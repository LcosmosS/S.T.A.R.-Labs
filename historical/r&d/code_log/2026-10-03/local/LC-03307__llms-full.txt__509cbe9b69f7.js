// Use 8-bit format for encoded normals, default is 16-bit
const normalTexture = scenePass.getTexture( 'normal' );
normalTexture.type = THREE.UnsignedByteType;
