import bpy
import re
import os
from types import SimpleNamespace
from math import radians, degrees

from .enum_values import *
from .preferences import *

# -----------------------------------------------------------------------------
# utility functions

def mu_ui_col_split(layout, factor=0.02):
    spl = layout.split(factor=factor)
    spl.column()
    spl2 = spl.column().split(factor=1-factor/(1-factor))
    return spl2.column()

def mu_assign_material_slots(object, material_list):
    """Given an object and a list of material names removes all material slots from the object
       adds new ones for each material in the material list, adds the materials to the slots as well."""

    scene = bpy.context.scene
    active_object = bpy.context.active_object
    bpy.context.view_layer.objects.active = object

    # Remove all current material slots
    #  By looping until the material slots list is empty
    while len(object.material_slots) != 0:
        bpy.ops.object.material_slot_remove()

    # re-add them and assign material
    i = 0
    for mat in material_list:
        material = bpy.data.materials[mat]
        object.data.materials.append(material)
        i += 1

    # restore active object:
    bpy.context.view_layer.objects.active = active_object

def mu_assign_to_data(object, material, index, edit_mode, all = True):
    """Assign the material to the object data (polygons/splines)"""

    if object.type == 'MESH':
        # now assign the material to the mesh
        mesh = object.data
        if all:
            for poly in mesh.polygons:
                poly.material_index = index
        else:
            for poly in mesh.polygons:
                if poly.select:
                    poly.material_index = index

        mesh.update()

    elif object.type in {'CURVE', 'SURFACE', 'TEXT'}:
        bpy.ops.object.mode_set(mode = 'EDIT')    # This only works in Edit mode

        # If operator was run in Object mode
        if not edit_mode:
            # Select everything in Edit mode
            bpy.ops.curve.select_all(action = 'SELECT')

        bpy.ops.object.material_slot_assign()   # Assign material of the current slot to selection

        if not edit_mode:
            bpy.ops.object.mode_set(mode = 'OBJECT')



def mu_new_material_name(material):
    """Generate a new material name, if it exists: append a suitable suffix to it"""

    for mat in bpy.data.materials:
        name = mat.name

        if (name == material):
            try:
                base, suffix = name.rsplit('.', 1)

                # trigger the exception
                num = int(suffix, 10)
                material = base + "." + '%03d' % (num + 1)
            except ValueError:
                material = material + ".001"

    return material


def mu_clear_materials(object):
    """Clear out all the material slots for the current object"""

    for mat in object.material_slots:
        bpy.ops.object.material_slot_remove()


def mu_assign_material(self, material_name = "Default", override_type = 'APPEND_MATERIAL', link_override = 'KEEP'):
    """Assign the defined material to selected polygons/objects"""

    # get active object so we can restore it later
    active_object = bpy.context.active_object

    edit_mode = False
    all_polygons = True
    if (not active_object is None) and active_object.mode == 'EDIT':
        edit_mode = True
        all_polygons = False
        bpy.ops.object.mode_set()

    # check if material exists, if it doesn't then create it
    found = False
    for material in bpy.data.materials:
        if material.name == material_name:
            target = material
            found = True
            break

    if not found:
        target = bpy.data.materials.new(mu_new_material_name(material_name))
        target.use_nodes = True         # When do we not want nodes today?


    index = 0
    objects = bpy.context.selected_editable_objects

    for obj in objects:
        # Apparently selected_editable_objects includes objects as cameras etc
        if not obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META', 'GPENCIL'}:
            continue

        if obj.type == 'GPENCIL':
            if not target.is_grease_pencil:
                continue
        elif target.is_grease_pencil:
            continue

        # set the active object to our object
        scene = bpy.context.scene
        bpy.context.view_layer.objects.active = obj

        if link_override == 'KEEP':
            if len(obj.material_slots) > 0:
                link = obj.material_slots[0].link
            else:
                link = 'DATA'
        else:
            link = link_override

        # If we should override all current material slots
        if override_type == 'OVERRIDE_ALL' or obj.type == 'META':

            # If there's more than one slot, Clear out all the material slots
            if len(obj.material_slots) > 1:
                mu_clear_materials(obj)

            # If there's no slots left/never was one, add a slot
            if len(obj.material_slots) == 0:
                bpy.ops.object.material_slot_add()

            # Assign the material to that slot
            obj.material_slots[0].link = link
            obj.material_slots[0].material = target

            if obj.type == 'META':
                self.report({'INFO'}, "Meta balls only support one material, all other materials overriden!")

        # If we should override each material slot
        elif override_type == 'OVERRIDE_SLOTS':
            i = 0
            # go through each slot
            for material in obj.material_slots:
                # assign the target material to current slot
                if not link_override == 'KEEP':
                    obj.material_slots[i].link = link
                obj.material_slots[i].material = target
                i += 1

        elif override_type == 'OVERRIDE_CURRENT':
            active_slot = obj.active_material_index

            if len(obj.material_slots) == 0:
                self.report({'INFO'}, 'No material slots found! A material slot was added!')
                bpy.ops.object.material_slot_add()

            obj.material_slots[active_slot].material = target

        # if we should keep the material slots and just append the selected material (if not already assigned)
        elif override_type == 'APPEND_MATERIAL':
            found = False
            i = 0
            material_slots = obj.material_slots

            if (obj.data.users > 1) and (len(material_slots) >= 1 and material_slots[0].link == 'OBJECT'):
                self.report({'WARNING'}, 'Append material is not recommended for linked duplicates! ' +
                                            'Unwanted results might happen!')

            # check material slots for material_name materia
            for material in material_slots:
                if material.name == material_name:
                    found = True
                    index = i

                    # make slot active
                    obj.active_material_index = i
                    break
                i += 1

            if not found:
                # In Edit mode, or if there's not a slot, append the assigned material
                #  If we're overriding, there's currently no materials at all, so after this there will be 1
                #  If not, this adds another slot with the assigned material

                index = len(obj.material_slots)
                bpy.ops.object.material_slot_add()
                obj.material_slots[index].link = link
                obj.material_slots[index].material = target
                obj.active_material_index = index

            if obj.type == 'GPENCIL':
                self.report({'WARNING'}, "Material not assigned to Grease Pencil Stroke! Only appended to object!")
            else:
                mu_assign_to_data(obj, target, index, edit_mode, all_polygons)

    # We shouldn't risk unsetting the active object
    if not active_object is None:
        # restore the active object
        bpy.context.view_layer.objects.active = active_object

    if edit_mode:
        bpy.ops.object.mode_set(mode='EDIT')

    return {'FINISHED'}


def mu_select_by_material_name(self, find_material_name, extend_selection = False, internal = False):
    """Searches through all objects, or the polygons/curves of the current object
    to find and select objects/data with the desired material"""

    # in object mode selects all objects with material find_material_name
    # in edit mode selects all polygons with material find_material_name

    find_material = bpy.data.materials.get(find_material_name)

    if find_material is None:
        self.report({'INFO'}, "The material " + find_material_name + " doesn't exists!")
        return {'CANCELLED'} if not internal else -1

    # check for edit_mode
    edit_mode = False
    found_material = False

    scene = bpy.context.scene

    # set selection mode to polygons
    scene.tool_settings.mesh_select_mode = False, False, True

    active_object = bpy.context.active_object

    if (not active_object is None) and (active_object.mode == 'EDIT'):
        edit_mode = True

    if not edit_mode:
        objects = bpy.context.visible_objects

        for obj in objects:
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
                mat_slots = obj.material_slots
                for material in mat_slots:
                    if material.material == find_material:
                        obj.select_set(state = True)

                        found_material = True

                        # the active object may not have the material!
                        # set it to one that does!
                        bpy.context.view_layer.objects.active = obj
                        break
                    else:
                        if not extend_selection:
                            obj.select_set(state=False)

            #deselect non-meshes
            elif not extend_selection:
                obj.select_set(state=False)

        if not found_material:
            if not internal:
                self.report({'INFO'}, "No objects found with the material " +
                                        find_material_name + "!")
            return {'FINISHED'} if not internal else 0

    else:
        # it's edit_mode, so select the polygons

        if active_object.type == 'MESH':
            # if not extending the selection, deselect all first
            #  (Without this, edges/faces were still selected
            #   while the faces were deselcted)
            if not extend_selection:
                bpy.ops.mesh.select_all(action = 'DESELECT')

        objects = bpy.context.selected_editable_objects

        for obj in objects:
            bpy.context.view_layer.objects.active = obj

            if obj.type == 'MESH':
                bpy.ops.object.mode_set()

                mat_slots = obj.material_slots

                # same material can be on multiple slots
                slot_indeces = []
                i = 0
                for material in mat_slots:
                    if material.material == find_material:
                        slot_indeces.append(i)
                    i += 1

                mesh = obj.data

                for poly in mesh.polygons:
                    if poly.material_index in slot_indeces:
                        poly.select = True
                        found_material = True
                    elif not extend_selection:
                        poly.select = False

                mesh.update()

                bpy.ops.object.mode_set(mode = 'EDIT')


            elif obj.type in {'CURVE', 'SURFACE'}:
                # For Curve objects, there can only be one material per spline
                #  and thus each spline is linked to one material slot.
                #  So to not have to care for different data structures
                #  for different curve types, we use the material slots
                #  and the built in selection methods
                #  (Technically, this should work for meshes as well)

                mat_slots = obj.material_slots

                i = 0
                for material in mat_slots:
                    bpy.context.active_object.active_material_index = i

                    if material.material == find_material:
                        bpy.ops.object.material_slot_select()
                        found_material = True
                    elif not extend_selection:
                        bpy.ops.object.material_slot_deselect()

                    i += 1

            elif not internal:
                # Some object types are not supported
                #  mostly because don't really support selecting by material (like Font/Text objects)
                #  ore that they don't support multiple materials/are just "weird" (i.e. Meta balls)
                self.report({'WARNING'}, "The type '" +
                                            obj.type +
                                            "' isn't supported in Edit mode by Material Utilities!")
                #return {'CANCELLED'}

        bpy.context.view_layer.objects.active = active_object

        if (not found_material) and (not internal):
            self.report({'INFO'}, "Material " + find_material_name + " isn't assigned to anything!")

    return {'FINISHED'} if not internal else 1


def mu_copy_material_to_others(self):
    """Copy the material to of the current object to the other seleceted all_objects"""
    # Currently uses the built-in method

    active_object = bpy.context.active_object
    if active_object.mode == 'EDIT':
        bpy.ops.object.mode_set()

        mesh = active_object.data
        materials = active_object.material_slots.keys()
        material_index = mesh.polygons[mesh.polygons.active].material_index
        material = materials[material_index]

        objects = bpy.context.selected_editable_objects

        for obj in objects:
            try:
                mi = obj.material_slots.keys().index(material)
            except ValueError:
                mi = len(obj.material_slots)
                obj.data.materials.append(bpy.data.materials[material])
                obj.active_material_index = mi

            for p in obj.data.polygons:
                if p.select:
                    p.material_index = mi

        bpy.ops.object.mode_set(mode = 'EDIT')
    else:
        bpy.ops.object.material_slot_copy()

    return {'FINISHED'}


def mu_cleanmatslots(self, affect, selected_collection = ""):
    """Clean the material slots of the selected objects"""

    # check for edit mode
    edit_mode = False
    active_object = bpy.context.active_object
    if active_object.mode == 'EDIT':
        edit_mode = True
        bpy.ops.object.mode_set()

    objects = []

    if affect == 'ACTIVE':
        objects = [active_object]
    elif affect == 'SELECTED':
        objects = bpy.context.selected_editable_objects
    elif affect == "ACTIVE_COLLECTION":
        objects = bpy.context.collection.objects
    elif affect == "SELECTED_COLLECTION":
        objects = bpy.data.collections[selected_collection].objects
    elif affect == 'SCENE':
        objects = bpy.context.scene.objects
    else: # affect == 'ALL'
        objects = bpy.data.objects

    for obj in objects:
        used_mat_index = []  # we'll store used materials indices here
        assigned_materials = []
        material_list = []
        material_names = []

        materials = obj.material_slots.keys()

        if obj.type == 'MESH':
            # check the polygons on the mesh to build a list of used materials
            mesh = obj.data

            for poly in mesh.polygons:
                # get the material index for this face...
                material_index = poly.material_index

                if material_index >= len(materials):
                    poly.select = True
                    self.report({'ERROR'},
                                "A poly with an invalid material was found, this should not happen! Canceling!")
                    return {'CANCELLED'}

                # indices will be lost: Store face mat use by name
                current_mat = materials[material_index]
                assigned_materials.append(current_mat)

                # check if index is already listed as used or not
                found = False
                for mat in used_mat_index:
                    if mat == material_index:
                        found = True

                if not found:
                    # add this index to the list
                    used_mat_index.append(material_index)

            # re-assign the used materials to the mesh and leave out the unused
            for u in used_mat_index:
                material_list.append(materials[u])
                # we'll need a list of names to get the face indices...
                material_names.append(materials[u])

            mu_assign_material_slots(obj, material_list)

            # restore face indices:
            i = 0
            for poly in mesh.polygons:
                material_index = material_names.index(assigned_materials[i])
                poly.material_index = material_index
                i += 1

        elif obj.type in {'CURVE', 'SURFACE'}:

            splines = obj.data.splines

            for spline in splines:
                # Get the material index of this spline
                material_index = spline.material_index

                # indices will be last: Store material use by name
                current_mat = materials[material_index]
                assigned_materials.append(current_mat)

                # check if indek is already listed as used or not
                found = False
                for mat in used_mat_index:
                    if mat == material_index:
                        found = True

                if not found:
                    # add this index to the list
                    used_mat_index.append(material_index)

            # re-assigned the used materials to the curve and leave out the unused
            for u in used_mat_index:
                material_list.append(materials[u])
                # we'll need a list of names to get the face indices
                material_names.append(materials[u])

            mu_assign_material_slots(obj, material_list)

            # restore spline indices
            i = 0
            for spline in splines:
                material_index = material_names.index(assigned_materials[i])
                spline.material_index = material_index
                i += 1

        else:
            # Some object types are not supported
            self.report({'WARNING'},
                        "The type '" + obj.type + "' isn't currently supported " +
                        "for Material slots cleaning by Material Utilities!")

    if edit_mode:
        bpy.ops.object.mode_set(mode='EDIT')

    return {'FINISHED'}

def mu_remove_material(self, for_active_object = False):
    """Remove the active material slot from selected object(s)"""

    if for_active_object:
        bpy.ops.object.material_slot_remove()
    else:
        last_active = bpy.context.active_object
        objects = bpy.context.selected_editable_objects

        for obj in objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.material_slot_remove()

        bpy.context.view_layer.objects.active =  last_active

    return {'FINISHED'}

def mu_remove_all_materials(self, for_active_object = False):
    """Remove all material slots from selected object(s)"""

    if for_active_object:
        obj = bpy.context.active_object

        # Clear out the material slots
        obj.data.materials.clear()

    else:
        last_active = bpy.context.active_object
        objects = bpy.context.selected_editable_objects

        for obj in objects:
            obj.data.materials.clear()

        bpy.context.view_layer.objects.active = last_active

    return {'FINISHED'}

def mu_do_replace_material(self, mat_org, mat_rep, all_objects=False, update_selection=False):
    """Replace one material with another material"""

    if mat_org != mat_rep and None not in (mat_org, mat_rep):
        scn = bpy.context.scene

        if all_objects:
            objs = bpy.data.objects
        else:
            objs = bpy.context.selected_editable_objects

        for obj in objs:
            if obj.type == 'MESH':
                match = False

                for mat in obj.material_slots:
                    if mat.material == mat_org:
                        mat.material = mat_rep

                        # Indicate which objects were affected
                        if update_selection:
                            obj.select_set(state = True)
                            match = True

                if update_selection and not match:
                    obj.select_set(state = False)

def mu_do_replace_multiple_materials(self, mats_org_list, mats_rep_list, all_objects=False, update_selection=False):
    """Take a list of materials, and replace each of them with the matching one in the second list"""

    mats_org_list_len = len(mats_org_list)
    mats_rep_list_len = len(mats_rep_list)

    if mats_org_list_len == 0:
        self.report({'ERROR'},
                    "List of materials to replace is empty! Canceling!")
        return {'CANCELLED'}
    if mats_rep_list_len == 0:
        self.report({'ERROR'},
                    "List of materials to replace with is empty! Canceling!")
        return {'CANCELLED'}

    mat_rep_last = mats_rep_list[0]

    for i in range(mats_org_list_len):
        mat_org = mats_org_list[i]
        mat_rep = mat_rep_last if i >= mats_rep_list_len else mats_rep_list[i]

        mu_do_replace_material(self, mat_org, mat_rep, all_objects, update_selection)

        mat_rep_last = mat_rep

    return {'FINISHED'}

def mu_replace_material(self, material_a, material_b, all_objects=False, update_selection=False):
    """Replace one material with another material"""

    # material_a is the name of original material
    # material_b is the name of the material to replace it with
    # 'all' will replace throughout the blend file

    mat_org = bpy.data.materials.get(material_a)
    mat_rep = bpy.data.materials.get(material_b)

    mu_do_replace_material(self, mat_org, mat_rep, all_objects, update_selection)

    return {'FINISHED'}

def mu_get_materials_as_list(self, material_str_list):
    """Take a list of material names as strings, and return a list with matching materials"""

    material_list = []

    for mat_str in material_str_list:
        mat = bpy.data.materials.get(mat_str)

        if (mat is None):
            self.report({'WARNING'}, "Could not find material '" + mat_str + "'! Skipping!")
        else:
            material_list.append(mat)

    return material_list

def mu_replace_multiple_materials(self, materials_a, materials_b, all_objects=False, update_selection=False):
    """Replace multiple materials with another material"""

    # material_a is a text block with materials to replace
    # material_b is a possible text block with materials to replace it with
    # 'all' will replace throughout the blend file

    mats_org_strlst = []
    mats_rep_strlst = []

    if not materials_a in bpy.data.texts.keys():
        error_msg = "No text block name given" if materials_a == "" else "Couldn't find a text block called " + materials_a
        self.report({'ERROR'},
                    error_msg + "! Canceling!")
        return {'CANCELLED'}

    mat_org_str = bpy.data.texts[materials_a].as_string()
    mats_org_strlst = mat_org_str.split("\n")


    if (materials_b != ""):
        if not materials_a in bpy.data.texts.keys():
            self.report({'ERROR'},
                        "Couldn't find a text block called " + materials_b + "! Canceling!")
            return {'CANCELLED'}

        mat_rep_str = bpy.data.texts[materials_b].as_string()
        mats_rep_strlst = mat_rep_str.split("\n")
    else:
        mats_org_strlst_old = mats_org_strlst
        mats_org_strlst = []

        for mat in mats_org_strlst_old:
            mat = mat.replace("\t", "  ")
            mats = re.split("\s\s+", mat)

            mats_org_strlst.append(mats[0])
            if len(mats) != 1:
                mats_rep_strlst.append(mats[1])

    mats_org_list = mu_get_materials_as_list(self, mats_org_strlst)
    mats_rep_list = mu_get_materials_as_list(self, mats_rep_strlst)

    mats_org_list_len = len(mats_org_list)
    mats_rep_list_len = len(mats_rep_list)

    if (mats_org_list_len != mats_rep_list_len):
        self.report({'WARNING'},
                    "Mismatching length of material lists, unexpected results might occur! %d original materials, %d replacement materials" %
                    (mats_org_list_len, mats_rep_list_len))

    return mu_do_replace_multiple_materials(self, mats_org_list, mats_rep_list, all_objects, update_selection)

def mu_set_fake_user(self, fake_user, materials, selected_collection = ""):
    """Set the fake user flag for the objects material"""

    if materials == 'ALL':
        mats = (mat for mat in bpy.data.materials if mat.library is None)
    elif materials == 'UNUSED':
        mats = (mat for mat in bpy.data.materials if mat.library is None and mat.users == 0)
    else:
        mats = []
        if materials == 'ACTIVE':
            objs = [bpy.context.active_object]
        elif materials == 'SELECTED':
            objs = bpy.context.selected_objects
        elif materials == "ACTIVE_COLLECTION":
            objs = bpy.context.collection.objects
        elif materials == "SELECTED_COLLECTION":
            objs = bpy.data.collections[selected_collection].objects
        elif materials == 'SCENE':
            objs = bpy.context.scene.objects
        else: # materials == 'USED'
            objs = bpy.data.objects
            # Maybe check for users > 0 instead?

        mats = (mat for ob in objs
                    if hasattr(ob.data, "materials")
                        for mat in ob.data.materials
                            if mat.library is None)

    if fake_user == 'TOGGLE':
        done_mats = []
        for mat in mats:
            if  not mat.name in done_mats:
                mat.use_fake_user = not mat.use_fake_user
            done_mats.append(mat.name)
    else:
        fake_user_val = fake_user == 'ON'
        for mat in mats:
            mat.use_fake_user = fake_user_val

    for area in bpy.context.screen.areas:
        if area.type in ('PROPERTIES', 'NODE_EDITOR'):
            area.tag_redraw()

    return {'FINISHED'}


def mu_change_material_link(self, link, affect, override_data_material = False, selected_collection = "", unlink_old = False):
    """Change what the materials are linked to (Object or Data), while keeping materials assigned"""

    objects = []

    if affect == "ACTIVE":
        objects = [bpy.context.active_object]
    elif affect == "SELECTED":
        objects = bpy.context.selected_objects
    elif affect == "ACTIVE_COLLECTION":
        objects = bpy.context.collection.objects
    elif affect == "SELECTED_COLLECTION":
        objects = bpy.data.collections[selected_collection].objects
    elif affect == 'Scene':
        objects = bpy.context.scene.objects
    elif affect == "ALL":
        objects = bpy.data.objects

    for object in objects:
        index = 0
        for slot in object.material_slots:
            present_material = slot.material

            if unlink_old:
                slot.material = None

            if link == 'TOGGLE':
                slot.link = ('DATA' if slot.link == 'OBJECT' else 'OBJECT')
            else:
                slot.link = link

            if slot.link == 'OBJECT':
                override_data_material = True
            elif slot.material is None:
                override_data_material = True
            elif not override_data_material:
                self.report({'INFO'},
                            'The object Data for object ' + object.name_full + ' already had a material assigned ' +
                            'to slot #' + str(index) + ' (' + slot.material.name + '), it was not overriden!')

            if override_data_material:
                slot.material = present_material

            index = index + 1

    return {'FINISHED'}

def mu_join_objects(self, materials):
    """Join objects together based on their material"""

    for material in materials:
        mu_select_by_material_name(self, material, False, True)

        bpy.ops.object.join()

    return {'FINISHED'}

def mu_set_auto_smooth(self, angle, affect, set_smooth_shading, selected_collection = ""):
    """Set Auto smooth values for selected objects"""
    # Inspired by colkai

    objects = []
    objects_affected = 0

    if affect == "ACTIVE":
        objects = [bpy.context.active_object]
    elif affect == "SELECTED":
        objects = bpy.context.selected_editable_objects
    elif affect == "ACTIVE_COLLECTION":
        objects = bpy.context.collection.objects
    elif affect == "SELECTED_COLLECTION":
        objects = bpy.data.collections[selected_collection].objects
    elif affect == 'Scene':
        objects = bpy.context.scene.objects
    elif affect == "ALL":
        objects = bpy.data.objects

    if len(objects) == 0:
        self.report({'WARNING'}, 'No objects available to set Auto Smooth on')
        return {'CANCELLED'}

    for object in objects:
        if object.type == "MESH":
            if set_smooth_shading:
                for poly in object.data.polygons:
                    poly.use_smooth = True

                #bpy.ops.object.shade_smooth()

            object.data.use_auto_smooth = 1
            object.data.auto_smooth_angle = angle  # 35 degrees as radians

            objects_affected += 1

    self.report({'INFO'}, 'Auto smooth angle set to %.0f° on %d of %d objects' %
                            (degrees(angle), objects_affected, len(objects)))

    return {'FINISHED'}

def mu_remove_unused_materials(self):
    """Remove any unused (zero users) materials"""
    # By request by Hologram

    count = 0

    for mat in bpy.data.materials:
        if mat.users == 0:
            bpy.data.materials.remove(mat)
            count += 1

    self.report({'INFO'}, '%d unused materials were removed' %
                            (count))

    return {'FINISHED'}

def mu_materials_filter_poll(self, material):
    return not material.is_grease_pencil

def mu_get_filetype(filename):
    """Look at the filename to determine file type, map type, and colorspace"""

    filename = filename.lower()

    ext = os.path.splitext(filename)[1].strip('.')
    type = 'NOT_IMG'
    colorspace = 'NA'
    override_colorspace = False
    texture_map = 'UNKNOWN'
    non_color = False
    has_alpha = False
    is_greyscale = False

    if ext == 'jpg' or ext == 'jpeg':
        type = 'JPG'
        colorspace = 'sRGB'
        override_colorspace = False
    elif ext == 'png':
        type = 'PNG'
        colorspace = 'sRGB'
        override_colorspace = False
    elif ext == 'exr':
        type = 'EXR'
        colorspace = 'LINEAR'
        override_colorspace = True
    elif ext == 'hdr':
        type = 'HDR'
        colorspace = 'LINEAR'
        override_colorspace = True
    elif ext == 'tif' or ext == 'tiff':
        type = 'TIF'
        colorspace = 'LINEAR'
        override_colorspace = True
    elif ext == 'tga':
        type = 'TGA'
        colorspace = 'LINEAR'
        override_colorspace = True

    if 'albedo' in filename:
        texture_map = 'ALBEDO'
        has_alpha = True
    elif 'diffuse' in filename:
        texture_map = 'DIFFUSE'
        has_alpha = True
    elif 'ao' in filename or 'occlusion' in filename:
        texture_map = 'AO'
        non_color = True
        is_greyscale = True
    elif 'rough' in filename:
        texture_map = 'ROUGHNESS'
        non_color = True
        is_greyscale = True
    elif 'gloss' in filename:
        texture_map = 'GLOSSINESS'
        non_color = True
        is_greyscale = True
    elif 'spec' in filename:
        texture_map = 'SPECULAR'
        non_color = True
        is_greyscale = True
    elif 'refl' in filename:
        texture_map = 'REFLECTION'
        non_color = True
        is_greyscale = True
    elif 'metal' in filename:
        texture_map = 'METALNESS'
        non_color = True
        is_greyscale = True
    elif 'height' in filename:
        texture_map = 'HEIGHT'
        non_color = True
        is_greyscale = True
    elif 'disp' in filename or 'dsp' in filename:
        texture_map = 'DISPLACEMENT'
        non_color = True
        is_greyscale = True
    elif 'bump' in filename or 'bmp' in filename:
        texture_map = 'BUMP'
        non_color = True
        is_greyscale = True
    elif 'nor' in filename or 'nrm' in filename:
        texture_map = 'NORMAL'
        non_color = True
    elif 'col' in filename or 'base' in filename:
        texture_map = 'COLOR'
        has_alpha = True
    elif 'alpha' in filename or 'opacity' in filename or 'transparent' in filename:
        texture_map = 'ALPHA'
        non_color = True
        is_greyscale = True
    elif 'mask' in filename:
        texture_map = 'MASK'
        non_color = True
        is_greyscale = True
    elif 'trans' in filename:
        texture_map = 'TRANSMISSION'
    elif 'emission' in filename:
        texture_map = 'EMISSION'
    elif 'render' in filename:
        texture_map = 'RENDER'

    if override_colorspace:
        if 'filmic' in filename:
            colorspace = 'FILMIC_LOG' if 'log' in filename else 'FILMIC_sRGB'
        elif 'acescg' in filename:
            colorspace = 'ACEScg'
        elif 'aces' in filename:
            colorspace = 'ACES'
        elif 'linear' in filename:
            colorspace = 'LINEAR'
        elif 'srgb' in filename:
            colorspace = 'sRGB'

    return SimpleNamespace(type=type, colorspace=colorspace, map=texture_map, orig_map=texture_map,
                           override_colorspace=override_colorspace, non_color=non_color, is_greyscale=is_greyscale, has_alpha=has_alpha)

def mu_faux_shader_node(out_node):
    """Create a 'faux shader', to be used instead of an existing shader node"""

    return SimpleNamespace(name='FAUX', bl_idname='FAUX', location=out_node.location, width=out_node.width)

def mu_set_image_colorspace(colsp, filetype):
    """Set the colorspace of an internal image block to match the colorspace in the texture file"""

    if filetype.non_color and not filetype.override_colorspace:
        colsp.name = 'Non-Color'
    elif filetype.colorspace == 'FILMIC_sRGB':
        colsp.name = 'Filmic sRGB'
    elif filetype.colorspace == 'FILMIC_LOG':
        colsp.name = 'Filmic Log'
    elif filetype.colorspace == 'LINEAR':
        colsp.name = 'Linear'
    elif filetype.colorspace == 'ACES':
        colsp.name = 'Linear ACES'
    elif filetype.colorspace == 'ACEScg':
        colsp.name = 'Linear ACEScg'
    elif filetype.colorspace == 'sRGB':
        colsp.name = 'sRGB'

def mu_get_ocio_colorspace(colsp, imgtype):
    """Get the OCIO Color Space based on incoming colorspace"""
    cs = 'Other'

    if colsp in mu_ocio_colorspace_map:
        if imgtype in mu_ocio_colorspace_map[colsp]:
            cs = mu_ocio_colorspace_map[colsp][imgtype]
        else:
            cs = mu_ocio_colorspace_map[colsp]['_DEFAULT']
    else:
        cs = mu_ocio_colorspace_map['_DEFAULT']

    return cs

def mu_calc_node_location(first_node, node, filetype, engine='', x_offset=-100, y_offset=0, map=None, prefs = None):
    """Caculate the proper location of the, to be, added texture node, based on the map type"""

    location = [0,0]
    ft_map = 'COLOR'
    if map is None:
        map = filetype.map
    grp = 'EXP' if prefs is None else prefs.pos_group

    if filetype is None or (engine == 'CYCLES' and map == '_DISPLACEMENT'):
        ft_map = map
    else:
        ft_map = filetype.map

    if engine == 'CYCLES':
        if map == '_BUMPNODE' or map == '_NORMALNODE':
            x_offset -= 0 + 50
        elif map == '_DISPLACEMENT':
            x_offset -= first_node.width + node.width + 10
        elif map == '_INVERT':
            x_offset -= 0 + 50
        elif map == '_UVNODE':
            x_offset += 585 + 50
        elif map == '_UVREROUTE':
            x_offset += 370 + 50
        elif map == 'BUMP':
            x_offset += 200 + 50
        elif map == 'HEIGHT' or map == 'DISPLACEMENT':
            x_offset -= 150
        elif map == 'NORMAL':
            x_offset += 200 + 50
        elif map == 'GLOSSINESS':
            x_offset += 200 + 50
    elif engine == 'OCTANE':
        if map == '_UVNODE' or map == '_TRANSFORM':
            x_offset += 500 + 50
        elif map == '_UVREROUTE' or map == '_TRANSFORMREROUTE':
            x_offset += 270 + 50
        elif map == '_COLORSPACENODE':
            x_offset += 500 + 50
        elif map == 'HEIGHT' or map == 'DISPLACEMENT':
            x_offset += 150 + 50
        elif map == '_DISPLACEMENT':
            x_offset -= 40
        elif map == 'EMISSION':
            x_offset += 150 + 50
        elif map == '_EMISSION':
            x_offset -= 40

    location[0] = first_node.location[0] - first_node.width*2 - x_offset
    location[1] = first_node.location[1] + y_offset

    if ft_map != 'None':# and ft_map != 'UNKNOWN':
        location[1] -= mu_node_positions[engine][grp][first_node.bl_idname][ft_map]

    return location

def mu_add_octane_node(type, prefs=None, filetype=None, nodes=[], name=None, label=None):
    node    = None
    is_img  = False
    lbl_sfx = ''

    # m = bpy.data.materials[mat.name]
    if type == 'uvmap':
        type = 'OctaneMeshUVProjection'
    elif type == 'transform' or type == '2Dtransform':
        type = 'Octane2DTransformation'
    elif type == '3Dtransform':
        type = 'Octane3DTransformation'
    elif type == 'colorspace':
        type = 'OctaneOCIOColorSpace'
    elif type == 'displacement':
        type = 'OctaneTextureDisplacement'
    elif type == 'emission':
        type = 'OctaneTextureEmission'
    elif type == 'RGBimage':
        type = 'OctaneRGBImage'
    elif type == 'alpha_image':
        type = 'OctaneAlphaImage'
    elif type == 'image':
        is_img = True
        if filetype.is_greyscale: #non_color and filetype.map != 'NORMAL':
            type = 'OctaneGreyscaleImage'
            lbl_sfx = ' - Greyscale'
        else:
            type = 'OctaneRGBImage'
            lbl_sfx = ' - RGB'

    # count = len(m.node_tree.nodes)
    # bpy.ops.octane.add_default_node_helper(default_node_name=type)
    # node = nodes[count-1]
    
    node = nodes.new(type)

    if name is not None:
        if name == '_MAP':
            name = 'MUAdded' + filetype.map
        node.name = name
    if label is not None:
        node.label = label
    elif prefs.set_label and is_img:
        node.label = filetype.orig_map + lbl_sfx

    if prefs.collapse_texture_nodes: # and type != 'OctaneMeshUVProjection':
        node.hide = True

    # if type == 'OctaneMeshUVProjection':
    #     return node
    if type == 'OctaneTextureDisplacement':
        node.inputs['Height'].default_value = prefs.bump_distance
        return node

    if is_img:
        if filetype.non_color:
            node.inputs['Legacy gamma'].default_value = 1.0
        else:
            node.inputs['Legacy gamma'].default_value = prefs.gamma

        if filetype.map == 'GLOSSINESS':
            node.inputs['Invert'].default_value = True

    return node

def mu_add_image_texture(filename, filetype, prefs,
                         nodes = None, links = None, material = None,
                         out_node = None, first_node = None, engine = ''):
    """Add an image texture to the material node tree, and (if selected) try to connect it up"""

    x_offset = -100

    try:
        img = bpy.data.images.load(filename)
    except:
        raise NameError("Cannot load image %s" % filename)

    mu_set_image_colorspace(img.colorspace_settings, filetype) # Octane will ignore this, but for Cycles the colorspace is connected to the image data

    if engine == 'CYCLES':
        node = nodes.new('ShaderNodeTexImage')

        name = 'MUAdded' + filetype.map
        node.name = name
        if prefs.set_label:
            node.label = filetype.orig_map
        if prefs.collapse_texture_nodes:
            node.hide = True

        if prefs.connect and filetype.map != 'UNKNOWN':
            input = mu_node_inputs[engine][first_node.bl_idname][filetype.map]
            link_node = node

            if filetype.map == 'BUMP':
                bump_node = nodes.new('ShaderNodeBump')
                bump_node.name = 'MUAddedBumpNode'
                bump_node.location = mu_calc_node_location(first_node, node, filetype, engine, x_offset=x_offset, map='_BUMPNODE', prefs=prefs)
                bump_node.inputs['Distance'].default_value = prefs.bump_distance

                i = mu_node_inputs[engine]['ShaderNodeBump'][filetype.map]
                links.new(node.outputs['Color'], bump_node.inputs[i])
                link_node = bump_node
                #links.new(bump_node.outputs[0], first_node.inputs[input])
            elif filetype.map == 'NORMAL':
                nrm_node = nodes.new('ShaderNodeNormalMap')
                nrm_node.name = 'MUAddedNormalMapNode'
                nrm_node.location = mu_calc_node_location(first_node, node, filetype, engine, x_offset=x_offset, map='_NORMALNODE', prefs=prefs)

                i = mu_node_inputs[engine]['ShaderNodeNormalMap'][filetype.map]
                links.new(node.outputs['Color'], nrm_node.inputs[i])
                link_node = nrm_node
                #links.new(nrm_node.outputs[0], first_node.inputs[input])
            elif filetype.map == 'GLOSSINESS':
                inv_node = nodes.new('ShaderNodeInvert')
                inv_node.name = 'MUAddedInvertNode'
                inv_node.location = mu_calc_node_location(first_node, node, filetype, engine, x_offset=x_offset, map='_INVERT', prefs=prefs)
                inv_node.hide = True

                links.new(node.outputs['Color'], inv_node.inputs['Color'])
                link_node = inv_node
            elif filetype.map == 'DISPLACEMENT':
                dsp_node = nodes.new('ShaderNodeDisplacement')
                dsp_node.name = 'MUAddedDisplacementNode'
                dsp_node.location = mu_calc_node_location(first_node, node, filetype, engine, x_offset=x_offset, map='_DISPLACEMENT', prefs=prefs)

                links.new(node.outputs['Color'], dsp_node.inputs['Height'])
                links.new(dsp_node.outputs['Displacement'], out_node.inputs['Displacement'])

            if input is not None:
                links.new(link_node.outputs[0], first_node.inputs[input])
            else:
                print("Material Utilities - No input for %s to %s found, skipping link" % (filetype.map, first_node.bl_idname))

            if filetype.has_alpha and prefs.connect_alpha:
                input = mu_node_inputs[engine][first_node.bl_idname]['ALPHA']
                if input is not None:
                    links.new(node.outputs['Alpha'], first_node.inputs[input])

            node.image = img
    elif engine == 'OCTANE':
        node = mu_add_octane_node('image', filetype=filetype, nodes=nodes, prefs=prefs, name='_MAP')
        node.image = img

        if prefs.connect and filetype.map != 'UNKNOWN':
            input = mu_node_inputs[engine][first_node.bl_idname][filetype.map]
            link_node = node
            
            if filetype.map == 'EMISSION':
                emit_node = mu_add_octane_node('emission', nodes=nodes, prefs=prefs, name='MUAddedEmissionNode')
                emit_node.location = mu_calc_node_location(first_node, node, filetype, engine, x_offset, prefs=prefs, map='_EMISSION')
                
                links.new(node.outputs[0], emit_node.inputs['Texture'])
                link_node = emit_node
            elif filetype.map == 'DISPLACEMENT':
                disp_node = mu_add_octane_node('displacement', nodes=nodes, prefs=prefs, name='MUAddedDisplacementNode')
                disp_node.location = mu_calc_node_location(first_node, node, filetype, engine, x_offset, prefs=prefs, map='_DISPLACEMENT')
                
                links.new(node.outputs[0], disp_node.inputs['Texture'])
                link_node = disp_node

            if input is not None:
                links.new(link_node.outputs[0], first_node.inputs[input])
            else:
                print("Material Utilities - No input for %s to %s found, skipping link" % (filetype.map, first_node.bl_idname))

    node.location = mu_calc_node_location(first_node, node, filetype, engine, x_offset, prefs=prefs)

    return node

def mu_replace_image(self, filename, filetype, prefs, node, engine):
    """Replace the image file in an existing, specified, texture node"""

    try:
        img = bpy.data.images.load(filename)
    except:
        self.report({'WARNING'}, "Cannot load image %s" % filename)
        return

    if prefs.set_fake_user:
        node.image.use_fake_user = True

    mu_set_image_colorspace(img.colorspace_settings, filetype) # Octane will ignore this, but for Cycles the colorspace is connected to the image data

    node.image = img
    print("Replaced file in node '%s' ('%s') with %s" % (node.name, node.label, filename))

def mu_replace_selected_image_textures(self, filename, filetype, prefs, nodes=[], engine=''):
    """Replace the image files in the selected nodes, if matching, with a new set"""

    found      = False
    found_node = None

    for node in nodes:
        if (engine == 'CYCLES' and node.bl_idname == 'ShaderNodeTexImage') or \
           (engine == 'OCTANE' and node.bl_idname in ['OctaneGreyscaleImage', 'OctaneRGBImage']):
            ft = mu_get_filetype(node.image.name)
            if node.label.upper() == filetype.map or ft.map == filetype.map:
                found      = True
                found_node = node
                break

    if found:
        mu_replace_image(self, filename, filetype, prefs, found_node, engine)
    else:
        print("Didn't find a texture node for '%s'" % filename)

def mu_replace_image_texture(self, filename, filetype, prefs, nodes = None,
                             out_node = None, first_node = None, engine=''):
    """Try to find and replace the image file in an existing texture node"""

    found = False
    found_node = None

    # If it's a height/displacement map, look for it in the Displacement input on the Material out node
    if filetype.map == 'DISPLACEMENT' or filetype.map == 'HEIGHT':
        if out_node.inputs['Displacement'].is_linked:
            disp_node = out_node.inputs['Displacement'].links[0].from_node
            if disp_node.inputs['Height'].is_linked:
                node = disp_node.inputs['Height'].links[0].from_node

                if node is not None and node.bl_idname == 'ShaderNodeTexImage':
                    found = True
                    found_node = node

    # Look for matching texture nodes in the inputs of the first shader node
    #  If the node setup is more complex (and the first node isn't a Principled BSDF or similar)
    #  we wont go looking for it further (even if we could), because it would get too involved
    #  Easier to just go through the whole node list than a bunch of links
    if not found and first_node is not None:
        input = mu_node_inputs[engine][first_node.bl_idname][filetype.map]
        if input is not None and first_node.inputs[input].is_linked:
            node = first_node.inputs[input].links[0].from_node
            
            if node is not None and node.bl_idname == 'ShaderNodeTexImage':
                found = True
                found_node = node

    # Just search through all nodes if we haven't found the right one yet (and wide search is enabled)
    if not found and prefs.go_wide:
        # Use the replaced selected textures functions, but use all nodes as "selected" nodes
        return mu_replace_selected_image_textures(self, filename, filetype, prefs, nodes, engine)

    if found:
        mu_replace_image(self, filename, filetype, prefs, found_node, engine)
    else:
        print("Didn't find a texture node for '%s'" % filename )

def mu_add_image_textures(self, prefs, directory = None, file_list = [], file_path = ''):
    """Add a new texture set to the material (doesn't care about any existing textures)"""

    files = []

    if directory is not None:
        dir = os.path.dirname(directory)
        for filename in os.listdir(dir):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                files.append(f)
    else:
        dir = os.path.dirname(file_path)
        for file in file_list:
            f = os.path.join(file_path, file.name)
            files.append(f)

    dir_name = os.path.basename(dir)

    engine = bpy.data.scenes['Scene'].render.engine
    mat    = bpy.context.active_object.active_material

    if engine == 'CYCLES' or engine == 'BLENDER_EEVEE': # Cycles and Eevee uses the same nodes
        engine = 'CYCLES'
    elif engine == 'octane':
        engine = engine.upper()
    else:
        print("Material Utilities - Add image Textures: Unsupported render engine: ", bpy.data.scenes['Scene'].render.engine)
        self.report({'WARNING'}, "The render engine '" + bpy.data.scenes['Scene'].render.engine +
                                    "' isn't supported by Material Utilities!")
        return {'CANCELLED'}

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    out_node    = nodes.get('Material Output')
    first_node  = None
    has_bump    = False
    has_normal  = False
    gloss_rough = 0
    gloss_node  = None
    rough_node  = None
    has_displace = False
    bump_tex_node   = None
    normal_tex_node = None
    displace_tex_node = None
    colorspaces = {}

    if out_node is None:
        self.report({'WARNING'}, "Couldn't find an Material Output! Creating one!")
        out_node = bpy.ops.node.add_node(type="ShaderNodeOutputMaterial", use_transform=False)
        out_node.location = (400, 100)

    if out_node.inputs['Surface'].is_linked:
        first_node = out_node.inputs['Surface'].links[0].from_node
    else:
        msg = "Couldn't find a surface node connected to the material output!"
        if prefs.connect:
            prefs.connect = False
            msg += " Wont try to connect added textures!"
        print("Material Utilies - " + msg)
        self.report({'WARNING'},  msg)

        # Create a "faux-node" so to aid in further operations
        first_node = mu_faux_shader_node(out_node)
        first_node.location[0] -= first_node.width + 300

    # If the first node is an unsupported note
    if first_node.bl_idname not in mu_node_positions[engine][prefs.pos_group].keys():
        if first_node.bl_idname != 'FAUX':
            msg = "The first node ('%s') is not supported!" % first_node.name
            if prefs.connect:
                prefs.connect = False
                msg += " Wont try to connect added textures!"
            print("Material Utilites - " + msg)
            self.report({'WARNING'}, msg)

        location = first_node.location

        # Create a "faux-node" so to aid in further operations
        first_node = mu_faux_shader_node(out_node)
        first_node.location = location

    added_nodes = []

    for file in files:
        filename = os.path.basename(file)
        filetype = mu_get_filetype(filename)

        if filetype.type == 'NOT_IMG' or filetype.map == 'RENDER':
            print("Skipping: %s (%s / %s)" % (filename, filetype.type, filetype.map))
            continue

        if filetype.map == 'HEIGHT':
            if prefs.height_map != 'NC':
                filetype.map = prefs.height_map
        elif filetype.map == 'REFLECTION':
            if prefs.reflection_as_specular:
                filetype.map = 'SPECULAR'

        try:
            node = mu_add_image_texture(file, filetype=filetype, prefs=prefs, nodes=nodes, links=links, material=mat,
                                        out_node=out_node, first_node=first_node, engine=engine)
            
            if filetype.map == 'GLOSSINESS':
                gloss_rough += 1
                gloss_node = node
            if filetype.map == 'ROUGHNESS':
                gloss_rough += 1
                rough_node = node

            if engine == 'CYCLES':
                if filetype.map == 'BUMP':
                    has_bump = True
                    bump_tex_node = node
                if filetype.map == 'NORMAL':
                    has_normal = True
                    normal_tex_node = node
                if filetype.map == 'DISPLACEMENT':
                   has_displace = True
                   displace_tex_node = node
            elif engine == 'OCTANE':
                color = 'GREYSCALE' if filetype.is_greyscale else 'RGB'

                if filetype.colorspace not in colorspaces:
                    colorspaces[filetype.colorspace] = {}
                if color not in colorspaces[filetype.colorspace]:
                    colorspaces[filetype.colorspace][color] = []

                colorspaces[filetype.colorspace][color].append(node)

            added_nodes.append(node)
        except NameError as err:
            self.report({'WARNING'}, str(err))

    if gloss_rough > 1:
        connected = "one"
        if rough_node.outputs[0].is_linked:
            gloss_node.location.x -= 150
            connected = "Roughness"
        else:
            rough_node.location.x -= 150
            connected = "Glossiness"

        self.report({'WARNING'}, "Texture set has both Roughness and Glossiness, " + connected + " has taken presidence!")

    if prefs.connect:
        uvmap     = None
        reroute   = None
        has_uvmap = False
        
        mu_prefs = materialutilities_get_preferences(bpy.context)

        if engine == 'CYCLES':
            if mu_prefs.tex_add_new_uvmap:
                if nodes.find('MUAddedUVMap') >= 0:
                    has_uvmap = True
            else:
                if nodes.find('MUAddedUVMap') >= 0:
                    uvmap = nodes['MUAddedUVMap']
                elif nodes.find('UV Map') >= 0:
                    uvmap = nodes['UV Map']

            if uvmap is not None:
                if uvmap.outputs['UV'].links[0].to_node.bl_idname == 'NodeReroute':
                    reroute = uvmap.outputs['UV'].links[0].to_node
            else:
                uvmap = nodes.new('ShaderNodeUVMap')
                uvmap.name     = 'MUAddedUVMap'
                uvmap.label    = dir_name + " - UV"
                uvmap.location = mu_calc_node_location(first_node, uvmap, None, engine, map='_UVNODE', prefs=prefs)

            if reroute is None:
                reroute = nodes.new('NodeReroute')
                reroute.name     = 'MUAddedUVReroute'
                reroute.location = mu_calc_node_location(first_node, uvmap, None, engine, map='_UVREROUTE', prefs=prefs)

                links.new(uvmap.outputs['UV'], reroute.inputs['Input'])

            if has_uvmap:
                reroute.location.y += 150
                uvmap.location.y   += 150

            if has_bump:
                bump_node   = nodes['MUAddedBumpNode']
            if has_normal:
                normal_node = nodes['MUAddedNormalMapNode']

            if has_normal and has_bump:
                uvmap.location.x   -= 200
                reroute.location.x -= 20

                # Seperate the bump and normal nodes
                bump_node.location.x       += 75
                bump_tex_node.location.x   -= 100
                normal_node.location.x     -= 90
                normal_node.location.y     -= 140
                normal_tex_node.location.x -= 100
                normal_tex_node.location.y -= 240

                links.new(normal_node.outputs['Normal'], bump_node.inputs['Normal'])
                links.new(bump_node.outputs['Normal'], first_node.inputs['Normal'])

            for node in added_nodes:
                links.new(reroute.outputs['Output'], node.inputs['Vector'])

            if prefs.stairstep and not prefs.pos_group == 'COL':
                from operator import attrgetter
                added_nodes.sort(key=attrgetter('location.y'), reverse=True)
                pos_y = first_node.location.y
                offs_y1 = 250
                offs_y2 = 40
                offs_x1 = 250
                offs_x2 = 300
                offs_x3 = offs_x1 * 2
                odd = True

                if uvmap is not None:
                    uvmap.location.x   -= offs_x2
                    reroute.location.x -= offs_x2
                
                for node in added_nodes:
                    if node.name == 'MUAddedGLOSSINESS' or not node.outputs[0].is_linked:
                        if node.name == 'MUAddedAO':
                            node.location.y = first_node.location.y + offs_y1 + offs_y2
                        elif node.name == 'MUAddedGLOSSINESS' or node.name == 'MUAddedROUGHNESS':
                            node.location.x -= offs_x2
                            node.location.y = first_node.location.y + offs_y1 + offs_y2
                            if node.name == 'MUAddedGLOSSINESS':
                                nodes['MUAddedInvertNode'].location = node.location
                                nodes['MUAddedInvertNode'].location.x += offs_x2
                                nodes['MUAddedInvertNode'].location.y -= 20
                        
                        continue
                    if node.name in ['MUAddedDISPLACEMENT', 'MUAddedBUMP', 'MUAddedNORMAL']:
                        continue

                    node.location.y = pos_y

                    if odd:
                        pos_y -= offs_y1
                    else:
                        pos_y -= offs_y2
                        node.location.x -= offs_x1

                    # if node.name in ['MUAddedDISPLACEMENT', 'MUAddedBUMP', 'MUAddedNORMAL']:
                    #     if node.name == 'MUAddedDISPLACEMENT':
                    #         nid = 'MUAddedDisplacementNode'
                    #     elif node.name == 'MUAddedBUMP':
                    #         nid = 'MUAddedBumpNode'
                    #     elif node.name == 'MUAddedNORMAL':
                    #         nid = 'MUAddedNormalMapNode'
                    #     pos_t = mu_calc_node_location(first_node, node, None, engine, prefs=prefs, map='None')
                    #     node.location.x = pos_t[0]
                    #     nodes[nid].location = node.location
                    #     if odd:
                    #         print("ODD")
                    #         node.location.x -= offs_x3
                    #     else:
                    #         print("EVEN")
                    #         node.location.x -= offs_x3

                    odd = not odd

                if has_displace:
                    pos_t = mu_calc_node_location(first_node, displace_tex_node, None, engine, prefs=prefs, map='None')
                    pos_t[1] = pos_y
                    
                    displace_tex_node.location = pos_t
                    nodes['MUAddedDisplacementNode'].location.y = first_node.location.y - 700
                    nodes['MUAddedDisplacementNode'].location.x = first_node.location.x

                    if odd:
                        pos_y -= offs_y1
                    else:
                        pos_y -= offs_y2
                        displace_tex_node.location.x -= offs_x1

                    odd = not odd

                if has_bump:
                    pos_t = mu_calc_node_location(first_node, bump_node, None, engine, prefs=prefs, map='None')
                    pos_t[1] = pos_y

                    bump_tex_node.location = pos_t
                    bump_tex_node.location.x -= offs_x3
                    bump_node.location = pos_t
                    bump_node.location.y = pos_y

                    if odd:
                        pos_y -= offs_y1
                    else:
                        pos_y -= offs_y2

                    odd = not odd

                if has_normal:
                    pos_t = mu_calc_node_location(first_node, normal_node, None, engine, prefs=prefs, map='None')
                    pos_t[1] = pos_y

                    normal_tex_node.location = pos_t
                    normal_tex_node.location.x -= offs_x3
                    normal_node.location = pos_t
                    normal_node.location.y = pos_y
                    if has_bump:
                        normal_node.location.x -= offs_x1


        elif engine == 'OCTANE':
            transform  = None
            reroute_tr = None
            cs_nodes   = []

            if mu_prefs.tex_add_new_uvmap:
                if nodes.find('MUAddedUVMapOctane') >= 0:
                    has_uvmap = True
            else:
                if nodes.find('MUAddedUVMapOctane') >= 0:
                    uvmap = nodes['MUAddedUVMapOctane']
                elif nodes.find('Mesh UV projection') >= 0:
                    uvmap = nodes['Mesh UV projection']
                if nodes.find('MUAddedTransformOctane') >= 0:
                    transform = nodes['MUAddedTransformOctane']
                elif nodes.find('2D transformation') >= 0:
                    transform = nodes['2D transformation']
                elif nodes.find('3D transformation') >= 0:
                    transform = nodes['3D transformation']

            if uvmap is not None:
                if uvmap.outputs['Projection out'].links[0].to_node.bl_idname == 'NodeReroute':
                    reroute = uvmap.outputs['Projection out'].links[0].to_node
            else:
                uvmap = mu_add_octane_node('uvmap', name='MUAddedUVMapOctane', label=dir_name + " - UV", nodes=nodes, prefs=prefs)
                uvmap.location = mu_calc_node_location(first_node, uvmap, None, engine, map='_UVNODE', prefs=prefs)

            if reroute is None:
                reroute = nodes.new('NodeReroute')
                reroute.name     = 'MUAddedUVReroute'
                reroute.location = mu_calc_node_location(first_node, uvmap, None, engine, map='_UVREROUTE', prefs=prefs)

                links.new(uvmap.outputs['Projection out'], reroute.inputs['Input'])

            if transform is not None:
                if transform.outputs['Transform out'].links[0].to_node.bl_idname == 'NodeReroute':
                    reroute_tr = transform.outputs['Transform out'].links[0].to_node
            else:
                transform = mu_add_octane_node('transform', name='MUAddedTransformOctane', label=dir_name + " - Transform", nodes=nodes, prefs=prefs)
                transform.location = mu_calc_node_location(first_node, transform, None, engine, map='_TRANSFORM', prefs=prefs)

            if reroute_tr is None:
                reroute_tr = nodes.new('NodeReroute')
                reroute_tr.name     = 'MUAddedUVTransformReroute'
                reroute_tr.location = mu_calc_node_location(first_node, transform, None, engine, map='_TRANSFORMREROUTE', prefs=prefs)

                links.new(transform.outputs['Transform out'], reroute_tr.inputs['Input'])

            if prefs.add_colorspace:
                y_offset = 0
                for cs, nodetypes in colorspaces.items():
                    for nt, texnodes in nodetypes.items():
                        cs_node = mu_add_octane_node('colorspace', name='MUAddedColorSpace_' + cs + '_' + nt, 
                                                     label='ColorSpace - %s (%s)' % (cs, nt), nodes=nodes, prefs=prefs)
                        cs_node.location = mu_calc_node_location(first_node, cs_node, None, engine, map='_COLORSPACENODE', prefs=prefs, y_offset=y_offset)
                        cs_node.ocio_color_space_name = mu_get_ocio_colorspace(cs,nt)
                        
                        cs_nodes.append(cs_node)

                        for txnode in texnodes:
                            links.new(cs_node.outputs[0], txnode.inputs['Color space'])

                        y_offset -= 100 if prefs.pos_group == 'EXP' else 40

            if has_uvmap:
                reroute.location.y -= 150
                uvmap.location.y   -= 150

            for node in added_nodes:
                links.new(reroute.outputs['Output'], node.inputs['Projection'])
                links.new(reroute_tr.outputs['Output'], node.inputs['UV transform'])

            if prefs.stairstep and not prefs.pos_group == 'COL':
                from operator import attrgetter
                added_nodes.sort(key=attrgetter('location.y'), reverse=True)
                pos_y = first_node.location.y
                offs_y1 = 330
                offs_y2 = 40
                offs_x1 = 220
                offs_x2 = 300
                offs_x3 = offs_x1 * 2
                odd = True

                if uvmap is not None:
                    uvmap.location.x   -= offs_x2
                    reroute.location.x -= offs_x2
                if transform is not None:
                    transform.location.x  -= offs_x2
                    reroute_tr.location.x -= offs_x2
                for cs_node in cs_nodes:
                    cs_node.location.x -= offs_x2
                
                for node in added_nodes:
                    if not node.outputs[0].is_linked:
                        if node.name == 'MUAddedAO':
                            node.location.y = first_node.location.y + offs_y1 + offs_y2
                        elif node.name == 'MUAddedGLOSSINESS' or node.name == 'MUAddedROUGHNESS':
                            node.location.x -= offs_x2
                            node.location.y = first_node.location.y + offs_y1 + offs_y2
                        elif node.name == 'MUAddedHEIGHT' or node.name == 'MUAddedBUMP':
                            pos_t = mu_calc_node_location(first_node, node, None, engine, prefs=prefs, map='None')
                            node.location.x = pos_t[0] - offs_x1
                            node.location.y = first_node.location.y + offs_y1 + offs_y2
                        
                        continue

                    node.location.y = pos_y

                    if odd:
                        pos_y -= offs_y1
                    else:
                        pos_y -= offs_y2
                        node.location.x -= offs_x1

                    if node.name == 'MUAddedDISPLACEMENT' or node.name == 'MUAddedEMISSION':
                        nid = 'MUAddedDisplacementNode' if node.name == 'MUAddedDISPLACEMENT' else 'MUAddedEmissionNode'
                        pos_t = mu_calc_node_location(first_node, node, None, engine, prefs=prefs, map='None')
                        node.location.x = pos_t[0]
                        nodes[nid].location = node.location
                        node.location.x -= offs_x3

                    odd = not odd

    return {'FINISHED'}

def mu_replace_image_textures(self, prefs, directory = None, file_list = [], file_path = ''):
    """Try to find and replace image files in existing texture nodes with a new set (Does NOT add a new texture if there's an new image texture without matching node!)"""

    files = []

    if directory is not None:
        dir = os.path.dirname(directory)
        for filename in os.listdir(dir):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                files.append(f)
    else:
        dir = os.path.dirname(file_path)
        for file in file_list:
            f = os.path.join(file_path, file.name)
            files.append(f)

    engine = bpy.data.scenes['Scene'].render.engine
    mat    = bpy.context.active_object.active_material

    if engine == 'CYCLES' or engine == 'BLENDER_EEVEE': # Cycles and Eevee uses the same nodes
        engine = 'CYCLES'
    elif engine == 'octane':
        engine = engine.upper()
    else:
        print("Material Utilities - Add image Textures: Unsupported render engine: ", bpy.data.scenes['Scene'].render.engine)
        self.report({'WARNING'}, "The render engine '" + bpy.data.scenes['Scene'].render.engine +
                                    "' isn't supported by Material Utilities!")
        return {'CANCELLED'}

    nodes = mat.node_tree.nodes
    out_node   = nodes.get('Material Output')
    first_node = None

    if out_node is None:
        self.report({'WARNING'}, "Couldn't find an Material Output!")
    elif out_node.inputs['Surface'].is_linked:
        first_node = out_node.inputs['Surface'].links[0].from_node

    if first_node is not None and first_node.bl_idname not in mu_node_inputs[engine].keys():
        first_node = None

    for file in files:
        filename = os.path.basename(file)
        filetype = mu_get_filetype(filename)
        
        if filetype.type == 'NOT_IMG' or filetype.map == 'RENDER':
            print("Skipping: %s (%s / %s)" % (filename, filetype.type, filetype.map))
            continue

        if prefs.only_selected:
            mu_replace_selected_image_textures(self, file, filetype=filetype, prefs=prefs, nodes=prefs.context.selected_nodes, engine=engine)
        else:
            mu_replace_image_texture(self, file, filetype=filetype, prefs=prefs, nodes=nodes, out_node=out_node, first_node=first_node, engine=engine)

    return {'FINISHED'}