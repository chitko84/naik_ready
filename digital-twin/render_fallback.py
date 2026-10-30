import bpy
import sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.use_compositing=False
scene.render.resolution_x=960;scene.render.resolution_y=600;scene.render.resolution_percentage=100
scene.render.threads_mode='FIXED';scene.render.threads=8
for c in bpy.data.collections:
 if c.name.startswith('09_'):c.hide_render=True
camera_data=bpy.data.cameras.new('Browser fallback camera');cam=bpy.data.objects.new('Browser fallback camera',camera_data);scene.collection.objects.link(cam)
cam.location=(20,-18,10);cam.rotation_euler=(Vector((6,0,1.3))-cam.location).to_track_quat('-Z','Y').to_euler();camera_data.lens=48
scene.timeline_markers.clear()
world=bpy.data.worlds.new('Browser daylight');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.6,.78,1,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65;scene.world=world
sun_data=bpy.data.lights.new('Browser sun','SUN');sun_data.energy=2.4;sun_data.angle=.25;sun=bpy.data.objects.new('Browser sun',sun_data);scene.collection.objects.link(sun);sun.rotation_euler=(.45,-.4,-.5)
for o in bpy.data.objects:
 if o.type=='LIGHT' and o!=sun:o.hide_render=True
original_hidden={o:o.hide_render for o in bpy.data.objects}
for mode,frame in ([('normal',40)] if '--normal-only' in sys.argv else [('normal',40),('blocked',190),('assistance',285),('resolved',468)]):
 scene.frame_set(frame);scene.camera=cam;scene.view_settings.exposure=0
 for o in bpy.data.objects:o.hide_render=original_hidden.get(o,False)
 if mode=='normal':
  for c in bpy.data.collections:
   if c.name.startswith(('04_','05_')):
    for o in c.objects:o.hide_render=True
 scene.render.filepath=str(ROOT/'frontend/public/twin'/f'{mode}.jpg');scene.render.image_settings.file_format='JPEG';scene.render.image_settings.quality=88
 bpy.ops.render.render(write_still=True)
