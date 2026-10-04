const uvScaled = uv().mul( 10 ).toVar();

material.colorNode = texture( map, uvScaled );
