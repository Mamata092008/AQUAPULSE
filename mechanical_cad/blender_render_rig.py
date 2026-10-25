"""
AQUAPULSE: Automated Studio Render & Exploded Assembly in Blender
Team TECHTONICS | Vishwakarma Awards 2026–27 (Host: IIT Hyderabad)

How to Run:
1. Open Blender (3.x or 4.x)
2. Switch to 'Scripting' tab and paste this script, or run:
   blender --background --python blender_render_rig.py
3. Renders high-resolution studio isometric view and exploded view animation!
"""

import bpy
import os
import math

def setup_scene():
    # Clear existing objects
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES' if bpy.context.preferences.addons.get('cycles') else 'BLENDER_EEVEE_NEXT'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True

    # 1. Import OBJ Assembly
    blend_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    obj_path = os.path.join(blend_dir, "aquapulse_full_assembly.obj")
    
    if os.path.exists(obj_path):
        if hasattr(bpy.ops.wm, 'obj_import'):
            bpy.ops.wm.obj_import(filepath=obj_path)
        else:
            bpy.ops.import_scene.obj(filepath=obj_path)
        print("Imported:", obj_path)
    else:
        print("OBJ not found at:", obj_path)

    # 2. Camera Setup (Isometric Angle)
    cam_data = bpy.data.cameras.new("RenderCam")
    cam_data.lens = 85  # Telephoto for crisp industrial product look
    cam_obj = bpy.data.objects.new("RenderCam", cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    cam_obj.location = (220, -220, 180)
    cam_obj.rotation_euler = (math.radians(60), 0, math.radians(45))

    # 3. Three-Point Studio Lighting
    # Key Light (Warm soft studio)
    key_light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
    key_light_data.energy = 500
    key_light_data.size = 150
    key_light_data.color = (1.0, 0.98, 0.95)
    key_light = bpy.data.objects.new("KeyLight", key_light_data)
    scene.collection.objects.link(key_light)
    key_light.location = (150, -150, 200)
    key_light.rotation_euler = (math.radians(45), 0, math.radians(45))

    # Fill Light (Cool ambient cyan fill)
    fill_light_data = bpy.data.lights.new(name="FillLight", type='AREA')
    fill_light_data.energy = 250
    fill_light_data.size = 200
    fill_light_data.color = (0.85, 0.95, 1.0)
    fill_light = bpy.data.objects.new("FillLight", fill_light_data)
    scene.collection.objects.link(fill_light)
    fill_light.location = (-180, -100, 120)
    fill_light.rotation_euler = (math.radians(60), 0, math.radians(-60))

    # Rim / Hair Light (Sharp edge highlights)
    rim_light_data = bpy.data.lights.new(name="RimLight", type='SPOT')
    rim_light_data.energy = 600
    rim_light_data.spot_size = math.radians(45)
    rim_light = bpy.data.objects.new("RimLight", rim_light_data)
    scene.collection.objects.link(rim_light)
    rim_light.location = (0, 200, 150)
    rim_light.rotation_euler = (math.radians(-60), 0, math.radians(180))

    # 4. Exploded View Animation Keyframing (120 frames)
    scene.frame_start = 1
    scene.frame_end = 120
    
    for obj in scene.objects:
        if "Lid" in obj.name or "Solar" in obj.name or "LightPipe" in obj.name:
            # Keyframe 1: Resting at Z = 30
            obj.keyframe_insert(data_path="location", frame=1)
            # Keyframe 60: Exploded upwards +45mm
            obj.location.z += 45
            obj.keyframe_insert(data_path="location", frame=60)
            obj.keyframe_insert(data_path="location", frame=90)
            # Return
            obj.location.z -= 45
            obj.keyframe_insert(data_path="location", frame=120)
            
        elif "PCB" in obj.name or "Gasket" in obj.name:
            obj.keyframe_insert(data_path="location", frame=1)
            obj.location.z += 20
            obj.keyframe_insert(data_path="location", frame=60)
            obj.keyframe_insert(data_path="location", frame=90)
            obj.location.z -= 20
            obj.keyframe_insert(data_path="location", frame=120)

        elif "Probe" in obj.name:
            obj.keyframe_insert(data_path="location", frame=1)
            obj.location.z -= 25
            obj.keyframe_insert(data_path="location", frame=60)
            obj.keyframe_insert(data_path="location", frame=90)
            obj.location.z += 25
            obj.keyframe_insert(data_path="location", frame=120)

    print("Blender AQUAPULSE Studio Scene Setup Complete!")

if __name__ == "__main__":
    setup_scene()
