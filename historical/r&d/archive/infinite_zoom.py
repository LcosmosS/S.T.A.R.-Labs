"""
infinite_zoom.py
----------------
Implements infinite-zoom navigation for Blender using the ACSC
Paradox Correction workflow and Heegner-point stabilization.

This module:
- dynamically rescales the scene
- shifts the origin to maintain precision
- applies paradox correction at each zoom level
"""

import bpy
import mathutils
from .paradox_correction import ParadoxCorrection


class InfiniteZoom:
    """
    Infinite zoom controller for Blender.
    """

    def __init__(self, k_factor=1000.0):
        self.k = k_factor
        self.corrector = ParadoxCorrection(k_factor=k_factor)

    def recenter_origin(self, obj):
        """
        Shift the entire scene so that obj becomes the new origin.
        """
        offset = obj.location.copy()
        for o in bpy.data.objects:
            o.location -= offset

    def zoom_step(self, obj_name, zoom_factor):
        """
        Perform a single zoom step:
        - apply paradox correction
        - recenter origin
        - scale scene
        """
        obj = bpy.data.objects.get(obj_name)
        if not obj:
            return

        # Apply paradox correction to the object
        corrected = self.corrector.paradox_correct(obj.location)
        obj.location = corrected

        # Recenter origin around the object
        self.recenter_origin(obj)

        # Scale the entire scene
        for o in bpy.data.objects:
            o.scale *= zoom_factor

    def infinite_zoom(self, obj_name, steps=10, zoom_factor=0.1):
        """
        Perform multiple zoom steps to simulate infinite zoom.
        """
        for _ in range(steps):
            self.zoom_step(obj_name, zoom_factor)
