# Ported from 2.6 (& 2.7) to 2.8 by
#    Christopher Hindefjord (chrishinde) 2019
#
# ## Original:
#   (c) 2010 Michael Williamson (michaelw)
#   ported from original by Michael Williamson
# ###
#
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Material Utilities",
    "author": "chrishinde",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Shift + Q key",
    "description": "Menu of material tools (assign, select..) in the 3D View",
    "warning": "Under development!",
    "wiki_url": "https://github.com/ChrisHinde/MaterialUtils",
    "category": "Materials"
}

"""
This script has several functions and operators, grouped for convenience:

* assign material:
    offers the user a list of ALL the materials in the blend file and an
    additional "new" entry the chosen material will be assigned to all the
    selected objects in object mode.

    in edit mode the selected polygons get the selected material applied.

    if the user chose "new" the new material can be renamed using the
    "last operator" section of the toolbox.
    After assigning the material "clean material slots" and
    "material to texface" are auto run to keep things tidy
    (see description bellow)


* select by material
    in object mode this offers the user a menu of all materials in the blend
    file any objects using the selected material will become selected, any
    objects without the material will be removed from selection.

    in edit mode:  the menu offers only the materials attached to the current
    object. It will select the polygons that use the material and deselect those
    that do not.

* clean material slots
    for all selected objects any empty material slots or material slots with
    materials that are not used by the mesh polygons will be removed.

* remove material slots
    removes all material slots of the active object.

* material to texface
    transfers material assignments to the UV editor. This is useful if you
    assigned materials in the properties editor, as it will use the already
    set up materials to assign the UV imag  es per-face. It will use the first
    enabled image texture it finds.

* texface to materials
    creates texture materials from images assigned in UV editor.

* replace materials
    lets your replace one material by another. Optionally for all objects in
    the blend, otherwise for selected editable objects only. An additional
    option allows you to update object selection, to indicate which objects
    were affected and which not.

* set fake user
    enable/disable fake user for materials. You can chose for which materials
    it shall be set, materials of active / selected / objects in current scene
    or used / unused / all materials.

"""


import bpy
import bmesh
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty
#from bpy.types import EnumPropertyItem

#from .functions import *

# -----------------------------------------------------------------------------
# functions  (To be moved to separate file)


def mu_assign_material_slots(obj, material_list):
    """Given an object and a list of material names removes all material slots from the object
       adds new ones for each material in matlist adds the materials to the slots as well."""

    scn = bpy.context.scene
    active_obj = bpy.context.active_object
    bpy.context.view_layer.objects.active = obj

    for s in obj.material_slots:
        bpy.ops.object.material_slot_remove()

    # re-add them and assign material
    i = 0
    for mat in material_list:
        material = bpy.data.materials[mat]
        obj.data.materials.append(material)
        i += 1

    # restore active object:
    bpy.context.view_layer.objects.active = ob_active


def mu_assign_material(self, material_name = "Default", override_type = 'APPEND_MATERIAL'):
    """Assign the defined material to selected polygons/objects"""

    print("ASSMat: " + material_name + " : " + override_type)

    # get active object so we can restore it later
    active_obj = bpy.context.active_object

    # check if material exists, if it doesn't then create it
    found = False
    for material in bpy.data.materials:
        if material.name == material_name:
            target = material
            found = True
            break

    if not found:
        target = bpy.data.materials.new(material_name)
        target.use_nodes = True         # When do we not want nodes today?


    editmode = False
    allpolygons = True
    if active_obj.mode == 'EDIT':
        editmode = True
        allpolygons = False
        bpy.ops.object.mode_set()

    index = 0
    objects = bpy.context.selected_editable_objects

    for obj in objects:
        # set the active object to our object
        scn = bpy.context.scene
        bpy.context.view_layer.objects.active = obj


        # If we should override all current material slots
        if override_type == 'OVERRIDE_ALL' or obj.type == 'META':
            # Clear out the material slots
            obj.data.materials.clear()
            # and then append the target material (no need spend time on assigning to each ploygon)
            obj.data.materials.append(target)

            if obj.type == 'META':
                self.report({'INFO'}, "Meta balls only support one material, all other materials overriden!")

        # If we should override each material slot
        elif override_type == 'OVERRIDE_SLOTS':
            i = 0
            # go through each slot
            for material in obj.material_slots:
                # assign the target material to current slot
                obj.data.materials[i] = target
                i += 1

        # if we should keep the material slots and just append the selected material (if not already assigned)
        elif override_type == 'APPEND_MATERIAL':
            found = False
            i = 0
            material_slots = obj.material_slots

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
                # the material is not attached to the object
                if (len(obj.data.materials) == 1) and not editmode:
                    # in object mode, override the material if it's just one slot used
                    obj.data.materials[0] = target
                    index = 0
                else:
                    # In Edit mode, or if there's not a slot, append the assigned material
                    #  If we're overriding, there's currently no materials at all, so after this there will be 1
                    #  If not, this adds another slot with the assigned material
                    index = len(obj.data.materials)
                    obj.data.materials.append(target)
                    obj.active_material_index = index

            if obj.type == 'MESH':
                # now assign the material to the mesh
                mesh = obj.data
                if allpolygons:
                    for poly in mesh.polygons:
                        poly.material_index = index
                elif allpolygons == False:
                    for poly in mesh.polygons:
                        if poly.select:
                            poly.material_index = index

                mesh.update()

            elif obj.type in {'CURVE', 'SURFACE', 'TEXT'}:
                bpy.ops.object.mode_set(mode='EDIT')    # This only works in Edit mode

                # If operator was run in Object mode
                if not editmode:
                    # Select everything in Edit mode
                    bpy.ops.curve.select_all(action='SELECT')

                bpy.ops.object.material_slot_assign()   # Assign material of the current slot to selection

                if not editmode:
                    bpy.ops.object.mode_set(mode='OBJECT')

    #restore the active object
    bpy.context.view_layer.objects.active = active_obj

    if editmode:
        bpy.ops.object.mode_set(mode='EDIT')

    print("End of Assign material!")
    return {'FINISHED'}

def mu_select_by_material_name(self, find_material_name, extend_selection = False):
    """Searches through all objects, or the polygons/curves of the current object
    to find and select objects/data with the desired material"""

    # in object mode selects all objects with material find_material_name
    # in edit mode selects all polygons with material find_material_name

    find_material = bpy.data.materials.get(find_material_name)

    if find_material is None:
        self.report({'INFO'}, "The material " + find_material_name + " doesn't exists!")
        return {'CANCELLED'}

    # check for editmode
    editmode = False
    found_material = False

    scn = bpy.context.scene

    # set selection mode to polygons
    scn.tool_settings.mesh_select_mode = False, False, True

    active_obj = bpy.context.active_object

    if active_obj.mode == 'EDIT':
        editmode = True

    if not editmode:
        objects = bpy.data.objects
        for obj in objects:
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
                mat_slots = obj.material_slots
                for material in mat_slots:
                    if material.material == find_material:
                        obj.select_set(state=True)

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
            self.report({'INFO'}, "No objects found with the material " + find_material_name + "!")
            return {'CANCELLED'}

    else:
        # it's editmode, so select the polygons

        obj = active_obj

        if obj.type == 'MESH':
            # if not extending the selection, deselect all first
            #  (Without this, edges/faces were still selected
            #   while the faces were deselcted)
            if not extend_selection:
                bpy.ops.mesh.select_all(action='DESELECT')

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

            bpy.ops.object.mode_set(mode='EDIT')

            if not found_material:
                self.report({'INFO'}, "Material " + find_material_name + " isn't assigned to any faces!")
                return {'CANCELLED'}

        elif obj.type in {'CURVE', 'SURFACE'}:
            # For Curve objects, there can only be one material per spline
            #  and thus each spline is linked to one material slot.
            #  So to not have to care for different data structures for different curve types,
            #  we use the material slots and the built in selection methods
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

            if not found_material:
                self.report({'INFO'}, "Material " + find_material_name + " isn't assigned to slots!")

        else:
            # Some object types are not supported
            #  mostly because don't really support selecting by material (like Font/Text objects)
            #  ore that they don't support multiple materials/are just "weird" (i.e. Meta balls)
            self.report({'WARNING'}, "The type '" + obj.type + "' isn't supported in Edit mode by Material Utilities!")
            return {'CANCELLED'}

    return {'FINISHED'}

def mu_copy_material_to_others(self):
    #active_object = context.active_object

    bpy.ops.object.material_slot_copy()

    return {'FINISHED'}

# -----------------------------------------------------------------------------
# operator classes (To be moved to separate file)

class VIEW3D_OT_materialutilities_assign_material_edit(bpy.types.Operator):
    """Assign a material to the current selection"""

    bl_idname = "view3d.materialutilities_assign_material_edit"
    bl_label = "Assign Material (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: StringProperty(
            name = 'Material Name',
            description = 'Name of Material to assign to current selection',
            default = "",
            maxlen = 63,
            )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        material_name = self.material_name
        return mu_assign_material(self, material_name, 'APPEND_MATERIAL')
        #cleanmatslots()
        #mat_to_texface()

override_types = [
    ('OVERRIDE_ALL', "Override all assigned slots",
        "Remove any current material slots, and assign the current material"),
    ('OVERRIDE_SLOTS', 'Assign material to each slot',
        'Keep the material slots, but assign the selected material in each slot'),
    ('APPEND_MATERIAL', 'Append Material',
        'Add the material in a new slot, and assign it to the whole object')
]

class VIEW3D_OT_materialutilities_assign_material_object(bpy.types.Operator):
    """Assign a material to the current selection"""

    bl_idname = "view3d.materialutilities_assign_material_object"
    bl_label = "Assign Material (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: StringProperty(
            name = 'Material Name',
            description = 'Name of Material to assign to current selection',
            default = "",
            maxlen = 63,
            )
    override_type: EnumProperty(
            name = 'Assignment method',
            description = '',
            items = override_types
            )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        material_name = self.material_name
        override_type = self.override_type
        result = mu_assign_material(self, material_name, override_type)
        print("Material Assigned!")
        #cleanmatslots()
        #mat_to_texface()
        return result


class VIEW3D_OT_materialutilities_select_by_material_name(bpy.types.Operator):
    """Select geometry that has the defined material assigned to it
    It also allows the user to extend what's currently selected"""

    bl_idname = "view3d.materialutilities_select_by_material_name"
    bl_label = "Select By Material Name (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    extend: BoolProperty(
            name = 'Extend Selection',
            description = 'Keeps the current selection and adds faces with the material to the selection'
            )
    material_name: StringProperty(
            name = 'Material Name',
            description = 'Name of Material to Select',
            maxlen = 63,
            )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        material_name = self.material_name
        ext = self.extend
        return mu_select_by_material_name(self, material_name, ext)


class VIEW3D_OT_materialutilities_copy_material_to_others(bpy.types.Operator):
    """Copy the material(s) of the active object to other select objects"""

    bl_idname = "view3d.materialutilities_copy_material_to_others"
    bl_label = "Copy material(s) to others (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None) and (context.active_object.mode != 'EDIT')

    def execute(self, context):
        return mu_copy_material_to_others(self)

# -----------------------------------------------------------------------------
# menu classes  (To be moved to separate file)

class VIEW3D_MT_materialutilities_assign_material(bpy.types.Menu):
    """Submenu for selecting which material should be assigned to current selection
    The menu is filled programmatically with available materials"""

    bl_idname = "VIEW3D_MT_materialutilities_assign_material"
    bl_label = "Assign Material"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        bl_id = VIEW3D_OT_materialutilities_assign_material_object.bl_idname
        obj = context.object

        if obj.mode == 'EDIT':
            bl_id = VIEW3D_OT_materialutilities_assign_material_edit.bl_idname

        for material_name in bpy.data.materials.keys():
            layout.operator(bl_id,
                text = material_name,
                icon = 'MATERIAL_DATA').material_name = material_name

        layout.operator(bl_id,
                        text = "Add New Material",
                        icon = 'ADD')

class VIEW3D_MT_materialutilities_select_by_material(bpy.types.Menu):
    """Submenu for selecting which material should be used for selection
    The menu is filled programmatically with available materials"""

    bl_idname = "VIEW3D_MT_materialutilities_select_by_material"
    bl_label = "Select by Material"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        layout.label
        if obj.mode == 'OBJECT':
            #show all used materials in entire blend file
            for material_name, material in bpy.data.materials.items():
                # There's no point in showing materials with 0 users
                #  (It will still show materials with fake user though)
                if material.users > 0:
                    layout.operator(VIEW3D_OT_materialutilities_select_by_material_name.bl_idname,
                                    text = material_name,
                                    icon = 'MATERIAL_DATA',
                                    ).material_name = material_name

        elif obj.mode == 'EDIT':
            #show only the materials on this object
            materials = obj.material_slots.keys()
            for material in materials:
                layout.operator(VIEW3D_OT_materialutilities_select_by_material_name.bl_idname,
                    text = material,
                    icon = 'MATERIAL_DATA').material_name = material

class VIEW3D_MT_materialutilities_select_by_material(bpy.types.Menu):
    """Submenu for selecting which material should be used for selection
    The menu is filled programmatically with available materials"""

    bl_idname = "VIEW3D_MT_materialutilities_select_by_material"
    bl_label = "Select by Material"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        layout.label
        if obj.mode == 'OBJECT':
            #show all used materials in entire blend file
            for material_name, material in bpy.data.materials.items():
                # There's no point in showing materials with 0 users
                #  (It will still show materials with fake user though)
                if material.users > 0:
                    layout.operator(VIEW3D_OT_materialutilities_select_by_material_name.bl_idname,
                                    text = material_name,
                                    icon = 'MATERIAL_DATA',
                                    ).material_name = material_name

        elif obj.mode == 'EDIT':
            #show only the materials on this object
            materials = obj.material_slots.keys()
            for material in materials:
                layout.operator(VIEW3D_OT_materialutilities_select_by_material_name.bl_idname,
                    text = material,
                    icon = 'MATERIAL_DATA').material_name = material

class VIEW3D_MT_materialutilities_main(bpy.types.Menu):
    """Main menu for the Material utilities"""

    bl_idname = "VIEW3D_MT_materialutilities_main"
    bl_label = "Material Utilities"

    def draw(self, context):
        obj = context.object

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.menu(VIEW3D_MT_materialutilities_assign_material.bl_idname,
                     icon = 'ADD')
        layout.menu(VIEW3D_MT_materialutilities_select_by_material.bl_idname,
                     icon = 'VIEWZOOM')
        layout.separator()

        layout.operator(VIEW3D_OT_materialutilities_copy_material_to_others.bl_idname,
                         text = 'Copy material to others',
                         icon = 'COPY_ID')

        layout.separator()

#        layout.operator("view3d.clean_material_slots",
#                        text="Clean Material Slots",
#                        icon='CANCEL')
#        layout.operator("view3d.material_remove",
#                        text="Remove Material Slots",
#                        icon='CANCEL')
#        layout.operator("view3d.material_to_texface",
#                        text="Material to Texface",
#                        icon='MATERIAL_DATA')
#        layout.operator("view3d.texface_to_material",
#                        text="Texface to Material",
#                        icon='MATERIAL_DATA')

        layout.separator()
#        layout.operator("view3d.replace_material",
#                        text='Replace Material',
#                        icon='ARROW_LEFTRIGHT')

#        layout.operator("view3d.fake_user_set",
#                        text='Set Fake User',
#                        icon='UNPINNED')

# This allows you to right click on a button and link to the manual
def materialutilities_manual_map():
    url_manual_prefix = "https://github.com/ChrisHinde/MaterialUtils/"
    url_manual_mapping = (
        ("bpy.ops.view3d.materialutilities_assign_material_object", ""),
        ("bpy.ops.view3d.materialutilities_assign_material_edit", ""),
        ("bpy.ops.view3d.materialutilities_select_by_material_name", ""),
    )
    return url_manual_prefix, url_manual_mapping

classes = (
    VIEW3D_OT_materialutilities_assign_material_object,
    VIEW3D_OT_materialutilities_assign_material_edit,
    VIEW3D_OT_materialutilities_select_by_material_name,
    VIEW3D_OT_materialutilities_copy_material_to_others,

    VIEW3D_MT_materialutilities_assign_material,
    VIEW3D_MT_materialutilities_select_by_material,
    VIEW3D_MT_materialutilities_main,
)


register, unregister = bpy.utils.register_classes_factory(classes)


def mu_register():
    """Register the classes of Material Utilities together with the default shortcut (Shift+Q)"""
    register()

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name = "3D View", space_type = "VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', ctrl = False, shift = True)
        kmi.properties.name = VIEW3D_MT_materialutilities_main.bl_idname

        bpy.utils.register_manual_map(materialutilities_manual_map)


def mu_unregister():
    """Unregister the classes of Material Utilities together with the default shortcut for the menu"""
    unregister()

    bpy.utils.unregister_manual_map(materialutilities_manual_map)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["3D View"]
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == VIEW3D_MT_materialutilities_main.bl_idname:
                    km.keymap_items.remove(kmi)
                    break

#if __name__ == "__main__":
#    mu_register()

print("MU Start!")
mu_register()
