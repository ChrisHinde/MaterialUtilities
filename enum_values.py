import bpy

mu_override_type_enums = [
    ('OVERRIDE_ALL', "Override all assigned slots",
        "Remove any current material slots, and assign the current material"),
    ('OVERRIDE_CURRENT', "Assign material to currently selected slot",
        "Only assign the material to the material slot that\'s currently selected"),
    ('OVERRIDE_SLOTS', "Assign material to each slot",
        "Keep the material slots, but assign the selected material in each slot"),
    ('APPEND_MATERIAL', "Append Material",
        "Add the material in a new slot, and assign it to the whole object")
]

mu_affect_enums = (('ACTIVE', "Active object", "Affect the active object only"),
                   ('SELECTED', "Selected objects", "Affect all selected objects"),
                   ('ACTIVE_COLLECTION', "Active collection", "Materials of objects in active collection"),
                   ('SELECTED_COLLECTION', "Select collection ", "Materials of objects in the selected collection"),
                   ('SCENE', "Scene objects", "Affect all objects in the current scene"),
                   ('ALL', "All", "All objects in this blend file"))

mu_fake_user_set_enums = (('ON', "On", "Enable fake user"),
                          ('OFF', "Off", "Disable fake user"),
                          ('TOGGLE', "Toggle", "Toggle fake user"))
mu_fake_user_affect_enums = (('ACTIVE', "Active object", "Materials of active object only"),
                             ('SELECTED', "Selected objects", "Materials of selected objects"),
                             ('ACTIVE_COLLECTION', "Active collection", "Materials of objects in active collection"),
                             ('SELECTED_COLLECTION', "Select collection ", "Materials of objects in the selected collection"),
                             ('SCENE', "Scene objects", "Materials of objects in current scene"),
                             ('USED', "Used", "All materials used by objects"),
                             ('UNUSED', "Unused", "Currently unused materials"),
                             ('ALL', "All", "All materials in this blend file"))

mu_link_to_enums = (('DATA', "Data", "Link the materials to the data"),
                    ('OBJECT', "Object", "Link the materials to the object"),
                    ('TOGGLE', "Toggle", "Toggle what the materials are currently linked to"))
mu_link_affect_enums = (('ACTIVE', "Active object", "Materials of active object only"),
                        ('SELECTED', "Selected objects", "Materials of selected objects"),
                        ('ACTIVE_COLLECTION', "Active collection", "Materials of objects in active collection"),
                        ('SELECTED_COLLECTION', "Select collection ", "Materials of objects in the selected collection"),
                        ('SCENE', "Scene objects", "Materials of objects in current scene"),
                        ('ALL', "All", "All materials in this blend file"))

mu_material_slot_move_enums = (('TOP', "Top", "Move slot to the top"),
                               ('BOTTOM', "Bottom", "Move slot to the bottom"))

mu_merge_basse_names_pattern_enums = (
                        ('DEFAULT', "Default", "Use the default pattern: Material.xxx (eg. Metal.001, Metal.002)"),
                        ('SIMPLE', "Define delimiter", "Use another delimiter (as _ or -) instead of the default . (dot)"),
                        ('REGEX', "Regex pattern", "Define a custom pattern using (Python style) Regular Expressions")
                        )

mu_texture_directory_enums = (
    ('DEFAULT', "Default directory", "Use the texture directory set in the File Paths preferences"),
    ('LAST',    "Last used", "Use the directory used in the previous import"),
    ('CUSTOM',  "Custom", "Set a custom directory to use"),
)
mu_import_dialog_enums = (
    ('DIR',   "Select directory", "Open a dialog to select a directory"),
    ('FILES', "Select files", "Open a dialog to select individual files"),
)
mu_height_map_option_enums = (
    ('DISPLACEMENT', "As Displacement", "Connect the Height map to Displacemnt"),
    ('BUMP', "As Bump", "Connect the Height map to Bump"),
    ('NC',   "Don't connect", "Add the map, but don't connect it to the node setup"),
)
mu_emission_map_option_enums = (
    ('NODE',  "Use Texture Emission Node", "Connect the Emission map to the Emission input via an Texture Emission node\n" +
                                        " NB: Emission color will be set to 100% white, and Emission weight to 1.0"),
    ('COLOR', "Connect to Emission color", "Connect the Emission map to the Emission color input directly\n NB: Emission weight will be set to 1.0"),
    ('NC',    "Don't connect", "Add the map, but don't connect it to the node setup")
)
mu_octane_std_material_enums = (
    ('UNIVERSAL', "Universal Material", "Use Octane Universal Material"),
    ('STD_SURF',  "Standard Surface Material", "Use the (Autodesk) Standard Surfaco Material")
)

mu_supported_engines = ['CYCLES', 'BLENDER_EEVEE', 'octane']

mu_default_shader_nodes = {
    'CYCLES': 'ShaderNodeBsdfPrincipled',
    'OCTANE': {
        '_DEFAULT':  'OctaneUniversalMaterial',
        'UNIVERSAL': 'OctaneUniversalMaterial',
        'STD_SURF':  'OctaneStandardSurfaceMaterial'}
}

mu_node_positions = {   # Y-positions for adding nodes to the shader node tree
    'CYCLES': {
      'EXP': {  # Expanded nodes
          'ShaderNodeBsdfPrincipled': {
            'AO': -200,                                 # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'REFLECTION': -450,                         # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'DIFFUSE': 76, 'ALBEDO': 76, 'COLOR': 76,   # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 268.5, 'GLOSSINESS': 268.5,    # Same input, but different values
            'SPECULAR': 226,
            'METALNESS': 206,
            'HEIGHT': 700, 'DISPLACEMENT': 750,         # MAY BE AUTOMATICALLY CONNECTED, Place bellow
            'BUMP': 546, 'NORMAL': 546,                 # In Cycles Bump and Normal is done via the same input
            'ALPHA': 525, 'MASK': 525,                  # Currently treating Alpha and Mask as the same thing
            'TRANSMISSION': 440,
            'EMISSION': 482,
            'UNKNOWN': -700,
            '_DISPLACEMENT': 500,
            '_UVNODE': 268, '_UVREROUTE': 300,
        },
        'ShaderNodeBsdfDiffuse':{
            'AO': -500,                                 # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'REFLECTION': -450, 'GLOSSINESS': -400,     # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'ALPHA': -350, 'MASK': -300,                # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'TRANSMISSION': -250, 'EMISSION': -200,     # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'SPECULAR': -150, 'METALNESS': -100,        # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'DIFFUSE': 24, 'ALBEDO': 24, 'COLOR': 24,   # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 45,
            'BUMP': 66, 'NORMAL': 66,                   # In Cycles Bump and Normal is done via the same input
            'HEIGHT': 126, 'DISPLACEMENT': 126,         # MAY BE AUTOMATICALLY CONNECTED, Place bellow
            'UNKNOWN': -700,
            '_DISPLACEMENT': 150,
            '_UVNODE': 48, '_UVREROUTE': 51,
        },
        'ShaderNodeBsdfGlossy':{
            'AO': -500,                                 # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'REFLECTION': -450, 'GLOSSINESS': -400,     # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'ALPHA': -350, 'MASK': -300,                # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'TRANSMISSION': -250, 'EMISSION': -200,     # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'SPECULAR': -150, 'METALNESS': -100,        # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'DIFFUSE': 66, 'ALBEDO': 66, 'COLOR': 66,   # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 87,                            # Same input, but different values
            'BUMP': 108, 'NORMAL': 108,                 # In Cycles Bump and Normal is done via the same input
            'HEIGHT': 168, 'DISPLACEMENT': 168,         # MAY BE AUTOMATICALLY CONNECTED, Place bellow
            'UNKNOWN': -700,
            '_DISPLACEMENT': 150,
            '_UVNODE': 48, '_UVREROUTE': 51,
        },
        'FAUX': {
            'AO': -600, 'REFLECTION': -450, 'ALPHA': -300, 'MASK': -150,
            'DIFFUSE': 0, 'ALBEDO': 0, 'COLOR': 0,
            'SPECULAR': 150, 'METALNESS': 300,
            'ROUGHNESS': 150, 'GLOSSINESS': 300,
            'TRANSMISSION': 450, 'EMISSION': 600,
            'BUMP': 750, 'NORMAL': 750,
            'HEIGHT': 900, 'DISPLACEMENT': 900,
            'UNKNOWN': -700,
            '_DISPLACEMENT': 950,
            '_UVNODE': 50, '_UVREROUTE': 50,
        }
      },
      'COL': {  # Collapsed nodes
        'ShaderNodeBsdfPrincipled': {
            'AO': -80,                                    # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'REFLECTION': -120,                           # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'DIFFUSE': 106, 'ALBEDO': 106, 'COLOR': 106,  # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 331, 'GLOSSINESS': 298,          # Same input, but different values
            'SPECULAR': 264,
            'METALNESS': 230,
            'HEIGHT': 600, 'DISPLACEMENT': 750,           # MAY BE AUTOMATICALLY CONNECTED, Place bellow
            'BUMP': 570, 'NORMAL': 570,                   # In Cycles Bump and Normal is done via the same input
            'ALPHA': 540, 'MASK': 540,                    # Currently treating Alpha and Mask as the same thing
            'TRANSMISSION': 459,
            'EMISSION': 500,
            'UNKNOWN': -200,
            '_DISPLACEMENT': 650,
            '_UVNODE': 268, '_UVREROUTE': 300,
        },
        'ShaderNodeBsdfDiffuse':{
            'AO': -500,                                 # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'REFLECTION': -450, 'GLOSSINESS': -400,     # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'ALPHA': -350, 'MASK': -300,                # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'TRANSMISSION': -250, 'EMISSION': -200,     # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'SPECULAR': -150, 'METALNESS': -100,        # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'DIFFUSE': 34, 'ALBEDO': 34, 'COLOR': 34,   # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 75,
            'BUMP': 125, 'NORMAL': 125,                   # In Cycles Bump and Normal is done via the same input
            'HEIGHT': 250, 'DISPLACEMENT': 300,           # MAY BE AUTOMATICALLY CONNECTED, Place bellow
            'UNKNOWN': -200,
            '_DISPLACEMENT': 300,
            '_UVNODE': 48, '_UVREROUTE': 80,
        },
        'ShaderNodeBsdfGlossy':{
            'AO': -500,                                 # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'REFLECTION': -450, 'GLOSSINESS': -400,     # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'ALPHA': -350, 'MASK': -300,                # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'TRANSMISSION': -250, 'EMISSION': -200,     # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'SPECULAR': -150, 'METALNESS': -100,        # NOT AUTOMATICALLY CONNECTED TO NODE, Place above
            'DIFFUSE': 34, 'ALBEDO': 34, 'COLOR': 34,   # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 75,
            'BUMP': 125, 'NORMAL': 125,                   # In Cycles Bump and Normal is done via the same input
            'HEIGHT': 150, 'DISPLACEMENT': 300,           # MAY BE AUTOMATICALLY CONNECTED, Place bellow
            'UNKNOWN': -200,
            '_DISPLACEMENT': 300,
            '_UVNODE': 48, '_UVREROUTE': 80,
        },
        'FAUX': {
            'AO': -200, 'REFLECTION': -150, 'ALPHA': -100, 'MASK': -50,
            'DIFFUSE': 0, 'ALBEDO': 0, 'COLOR': 0,
            'SPECULAR': 50, 'METALNESS': 100,
            'ROUGHNESS': 150, 'GLOSSINESS': 200,
            'TRANSMISSION': 250, 'EMISSION': 300,
            'BUMP': 350, 'NORMAL': 400,
            'HEIGHT': 450, 'DISPLACEMENT': 500,
            'UNKNOWN': -300,
            '_UVNODE': 50, '_UVREROUTE': 50,
        }
      }
    },
    'OCTANE': {
        'EXP': {
            'OctaneUniversalMaterial': {
                'AO': -800, 'REFLECTION': -1000,
                'TRANSMISSION': -450,
                'DIFFUSE': -100, 'ALBEDO': -100, 'COLOR': -100,
                'SPECULAR': 600, 'METALNESS': 250,
                'ROUGHNESS': 950, 'GLOSSINESS': 950,
                'ALPHA': 1300, 'MASK': 1300,
                'BUMP': 1650, 'NORMAL': 2000,
                'HEIGHT': 2350, 'DISPLACEMENT': 2350,
                'EMISSION': 2700,

                '_TRANSFORM': 750, '_TRANSFORMREROUTE': 783,
                '_UVNODE': 980, '_UVREROUTE': 1013,
                '_COLORSPACENODE': 450,
                'UNKNOWN': -1500,

                # 'AO': -240, 'REFLECTION': -320,
                # 'ALPHA': -160, 'MASK': -80,
                # 'DIFFUSE': 180, 'ALBEDO': 180, 'COLOR': 180,
                # 'SPECULAR': 309, 'METALNESS': 212,
                # 'ROUGHNESS': 402, 'GLOSSINESS': 402,
                # 'TRANSMISSION': 84, 'EMISSION': 1824,
                # 'BUMP': 1608, 'NORMAL': 1640,
                # 'HEIGHT': 1670, 'DISPLACEMENT': 1670,
                # 'UNKNOWN': -500,
                # '_UVNODE': 1000, '_UVREROUTE': 1000,
            },
            'OctaneStandardSurfaceMaterial': {
                'AO': -800, 'REFLECTION': -1000,
                'DIFFUSE': -450, 'ALBEDO': -450, 'COLOR': -450,
                'METALNESS': -100,
                'SPECULAR': 250,
                'ROUGHNESS': 600, 'GLOSSINESS': 600,
                'TRANSMISSION': 950,
                'EMISSION': 1300,
                'BUMP': 1650, 'NORMAL': 2000,
                'HEIGHT': 2350, 'DISPLACEMENT': 2350,
                'ALPHA': 2700, 'MASK': 2700,

                '_TRANSFORM': 750, '_TRANSFORMREROUTE': 783,
                '_UVNODE': 980, '_UVREROUTE': 1013,
                '_COLORSPACENODE': 450,
                'UNKNOWN': -1500,
            },
            'FAUX': {
                'AO': -300, 'REFLECTION': -400, 'ALPHA': -200, 'MASK': -100,
                'DIFFUSE': 0, 'ALBEDO': 0, 'COLOR': 0,
                'SPECULAR': 100, 'METALNESS': 100,
                'ROUGHNESS': 200, 'GLOSSINESS': 300,
                'TRANSMISSION': 400, 'EMISSION': 500,
                'BUMP': 600, 'NORMAL': 700,
                'HEIGHT': 800, 'DISPLACEMENT': 900,
                'UNKNOWN': -500,
                '_COLORSPACENODE': 100,
                '_UVNODE': 50, '_UVREROUTE': 50,
            }
        },
        'COL': {
            'OctaneUniversalMaterial': {
                'AO': -100, 'REFLECTION': -200,
                'TRANSMISSION': 40,
                'DIFFUSE': 113, 'ALBEDO': 113, 'COLOR': 113,
                'SPECULAR': 259, 'METALNESS': 186,
                'ROUGHNESS': 332, 'GLOSSINESS': 332,

                'ALPHA': 970, 'MASK': 970,
                'BUMP': 1043, 'NORMAL': 1116,
                'HEIGHT': 1189, 'DISPLACEMENT': 1189,
                'EMISSION': 1275,
                'UNKNOWN': -300,

                '_UVNODE': 750, '_UVREROUTE': 760,
                '_TRANSFORM': 710, '_TRANSFORMREROUTE': 720,
                '_COLORSPACENODE': 500,
            },
            'OctaneStandardSurfaceMaterial': {
                'AO': -100, 'REFLECTION': -300,
                'DIFFUSE': 40, 'ALBEDO': 40, 'COLOR': 40,
                'SPECULAR': 186, 'METALNESS': 113,
                'ROUGHNESS': 259, 'GLOSSINESS': 259,
                'TRANSMISSION': 332,

                'EMISSION': 955,
                'BUMP': 1043, 'NORMAL': 1116,
                'HEIGHT': 1185, 'DISPLACEMENT': 1185,
                'ALPHA': 1250, 'MASK': 1250,
                'UNKNOWN': -200,

                '_UVNODE': 750, '_UVREROUTE': 760,
                '_TRANSFORM': 710, '_TRANSFORMREROUTE': 720,
                '_COLORSPACENODE': 500,
            },
            'FAUX': {
                'AO': -240, 'REFLECTION': -320, 'ALPHA': -160, 'MASK': -80,
                'DIFFUSE': 0, 'ALBEDO': 0, 'COLOR': 0,
                'SPECULAR': 80, 'METALNESS': 80,
                'ROUGHNESS': 160, 'GLOSSINESS': 240,
                'TRANSMISSION': 320, 'EMISSION': 400,
                'BUMP': 480, 'NORMAL': 560,
                'HEIGHT': 640, 'DISPLACEMENT': 720,
                'UNKNOWN': -500,
                '_UVNODE': 50, '_UVREROUTE': 50, '_TRANSFORM': 150, '_TRANSFORMREROUTE': 150,
                '_COLORSPACENODE': 230,
            }
        }
    }
}
mu_node_inputs = { # input <-> output mappings for adding nodes to the shader node tree
    # We have mappings since:
    #   a) Not all map ids matches 1:1 to shader node input names (even capitalized, like 'Color' vs 'Base Color')
    #   b) We have some special "maps"/nodes (eg. '_BUMPNODE')
    'CYCLES': {
        'ShaderNodeBsdfPrincipled': {
            'AO': None, 'REFLECTION': None,                                          # NOT AUTOMATICALLY CONNECTED TO NODE
            'HEIGHT': None, 'DISPLACEMENT': None,                                    # Not connected to shader node
            'DIFFUSE': 'Base Color', 'ALBEDO': 'Base Color', 'COLOR': 'Base Color',  # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 'Roughness', 'GLOSSINESS': 'Roughness',                     # Same input, but different values
            'SPECULAR': 'Specular',
            'METALNESS': 'Metallic',
            'BUMP': 'Normal', 'NORMAL': 'Normal',                                    # In Cycles Bump and Normal is done via the same input
            '_BUMPNODE': 'Normal', '_NORMALNODE': 'Normal',                          # Cycles converting nodes
            'ALPHA': 'Alpha', 'MASK': 'Alpha',                                       # Currently treating Alpha and Mask as the same thing
            'TRANSMISSION': 'Transmission',
            'EMISSION': 'Emission'
        },
        'ShaderNodeBsdfDiffuse': {
            'AO': None, 'REFLECTION': None, 'GLOSSINESS': None,       # NOT AUTOMATICALLY CONNECTED TO NODE
            'ALPHA': None, 'MASK': None,  'TRANSMISSION': None,       # NOT AUTOMATICALLY CONNECTED TO NODE
            'EMISSION': None, 'SPECULAR': None, 'METALNESS': None,    # NOT AUTOMATICALLY CONNECTED TO NODE
            'HEIGHT': None, 'DISPLACEMENT': None,                     # Not connected to shader node
            'DIFFUSE': 'Color', 'ALBEDO': 'Color', 'COLOR': 'Color',  # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 'Roughness',
            'BUMP': 'Normal', 'NORMAL': 'Normal',                     # In Cycles Bump and Normal is done via the same input
            '_BUMPNODE': 'Normal', '_NORMALNODE': 'Normal',           # Cycles converting nodes
        },
        'ShaderNodeBsdfGlossy': {
            'AO': None, 'REFLECTION': None, 'GLOSSINESS': None,       # NOT AUTOMATICALLY CONNECTED TO NODE
            'ALPHA': None, 'MASK': None,  'TRANSMISSION': None,       # NOT AUTOMATICALLY CONNECTED TO NODE
            'EMISSION': None, 'SPECULAR': None, 'METALNESS': None,    # NOT AUTOMATICALLY CONNECTED TO NODE
            'HEIGHT': None, 'DISPLACEMENT': None,                     # Not connected to shader node
            'DIFFUSE': 'Color', 'ALBEDO': 'Color', 'COLOR': 'Color',  # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 'Roughness',
            'BUMP': 'Normal', 'NORMAL': 'Normal',                     # In Cycles Bump and Normal is done via the same input
            '_BUMPNODE': 'Normal', '_NORMALNODE': 'Normal',           # Cycles converting nodes
        },
        'ShaderNodeBump': {
            'BUMP': 'Height', 'HEIGHT': 'Height'
        },
        'ShaderNodeNormalMap': {
            'NORMAL': 'Color'
        },
        'FAUX': {
            'AO': None, 'REFLECTION': None, 'ALPHA': None, 'MASK': None,
            'DIFFUSE': None, 'ALBEDO': None, 'COLOR': None,
            'SPECULAR': None, 'METALNESS': None,
            'ROUGHNESS': None, 'GLOSSINESS': None,
            'TRANSMISSION': None, 'EMISSION': None,
            'BUMP': None, 'NORMAL': None,
            'HEIGHT': None, 'DISPLACEMENT': None,
            '_BUMPNODE': None, '_NORMALNODE': None,
        }
    },
    'OCTANE': {
        'OctaneUniversalMaterial': {
            'AO': None, 'REFLECTION': None,                              # NOT AUTOMATICALLY CONNECTED TO NODE
            'HEIGHT': None,                                              # Not connected to shader node
            'DIFFUSE': 'Albedo', 'ALBEDO': 'Albedo', 'COLOR': 'Albedo',  # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 'Roughness', 'GLOSSINESS': 'Roughness',         # Same input, but different values
            'SPECULAR': 'Specular',
            'METALNESS': 'Metallic',
            'BUMP': 'Bump', 'NORMAL': 'Normal', 'DISPLACEMENT': 'Displacement',
            'ALPHA': 'Opacity', 'MASK': 'Opacity',                       # Currently treating Alpha and Mask as the same thing
            'TRANSMISSION': 'Transmission',
            'EMISSION': 'Emission',
        },
        'OctaneStandardSurfaceMaterial': {
            'AO': None, 'REFLECTION': None,                              # NOT AUTOMATICALLY CONNECTED TO NODE
            'HEIGHT': None,                                              # Not connected to shader node
            'DIFFUSE': 'Base color', 'ALBEDO': 'Base color', 'COLOR': 'Base color',  # Treating Albedo/Diffuse/Color as the same
            'ROUGHNESS': 'Specular roughness', 'GLOSSINESS': 'Specular roughness',     # Same input, but different values
            'SPECULAR': 'Specular color',
            'METALNESS': 'Metalness',
            'BUMP': 'Bump', 'NORMAL': 'Normal', 'DISPLACEMENT': 'Displacement',
            'ALPHA': 'Opacity', 'MASK': 'Opacity',                       # Currently treating Alpha and Mask as the same thing
            'TRANSMISSION': 'Transmission color',
            'EMISSION': 'Emission', 'EMISSION_COLOR': 'Emission color',
        },
        'FAUX': {
            'AO': None, 'REFLECTION': None, 'ALPHA': None, 'MASK': None,
            'DIFFUSE': None, 'ALBEDO': None, 'COLOR': None,
            'SPECULAR': None, 'METALNESS': None,
            'ROUGHNESS': None, 'GLOSSINESS': None,
            'TRANSMISSION': None, 'EMISSION': None,
            'BUMP': None, 'NORMAL': None,
            'HEIGHT': None, 'DISPLACEMENT': None,
            '_BUMPNODE': None, '_NORMALNODE': None,
        }
    }
}
mu_ocio_colorspace_map = {
    '_DEFAULT': 'sRGB',
    'sRGB': {
        '_DEFAULT': 'sRGB',
        'GREYSCALE': 'sRGB'
    }
}