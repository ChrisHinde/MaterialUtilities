# PBR Texture Set Import

## Table of Contents

- [Introduction](#introduction)
- [Support and Compatibility](#support-and-compatibility)
  - [Supported Render Engines](#supported-render-engines)
  - [Supported Texture Maps](#supported-texture-maps)
  - [Supported File Types](#supported-file-types)
- [Color spaces](#color-spaces)
- [Popup menu](#popup-menu)
  - [Open Image Texture Set](#open-image-texture-set)
  - [Replace Image Texture Set](#replace-image-texture-set)
- [Add new PBR material](#add-new-pbr-material)
- [Preferences](#preferences)

## Introduction

This feature lets you import a whole set of textures in one action. It's main purpose is to add a set of PBR (Physically Based Rendering) textures (sometimes called a *PBR material*), but it will import any set of textures to your material (no matter if they follow a certain naming convention or not).
If you've already added a texture set to your material you can also automatically replace those textures with a new set (keeping the overall material setup)

You can access the functions of this feature in the same way as the main menu for Material Utilities: with the keyboard shortcut `Shift+Q` (by default), but in the *Shader Editor* instead of the *3D View*. There is also an addition to the *Specials* in the Material Utilities menu in the *3D View* 

### Background

This started with I (ChrisHinde) had a want to try out several different textures sets on a single object, and I found the manual actions tedious. Hopefully this will also help someone else in a similar situation.

## Support and Compatibility

### Supported Render Engines

Unlike the rest of the Material Utilities, this feature is limited to specific render engines, simply due to that different render engines use different shader and texture nodes. But support for more render engines could be added if they are requested.
Currently the supported render engines are:

- **Cycles**/**Eevee** (or any other engine that might use the same nodes)
- **Octane Render** (Both add-on and the Octane Blender Build)

### Supported Texture Maps

While any texture can be imported with this feature, only specific texture maps will be recognized and connected properly.

- **AO**/**Ambient Occlusion** ¤
  Will not be automatically connected
- **Albedo**/**Diffuse**/**Color**
  Treated as the same type of map
- **Alpha**/**Opacity**/**Mask** ¤
  Treated as the same type, connected to **Alpha** or **Opacity**
- **Bump** ¤
  Will be connected through a *Bump* node for Cycles
- **Displacement** ¤
  Will be connected through a *Displacement* node, connected to the Material Output, for Cycles.
- **Emission**
  Will be connected through a *Texture Emission* node for Octane.
- **Glossiness** ¤
 Will be inverted, with an invert node for Cycles, or in the texture options for Octane, and connected as **Roughness**
- **Height** ¤
Can be imported/connected as either *Bump* or *Displacement*, or not connected at all, depending on the chosen option in the import dialog.
- **Metalness**/**Metallic** ¤
- **Normal** ¤
Will be connected through a *Normal Map* node, and then via the *Bump* node, if also added, for Cycles.
- **Roughness** ¤
- **Specular** ¤
- **Transmission**
- ***Render***/***Sample***
Some texture sets might contain a sample render among the textures, if one is detected it will be ignored and not imported

Maps marked with ¤ will be treated as "non-color" (see [Color Spaces](#color-spaces) for more information)

**Notable:** The different maps are detected via their filenames (e.g. `tiledfloor_diffuse.jpg`, `brickwalldiff.png` will be interpreted as Diffuse maps), but the process to do so isn´t necessarily 100% accurate. It can give both false positives and false negatives (e.g. `maoi_displace.png` could be identified as an AO map instead of an Displacement map). The maps are detected in order of "importance", to try to avoid any major issues.

### Supported Shader Nodes

The main idea is to import PBR textures and connect them up to a universal/principled shader node (that can take full use of a PBR texture set), support for some more basic shaders has been added.
- **Cycles**/**Eevee**
  - **Principled BSDF**
  - **Diffuse BSDF** (Only connects *Color*, *Roughness*, *Bump*, and *Normal*)
  - **Glossy BSDF** (Only connects *Color*, *Roughness*, *Bump*, and *Normal*)
- **Octane Render**
  - **Universal Material**
  - **Standard Surface Material**
  (Emission maps can be connected either directly to the *Emission color* input or via an *Texture Emission* node. In either case the *Emission weight* will be set to `1.0`)

### Supported File Types

The currently recognized file formats are:

- JPG
- PNG
- EXR
- HDR
- TIFF
- TGA

All other filetypes will be ignored.

## Color Spaces

By default* the color space will be set to (sRGB) Linear for most filetypes, except for JPG and PNG, which will be set to sRGB. The default color space can be overridden if there's an appropriate tag in the filename (e.g. `brick_diffuse_aces.exr`). For JPG and PNG files any such tags will be ignored (by default*), and the sRGB color space kept.

Additionally some maps, that shouldn't contain any color data, will be treated as "non-color" (marked with ¤ in the [list of supported texture maps](#supported-texture-maps)).
For Cycles that means that the color space will set to *Non-Color*, unless the color space is overridden.
For Octane those textures will be added as Greyscale (or *Grayscale*) images (except *Normal maps*).

(*You *can* change this behavior, but it isn't exposed in the preferences, so if you *really* want to, you can change it in `enum_values.py`, look for `colorspace` and `texturemaps`)

### Color Spaces in Octane

In Octane there is a *Color space* node (instead of just a property of the image data, as for Cycles), that also have the possibility to have any number of available color spaces (depending on the loaded OCIO configuration).
So for imports into an Octane material setup we can add (if enabled) a *Color space* node for each unique color space. We will also add one *Color space* node connected to just *RGB images*, and one connected to just *Grayscale images* (So if the color map is ACES, but the rest is sRGB you'll get one *Color space* node for ACES, one for sRGB color, one for sRGB greyscale).

**NB:** For the *Color space* nodes to work correctly, you **do need** some kind of OCIO config set in the Octane Add-on settings.
(*Material Utilities* assumes that the config loaded is the official ACES config, if not the default "IDs" might not be compatible, if so, you can manually change the mapping by looking for `mu_ocio_colorspace_map` in `enum_values.py`)

### Recognized color spaces

- **sRGB**
- **Linear sRGB**
- **ACES** (linear)
- **ACEScg** (linear)
- **Filmic** (only recognized by Cycles)
- **Filmic Log** (only recognized by Cycles)

## Popup menu

You access the popup menu via `[Shift+Q]` in the *Shader Editor* (There is also an option, in the preferences, to add it to the top menu in the editor)

Either option in the menu will bring up a file selection dialog. By default this dialog will let you select a specific directory (but not specific files), you can change the default behavior in the preferences, or by holding `[Ctrl]` or `[Shift]` while clicking (or hitting `[Enter]`) on the option (`[Ctrl]` will always bring up directory selection, `[Shift]` will always bring up file selection)

[IMG]

### Open Image Texture Set

#### Importing

After you've selected a directory (or specific files) *Material Utilities* will go through the files, try to determine the texture map type, [color space](#color-spaces), add the appropriate image texture node, and then connect them (if enabled) to the shader node.

**Please note** that the import might take some time (especially with Octane [remember to have the render server running]), and that Blender will become unresponsive during the import (and no progress information will, at the moment, be shown).

#### Import options

- ##### Connections
  - **Connect to Shader**
  Connect each imported texture to the shader node (otherwise the image texture nodes will be added to the node setup, but no connections will be automatically made)
  - **Connect Alpha Channel**
  For Cycles: Connects the *Alpha* output of the *Color*/*Diffuse* node to the *Alpha* input of the shader node.
  For Octane: Detects the tags: `walpha`, `w_alpha`, `withalpha`, and `with_alpha`, in the filename (no analysis of the image data will be done), and then adds a new *Alpha Image Texture* node with the image, connecting it to the *Opacity* input of the material node.
  - **Add Color Spaces** (Octane)
  Will add one, or multiple, *OCIO Color Space* node(s), set the appropriate color space, and connect to the *Color space* input of the texture node.
  Read more in the [Color space](#color-spaces) section.
- ##### Appearance
  - **Set node labels**
  Sets the labels of the added nodes to match the texture map. In Octane whether it is an *RGB* or *Greyscale* node will be added to the label.
  Ex: `DIFFUSE` or `DIFFUSE - RGB` for Octane
  - **Collapse texture nodes**
  Whether or not to collapse (or "hide") the texture nodes. This will give a neater node setup, but might not be wanted if you plan to change the different node options.
  - **Stair step nodes**
  If you don't want to have collapsed nodes you have the option to have the texture nodes arranged in two columns, in an alternating fashion. This will make the node setup more compact (vertically). Otherwise the texture nodes will be arranged in a single column (with no overlapping)
- ##### Map options
  - **Reflection as Specular**
  Import, and connect (if enabled), the reflection map as a specular map. Otherwise reflection maps will not be connected to the shader node.
  - **Height Map Treatment**
  Choose how height maps should be imported and treated.
    - **As Displacement** - Import the height map as displacement (will add the appropriate nodes, if node connection is enabled)
    - **As Bump** - Import the height mop as a bump map.
    - **Don't connect** - Imports the height map, but it will not be connected (and placed above the node setup)

    **NB:** Importing Height as Displacement or Bump might take prescedence over actual displacement or bump maps.
  - **Emission map treatment** (only for *Standard Surface Material* in Octane)
  Choose how the emission map will be added and connected to the material node.
    - **Use Texture Emission Node** - Add an *Texture Emission* node, and connect the emission map via it. Will set *Emission weight* to `1.0` and *Emission color* to 100% white.
    - **Connect to Emission color** - Connects the emission map directly to the *Emission color* input of the material5. Will set *Emission weight to `1.0`.
    - **Don't connect** - The emission map will be imported, but not connected to the material node.

### Replace Image Texture Set

When using *Replace Image Texture Set* no additional nodes will be added, instead the selected texture maps will be matched to the existing texture nodes. If a matching node is found, the image in the existing node will be replaced with the image in the texture set being imported.
**NB:** If no matching node is found, that texture map will be ignored. Likewise: if there exist a texture node, in the current node setup, that doesn't have a matching texture map in the set that is being imported, that node will be left as is (at least in the current version).

#### Import options

- **Only selected nodes**
Will only consider the selected nodes when looking for textures to replace, all other textures will be left as-is.
- **Wide search**
Go through all nodes in the material, if the matching node is not immediately found (connected to the first shader node). With this disabled it will only look at the image texture nodes connect to the first shader node. Wide search might take a longer time (in material setups with more nodes), but is also needed for node setups where the image textures aren't connected directly to the shader node. (The alternative being to manual select the correct nodes, and enable *Only selected nodes*)
- **Set Fake user**
Will set the *Fake user* flag on the images that gets replaced (to keep them in the .blend-file)

## Assign new PBR material

*Assign new PBR material* functions like *Open Image Texture Set*, but it will create a whole new material, with a Principled BSDF shader for Cycles, or Universal Material (or Stand Surface Material) for Octane, that the texture set then will be added to.
The import settings in the right properties panel is the same as for [Open Image Texture Set](#open-image-texture-set), with added *Material Options*:

### Where to find it

You can access *Assign new PBR material* via *Specials* in the [3D viewport menu](usage.md#popup-menu), by holding `[Ctrl]` or `[Shift]` (see [opening the Popup menu](#popup-menu)), or it can be added as an button to the [*Assign Material* dialog](usage.md#assign-material) (needs to be enabled in the [preferences](#preferences)).

[IMG]

### Material options

- **Assignment method** (In *Object mode*)
Decides how the new material should be assigned to the object, [read more about the options in the main documentation](usage.md#assignment-method).
- **Material Node Type** (Octane only)
Lets you set whether to base the new material on an *Universal Material* Node, or a *Standard Surface Material*. (Tip: You can set the default option in the [preferences](#preferences))
- **Material Name**
The name you want the material to have, if it is left empty the name of the directory will be used.

## Preferences

In the [add-on preferences](usage.md#preferences) you can find and change several preferences that affects how the PBR texture import works.

- **Add menu to shader editor header**
Adds an extra *Material Utilities* menu option to the shader editor header, where you can access the PBR texture import functions.
- **Add to Assign Material dialog**
Will add an button to the upper left in the [Assign Material dialog](usage.md#assign-material)

### File Selection

- **Texture directory**
  Lets you choose the directory that should be shown, by default, when using PBR texture import
  - **Default directory** - Will use the global texture directory, set in Blender's *File paths* preferences.
  - **Last used** - Will re-open the directory from where the last import happened.
  - **Custom directory** - Lets you choose a custom directory
- **Custom directory**
  If you choose *Custom directory* for *Texture directory*, you can set that here.
- **File selection**
Set whether you want to choose a directory or specific texture files, by default, when importing textures.

### Connections & Support Nodes

- **Connect to shader**
Enable connecting the added texture nodes to shader node, by default
- **Connect Alpha channel**
Enable connecting Alpha to the shader node, by default.
- **Reflection as Specular**
Enable importing Reflection maps as Specular maps, by default.
- **Add new UV Map node**
Always add new UV map nodes when importing ([Opening](#open-image-texture-set)) texture sets.
(This isn't exposed in the import dialog)

### Placement & Appearance

These options set the defaults for the properties under [Appearance](#appearance) in the import dialog.

### Height & Bump Options

- **Height map treatment**
Will set the default option for how to treat height maps, under [*Map options*](#map-options) in the import dialog.
- **Bump distance**
The default value for *Distance* on added *Bump* nodes (only Cycles/Eevee).
(This isn't exposed in the import dialog)

### Replacing Textures

These options set the defaults for the properties in the [Replace textures](#replace-image-texture-set) dialog.

### Octane Specific

- **Add Color spaces**
Enable *Add Color spaces*, under [Connections](#connections) in the import dialog, by default.

# Document info

Written by ChrisHinde for version 3.0.0 of Material Utilities (2023-06-25, v1)
CC-BY-SA