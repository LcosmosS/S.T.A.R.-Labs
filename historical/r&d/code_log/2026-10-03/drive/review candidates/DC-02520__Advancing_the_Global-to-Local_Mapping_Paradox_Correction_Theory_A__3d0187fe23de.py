def create_filaments(nodes):
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_level().get_world()
    filament_bp_class = unreal.load_asset('/Game/Filament_BP.Filament_BP_C')
    for i, node1 in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            node2 = nodes[j]
            reg_diff = abs(node1['reg'] - node2['reg'])
            if reg_diff < 5000:
                weight = 1 / (1 + reg_diff / 100)
                if weight > 0.7:
                    start = unreal.Vector(node1['log_delta'] * 100, node1['log_cond'] * 100, node1['rank'] * 100)
                    end = unreal.Vector(node2['log_delta'] * 100, node2['log_cond'] * 100, node2['rank'] * 100)
                    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(filament_bp_class, start)
                           *                     # Set filament properties (e.g., endpoints, thickness)
