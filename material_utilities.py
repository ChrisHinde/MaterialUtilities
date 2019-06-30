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
    "blender": (2, 8, 0),
    "location": "View3D > Shift + Q key",
    "description": "Menu of material tools (assign, select..) in the 3D View",
    "warning": "Under development!"}

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
from bpy.props import StringProperty, BoolProperty, EnumProperty

#from .functions import *

# -----------------------------------------------------------------------------
# functions  (To be moved to separate file)

def mu_select_by_material_name(self, find_material_name, extend_selection=False):
    """Searches through all (mesh) objects, or the polygons of the current object
    to find and select objects/polygons with the desired material"""

    # in object mode selects all objects with material find_material_name
    # in edit mode selects all polygons with material find_material_name

    find_material = bpy.data.materials.get(find_material_name)

    if find_material is None:
        return

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
        objs = bpy.data.objects
        for obj in objs:
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
    else:
        # it's editmode, so select the polygons

        # if not extending the selection, deselect all first
        #  (Without this, edges/faces were still selected
        #   while the faces were deselcted)
        if not extend_selection:
            bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set()

        obj = active_obj
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

        if not found_material:
            self.report({'INFO'}, "Material " + find_material_name + " isn't assigned to any faces!")

        bpy.ops.object.mode_set(mode='EDIT')

# -----------------------------------------------------------------------------
# operator classes (To be moved to separate file)



class VIEW3D_OT_materialutilities_select_by_material_name(bpy.types.Operator):
    """Select geometry that has the defined material assigned to it
    It also allows the user to extend what's currently selected"""
    bl_idname = "view3d.materialutilities_select_by_material_name"
    bl_label = "Select By Material Name (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    extend: BoolProperty(
            name='Extend Selection',
            description='Keeps the current selection and adds faces with the material to the selection'
            )
    matname: StringProperty(
            name='Material Name',
            description='Name of Material to Select',
            maxlen=63,
            )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        material_name = self.matname
        ext = self.extend
        mu_select_by_material_name(self, material_name, ext)
        return {'FINISHED'}

# -----------------------------------------------------------------------------
# menu classes  (To be moved to separate file)


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
                                    text=material_name,
                                    icon='MATERIAL_DATA',
                                    ).matname = material_name

        elif obj.mode == 'EDIT':
            #show only the materials on this object
            mats = obj.material_slots.keys()
            for m in mats:
                layout.operator(VIEW3D_OT_materialutilities_select_by_material_name.bl_idname,
                    text=m,
                    icon='MATERIAL_DATA').matname = m


class VIEW3D_MT_materialutilities_main(bpy.types.Menu):
    """Main menu for the Material utilities"""

    bl_idname = "VIEW3D_MT_materialutilities_main"
    bl_label = "Material Utilities"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.menu(VIEW3D_MT_materialutilities_select_by_material.bl_idname, icon='VIEWZOOM')
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

classes = (
    VIEW3D_OT_materialutilities_select_by_material_name,

    VIEW3D_MT_materialutilities_select_by_material,
    VIEW3D_MT_materialutilities_main,
)

register, unregister = bpy.utils.register_classes_factory(classes)

def mu_register():
    """Register the classes of Material Utilities together with the default shortcut (Shift+Q)"""
    register()

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', ctrl=False, shift=True)
        kmi.properties.name = VIEW3D_MT_materialutilities_main.bl_idname


def mu_unregister():
    """Unregister the classes of Material Utilities together with the default shortcut for the menu"""
    unregister()
#    for cls in reversed(classes):
#        unregister_class(cls)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["3D View"]
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == VIEW3D_MT_materialutilities_main.bl_idname:
                    km.keymap_items.remove(kmi)
                    break

#if __name__ == "__main__":
#    register()

print("MU Start!")
mu_register()
