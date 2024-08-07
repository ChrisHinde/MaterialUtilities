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

def mu_ui_col_split(layout, factor=0.02):
    spl = layout.split(factor=factor)
    spl.column()
    spl2 = spl.column().split(factor=1-factor/(1-factor))
    return spl2.column()

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
        name = "Change Link To",
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

    use_legacy_cleanmatslots_ui: BoolProperty(
        name = "Use Legacy Clean Material Slots",
        description = "Use the legacy version (default) of the UI for the Clean Material Slots operator",
        default = True
    )

    cleanmatslots_only_active: BoolProperty(
        name = "Only active object",
        description = "Have (clean material slots on) Only active object enabled by default",
        default = False
    )
    cleanmatslots_affect: EnumProperty(
        name = "Affect",
        description = "Which object(s) to clean material slots on",
        items = mu_affect_enums,
        default = 'SELECTED'
        )

    merge_use_selected_material: BoolProperty(
            name = "Use Selected Material",
            default = False,
            description = "Use the selected material (e.g. \"Material.004\") instead of the \"base material\" (e.g. \"Material\") "
                            "as basis for the merge material",
            )
    merge_remove_unused: BoolProperty(
            name = "Remove left over materials",
            default = False,
            description = "Remove the left over (unused) materials (e.g. \"Material.042\") after merging the materials.\n"
                            "These will be automatically removed after save (and reopen) of the file.\n"
                            "(NB: Only removes related materials, other unused materials will be left)",
            )

    # Preferences for texture import
    add_pbr_import_to_assign_dlg: BoolProperty(
        name = "Add to Assign Material dialog (in the 3D viewport)",
        description = "Add 'Assign PBR Material' to the 'Assign Material' popup dialog",
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
        description = "Default custom directory for loading PBR textures",
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
        name = "Add menu to shader editor header",
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
    tex_add_new_uvmap: BoolProperty(
        name = "Add new UV Map node",
        description = "Always add a new UV Map node on import, even if one exists",
        default = False,
        )
    tex_go_wide: BoolProperty(
        name = "Wide search",
        description = "Go through all nodes in the material, to find the right node, if not immediately found.\n"
                        "This might take a longer time in complex materials, and might also replace unwanted textures",
        default = False,
        )
    tex_reflection_as_specular: BoolProperty(
        name = "Reflection as Specular",
        description = "Connect Reflection maps as Specular",
        default = True,
        )
    tex_invert_normals_y: EnumProperty(
        name = "Invert Normals Y channel",
        description = "Default option for adding invert the normals texture Y channel",
        items = mu_texture_invert_normals_options_enums,
        default = 'LAST'
        )
    tex_last_invert_normals_y: BoolProperty(
        name = "Last value of 'Invert Normals Y channel'",
        description = "",
        default = False
        )
    tex_add_colorspaces: BoolProperty(
        name = "Add Color spaces",
        description = "Add appropriate Color space nodes",
        default = True,
        )
    tex_add_gamma_nodes: BoolProperty(
        name = "Add common gamma nodes",
        description = "Add (float value) node(s) for texture (legacy) gamma",
        default = False
    )
    tex_gamma_color: FloatProperty(
        name = "Gamma (Color)",
        description = "Default gamma value for color/RGB textures",
        default = 2.2
    )
    tex_gamma_noncolor: FloatProperty(
        name = "Gamma (Non-Color)",
        description = "Default gamma value for non-color textures",
        default = 1.0
    )
    tex_hide_gamma_values: BoolProperty(
        name = "Hide gamma values on import",
        description = "Hide the gamma value inputs in the import dialog.\n"
                        "If you don't have any plans to change the gamma values, beyond the defaults set here, on imports, "
                        "hiding them will declutter the import options some",
        default = False
    )
    tex_stair_step: BoolProperty(
        name = "Stair step nodes",
        description = "Arrange the image nodes in a \"stair step\" (alternating) layout (Does not affect collapsed nodes).",
        default = True,
        )

    # Preferences UI helpers
    #  This is inspired(/borrowed) from the Magic UV addon and Nutti
    pref_category: EnumProperty(
        name = "Category",
        description = "Preferences Category",
        items = [
            ('DEFAULTS', "Defaults",           "Default options for Material Utilities in the 3D View"),
            ('TEXTURE',  "Texture Set Import", "Default options for PBR texture import"),
            ('MISC',     "Miscellaneous",      "Miscellaneous settings for Material Utilities"),
        ],
        default = 'DEFAULTS'
    )
    defaults_assign_expanded: BoolProperty(
        name = "Assign Material"
    )
    defaults_fake_user_expanded: BoolProperty(
        name = "Set Fake User"
    )
    defaults_link_expanded: BoolProperty(
        name = "Set Link To"
    )
    defaults_auto_smooth_expanded: BoolProperty(
        name = "Set Auto Smooth"
    )
    defaults_cleanmatslots_expanded: BoolProperty(
        name = "Clean Material Slots"
    )
    defaults_mergematerials_expanded: BoolProperty(
        name = "Merge Base Names"
    )
    defaults_textures_expanded: BoolProperty(
        name = "PBR Texture Set Import"
    )
    textures_file_selection_expanded: BoolProperty(
        name = "File Selection"
    )
    textures_height_expanded: BoolProperty(
        name = "Height & Bump Options"
    )
    textures_connections_expanded: BoolProperty(
        name = "Connections & Support Nodes"
    )
    textures_appearance_expanded: BoolProperty(
        name = "Placement & Appearance"
    )
    textures_replace_expanded: BoolProperty(
        name = "Replacing Textures"
    )
    textures_octane_specific_expanded: BoolProperty(
        name = "Octane Specific"
    )
    misc_limits_expanded: BoolProperty(
        name = "Limits"
    )
    misc_extra_expanded: BoolProperty(
        name = "Extra / Experimental"
    )

    def draw(self, context):
        layout = self.layout

        layout.row().prop(self, 'pref_category', expand=True)

        if self.pref_category == 'DEFAULTS':
            layout.separator()
            layout.label(text = "Here you can change the default values and behaviors of the Material Utilities, categorized by function")
            layout.separator()

            layout.prop(self, 'defaults_assign_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.defaults_assign_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.defaults_assign_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, "new_material_name", icon = "MATERIAL")
                col.prop(self, "override_type",     expand = False)
                layout.separator()

            layout.prop(self, 'defaults_fake_user_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.defaults_fake_user_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.defaults_fake_user_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, "fake_user",        expand = False)
                col.prop(self, "fake_user_affect", expand = False)
                layout.separator()

            layout.prop(self, 'defaults_link_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.defaults_link_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.defaults_link_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, "link_to",        expand = False)
                col.prop(self, "link_to_affect", expand = False)
                layout.separator()

            layout.prop(self, 'defaults_auto_smooth_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.defaults_auto_smooth_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.defaults_auto_smooth_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, "auto_smooth_angle", expand = False)
                col.prop(self, "set_smooth_affect", expand = False)

            layout.prop(self, 'defaults_mergematerials_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.defaults_mergematerials_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.defaults_mergematerials_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, "merge_use_selected_material", expand = False)
                col.prop(self, "merge_remove_unused", expand = False)

            layout.prop(self, 'defaults_cleanmatslots_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.defaults_cleanmatslots_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.defaults_cleanmatslots_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, "use_legacy_cleanmatslots_ui", expand = False)
                if self.use_legacy_cleanmatslots_ui:
                    col.prop(self, "cleanmatslots_only_active", expand = False)
                else:
                    col.prop(self, "cleanmatslots_affect", expand = False)

            layout.separator()

        elif self.pref_category == 'TEXTURE':
            layout.separator()
            layout.label(text = "Options and default values for PBR texture set import (Shift+Q in the Shader Editor)")
            layout.separator()

            col = mu_ui_col_split(layout)
            col.prop(self, 'tex_add_to_editor_header',     expand = False)
            col.prop(self, 'add_pbr_import_to_assign_dlg', expand = False)

            layout.separator()

            layout.prop(self, 'textures_file_selection_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.textures_file_selection_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.textures_file_selection_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, 'tex_texture_directory', expand = False)
                if self.tex_texture_directory == 'CUSTOM':
                        col.prop(self, 'tex_texture_directory_path')
                col.prop(self, 'tex_default_dialog', expand = False)
                layout.separator()

            layout.prop(self, 'textures_connections_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.textures_connections_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.textures_connections_expanded:
                layout.separator()
                col = mu_ui_col_split(layout).split()
                col1 = col.column()
                col1.prop(self, 'tex_connect',           expand = False)
                col1.prop(self, 'tex_use_alpha_channel', expand = False)
                col1.prop(self, 'tex_invert_normals_y',  expand = False)
                col2 = col.column()
                col2.prop(self, 'tex_reflection_as_specular', expand = False)
                col2.prop(self, 'tex_add_new_uvmap',          expand = False)
                layout.separator()
    
            layout.prop(self, 'textures_appearance_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.textures_appearance_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.textures_appearance_expanded:
                layout.separator()
                col = mu_ui_col_split(layout).split()
                col1 = col.column()
                col1.prop(self, 'tex_collapse_texture_nodes', expand = False)
                col1.prop(self, 'tex_stair_step',             expand = False)
                col2 = col.column()
                col2.prop(self, 'tex_set_label', expand = False)
                layout.separator()

            layout.prop(self, 'textures_height_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.textures_height_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.textures_height_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, 'tex_height_map_option', expand = False)
                col.prop(self, 'tex_bump_distance',     expand = False)
                layout.separator()
    
            layout.prop(self, 'textures_replace_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.textures_replace_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.textures_replace_expanded:
                layout.separator()
                col = mu_ui_col_split(layout).split()
                col1 = col.column()
                col1.prop(self, 'tex_only_selected', expand = False)
                col1.prop(self, 'tex_go_wide',       expand = False)
                col2 = col.column()
                col2.prop(self, 'tex_set_fake_user', expand = False)
                layout.separator()

            layout.prop(self, 'textures_octane_specific_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.textures_octane_specific_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.textures_octane_specific_expanded:
                layout.separator()
                col = mu_ui_col_split(layout).split()
                col1 = col.column()
                col1.prop(self, 'tex_add_colorspaces', expand = False)
                col2 = col.column()
                col2.prop(self, 'tex_add_gamma_nodes',   expand = False)
                col2.prop(self, 'tex_hide_gamma_values', expand = False)
                col2.separator()
                col2.label(text="Defaults")
                col2.prop(self, 'tex_gamma_color',    expand = False)
                col2.prop(self, 'tex_gamma_noncolor', expand = False)

            layout.separator()

        elif self.pref_category == 'MISC':
            layout.separator()

            layout.prop(self, 'misc_limits_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.misc_limits_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.misc_limits_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, "search_show_limit",     expand = False)
                col.prop(self, "search_show_btm_limit", expand = False)
                col.prop(self, "material_show_limit",   expand = False)
                layout.separator()
            
            layout.prop(self, 'misc_extra_expanded',
                        icon='DISCLOSURE_TRI_DOWN' if self.misc_extra_expanded
                        else 'DISCLOSURE_TRI_RIGHT')
            if self.misc_extra_expanded:
                layout.separator()
                col = mu_ui_col_split(layout)
                col.prop(self, "include_gp_materials", expand = False)
                col.prop(self, "show_multiple_materials_replacement", expand = False)

            layout.separator()


def materialutilities_get_preferences(context):
    return context.preferences.addons[__package__].preferences

def materialutilities_get_preferences_static(context):
    return context.preferences.addons['MaterialUtilities'].preferences
