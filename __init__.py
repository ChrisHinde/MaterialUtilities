# Material Utilities v3.0.2
#
#  Usage: Shift + Q in the 3D viewport or Shader Node Editor
#
# Ported from 2.6/2.7 to 2.8x+ by
#    Chris Hindefjord (chrishinde) 2019-2024
#
# ## Port based on 2010 version by MichaelW with some code added from latest 2.7x version
# ## Same code may be attributed to one of the following awesome people!
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
    "author": "ChrisHinde, MichaleW",
    "version": (3, 0, 2),
    "blender": (4, 2, 0),
    "location": "View3D > Shift + Q key",
    "description": "Menu of material tools (assign, select..) in the 3D View",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/materials/material_utils.html",
    "category": "Material"
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

if "bpy" in locals():
    import importlib
    if "enum_values" in locals():
        importlib.reload(enum_values)
    if "functions" in locals():
        importlib.reload(functions)
    if "operators" in locals():
        importlib.reload(operators)
    if "menues" in locals():
        importlib.reload(menus)
    if "preferences" in locals():
        importlib.reload(preferences)
else:
    from .enum_values import *
    from .functions import *
    from .operators import *
    from .menus import *
    from .preferences import *

import bpy
from bpy.props import (
    PointerProperty,
    )
from bpy.types import (
    AddonPreferences,
    PropertyGroup,
    )


# All classes used by Material Utilities, that need to be registered
classes = (
    VIEW3D_OT_materialutilities_assign_material_object,
    VIEW3D_OT_materialutilities_assign_material_edit,
    VIEW3D_OT_materialutilities_select_by_material_name,
    VIEW3D_OT_materialutilities_copy_material_to_others,

    VIEW3D_OT_materialutilities_clean_material_slots,
    VIEW3D_OT_materialutilities_remove_material_slot,
    VIEW3D_OT_materialutilities_remove_all_material_slots,

    VIEW3D_OT_materialutilities_replace_material,
    VIEW3D_OT_materialutilities_replace_multiple_materials,
    VIEW3D_OT_materialutilities_fake_user_set,
    VIEW3D_OT_materialutilities_change_material_link,

    MATERIAL_OT_materialutilities_merge_base_names,
    MATERIAL_OT_materialutilities_join_objects,
    MATERIAL_OT_materialutilities_auto_smooth_angle,
    MATERIAL_OT_materialutilities_remove_unused_materials,

    MATERIAL_OT_materialutilities_material_slot_move,

    VIEW3D_MT_materialutilities_assign_material,
    VIEW3D_MT_materialutilities_select_by_material,

    VIEW3D_MT_materialutilities_clean_slots,
    VIEW3D_MT_materialutilities_specials,

    VIEW3D_MT_materialutilities_main,

    NODE_OT_materialutilities_select_texture_files,
    NODE_OT_materialutilities_select_texture_directory,
    
    NODE_OT_materialutilities_add_image_textures,
    NODE_OT_materialutilities_replace_image_textures,
    NODE_MT_materialutilities_shadereditor_menu,
    
    VIEW3D_OT_materialutilities_assign_pbr_material,

    VIEW3D_MT_materialutilities_preferences
)


# This allows you to right click on a button and link to the manual
def materialutilities_manual_map():
    url_manual_prefix = "https://github.com/ChrisHinde/MaterialUtilities"
    url_manual_map = []

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

    bpy.types.VIEW3D_MT_object_context_menu.append(materialutilities_specials_menu)

    bpy.types.MATERIAL_MT_context_menu.prepend(materialutilities_menu_move)
    bpy.types.MATERIAL_MT_context_menu.append(materialutilities_menu_functions)

    mu_prefs = materialutilities_get_preferences(bpy.context)
    if mu_prefs.tex_add_to_editor_header:
        bpy.types.NODE_HT_header.append(materialutilities_shadereditor_menu)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name = "3D View", space_type = "VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', ctrl = False, shift = True)
        kmi.properties.name = VIEW3D_MT_materialutilities_main.bl_idname

        km_s = kc.keymaps.new(name = "Node Editor", space_type = "NODE_EDITOR")
        kmi_s = km_s.keymap_items.new('wm.call_menu', 'Q', 'PRESS', ctrl = False, shift = True)
        kmi_s.properties.name = NODE_MT_materialutilities_shadereditor_menu.bl_idname

        bpy.utils.register_manual_map(materialutilities_manual_map)


def unregister():
    """Unregister the classes of Material Utilities together with the default shortcut for the menu"""

    bpy.utils.unregister_manual_map(materialutilities_manual_map)

    bpy.types.VIEW3D_MT_object_context_menu.remove(materialutilities_specials_menu)

    bpy.types.MATERIAL_MT_context_menu.remove(materialutilities_menu_move)
    #kc = bpy.context.window_manager.keyconfigs.addon
    bpy.types.MATERIAL_MT_context_menu.remove(materialutilities_menu_functions)
    bpy.types.NODE_HT_header.remove(materialutilities_shadereditor_menu)

    keyconfigs = bpy.context.window_manager.keyconfigs
    defaultmap = keyconfigs.get("Blender").keymaps
    addonmap   = keyconfigs.get("Blender addon").keymaps

    km = addonmap["3D View"]
    for kmi in km.keymap_items:
        if kmi.idname == "wm.call_menu":
            if kmi.properties.name == VIEW3D_MT_materialutilities_main.bl_idname:
                km.keymap_items.remove(kmi)


    km = defaultmap["3D View"]
    for kmi in km.keymap_items:
        if kmi.idname == "wm.call_menu":
            if kmi.properties.name == VIEW3D_MT_materialutilities_main.bl_idname:
                km.keymap_items.remove(kmi)
                
    km = addonmap["Node Editor"]
    for kmi in km.keymap_items:
        if kmi.idname == "wm.call_menu":
            if kmi.properties.name == NODE_MT_materialutilities_shadereditor_menu.bl_idname:
                km.keymap_items.remove(kmi)


    km = defaultmap["Node Editor"]
    for kmi in km.keymap_items:
        if kmi.idname == "wm.call_menu":
            if kmi.properties.name == NODE_MT_materialutilities_shadereditor_menu.bl_idname:
                km.keymap_items.remove(kmi)

    mu_classes_unregister()

if __name__ == "__main__":
    register()
