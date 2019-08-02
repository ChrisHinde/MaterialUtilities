import bpy

from bpy.types import (
    AddonPreferences,
    PropertyGroup,
    )
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty,
    IntProperty
    )


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
    search_show_limit: IntProperty(
        name = "'Show Search' Limit",
        description = "How many materials should there be before the 'Search' option is shown "
                      "in the Assign Material and Select By Material menus\n"
                      "Set it to 0 to always show 'Search'",
        min = 0,
        default = 0
    )

    def draw(self, context):
        layout = self.layout

        #box = layout.box()
        #box.label(text="Material Settings")

        layout.row().prop(self, "new_material_name", icon = "MATERIAL", expand = False)

        #box = layout.box()
        #box.label(text="Miscellaneous")

        layout.row().prop(self, "search_show_limit", expand = False)


def materialutilities_get_preferences(context):
    return context.preferences.addons[__package__].preferences
