import { Fn, If, Discard, uv } from 'three/tsl';

const customFragment = Fn( () => {

	If( uv().x.lessThan( 0.5 ), () => {

		Discard();

	} );

	return vec4( 1, 0, 0, 1 );

} );

material.colorNode = customFragment();
