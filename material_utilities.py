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
    set up materials to assign the UV images per-face. It will use the first
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
from bpy.props import StringProperty, BoolProperty, EnumProperty


# -----------------------------------------------------------------------------
# menu classes

class VIEW3D_MT_MaterialUtilsMasterMenu(bpy.types.Menu):
    bl_label: "Material Utils Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

#        layout.menu("VIEW3D_MT_assign_material", icon='ZOOMIN')
        layout.menu("VIEW3D_MT_MaterialUtilsSelectMaterialMenu", icon='HAND')
#        layout.separator()
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


class VIEW3D_MT_MaterialUtilsSelectMaterialMenu(bpy.types.Menu):
    bl_label: "Select by Material"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        ob = context.object
        layout.label
        if ob.mode == 'OBJECT':
            #show all used materials in entire blend file
            for material_name, material in bpy.data.materials.items():
                if material.users > 0:
                    layout.operator("view3d.select_material_by_name",
                                    text=material_name,
                                    icon='MATERIAL_DATA',
                                    ).matname = material_name

        elif ob.mode == 'EDIT':
            #show only the materials on this object
            mats = ob.material_slots.keys()
            for m in mats:
                layout.operator("view3d.select_material_by_name",
                    text=m,
                    icon='MATERIAL_DATA').matname = m


classes = (
    VIEW3D_MT_MaterialUtilsMasterMenu,
    MUSelectMaterialMenu
)

def register():
    bpy.utils.register_classes_factory(classes)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', ctrl=False, shift=True)
        kmi.properties.name = "VIEW3D_MT_MaterialUtilsMasterMenu"


def unregister():
    for cls in reversed(mu_classes):
        bpy.utils.unregister_class(cls)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["3D View"]
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "VIEW3D_MT_MaterialUtilsMasterMenu":
                    km.keymap_items.remove(kmi)
                    break

if __name__ == "__main__":
    register()
