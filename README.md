# Material utilities v2.1-beta
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

An add-on for Blender 2.8x that lets the user assign materials directly in the 3D viewport
(via a keyboard shortcut and a pop up menu), as well as select by material and more!

**This is Beta, it's stable, but it's not guaranteed bug free**\
Each part is tested thoroughly during development, but we can't guarantee that there in't a special case where a problem might occur!\
Please read the list of [Known issues](#known-issues) below, if your problem isn't listed, please leave a bug report.

## Version

The current **Beta** version of Material Utilities is [**v2.1.1**](CHANGELOG.md#v2.1.1)\
(Major version indicates big changes or feature adds, Minor version bigger bugfixes and changes to existing features,
  Patch version [last number] indicates small changes and fixes)

## Table of Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [Known issues](#known-issues)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Background

This is based on the Add-on *Material Utils*, originally written for Blender 2.4 (and then ported to 2.5, 2.6 etc).\
I was really missing this Add-on when I started using Blender 2.80. But I couldn't find any ports of it (or even any in development),
so I decided to port it myself, and this is the result!

The goal is to include (almost) every feature it had in 2.7x,
but I'm also adding some features that I think (and hope others will as well) will be useful!\
If you're missing something, please send in a request and we'll see what we can do!

If you want to know what's different (including code wise), take a look at the [Differences](differences.md) document.\
But here are some examples:
- Some functions (like "Clean Material Slots") now also work on Curve and Surface objects
- The Select By Material have the option to extend the current selecction
- Assign Material have options to override or append materials in Object Mode

## Installation

1. Download the Add-on as a ZIP-file.
2. In Blender 2.8x go to *Edit* > *Preferences*, select *Add-ons* in the left panel, and then *Install* in the upper right.
3. Browse to where you saved the ZIP-file, select it and click on *Install Add-on from File*.
4. Click the checkbox to the left to enable the Add-on.
5. Click the menu icon in the lower left and select *Save Current State*

## Usage

### Popup menu

The default shortcut for Material Utilities is `[Shift + Q]`.\
[![Material Utilities - popup menu](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_Menu-e1562975806841.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_Menu.png)

*Tip:* All operators and options have descriptive tooltips

You can set the defaults of several options, such as the default name for new materials, in the Preferences
(Open Blender Preferences, go to Add-ons, find *Material Utilities*)

- **Assign Material**\
  Gives you a list of all available materials (including the option to create a new material).\
  Assigns the material you choose to the current selection.\
  Add the top of the menu you have options to Add a new material and "Search" for a material
  (you can change when this appears in the preferences),
  which can be useful if you have a lot of materials in your project.
  Both of these will open the operator panel as a "dialog" in your viewport.\
  In the operator the `+` (plus) button to the right will let you add a new material.
  In Object Mode you have the option to select how the existing material (slots) should be treated
  (In Edit mode it will append the material if it's not already in a material slot).\
  [![Material Assignment](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_AssignMat5-e1564786914277.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_AssignMat5.png)

  - **Override all assigned slots**\
    Will remove any material previously assigned to the object(s) and add the one you've chosen
  - **Assign material to currently selected slot**\
    Sets the material you choose to only the currently active material slot (in the Material Properties panel).
    It will leave the rest of the materials untouched.
  - **Assign material to each slot**\
    Keeps all the material slots, and their assignment to respective parts of the object.
    But will replace each material in those slots with your chosen material.\
    (This is recommended when materials are linked to the object)
  - **Append material**\
    Keeps all materials slots, but appends your chosen material (if it's not already in a slot),
    and assigns the whole object to that material slot.\
    (This is **not recommended** when materials are linked to object, and there's linked duplicates of the object)

- **Select by Material**\
  Gives you a list of all available materials (in Edit mode it only shows the materials assigned to the object).\
  Selects all objects (in Object Mode) or faces (in Edit Mode) that have the material you choose.\
  In the operator panel `[F9]` you can choose to extend your current selection, otherwise what was selected before will be unselected first.\
  [![Select By Material](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_SelectByMat_2-e1563064147331.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_SelectByMat_2.png)

- **Copy Materials to Seleted** (Object Mode only)\
  Copies all the materials of the active object to the other selected objects.

- **Clean Slots**
  - **Clean Material Slots**\
    Removes any material slots that isn't assigned to any part of the object
  - **Remove Active Slot** (Object Mode only)\
    You can limit it to only the active object in the operator panel `[F9]`
  - **Remove All Material Slots** (Object Mode only)\
    Remove all material slots (and thus materials) assigned to the selected object(s).\
    You can limit it to only the active object in the operator panel `[F9]`

- **Replace Material**\
  Replace any occurence of one material, **Original**, with another material, **Replacement**.\
  In the operator panel you can also choose if you want it done "globally" (for all objects in the file),
  or just for selected objects.\
  You can also choose to have the objects that were affected by the change selected (objects not affected will be deselcted).\
  [![Replace Material](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_ReplaceMaterial_2-e1563065836955.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_ReplaceMaterial_2.png)

- **Set Fake User**\
  Set the Fake User flag (to preserve unused materials) of the materials to either
  **On** or **Off**, or **Toggle** (on a per material basis) their current states.\
  You can limit the action to **Unused** materials (Default), **Used** materials, **All** materials,
  materials of the **Selected** objects, of the **Active** object, or of all objects in the current **Scene**.\
  [![Set Fake User](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_SetFakeUser_2-e1564786813579.png)](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_SetFakeUser_2.png)

- **Change Material Link**\
  Change how the material slots are linked, to either the **Data** (i.e. Mesh Data) or to the **Object**,
  or **Toggle** (on a per material basis) what they are currently are linked to.\
  You can limit the action to material slots of the **Selected** objects (Default), of the **Active** object,
  of all objects in the current **Scene**, or of **All** objects in the file.\
  When switching to *Linked to Object* the materials assigned the materials assigned to the slots will be kept intact.\
  When switching to *Linked to Data* there's a possibility that there's already an material assigned to the *Mesh Data*.\
  If there is no material assigned to the data, the material of the object will be kept.\
  If there is an material assigned to the data, that material will be used by default, or you can force the use of the material assigned to the object, by enabling **Override Data Material** (Do note that this will affect all objects that share the same *Data* and have materials linked to the *Data*).\
  [![Change Material Link](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_ChangeMaterialLink_3-e1564786727327.png)](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_ChangeMaterialLink_3.png)

- **Specials**
  - **Merge Base Names**\
    Finds materials such as `Material`, `Material.001`, `Material.002` and merges them into a single material (`Material`).\
    You can select a specific **Material Base Name** (such as `MyMaterial`) to find duplicates of (`MyMaterial.001` etc).\
    By enabling **Auto Rename/Replace** it will find all materials that are "duplicates" and merge them into a single material.\
    **Do note** that this only keeps the base material (`MyMaterial`) and ignores the other versions (`MyMaterial.001` etc)\
    [![Merge Base Names](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_MergeBaseNames-e1563021414948.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_MergeBaseNames.png)

  - **Join By Material**\
    This is the opposite of "Seperate By Material" in Edit mode.
    It finds objects that have the same material and join them together.\
    You can set a specific **Material**, where all objects that have that material will be joined.\
    Or you can choose to **Automatically Join**, where objects that share the same material will be joined (no matter what the material is).\
    If there's different types of objects (Mesh, Curves etc) that shares the same material,
    those will be joined according to their type.\
    **Do note** that if the objects have multiple materials, the resulting joins might not be as you predicted.\
    **Tip:** If you have objects that you don't want to be affected, you can hide them from the viewport first.\
    [![Join By Material](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_JoinByMaterial-e1564691922884.png)](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_JoinByMaterial.png)


### Material Specials menu

Material Utilities adds some options to the **Material Specials** menu as well (accessible by the small downward pointing arrow to the right of the materials list).\
At the bottom of this menu (below **Paste Material**), most of the options from the popup menu (detailed above) is added.
And at the top two other options are added:

- **Move slot to top**\
  Moves the currently selected material slot to the top of the list
- **Move slot to bottom**\
  Moves the currently selected material slot to the bottom of the list

[![Material Specials menu](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_MaterialSpecials-e1562975670283.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_MaterialSpecials.png)

### Preferences

In the Add-on Preferences (Go to the Prefences in Blender [Edit menu] and the `Add-ons` section, find the Material Utilities Add-on, either by searching or selecting the `Material` category) you have the options to change some settings for this Add-on.\
The defaults section lets you set the default options (like the default material name when adding a new material)
for several of the operators that is described above.\
The `Show 'Search' Limit` lets you choose how many materials there should be before the `Search` option in the *Assing Material* and *Select By Material* menus. Set it to `0` (default) to always show `Search` in the menus.\
[![Material Utilities preferences](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_Preferences3-e1564790495840.png)](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_Preferences3.png)

## Known issues

There's currently no known issues.  

(**Do note** that each spline/curve in Curve Objects can only have one material,
  so you can't assign different materials to different parts of a spline)

## Support

Support is given when time is available, you can ask for support via https://chris.hindefjord.se/contact/. \
If you think you've find a bug, please
[report it by creating an issue](https://github.com/ChrisHinde/MaterialUtilities/issues)!\
Bug reports takes precedence over other support requests!

## Contributing

You're welcome to contribute to this Add-on.\
If you want to know where to start, take a look at the [TODO](TODO) file.

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgements

This Add-on is based on and uses (some) code by the following awesome people:\
Michael Williamson (michaelw) (original author)\
Sybren\
meta-androcto\
Saidenka\
lijenstina\
CoDEmanX\
SynaGl0w\
ideasman42

(If you think your code is used in this add-on, but you're not listed here,
please contact ChrisHinde so correct attribution can be given)
