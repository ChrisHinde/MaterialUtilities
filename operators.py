import bpy

from bpy.types import Operator
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty,
    IntProperty,
    FloatProperty,
    PointerProperty,
    CollectionProperty
    )


from .enum_values import *
from .functions import *
from .preferences import *

from types import SimpleNamespace

from math import radians

# -----------------------------------------------------------------------------
# operator classes

class VIEW3D_OT_materialutilities_assign_material_edit(bpy.types.Operator):
    """Assign a material to the current selection"""

    bl_idname = "view3d.materialutilities_assign_material_edit"
    bl_label = "Assign Material (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: StringProperty(
            name = 'Material Name',
            description = 'Name of Material to assign to current selection',
            default = "",
            maxlen = 63
            )
    new_material: BoolProperty(
            name = '',
            description = 'Add a new material, enter the name in the box',
            default = False
            )
    show_dialog: BoolProperty(
            name = 'Show Dialog',
            default = False
            )
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        if event.shift or event.ctrl:
            return bpy.ops.view3d.materialutilities_assign_pbr_material('INVOKE_DEFAULT')
        if self.show_dialog:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def draw(self, context):
        mu_prefs = materialutilities_get_preferences(context)
        factor = 0.85 if mu_prefs.add_pbr_import_to_assign_dlg else 0.9

        layout = self.layout

        col = layout.column()
        row = col.split(factor=factor, align=True)

        if self.new_material:
            row.prop(self, "material_name")
        else:
            row.prop_search(self, "material_name", bpy.data, "materials")

        row.prop(self, "new_material", expand = True, icon = 'ADD')

        if mu_prefs.add_pbr_import_to_assign_dlg:
            row.operator(VIEW3D_OT_materialutilities_assign_pbr_material.bl_idname, text="", icon='FILE_IMAGE')

    def execute(self, context):
        material_name = self.material_name

        if self.new_material:
            material_name = mu_new_material_name(material_name)
        elif material_name == "":
            self.report({'WARNING'}, "No Material Name given!")
            return {'CANCELLED'}

        return mu_assign_material(self, material_name, 'APPEND_MATERIAL')


class VIEW3D_OT_materialutilities_assign_material_object(bpy.types.Operator):
    """Assign a material to the current selection
    (See the operator panel [F9] for more options)"""

    bl_idname = "view3d.materialutilities_assign_material_object"
    bl_label = "Assign Material (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: StringProperty(
            name = 'Material Name',
            description = 'Name of Material to assign to current selection',
            default = "",
            maxlen = 63
            )
    override_type: EnumProperty(
            name = 'Assignment method',
            description = '',
            items = mu_override_type_enums
            )
    new_material: BoolProperty(
            name = '',
            description = 'Add a new material\nEnter a name for the new material in the box',
            default = False
            )
    show_dialog: BoolProperty(
            name = 'Show Dialog',
            default = False
            )

    @classmethod
    def poll(cls, context):
        return len(context.selected_editable_objects) > 0

    def invoke(self, context, event):
        if event.shift or event.ctrl:
            return bpy.ops.view3d.materialutilities_assign_pbr_material('INVOKE_DEFAULT')
        if self.show_dialog:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def draw(self, context):
        mu_prefs = materialutilities_get_preferences(context)
        factor = 0.85 if mu_prefs.add_pbr_import_to_assign_dlg else 0.9

        layout = self.layout

        col = layout.column()
        row = col.split(factor=factor, align = True)

        if self.new_material:
            row.prop(self, "material_name")
        else:
            row.prop_search(self, "material_name", bpy.data, "materials")

        row.prop(self, "new_material", expand = True, icon = 'ADD')

        if mu_prefs.add_pbr_import_to_assign_dlg:
            row.operator(VIEW3D_OT_materialutilities_assign_pbr_material.bl_idname, text="", icon='FILE_IMAGE')

        layout.prop(self, "override_type")


    def execute(self, context):
        material_name = self.material_name
        override_type = self.override_type

        if self.new_material:
            material_name = mu_new_material_name(material_name)
        elif material_name == "":
            self.report({'WARNING'}, "No Material Name given!")
            return {'CANCELLED'}

        result = mu_assign_material(self, material_name, override_type)
        return result

class VIEW3D_OT_materialutilities_select_by_material_name(bpy.types.Operator):
    """Select geometry that has the chosen material assigned to it
    (See the operator panel [F9] for more options)"""

    bl_idname = "view3d.materialutilities_select_by_material_name"
    bl_label = "Select By Material Name (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    extend_selection: BoolProperty(
            name = 'Extend Selection',
            description = 'Keeps the current selection and adds faces with the material to the selection'
            )
    material_name: StringProperty(
            name = 'Material Name',
            description = 'Name of Material to find and Select',
            maxlen = 63
            )
    show_dialog: BoolProperty(
            name = 'Show Dialog',
            default = False
    )

    @classmethod
    def poll(cls, context):
        return len(context.visible_objects) > 0

    def invoke(self, context, event):
        if self.show_dialog:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.prop_search(self, "material_name", bpy.data, "materials")

        layout.prop(self, "extend_selection", icon = "SELECT_EXTEND")

    def execute(self, context):
        material_name = self.material_name
        ext = self.extend_selection
        return mu_select_by_material_name(self, material_name, ext)


class VIEW3D_OT_materialutilities_copy_material_to_others(bpy.types.Operator):
    """Copy the material(s) of the active object to the other selected objects"""

    bl_idname = "view3d.materialutilities_copy_material_to_others"
    bl_label = "Copy material(s) to others (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False

        # Only enable in Edit mode if Face selection is enabled
        if context.active_object.mode == 'EDIT':
            return bpy.context.scene.tool_settings.mesh_select_mode[2]
        else:
            return True

    def execute(self, context):
        return mu_copy_material_to_others(self)


class VIEW3D_OT_materialutilities_clean_material_slots(bpy.types.Operator):
    """Removes any material slots from the selected objects that are not used"""

    bl_idname = "view3d.materialutilities_clean_material_slots"
    bl_label = "Clean Material Slots (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    only_active: BoolProperty(
            name = 'Only active object',
            description = 'Only remove the material slots for the active object ' +
                            '(otherwise do it for every selected object)',
            default = True
            )

    @classmethod
    def poll(cls, context):
        return len(context.selected_editable_objects) > 0

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "only_active", icon = "PIVOT_ACTIVE")

    def execute(self, context):
        affect = "ACTIVE" if self.only_active else "SELECTED"

        return mu_cleanmatslots(self, affect)


class VIEW3D_OT_materialutilities_remove_material_slot(bpy.types.Operator):
    """Remove the active material slot from selected object(s)
    (See the operator panel [F9] for more options)"""

    bl_idname = "view3d.materialutilities_remove_material_slot"
    bl_label = "Remove Active Material Slot (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    only_active: BoolProperty(
            name = 'Only active object',
            description = 'Only remove the active material slot for the active object ' +
                            '(otherwise do it for every selected object)',
            default = True
            )

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None) and (context.active_object.mode != 'EDIT')

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "only_active", icon = "PIVOT_ACTIVE")

    def execute(self, context):
        return mu_remove_material(self, self.only_active)

class VIEW3D_OT_materialutilities_remove_all_material_slots(bpy.types.Operator):
    """Remove all material slots from selected object(s)
    (See the operator panel [F9] for more options)"""

    bl_idname = "view3d.materialutilities_remove_all_material_slots"
    bl_label = "Remove All Material Slots (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    only_active: BoolProperty(
            name = 'Only active object',
            description = 'Only remove the material slots for the active object ' +
                            '(otherwise do it for every selected object)',
            default = True
            )

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None) and (context.active_object.mode != 'EDIT')

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "only_active", icon = "PIVOT_ACTIVE")

    def execute(self, context):
        return mu_remove_all_materials(self, self.only_active)


class VIEW3D_OT_materialutilities_replace_material(bpy.types.Operator):
    """Replace a material by name"""
    bl_idname = "view3d.materialutilities_replace_material"
    bl_label = "Replace Material (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    mat_org: StringProperty(
            name = "Original",
            description = "Material to find and replace",
            maxlen = 63,
            )
    mat_rep: StringProperty(name="Replacement",
            description = "Material that will be used instead of the Original material",
            maxlen = 63,
            )
    all_objects: BoolProperty(
            name = "All Objects",
            description = "Replace for all objects in this blend file (otherwise only selected objects)",
            default = True,
            )
    update_selection: BoolProperty(
            name = "Update Selection",
            description = "Select affected objects and deselect unaffected",
            default = True,
            )

    def draw(self, context):
        layout = self.layout

        layout.prop_search(self, "mat_org", bpy.data, "materials")
        layout.prop_search(self, "mat_rep", bpy.data, "materials")
        layout.separator()

        layout.prop(self, "all_objects", icon = "BLANK1")
        layout.prop(self, "update_selection", icon = "SELECT_INTERSECT")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        return mu_replace_material(self, self.mat_org, self.mat_rep, self.all_objects, self.update_selection)


class VIEW3D_OT_materialutilities_replace_multiple_materials(bpy.types.Operator):
    """Replace a list of material by names"""
    bl_idname = "view3d.materialutilities_replace_multiple_materials"
    bl_label = "Replace Multiple Material (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    mats_org: StringProperty(
            name = "Original",
            description = "Materials to find and replace",
            maxlen = 63
            )
    mats_rep: StringProperty(
            name = "Replacement",
            description = "Materials that will be used instead of the Original material",
            maxlen = 63
            )
    all_objects: BoolProperty(
            name = "All Objects",
            description = "Replace for all objects in this blend file (otherwise only selected objects)",
            default = True,
            )
    update_selection: BoolProperty(
            name = "Update Selection",
            description = "Select affected objects and deselect unaffected",
            default = True,
            )

    def draw(self, context):
        layout = self.layout

        layout.prop_search(self, "mats_org", bpy.data, "texts")
        layout.prop_search(self, "mats_rep", bpy.data, "texts")
        layout.separator()

        layout.prop(self, "all_objects", icon = "BLANK1")
        layout.prop(self, "update_selection", icon = "SELECT_INTERSECT")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        return mu_replace_multiple_materials(self, self.mats_org, self.mats_rep, self.all_objects, self.update_selection)

class VIEW3D_OT_materialutilities_fake_user_set(bpy.types.Operator):
    """Enable/disable fake user for materials"""

    bl_idname = "view3d.materialutilities_fake_user_set"
    bl_label = "Set Fake User (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    fake_user: EnumProperty(
            name = "Fake User",
            description = "Turn fake user on or off",
            items = mu_fake_user_set_enums,
            default = 'TOGGLE'
            )

    affect: EnumProperty(
            name = "Affect",
            description = "Which object's materials to affect",
            items = mu_fake_user_affect_enums,
            default = 'UNUSED'
            )
    selected_collection: StringProperty(
            name = "Collection",
            description = "Affect materials of the objects in this selected collection",
            default = ""
    )

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "fake_user", expand = True)
        layout.separator()

        layout.prop(self, "affect")

        if self.affect == 'SELECTED_COLLECTION':
            layout.prop_search(self, "selected_collection", bpy.data, "collections")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        return mu_set_fake_user(self, self.fake_user, self.affect, self.selected_collection)


class VIEW3D_OT_materialutilities_change_material_link(bpy.types.Operator):
    """Link the materials to Data or Object, while keepng materials assigned"""

    bl_idname = "view3d.materialutilities_change_material_link"
    bl_label = "Change Material Linking (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    override: BoolProperty(
            name = "Override Data material",
            description = "Override the materials assigned to the object data/mesh when switching to 'Linked to Data'\n" +
                            "(WARNING: This will override the materials of other linked objects, " +
                             "which have the materials linked to Data)",
            default = False,
            )
    unlink_old: BoolProperty(
            name = "Unlink Material From Old Link",
            description = "Unlink the material from what it is currently linked to, before it gets linked to the new option",
            default = False,
            )
    link_to: EnumProperty(
            name = "Link",
            description = "What should the material be linked to",
            items = mu_link_to_enums,
            default = 'OBJECT'
            )

    affect: EnumProperty(
            name = "Affect",
            description = "Which materials of objects to affect",
            items = mu_link_affect_enums,
            default = 'SELECTED'
            )
    selected_collection: StringProperty(
            name = "Collection",
            description = "Affect materials of the objects in this selected collection",
            default = ""
    )

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "link_to", expand = True)
        layout.separator()

        layout.prop(self, "affect")

        if self.affect == 'SELECTED_COLLECTION':
            layout.prop_search(self, "selected_collection", bpy.data, "collections")

        layout.separator()

        layout.prop(self, "override", icon = "DECORATE_OVERRIDE")
        layout.prop(self, "unlink_old", icon = "UNLINKED")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        return mu_change_material_link(self, self.link_to, self.affect, self.override, self.selected_collection, self.unlink_old)

class MATERIAL_OT_materialutilities_merge_base_names(bpy.types.Operator):
    """Merges materials that has the same base names but ends with .xxx (.001, .002 etc)"""

    bl_idname = "material.materialutilities_merge_base_names"
    bl_label = "Merge Base Names"
    bl_description = "Merge materials that has the same base names but ends with .xxx (.001, .002 etc)"

    material_base_name: StringProperty(
                            name = "Material Base Name",
                            default = "",
                            description = 'Base name for materials to merge ' +
                                          '(e.g. "Material" is the base name of "Material.001", "Material.002" etc.)'
                            )
    use_new_name: BoolProperty(
                            name = "New name",
                            description = "Give the material a new name instead of the original base name"
                            )
    material_new_name: StringProperty(
                            name = "New Material Name",
                            default = "",
                            description = 'Set a new name to use instead of the original Material Base Name'
                            )
    is_auto: BoolProperty(
                            name = "Auto Merge",
                            description = "Find all available duplicate materials and Merge them"
                            )
    pattern_to_use: EnumProperty(
                            name = "Pattern",
                            description = "Use another pattern than Material.xxx for merging materials.",
                            items = mu_merge_basse_names_pattern_enums,
                            default = 'DEFAULT',
                            )
    user_defined_pattern_simple: StringProperty(
                            name = "Delimiter",
                            description = "Delimiter to use instead of . (dot)",
                            default = "."
                            )
    user_defined_pattern_regex: StringProperty(
                            name = "RegEx pattern",
                            description = "The pattern to use for search and replace.\
                                            Use (Python Style) RegEx.\
                                            Make sure you have to groups (one for the name and one for the suffix)",
                            default = "^%BASE_NAME\.(\d{1,3})$"
                            )

    is_not_undo = False
    material_error = []          # collect mat for warning messages


    def replace_name(self, name = ""):
        """If the user chooses a material like 'Material.042', clean it up to get a base name ('Material')"""

        if (name != ""):
            self.material_base_name = name

        # use the chosen material as a base one, check if there is a name
        self.check_no_name = (False if self.material_base_name in {""} else True)

        delimiter = '.'

        if ( (self.pattern_to_use == 'REGEX') and (self.check_no_name is False) ):
            base, suffix = self.split_name_regex(self.material_base_name)
            self.material_base_name = base

            return

        if (self.pattern_to_use == 'SIMPLE'):
            delimiter = self.user_defined_pattern_simple

        # No need to do this if it's already "clean"
        #  (Also lessens the potential of error given about the material with the Base name)
        if delimiter not in self.material_base_name:
            return

        if self.check_no_name is True:
            for mat in bpy.data.materials:
                name = mat.name

                if name == self.material_base_name:
                    try:
                        if (self.pattern_to_use == 'REGEX'):
                            base, suffix = self.split_name_regex(name)
                        else:
                            base, suffix = name.rsplit(delimiter, 1)
                            # trigger the exception
                            num = int(suffix, 10)

                        self.material_base_name = base
                        mat.name = self.material_base_name
                        return
                    except ValueError:
                        if name not in self.material_error:
                            self.material_error.append(name)
                        return

        return

    def split_name_regex(self, name):
        """Split the material name using Regular Expressions"""

        import re

        pattern = self.user_defined_pattern_regex
        pattern = pattern.replace("%BASE_NAME", "(.*)")

        matches = re.search(pattern, name)

        if not matches:
            print("Not matching regex:" + name)
            return name, None

        base = matches.group(1)
        suffix = matches.group(2)

        return base, suffix


    def split_name(self, name):
        """Split the material name into a base and a suffix"""

        delimiter = '.'

        if (self.pattern_to_use == 'REGEX'):
            return self.split_name_regex(name)

        if (self.pattern_to_use == 'SIMPLE'):
            delimiter = self.user_defined_pattern_simple

        # No need to do this if it's already "clean"/there is no suffix
        if delimiter not in name:
            return name, None

        base, suffix = name.rsplit(delimiter, 1)

        try:
            # trigger the exception
            num = int(suffix, 10)
        except ValueError:
            # Not a numeric suffix
            # Don't report on materials not actually included in the merge!
            if ((self.is_auto or base == self.material_base_name)
                 and (name not in self.material_error)):
                self.material_error.append(name)
            return name, None

        if self.is_auto is False:
            if base == self.material_base_name:
                return base, suffix
            else:
                return name, None

        return base, suffix

    def fixup_slot(self, slot):
        """Fix material slots that was assigned to materials now removed"""

        if not slot.material:
            return

        base, suffix = self.split_name(slot.material.name)
        if suffix is None:
            return

        try:
            base_mat = bpy.data.materials[base]
        except KeyError:
            self.replace_name(slot.material.name)

            try:
                base_mat = bpy.data.materials[base]
            except KeyError:
                print("\n[Materials Utilities Specials]\nLink to base names\nError:"
                      "Base material %r not found\n" % base)
            return

        slot.material = base_mat

    def main_loop(self, context):
        """Loops through all objects and material slots to make sure they are assigned to the right material"""
        print("Main loop!")

        for obj in context.scene.objects:
            for slot in obj.material_slots:
                self.fixup_slot(slot)

    @classmethod
    def poll(self, context):
        return (context.mode == 'OBJECT') and (len(context.visible_objects) > 0)

    def draw(self, context):
        layout = self.layout

        box_1 = layout.box()
        col = box_1.column()
        row = col.split(factor = 0.93, align = True)
        row.prop_search(self, "material_base_name", bpy.data, "materials")
        row.prop(self, "use_new_name", text = "", icon = "STYLUS_PRESSURE")

        if (self.use_new_name):
            box_1.prop(self, "material_new_name")

        box_1.enabled = not self.is_auto

        layout.separator()

        box_2 = layout.box()
        box_2.prop(self, "pattern_to_use")

        if self.pattern_to_use == 'SIMPLE':
            box_2.prop(self, "user_defined_pattern_simple")
        elif self.pattern_to_use == 'REGEX':
            box_2.prop(self, "user_defined_pattern_regex")

        layout.prop(self, "is_auto", text = "Auto Rename/Replace", icon = "SYNTAX_ON")

    def invoke(self, context, event):
        self.is_not_undo = True
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # Reset Material errors, otherwise we risk reporting errors erroneously..
        self.material_error = []

        if not self.is_auto:
            self.replace_name()

            if self.check_no_name:
                self.main_loop(context)

                # IF the user wants to change the name, do it now
                if self.use_new_name:
                    bpy.data.materials[self.material_base_name].name = self.material_new_name
            else:
                self.report({'WARNING'}, "No Material Base Name given!")

                self.is_not_undo = False
                return {'CANCELLED'}
        else:
            self.main_loop(context)

            self.material_base_name = ""

        if self.material_error:
            materials = ", ".join(self.material_error)

            if len(self.material_error) == 1:
                waswere = " was"
                suff_s = ""
            else:
                waswere = " were"
                suff_s = "s"

            self.report({'WARNING'}, materials + waswere + " not removed or set as Base" + suff_s)

        self.is_not_undo = False
        return {'FINISHED'}

class MATERIAL_OT_materialutilities_material_slot_move(bpy.types.Operator):
    """Move the active material slot"""

    bl_idname = "material.materialutilities_slot_move"
    bl_label = "Move Slot"
    bl_description = "Move the material slot"
    bl_options = {'REGISTER', 'UNDO'}

    movement: EnumProperty(
                name = "Move",
                description = "How to move the material slot",
                items = mu_material_slot_move_enums
                )

    @classmethod
    def poll(self, context):
        # would prefer to access self.movement here, but can't..
        obj = context.active_object
        if not obj:
            return False
        if (obj.active_material_index < 0) or (len(obj.material_slots) <= 1):
            return False
        return True

    def execute(self, context):
        active_object = context.active_object
        active_material = context.object.active_material

        if self.movement == 'TOP':
            dir = 'UP'

            steps = active_object.active_material_index
        else:
            dir = 'DOWN'

            last_slot_index = len(active_object.material_slots) - 1
            steps = last_slot_index - active_object.active_material_index

        if steps == 0:
            self.report({'WARNING'}, active_material.name + " already at " + self.movement.lower() + '!')
        else:
            for i in range(steps):
                bpy.ops.object.material_slot_move(direction = dir)

            self.report({'INFO'}, active_material.name + ' moved to ' + self.movement.lower())

        return {'FINISHED'}



class MATERIAL_OT_materialutilities_join_objects(bpy.types.Operator):
    """Join objects that have the same (selected) material(s)"""

    bl_idname = "material.materialutilities_join_objects"
    bl_label = "Join by material (Material Utilities)"
    bl_description = "Join objects that share the same material"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: StringProperty(
                            name = "Material",
                            default = "",
                            description = 'Material to use to join objects'
                            )
    is_auto: BoolProperty(
                            name = "Auto Join",
                            description = "Join objects for all materials"
                            )

    is_not_undo = True
    material_error = []          # collect material names for warning messages


    @classmethod
    def poll(self, context):
        # This operator only works in Object mode
        return (context.mode == 'OBJECT') and (len(context.visible_objects) > 0)

    def draw(self, context):
        layout = self.layout

        box_1 = layout.box()
        box_1.prop_search(self, "material_name", bpy.data, "materials")
        box_1.enabled = not self.is_auto
        layout.separator()

        layout.prop(self, "is_auto", text = "Auto Join", icon = "SYNTAX_ON")

    def invoke(self, context, event):
        self.is_not_undo = True
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        # Reset Material errors, otherwise we risk reporting errors erroneously..
        self.material_error = []
        materials = []

        if not self.is_auto:
            if self.material_name == "":
                self.report({'WARNING'}, "No Material Name given!")

                self.is_not_undo = False
                return {'CANCELLED'}
            materials = [self.material_name]
        else:
            materials = bpy.data.materials.keys()

        result = mu_join_objects(self, materials)
        self.is_not_undo = False

        return result


class MATERIAL_OT_materialutilities_auto_smooth_angle(bpy.types.Operator):
    """Set Auto smooth values for selected objects"""
    # Inspired by colkai

    bl_idname = "view3d.materialutilities_auto_smooth_angle"
    bl_label = "Set Auto Smooth Angle (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    affect: EnumProperty(
            name = "Affect",
            description = "Which objects of to affect",
            items = mu_affect_enums,
            default = 'SELECTED'
            )
    selected_collection: StringProperty(
            name = "Collection",
            description = "Affect materials of the objects in this selected collection",
            default = ""
    )
    angle: FloatProperty(
            name = "Angle",
            description = "Maximum angle between face normals that will be considered as smooth",
            subtype = 'ANGLE',
            min = 0,
            max = radians(180),
            default = radians(35)
            )
    set_smooth_shading: BoolProperty(
            name = "Set Smooth",
            description = "Set Smooth shading for the affected objects\n"
                   "This overrides the currenth smooth/flat shading that might be set to different parts of the object",
            default = True
            )

    @classmethod
    def poll(cls, context):
        return (len(bpy.data.objects) > 0) and (context.mode == 'OBJECT')

    def invoke(self, context, event):
        self.is_not_undo = True
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "angle")
        layout.prop(self, "affect")

        if self.affect == 'SELECTED_COLLECTION':
            layout.prop_search(self, "selected_collection", bpy.data, "collections")

        layout.prop(self, "set_smooth_shading", icon = "BLANK1")

    def execute(self, context):
        return mu_set_auto_smooth(self, self.angle, self.affect, self.set_smooth_shading, self.selected_collection)

class MATERIAL_OT_materialutilities_remove_unused_materials(bpy.types.Operator):
    """Remove any unused (zero users) materials"""
    # On request by Hologram

    bl_idname = "view3d.materialutilities_remove_unused_materials"
    bl_label = "Remove unused materials (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return mu_remove_unused_materials(self)

class MU_materialutilites_select_texture_base(bpy.types.Operator):
    """Base class to collect common functions & properties for texture selecting dialogs"""
    
    only_selected: BoolProperty(
            name = "Only selected nodes",
            description = "Only replace image textures on the selected nodes",
            default = False,
            )
    set_fake_user: BoolProperty(
            name = "Set Fake user",
            description = "Set the fake user flag for existing images",
            default = False,
            )
    set_label: BoolProperty(
            name = "Set node labels",
            description = "Set the labels of the added nodes to the corresponding pass",
            default = True,
            )
    connect: BoolProperty(
            name = "Connect to shader",
            description = "Tries to connect the added textures to the right input",
            default = True,
            )
    use_alpha_channel: BoolProperty(
            name = "Connect Alpha channel",
            description = "Connects the alpha channel (if detected) of Diffuse texture to the opacity/alpha input",
            default = False,
            )
    collapse_texture_nodes: BoolProperty(
            name = "Collapse texture nodes",
            description = "Hides the texture nodes for a cleaner node setup",
            default = True,
            )
    reflection_as_specular: BoolProperty(
            name = "Reflection as Specular",
            description = "Connect Reflection maps as Specular",
            default = True,
            )
    add_colorspaces: BoolProperty(
            name = "Add Color spaces",
            description = "Add appropriate Color space nodes",
            default = True,
            )
    height_map_option: EnumProperty(
            name = "Height map treatment",
            description = "How should height maps be treated",
            items = mu_height_map_option_enums,
            default = 'DISPLACEMENT'
            )
    go_wide: BoolProperty(
            name = "Wide search",
            description = "Go through all nodes in the material, to find the right node, if not immediately found.\n"
                            "This might take a longer time in complex materials, and might also replace unwanted textures",
            default = True,
            )
    emission_map_option: EnumProperty(
            name = "Emission map treatment",
            description = "How should the emission map be treated",
            items = mu_emission_map_option_enums
            )

    stair_step: BoolProperty(
            name = "Stair step nodes",
            description = "Arrange the image nodes in a \"stair step\" (alternating) layout.",
            default = True,
            )

    override_type: EnumProperty(
            name = "Assignment method",
            description = "",
            items = mu_override_type_enums
            )
    material_name: StringProperty(
            name = "Material Name",
            description = "Name of the new material\n (The name of the directory will be used if this is left empty)",
            default = '',
            maxlen = 63
            )

    material_node_type: EnumProperty(
            name = "Material Node Type",
            description = "What material node type to use in the new material",
            items = mu_octane_std_material_enums,
            default = 'UNIVERSAL'
            )

    add_material: BoolProperty(
            default = False,
            )

    add: BoolProperty(
            default = False,
            )
    
    selecting_files: False

    @classmethod
    def poll(cls, context):
        if context.area.ui_type == 'ShaderNodeTree':
            return context.area.ui_type == 'ShaderNodeTree' and bpy.context.active_object.active_material is not None
        return context.area.ui_type == 'VIEW_3D'

    def draw(self, context):
        layout = self.layout

        if not self.add:
            layout.prop(self, 'only_selected')
            row = layout.row()
            row.prop(self, 'go_wide')
            row.enabled = not self.only_selected
            layout.prop(self, 'set_fake_user')
        else:
            box = layout.box()
            box.label(text = "Connections:")
            col = mu_ui_col_split(box)
            col.prop(self, 'connect')
            row = col.row()
            row.enabled = self.connect
            row.prop(self, 'use_alpha_channel')
            if bpy.data.scenes['Scene'].render.engine == 'octane':
                row = col.row()
                row.prop(self, 'add_colorspaces')
                row.enabled = self.connect

            box = layout.box()
            box.label(text = "Appearance:")
            col = mu_ui_col_split(box)
            col.prop(self, 'set_label')
            col.prop(self, 'collapse_texture_nodes')
            row = col.row()
            row.enabled = not self.collapse_texture_nodes
            row.prop(self, 'stair_step')

            box = layout.box()
            box.label(text = "Map options:")
            col = mu_ui_col_split(box)
            col.prop(self, 'reflection_as_specular')
            col.label(text = "Height Map Treatment")
            mu_ui_col_split(col).prop(self, 'height_map_option', text = "")

            if self.material_node_type == 'STD_SURF':
                col.label(text = "Emission map treatment")
                mu_ui_col_split(col).prop(self, 'emission_map_option', text = "")

            if self.add_material:
                box = layout.box()
                box.label(text = "Material options:")
                col = mu_ui_col_split(box)

                if context.active_object.mode == 'OBJECT':
                    col.label(text = "Assignment Method")
                    mu_ui_col_split(col).prop(self, 'override_type', text = "")

                if bpy.data.scenes['Scene'].render.engine == 'octane':
                    col.label(text = "Material Node Type")
                    mu_ui_col_split(col).prop(self, 'material_node_type', text = "")

                col.label(text = "Material Name")
                mu_ui_col_split(col).prop(self, 'material_name', text = "")

    def _invoke(self, context, event):
        mu_prefs = materialutilities_get_preferences(context)
        
        if mu_prefs.tex_texture_directory == 'DEFAULT':
            self.directory = bpy.context.preferences.filepaths.texture_directory
        elif mu_prefs.tex_texture_directory == 'LAST':
            self.directory = mu_prefs.tex_last_texture_directory
        else:
            self.directory = mu_prefs.tex_texture_directory_path

        self.set_fake_user          = mu_prefs.tex_set_fake_user
        self.only_selected          = mu_prefs.tex_only_selected
        self.go_wide                = mu_prefs.tex_go_wide
        self.set_label              = mu_prefs.tex_set_label
        self.connect                = mu_prefs.tex_connect
        self.use_alpha_channel      = mu_prefs.tex_use_alpha_channel
        self.collapse_texture_nodes = mu_prefs.tex_collapse_texture_nodes
        self.reflection_as_specular = mu_prefs.tex_reflection_as_specular
        self.add_colorspaces        = mu_prefs.tex_add_colorspaces
        self.height_map_option      = mu_prefs.tex_height_map_option
        self.stair_step             = mu_prefs.tex_stair_step

        if not self.add_material and bpy.data.scenes['Scene'].render.engine == 'octane':
            mat = context.active_object.active_material
            out_node = mat.node_tree.nodes.get('Material Output')
            if out_node is not None and out_node.inputs['Surface'].is_linked:
                first_node = out_node.inputs['Surface'].links[0].from_node
                if first_node.bl_idname == 'OctaneStandardSurfaceMaterial':
                    self.material_node_type = 'STD_SURF'

        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        print("Looking for textures in: ", self.directory)

        mu_prefs = materialutilities_get_preferences(context)
        mu_prefs.tex_last_texture_directory = self.directory

        if self.selecting_files:
            params = dict(file_path = self.directory, file_list = self.files)
        else:
            params = dict(directory = self.directory)

        if self.add:
            override_type = self.override_type if context.active_object.mode == 'OBJECT' else 'APPEND_MATERIAL'
            prefs = SimpleNamespace(set_label      = self.set_label,
                                    connect        = self.connect,
                                    connect_alpha  = self.use_alpha_channel,
                                    height_map     = self.height_map_option,
                                    bump_distance  = mu_prefs.tex_bump_distance,
                                    collapse_texture_nodes = self.collapse_texture_nodes,
                                    reflection_as_specular = self.reflection_as_specular,
                                    add_colorspace  = self.add_colorspaces,
                                    stairstep       = self.stair_step,
                                    align_nodes     = True,
                                    new_material    = self.add_material,
                                    material_name   = self.material_name,
                                    override_type   = override_type,
                                    mat_node_type   = self.material_node_type,
                                    emission_option = self.emission_map_option,
                                    pos_group       = 'COL' if self.collapse_texture_nodes else 'EXP',
                                    gamma           = 2.2,
                                    x_offset        = 300,
                                    context         = context
                                    )

            return mu_add_image_textures(self, prefs, **params)
        else:
            prefs = SimpleNamespace(set_fake_user  = self.set_fake_user,
                                    only_selected  = self.only_selected,
                                    go_wide        = self.go_wide,
                                    context        = context
                                    )

            return mu_replace_image_textures(self, prefs, **params)
            #mu_replace_image_textures(self, self.image_path, self.only_selected, self.set_fake_user)
    
class NODE_OT_materialutilites_select_texture_files(MU_materialutilites_select_texture_base):
    """Select image textures to import to shader setup"""
    
    bl_idname = 'node.materialutilities_select_texture_files'
    bl_label = "Select textures"
    bl_options = {'REGISTER', 'UNDO'}

    files: CollectionProperty(
                name="File Path",
                type=bpy.types.OperatorFileListElement,
                )
    directory: StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        self.selecting_files = True
        return self._invoke(context, event)

class NODE_OT_materialutilites_select_texture_directory(MU_materialutilites_select_texture_base):
    """Select directory with image textures to import to shader setup"""
    
    bl_idname = 'node.materialutilities_select_texture_directory'
    bl_label = "Select directory"
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(
                                name="Image set Path",
                                description="Path to image texture set"
                                )

    def invoke(self, context, event):
        self.selecting_files = False
        return self._invoke(context, event)

class NODE_OT_materialutilities_add_image_textures(bpy.types.Operator):
    """Open a PBR image texture set"""

    bl_idname = 'node.materialutilities_add_image_textures'
    bl_label = "Open image texture set (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if bpy.data.scenes['Scene'].render.engine not in mu_supported_engines:
            print("Material Utilities - Nodes menu: Unsupported render engine: ", bpy.data.scenes['Scene'].render.engine)
            return False
        return context.area.ui_type == 'ShaderNodeTree' and context.space_data.shader_type == 'OBJECT' and bpy.context.active_object.active_material is not None

    def invoke(self, context, event):
        mu_prefs = materialutilities_get_preferences(context)
        mode = mu_prefs.tex_default_dialog

        if event.shift:
            mode = 'FILES'
        elif event.ctrl:
            mode = 'DIR'

        if mode == 'FILES':
            bpy.ops.node.materialutilities_select_texture_files('INVOKE_DEFAULT', add = True)
            return  {'RUNNING_MODAL'}
        elif mode == 'DIR':
            bpy.ops.node.materialutilities_select_texture_directory('INVOKE_DEFAULT', add = True)
            return  {'RUNNING_MODAL'}

    def execute(self, context):
        return {'FINISHED'} #mu_open_image_texture_set(self, self.image_path)

class NODE_OT_materialutilities_replace_image_textures(bpy.types.Operator):
    """Replace image textures with matching from another set"""

    bl_idname = 'node.materialutilities_replace_image_textures'
    bl_label = "Replace image texture set (Material Utilities)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if bpy.data.scenes['Scene'].render.engine not in mu_supported_engines:
            print("Material Utilities - Nodes menu: Unsupported render engine: ", bpy.data.scenes['Scene'].render.engine)
            return False
        return context.area.ui_type == 'ShaderNodeTree' and context.space_data.shader_type == 'OBJECT' and bpy.context.active_object.active_material is not None

    def invoke(self, context, event):
        mu_prefs = materialutilities_get_preferences(context)
        mode = mu_prefs.tex_default_dialog
        
        if event.shift:
            mode = 'FILES'
        elif event.ctrl:
            mode = 'DIR'

        if mode == 'FILES':
            bpy.ops.node.materialutilities_select_texture_files('INVOKE_DEFAULT', add = False)
            return  {'RUNNING_MODAL'}
        elif mode == 'DIR':
            bpy.ops.node.materialutilities_select_texture_directory('INVOKE_DEFAULT', add = False)
            return  {'RUNNING_MODAL'}

    def execute(self, context):
        return {'FINISHED'}

class VIEW3D_OT_materialutilities_assign_pbr_material(bpy.types.Operator):
    """Import PBR textures in a new material"""

    bl_idname = 'view3d.materialutilities_assign_pbr_material'
    bl_label = "Assign PBR material"
    bl_description = "Import PBR textures in a new material"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if bpy.data.scenes['Scene'].render.engine not in mu_supported_engines:
            print("Material Utilities - Assign PBR Material: Unsupported render engine: ", bpy.data.scenes['Scene'].render.engine)
            return False
        return context.active_object is not None

    def invoke(self, context, event):
        mu_prefs = materialutilities_get_preferences(context)
        mode = mu_prefs.tex_default_dialog
        
        if event.shift:
            mode = 'FILES'
        elif event.ctrl:
            mode = 'DIR'

        if mode == 'FILES':
            bpy.ops.node.materialutilities_select_texture_files('INVOKE_DEFAULT', add = True, add_material = True)
            return  {'RUNNING_MODAL'}
        elif mode == 'DIR':
            bpy.ops.node.materialutilities_select_texture_directory('INVOKE_DEFAULT', add = True, add_material = True)
            return  {'RUNNING_MODAL'}

    def execute(self, context):
        return {'FINISHED'}