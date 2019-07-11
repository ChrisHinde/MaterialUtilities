import bpy

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
                        icon = 'X')
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
