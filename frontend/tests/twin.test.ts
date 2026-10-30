import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {Box3,Mesh} from 'three';
for(const mode of ['normal','blocked','assistance','resolved'])test(`original Blender ${mode} GLB parses with finite geometry and materials`,async()=>{const bytes=await readFile(new URL(`../public/twin/${mode}.glb`,import.meta.url));const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');let meshes=0;gltf.scene.traverse(o=>{if(o instanceof Mesh){meshes++;assert.ok(o.geometry.attributes.position.count>0);assert.ok(o.material)}});assert.ok(meshes>40);const box=new Box3().setFromObject(gltf.scene);assert.ok(!box.isEmpty());assert.ok([...box.min.toArray(),...box.max.toArray()].every(Number.isFinite));gltf.scene.traverse(o=>{if(o instanceof Mesh){o.geometry.dispose();const ms=Array.isArray(o.material)?o.material:[o.material];ms.forEach(m=>m.dispose())}})});
