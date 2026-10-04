// Access individual buffers as texture nodes
const colorTexture = scenePass.getTextureNode( 'output' );
const normalTexture = scenePass.getTextureNode( 'normal' );
const velocityTexture = scenePass.getTextureNode( 'velocity' );

// Depth is always available, even without MRT
const depthTexture = scenePass.getTextureNode( 'depth' );
