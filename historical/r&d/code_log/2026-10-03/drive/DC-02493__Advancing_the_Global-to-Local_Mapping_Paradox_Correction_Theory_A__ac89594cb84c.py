def spawn_nodes(nodes):
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_level().get_world()
    node_bp_class = unreal.load_asset('/Game/Node_BP.Node_BP_C')  # Update path
    for node in nodes:
        location = unreal.Vector(node['log_delta'] * 100, node['log_cond'] * 100, node['rank'] * 100)
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(node_bp_class, location)
        actor.set_actor_scale3d(unreal.Vector(node['volume'] * 0.1, node['volume'] * 0.1, node['volume'] * 0.1))
                        *         # Set material color based on rank
