import bpy

from bpy.types import (
    AddonPreferences,
    PropertyGroup,
    )
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty,
    IntProperty,
    FloatProperty
    )
from math import radians

from .enum_values import *

# Addon Preferences
class VIEW3D_MT_materialutilities_preferences(AddonPreferences):
    bl_idname = __package__

    new_material_name: StringProperty(
            name = "New Material name",
            description = "What Base name pattern to use for a new created Material\n"
                          "It is appended by an automatic numeric pattern depending\n"
                          "on the number of Scene's materials containing the Base",
            default = "Unnamed Material",
            )
    override_type: EnumProperty(
            name = 'Assignment method',
            description = '',
            items = mu_override_type_enums
            )
    fake_user: EnumProperty(
            name = "Set Fake User",
            description = "Default option for the Set Fake User (Turn fake user on or off)",
            items = mu_fake_user_set_enums,
            default = 'TOGGLE'
            )
    fake_user_affect: EnumProperty(
            name = "Affect",
            description = "Which materials of objects to affect",
            items = mu_fake_user_affect_enums,
            default = 'UNUSED'
            )
    link_to: EnumProperty(
            name = "Change Material Link To",
            description = "Default option for the Change Material Link operator",
            items = mu_link_to_enums,
            default = 'OBJECT'
            )
    link_to_affect: EnumProperty(
            name = "Affect",
            description = "Which materials of objects to affect by default with Change Material Link",
            items = mu_link_affect_enums,
            default = 'SELECTED'
            )
    search_show_limit: IntProperty(
            name = "Show 'Search' Limit",
            description = "How many materials should there be before the 'Search' option is shown "
                          "in the Assign Material and Select By Material menus\n"
                          "Set it to 0 to always show 'Search'",
            min = 0,
            default = 0
            )
    search_show_btm_limit: IntProperty(
            name = "Show 'Search' at Bottom Limit",
            description = "How many materials should there be before the 'Search' option is shown at the bottom"
                          "in the Assign Material and Select By Material menus\n"
                          "Set it to 0 to always show 'Search' at the bottom",
            min = 0,
            default = 50
            )
    material_show_limit: IntProperty(
            name = "Material List Menu Limit ",
            description = "The maximum number of materials to show in the Assign Material & Select By Material menus"
                          "(default: 1000). The limit is so not to slow down the opening of the menus,"
                          "when there's a lot of materials in the project.\n"
                          "Set it to 0 to always show all materials",
            min = 0,
            default = 1000
            )

    include_gp_materials: BoolProperty(
            name = "Show Grease Pencil materials",
            description = "Include Grease Pencil materials in the materials list",
            default = False
    )

    set_smooth_affect: EnumProperty(
            name = "Set Auto Smooth Affect",
            description = "Which objects to affect",
            items = mu_affect_enums,
            default = 'SELECTED'
            )
    auto_smooth_angle: FloatProperty(
            name = "Auto Smooth Angle",
            description = "Maximum angle between face normals that will be considered as smooth",
            subtype = 'ANGLE',
            min = 0,
            max = radians(180),
            default = radians(35)
            )
    show_multiple_materials_replacement: BoolProperty(
            name = "Enable Replace Multiple Materials",
            description = "Enable the Replace Multiple Materials option (NB: Experimental)",
            default = False
    )

    tex_texture_directory: EnumProperty(
            name = "Texture directory",
            description = "Default directory for loading PBR textures",
            items = mu_texture_directory_enums,
            default = 'DEFAULT'
            )
    tex_texture_directory_path: StringProperty(
            name = "Custom directory",
            description = "Default custem directory for loading PBR textures",
            subtype = 'DIR_PATH',
            default = '//',
            )
    tex_last_texture_directory: StringProperty(
            name = "Last Texture directory", description = "",
            subtype = 'DIR_PATH',
            default = '//'
            )
    tex_default_dialog: EnumProperty(
            name = "File selection",
            description = "Select directory or individual files for import by default",
            items = mu_import_dialog_enums,
            default = 'DIR'
            )
    tex_add_to_editor_header: BoolProperty(
            name = "Add menu to editor header",
            description = "Add Material Utilities menu to shader editor header",
            default = False,
            )
    tex_only_selected: BoolProperty(
            name = "Only selected nodes",
            description = "Only replace image textures on the selected nodes",
            default = False,
            )
    tex_set_fake_user: BoolProperty(
            name = "Set Fake user",
            description = "Set the fake user flag for existing images",
            default = False,
            )
    tex_set_label: BoolProperty(
            name = "Set node labels",
            description = "Set the labels of the added nodes to the corresponding pass",
            default = True,
            )
    tex_connect: BoolProperty(
            name = "Connect to shader",
            description = "Tries to connect the added textures to the right input",
            default = True,
            )
    tex_use_alpha_channel: BoolProperty(
            name = "Connect Alpha channel",
            description = "Connects the alpha channel (if detected) of Diffuse texture to the opacity/alpha input",
            default = False,
            )
    tex_collapse_texture_nodes: BoolProperty(
            name = "Collapse texture nodes",
            description = "Hides the texture nodes for a cleaner node setup",
            default = True,
            )
    tex_bump_distance: FloatProperty(
            name = "Bump distance",
            description = "Default distance value to use for added bump nodes",
            min = 0,
            default = 0.5
            )
    tex_height_map_option: EnumProperty(
            name = "Height map treatment",
            description = "How should height maps be treated",
            items = mu_height_map_option_enums,
            default = 'DISPLACEMENT'
            )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        box = layout.box()
        box.label(text = "Defaults")

        a = box.box()
        a.label(text = "Assign Material")
        a.prop(self, "new_material_name", icon = "MATERIAL")
        a.prop(self, "override_type", expand = False)

        b = box.box()
        b.label(text = "Set Fake User")
        b.row().prop(self, "fake_user", expand = False)
        b.row().prop(self, "fake_user_affect", expand = False)

        c = box.box()
        c.label(text = "Set Link To")
        c.row().prop(self, "link_to", expand = False)
        c.row().prop(self, "link_to_affect", expand = False)

        d = box.box()
        d.label(text = "Set Auto Smooth")
        d.row().prop(self, "auto_smooth_angle", expand = False)
        d.row().prop(self, "set_smooth_affect", expand = False)
        
        e = box.box()
        e.label(text = "PBR Texture Set Import")
        e.row().prop(self, 'tex_texture_directory', expand = False)
        if self.tex_texture_directory == 'CUSTOM':
                e.row().prop(self, 'tex_texture_directory_path')
        e.row().prop(self, 'tex_height_map_option', expand = False)
        e.row().prop(self, 'tex_bump_distance', expand = False)
        e.row().prop(self, 'tex_add_to_editor_header', expand = False)
        er = e.row()
        e1 = er.column()
        e1.row().prop(self, 'tex_set_label', expand = False)
        e1.row().prop(self, 'tex_connect', expand = False)
        e1.row().prop(self, 'tex_collapse_texture_nodes', expand = False)
        e2 = er.column()
        e2.row().prop(self, 'tex_use_alpha_channel', expand = False)
        e2.row().prop(self, 'tex_set_fake_user', expand = False)
        e2.row().prop(self, 'tex_only_selected', expand = False)

        box = layout.box()
        box.label(text = "Miscellaneous")

        box.prop(self, "include_gp_materials", expand = False)
        box.prop(self, "search_show_limit", expand = False)
        box.prop(self, "search_show_btm_limit", expand = False)
        box.prop(self, "material_show_limit", expand = False)
        box.prop(self, "show_multiple_materials_replacement", expand = False)


def materialutilities_get_preferences(context):
    return context.preferences.addons[__package__].preferences
