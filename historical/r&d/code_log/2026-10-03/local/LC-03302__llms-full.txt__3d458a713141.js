const contrast = .5;
const brightness = .5;

material.colorNode = texture( map ).mul( contrast ).add( brightness );
