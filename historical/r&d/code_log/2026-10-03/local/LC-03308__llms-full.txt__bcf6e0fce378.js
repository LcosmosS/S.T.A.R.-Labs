if ( showNormals ) {

	renderPipeline.outputNode = prePass;

} else {

	renderPipeline.outputNode = traaPass;

}

renderPipeline.needsUpdate = true;
