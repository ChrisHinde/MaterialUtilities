# Ported from 2.6 (& 2.7) to 2.8 by
#    Christopher Hindefjord (chrishinde) 2019
#
# ## Port based on 2010 version by MichaelW with some code added from latest 2.7x version
# ## Same code may be attributed to one of the follwing awesome people!
#  (c) 2016 meta-androcto, parts based on work by Saidenka, lijenstina
#  Materials Utils: by MichaleW, lijenstina,
#       (some code thanks to: CoDEmanX, SynaGl0w, ideasman42)
#  Link to base names: Sybren, Texture renamer: Yadoob
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


* select by material
    in object mode this offers the user a menu of all materials in the blend
    file any objects using the selected material will become selected, any
    objects without the material will be removed from selection.

    in edit mode:  the menu offers only the materials attached to the current
    object. It will select the polygons that use the material and deselect those
    that do not.

* clean material slots
    for all selected objects any empty material slots or material slots with
    materials that are not used by the mesh polygons or splines will be removed.

* remove material slots
    removes all material slots of the active (or selected) object(s).

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
#import bmesh
#from bpy.types import EnumPropertyItem

from .enum_values import *
from .functions import *
from .operators import *


# -----------------------------------------------------------------------------
# menu classes  (To be moved to separate file)

class VIEW3D_MT_materialutilities_assign_material(bpy.types.Menu):
    """Menu for choosing which material should be assigned to current selection"""
    # The menu is filled programmatically with available materials

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
    """Menu for choosing which material should be used for selection"""
    # The menu is filled programmatically with available materials

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

class VIEW3D_MT_materialutilities_clean_slots(bpy.types.Menu):
    """Menu for cleaning up the material slots"""

    bl_idname = "VIEW3D_MT_materialutilities_clean_slots"
    bl_label = "Clean Slots"

    def draw(self, context):
        layout = self.layout

        layout.label
        layout.operator(VIEW3D_OT_materialutilities_clean_material_slots.bl_idname,
                        text = "Clean Material Slots",
                        icon = 'TRASH')
        layout.separator()
        layout.operator(VIEW3D_OT_materialutilities_remove_material_slot.bl_idname,
                        text = "Remove Active Material Slot",
                        icon = 'REMOVE')
        layout.operator(VIEW3D_OT_materialutilities_remove_all_material_slots.bl_idname,
                        text = "Remove All Material Slot",
                        icon = 'CANCEL')


class VIEW3D_MT_materialutilities_select_by_material(bpy.types.Menu):
    """Menu for choosing which material should be used for selection"""
    # The menu is filled programmatically with available materials

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

class VIEW3D_MT_materialutilities_specials(bpy.types.Menu):
    """Spcials menu for Material Utilities"""

    bl_idname = "VIEW3D_MT_materialutilities_specials"
    bl_label = "Specials"

    def draw(self, context):
        layout = self.layout

        #layout.operator(VIEW3D_OT_materialutilities_set_new_material_name.bl_idname, icon = "SETTINGS")

        layout.separator()

        layout.operator(MATERIAL_OT_materialutilities_merge_base_names.bl_idname,
                        text = "Merge Base Names",
                        icon = "GREASEPENCIL")


class VIEW3D_MT_materialutilities_main(bpy.types.Menu):
    """Main menu for Material Utilities"""

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
                         text = 'Copy materials to others',
                         icon = 'COPY_ID')

        layout.separator()

        layout.menu(VIEW3D_MT_materialutilities_clean_slots.bl_idname,
                    icon = 'NODE_MATERIAL')

        layout.separator()
        layout.operator(VIEW3D_OT_materialutilities_replace_material.bl_idname,
                        text = 'Replace Material',
                        icon = 'OVERLAY')

        layout.operator(VIEW3D_OT_materialutilities_fake_user_set.bl_idname,
                       text = 'Set Fake User',
                       icon = 'FAKE_USER_OFF')

        layout.operator(VIEW3D_OT_materialutilities_change_material_link.bl_idname,
                       text = 'Change Material Link',
                       icon = 'LINKED')
        layout.separator()

        layout.menu(VIEW3D_MT_materialutilities_specials.bl_idname,
                        icon = 'SOLO_ON')

classes = (
    VIEW3D_OT_materialutilities_assign_material_object,
    VIEW3D_OT_materialutilities_assign_material_edit,
    VIEW3D_OT_materialutilities_select_by_material_name,
    VIEW3D_OT_materialutilities_copy_material_to_others,

    VIEW3D_OT_materialutilities_clean_material_slots,
    VIEW3D_OT_materialutilities_remove_material_slot,
    VIEW3D_OT_materialutilities_remove_all_material_slots,

    VIEW3D_OT_materialutilities_replace_material,
    VIEW3D_OT_materialutilities_fake_user_set,
    VIEW3D_OT_materialutilities_change_material_link,

    MATERIAL_OT_materialutilities_merge_base_names,

    MATERIAL_OT_materialutilities_material_slot_move,

    VIEW3D_MT_materialutilities_assign_material,
    VIEW3D_MT_materialutilities_select_by_material,

    VIEW3D_MT_materialutilities_clean_slots,
    VIEW3D_MT_materialutilities_specials,

    VIEW3D_MT_materialutilities_main,
)

def materialutilities_specials_menu(self, contxt):
    self.layout.separator()
    self.layout.menu(VIEW3D_MT_materialutilities_main.bl_idname)


def materialutilities_menu_move(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'

    layout.operator(MATERIAL_OT_materialutilities_material_slot_move.bl_idname,
                    icon = 'TRIA_UP_BAR',
                    text = 'Move slot to top').movement = 'TOP'
    layout.operator(MATERIAL_OT_materialutilities_material_slot_move.bl_idname,
                    icon = 'TRIA_DOWN_BAR',
                    text = 'Move slot to bottom').movement = 'BOTTOM'
    layout.separator()

def materialutilities_menu_functions(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'

    layout.separator()

    layout.menu(VIEW3D_MT_materialutilities_assign_material.bl_idname,
                 icon = 'ADD')
    layout.menu(VIEW3D_MT_materialutilities_select_by_material.bl_idname,
                 icon = 'VIEWZOOM')
    layout.separator()

    layout.separator()

    layout.menu(VIEW3D_MT_materialutilities_clean_slots.bl_idname,
                icon = 'NODE_MATERIAL')

    layout.separator()
    layout.operator(VIEW3D_OT_materialutilities_replace_material.bl_idname,
                    text = 'Replace Material',
                    icon = 'OVERLAY')

    layout.operator(VIEW3D_OT_materialutilities_fake_user_set.bl_idname,
                   text = 'Set Fake User',
                   icon = 'FAKE_USER_OFF')

    layout.operator(VIEW3D_OT_materialutilities_change_material_link.bl_idname,
                   text = 'Change Material Link',
                   icon = 'LINKED')
    layout.separator()

    layout.menu(VIEW3D_MT_materialutilities_specials.bl_idname,
                    icon = 'SOLO_ON')

# This allows you to right click on a button and link to the manual
def materialutilities_manual_map():
    print("ManMap")
    url_manual_prefix = "https://github.com/ChrisHinde/MaterialUtils/"
    url_manual_map = []
    #url_manual_mapping = ()
        #("bpy.ops.view3d.materialutilities_*", ""),
        #("bpy.ops.view3d.materialutilities_assign_material_edit", ""),
        #("bpy.ops.view3d.materialutilities_select_by_material_name", ""),)

    for cls in classes:
        if issubclass(cls, bpy.types.Operator):
            url_manual_map.append(("bpy.ops." + cls.bl_idname, ""))

    url_manual_mapping = tuple(url_manual_map)
    #print(url_manual_mapping)
    return url_manual_prefix, url_manual_mapping

mu_classes_register, mu_classes_unregister = bpy.utils.register_classes_factory(classes)


def register():
    """Register the classes of Material Utilities together with the default shortcut (Shift+Q)"""
    mu_classes_register()


    bpy.types.MATERIAL_MT_specials.prepend(materialutilities_menu_move)
    bpy.types.MATERIAL_MT_specials.append(materialutilities_menu_functions)

    bpy.types.VIEW3D_MT_object_specials.append(materialutilities_specials_menu)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name = "3D View", space_type = "VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', ctrl = False, shift = True)
        kmi.properties.name = VIEW3D_MT_materialutilities_main.bl_idname

        bpy.utils.register_manual_map(materialutilities_manual_map)


def unregister():
    """Unregister the classes of Material Utilities together with the default shortcut for the menu"""
    mu_classes_unregister()

    bpy.utils.unregister_manual_map(materialutilities_manual_map)

    bpy.types.VIEW3D_MT_object_specials.remove(materialutilities_specials_menu)

    bpy.types.MATERIAL_MT_specials.remove(materialutilities_menu_move)
    bpy.types.MATERIAL_MT_specials.remove(materialutilities_menu_functions)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["3D View"]
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == VIEW3D_MT_materialutilities_main.bl_idname:
                    km.keymap_items.remove(kmi)
                    break

if __name__ == "__main__":
    register()

#print("MU Start!")
#mu_register()
