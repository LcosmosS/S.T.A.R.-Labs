import bpy

# Create a new collection for all labels
if "Labels" not in bpy.data.collections:
    label_collection = bpy.data.collections.new("Labels")
    bpy.context.scene.collection.children.link(label_collection)
else:
    label_collection = bpy.data.collections["Labels"]

# Helper function to add a label
def add_label(name, location, scale=0.008, color=(1, 1, 1)):
    bpy.ops.object.text_add(location=location)
    text_obj = bpy.context.active_object
    text_obj.name = f"Label_{name}"
    text_obj.data.body = name
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    text_obj.scale = (scale, scale, scale)
    
    # Material for white text with emission
    mat = bpy.data.materials.new(name=f"Mat_{name}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 1.0  # Emission Strength
    text_obj.data.materials.append(mat)
    
    # Link to Labels collection
    label_collection.objects.link(text_obj)
    bpy.context.collection.objects.unlink(text_obj)

# ====================== SOLAR SYSTEM LABELS (Sun at origin) ======================
add_label("Sol", (0, 0, 0), scale=0.012, color=(1.0, 0.9, 0.6))   # Sun - golden

add_label("Mercury", (0.387 * 1e-4 * 1e6, 0, 0), scale=0.005)
add_label("Venus",   (0.723 * 1e-4 * 1e6, 0, 0), scale=0.005)
add_label("Earth",   (1.0   * 1e-4 * 1e6, 0, 0), scale=0.006, color=(0.3, 0.7, 1.0))
add_label("Mars",    (1.524 * 1e-4 * 1e6, 0, 0), scale=0.005)
add_label("Jupiter", (5.203 * 1e-4 * 1e6, 0, 0), scale=0.008)
add_label("Saturn",  (9.537 * 1e-4 * 1e6, 0, 0), scale=0.008)
add_label("Uranus",  (19.191* 1e-4 * 1e6, 0, 0), scale=0.007)
add_label("Neptune", (30.069* 1e-4 * 1e6, 0, 0), scale=0.007)

# ====================== FAMOUS OBJECTS ======================
add_label("Betelgeuse",    (0.000197 * 1e6, 0, 0), scale=0.009, color=(1.0, 0.4, 0.2))
add_label("Sirius",        (0.0000086*1e6, 0, 0), scale=0.008, color=(0.8, 0.9, 1.0))
add_label("Andromeda",     (0.778 * 1e6, 0, 0),   scale=0.015, color=(0.6, 0.8, 1.0))
add_label("M87 (Virgo)",   (16.4  * 1e6, 0, 0),   scale=0.018, color=(0.9, 0.3, 1.0))
add_label("Sagittarius A*", (0.008 * 1e6, 0, 0),   scale=0.010, color=(1.0, 0.2, 0.2))
add_label("Orion Nebula",   (0.000414*1e6, 0, 0), scale=0.009, color=(0.4, 1.0, 0.6))
add_label("Virgo Cluster",  (16.5  * 1e6, 0, 0),   scale=0.020, color=(0.7, 0.5, 1.0))

print("✅ All labels added! Check the 'Labels' collection in the Outliner.")