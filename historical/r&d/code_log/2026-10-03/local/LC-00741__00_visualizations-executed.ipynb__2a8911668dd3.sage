blender_script = f"""
import bpy
import math
import bmesh

bpy.ops.wm.read_factory_settings(use_empty=True)

points = {X.tolist()}

mesh = bpy.data.meshes.new("PointCloud")
obj = bpy.data.objects.new("PointCloud", mesh)
bpy.context.collection.objects.link(obj)

bm = bmesh.new()
for p in points:
    bm.verts.new(p)
bm.to_mesh(mesh)
bm.free()

cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
bpy.context.collection.objects.link(cam)
cam.location = (3, -4, 2)
cam.rotation_euler = (math.radians(70), 0, math.radians(45))
bpy.context.scene.camera = cam

light = bpy.data.objects.new("Light", bpy.data.lights.new("Light", type='SUN'))
bpy.context.collection.objects.link(light)
light.location = (5, -5, 5)

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.filepath = "figures/acsc_blender.png"
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

bpy.ops.render.render(write_still=True)
"""

blender_render(blender_script, "figures/acsc_blender.png")
