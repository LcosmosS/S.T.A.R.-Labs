const limitPosition = Fn( ( { position } ) => {

	const limit = 10;

	const result = vec3( position );

	If( result.y.greaterThan( limit ), () => {

		result.y = limit;

	} ).ElseIf( result.y.lessThan( limit ), () => {

		result.y = limit;

	} );

	return result;

} );

material.positionNode = limitPosition( { position: positionLocal } );
