# Copyright (C) 2023 jackk25

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
import os
import bmesh
import json
import math
from mathutils import Vector

if "bpy" in locals():
    import importlib
    if "utils" in locals():
        importlib.reload(utils)

from . import utils

def make_base_pillar(context, BASE_PILLAR_SIZE, PILLAR_VERTICAL_SCALE):
    bpy.ops.mesh.primitive_cube_add(
        size=BASE_PILLAR_SIZE, 
        location=Vector((0,0, -PILLAR_VERTICAL_SCALE)), 
        scale=Vector((1, 1, PILLAR_VERTICAL_SCALE))
    )

    # Changing the pillar origin
    old_cursor_position = context.scene.cursor.location
    context.scene.cursor.location = Vector((0, 0, 0))
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    context.scene.cursor.location = old_cursor_position

    original_pillar = context.object

    # Locking the object position
    original_pillar.lock_location[0] = True
    original_pillar.lock_location[1] = True

    fix_uvs(original_pillar.data)

    return original_pillar

def make_stairs(stair_height, stair_rotation):
    current_file_dir = os.path.dirname(__file__)
    obj_filepath = os.path.join(current_file_dir, "resources", "stairs.obj")

    if not os.path.exists(obj_filepath):
        print(f"Cannot find {obj_filepath}")
        return None
    
    old_objects = set(bpy.data.objects)


    try:
        bpy.ops.wm.obj_import(filepath=obj_filepath)
    except AttributeError:
        bpy.ops.import_scene.obj(filepath=obj_filepath)

    new_objects = set(bpy.data.objects) - old_objects
    if not new_objects:
        return None

    stair_obj = list(new_objects)[0]
    stair_obj.name = "Imported_Stairs"

    stair_obj.rotation_euler[2] = math.radians(stair_rotation)

    stair_obj.scale[1] = stair_height / 2

    return stair_obj

def calculate_stairs(height_map, x, y, first_stair_rotation):
    stairs = [1, 0, 0] # Height, Rotation, Amount of stairs

    if x > 0 and first_stair_rotation != 3:
        if 0 < (height_map[x-1][y] - height_map[x][y]) <= 2:
            stairs[0] = height_map[x-1][y] - height_map[x][y]
            stairs[1] = 3
            stairs[2] += 1

    if x < 15 and first_stair_rotation != 1:
        if 0 < (height_map[x+1][y] - height_map[x][y]) <= 2:
            stairs[0] = height_map[x+1][y] - height_map[x][y]
            stairs[1] = 1
            stairs[2] += 1


    if y > 0 and first_stair_rotation != 0:
        if 0 < (height_map[x][y-1] - height_map[x][y]) <= 2:
            stairs[0] = height_map[x][y-1] - height_map[x][y]
            stairs[1] = 0
            stairs[2] += 1


    if y < 15 and first_stair_rotation != 2:
        if 0 < (height_map[x][y+1] - height_map[x][y]) <= 2:
            stairs[0] = height_map[x][y+1] - height_map[x][y]
            stairs[1] = 2
            stairs[2] += 1


    return stairs

def make_jumppad():
    current_file_dir = os.path.dirname(__file__)
    blend_filepath = os.path.join(current_file_dir, "resources", "jump_pad.blend")

    if not os.path.exists(blend_filepath):
        print(f"Cannot find {blend_filepath}")
        return None

    object_name = "jumppad" 
    
    directory = blend_filepath + "/Object/"
    old_objects = set(bpy.data.objects)

    try:
        bpy.ops.wm.append(
            filepath=blend_filepath + "/Object/" + object_name, 
            directory=directory, 
            filename=object_name
        )
    except Exception as e:
        print(f"Failed to append jumppad: {e}")
        return None

    new_objects = set(bpy.data.objects) - old_objects
    if not new_objects:
        return None

    # The targeted filter to ensure we get the pad, not the orphaned particle planes
    jump_obj = None
    for obj in new_objects:
        if obj.name.startswith(object_name):
            jump_obj = obj
            break
            
    if not jump_obj:
        jump_obj = list(new_objects)[0]

    jump_obj.name = "Imported_JumpPad"

    return jump_obj

def build_grid(context, height_map, prefab_map, name):
    PILLAR_VERTICAL_SCALE = 10
    BASE_PILLAR_SIZE = 2

    # Create the collection for our pillars, and register it as a pattern
    collection = bpy.data.collections.new(name)
    collection.is_pattern = True
    context.collection.children.link(collection)

    original_pillar = make_base_pillar(context, BASE_PILLAR_SIZE, PILLAR_VERTICAL_SCALE)

    for x, row in enumerate(height_map):
        position_offset = Vector((x * BASE_PILLAR_SIZE, 0, 0))
        for y, height in enumerate(row):
            position_offset.y = y * BASE_PILLAR_SIZE
            position_offset.z = height
            prefab = prefab_map[x][y]

            pillar_copy = original_pillar.copy()

            pillar_copy.location += position_offset
            collection.objects.link(pillar_copy)
            
            pillar_copy.is_pillar = True
            pillar_copy.prefab_type = str(prefab)

            if str(prefab) == "s":
                stairs = calculate_stairs(height_map, x, y, 5)
                if stairs[2] > 0:
                    
                    stair_obj = make_stairs(stairs[0],stairs[1]*90)
                    stair_obj.location = position_offset.copy()

                    stair_obj.location.z = height

                    stair_obj.is_pillar = False
                    stair_obj.is_stair = True

                    collection.objects.link(stair_obj)

                    if stair_obj.name in context.collection.objects:
                        context.collection.objects.unlink(stair_obj)

                    if stairs [2] > 1:
                        stairs = calculate_stairs(height_map, x, y, stairs[1])

                        stair_obj = make_stairs(stairs[0],stairs[1]*90)
                        stair_obj.location = position_offset.copy()

                        stair_obj.location.z = height

                        stair_obj.is_pillar = False
                        stair_obj.is_stair = True

                        collection.objects.link(stair_obj)

                        if stair_obj.name in context.collection.objects:
                            context.collection.objects.unlink(stair_obj)

            if str(prefab) == "J":
                # By calling append directly inside the loop, Blender handles all the 
                # material duplication and node target isolation automatically.
                jump_obj = make_jumppad()
                
                if jump_obj:
                    jump_obj.location = position_offset.copy()
                    jump_obj.location.z = height

                    jump_obj.is_pillar = False
                    jump_obj.is_stair = False
                    jump_obj.is_jumppad = True 

                    collection.objects.link(jump_obj)

                    if jump_obj.name in context.collection.objects:
                        context.collection.objects.unlink(jump_obj)

    bpy.data.objects.remove(original_pillar)

    return {'FINISHED'}

def parse_height_map(height_map):
    parsed_map = []
    for row in height_map:
        row_storage = []
        block_storage = ""
        in_block = False
        for char in row:
            if char == '(':
                in_block = True
                continue
            if char == ')':
                in_block = False
                row_storage.append(int(block_storage))
                block_storage = ""
                continue
            if in_block == False:
                row_storage.append(int(char))
            if in_block:
                block_storage += char
        parsed_map.append(row_storage)
    return parsed_map

def parse_object_map(object_map):
    parsed_map = []
    for row in object_map:
        row_storage = []
        for col in row:
            row_storage.append(col)
        parsed_map.append(row_storage)
    return parsed_map

def fix_uvs(mesh_data):
    bm = bmesh.new()
    bm.from_mesh(mesh_data)

    uv_layer = bm.loops.layers.uv.active

    loaded_uvs = []

    current_file_dir = os.path.dirname(__file__)
    uv_filepath = os.path.join(current_file_dir, "resources", "cube.json")

    with open(uv_filepath,'r') as f:
        loaded_uvs = json.load(f)
    
    for index, face in enumerate(bm.faces):
        face_uvs = loaded_uvs[index]
        for loop_index, loop in enumerate(face.loops):
            uv = loop[uv_layer].uv
            loop_uv = face_uvs[loop_index]
            uv.x = loop_uv[0]
            uv.y = loop_uv[1]
    
    bm.to_mesh(mesh_data)
    mesh_data.update()
    bm.free()

def load(context, filepath=""):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()

        height_map = data[:16]
        object_map = data[17:]

        height_map = parse_height_map(height_map)
        object_map = parse_object_map(object_map)

        name = os.path.basename(filepath)

        return build_grid(context, height_map, object_map, name)