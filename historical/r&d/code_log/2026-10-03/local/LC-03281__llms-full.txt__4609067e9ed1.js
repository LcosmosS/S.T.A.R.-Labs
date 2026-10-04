const col = Fn( ( { r, g, b } ) => {

	return vec3( r, g, b );

} );


// Any of the options below will return a green color.

material.colorNode = col( 0, 1, 0 ); // option 1
material.colorNode = col( { r: 0, g: 1, b: 0 } ); // option 2
