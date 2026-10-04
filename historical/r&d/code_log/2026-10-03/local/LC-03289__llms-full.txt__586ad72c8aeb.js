// multiplication will be executed in vertex stage
const normalView = vertexStage( modelNormalMatrix.mul( normalLocal ) );

// normalize will be computed in fragment stage while `normalView` is computed on vertex stage
material.colorNode = normalView.normalize();
