"""Run with Blender 5.2+: blender -b source.blend --python export_browser.py
Creates merged browser snapshots from evaluated original geometry/materials.
Original .blend is never saved over. Source animation remains in the .blend.
"""
import bpy
import json
from pathlib import Path
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'frontend/public/twin'
OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene
original=list(scene.objects)
inspection={'frames':[scene.frame_start,scene.frame_end], 'fps':scene.render.fps,
            'collections':[(c.name,len(c.objects)) for c in bpy.data.collections],
            'markers':[(m.name,m.frame) for m in scene.timeline_markers], 'snapshots':{}}
# Keep source keyframed visual states; normal uses frame 1 with obstruction car excluded.
for mode,frame in [('normal',1),('blocked',190),('assistance',285),('resolved',468)]:
    scene.frame_set(frame)
    deps=bpy.context.evaluated_depsgraph_get()
    verts=[];faces=[];mat_ids=[];smooth=[];materials=[];lookup={};included=[]
    for obj in original:
        if obj.type not in {'MESH','FONT','CURVE'} or obj.hide_render:continue
        if any(c.name.startswith(('08_','09_')) for c in obj.users_collection):continue
        if mode=='normal' and any(c.name.startswith(('04_','05_')) for c in obj.users_collection):continue
        # Animated visibility in this source is often implemented as tiny scale.
        evaluated=obj.evaluated_get(deps)
        if max(abs(v) for v in evaluated.matrix_world.to_scale())<.001:continue
        try:mesh=evaluated.to_mesh()
        except RuntimeError:continue
        if mesh is None:continue
        offset=len(verts)
        verts.extend(tuple(evaluated.matrix_world@v.co) for v in mesh.vertices)
        local=[]
        for mat in mesh.materials:
            key=mat.name if mat else 'default'
            if key not in lookup:
                lookup[key]=len(materials);materials.append(mat or bpy.data.materials.new('default'))
            local.append(lookup[key])
        for poly in mesh.polygons:
            faces.append(tuple(offset+i for i in poly.vertices));mat_ids.append(local[poly.material_index] if local else 0);smooth.append(poly.use_smooth)
        included.append(obj.name)
        evaluated.to_mesh_clear()
    mesh=bpy.data.meshes.new('NaikReady_'+mode);mesh.from_pydata(verts,[],faces);mesh.update()
    merged=bpy.data.objects.new('Original Blender environment — '+mode,mesh);scene.collection.objects.link(merged)
    for mat in materials:mesh.materials.append(mat)
    for poly,mid,sm in zip(mesh.polygons,mat_ids,smooth):poly.material_index=mid;poly.use_smooth=sm
    bpy.ops.object.select_all(action='DESELECT');merged.select_set(True);bpy.context.view_layer.objects.active=merged
    bpy.ops.export_scene.gltf(filepath=str(OUT/(mode+'.glb')),export_format='GLB',use_selection=True,export_animations=False,export_cameras=False,export_lights=False,export_apply=True)
    inspection['snapshots'][mode]={'frame':frame,'objects_evaluated':len(included),'vertices':len(verts),'polygons':len(faces),'materials':len(materials),'size_bytes':(OUT/(mode+'.glb')).stat().st_size}
    bpy.data.objects.remove(merged,do_unlink=True);bpy.data.meshes.remove(mesh)
(ROOT/'digital-twin/EXPORT_REPORT.json').write_text(json.dumps(inspection,indent=2))
print('BROWSER_EXPORT_COMPLETE',json.dumps(inspection['snapshots']))
