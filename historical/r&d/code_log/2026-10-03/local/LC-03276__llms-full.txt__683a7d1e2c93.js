const posY = uniform( 0 ); // it's possible use uniform( 'float' )

// or using event to be done automatically
// { object } will be the current rendering object
posY.onObjectUpdate( ( { object } ) => object.position.y );

// you can also update manually using the .value property
posY.value = object.position.y;

material.colorNode = posY;
