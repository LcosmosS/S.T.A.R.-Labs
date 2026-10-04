const oscSine = Fn( ( { timer = time } ) => {

	return timer.add( 0.75 ).mul( Math.PI * 2 ).sin().mul( 0.5 ).add( 0.5 );

} );

const value = oscSine( { timer: value } );
