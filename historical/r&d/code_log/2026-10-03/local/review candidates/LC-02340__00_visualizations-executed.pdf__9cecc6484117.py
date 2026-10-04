      import bpy
      import math
      import bmesh

      bpy.ops.wm.read_factory_settings(use_empty=True)

      points =   {X.tolist()}

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


                                                        3