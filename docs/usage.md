# Material Utilities - Usage

## Table of Contents

- [Popup menu](#popup-menu)
  - [Assign Material](#assign-material)
  - [Select by Material](#select-by-material)
  - [Copy Materials to Selected](#copy-materials-to-selected)
  - [Clean Slots](#clean-slots)
  - [Replace Material](#replace-material)
  - [Replace Multiple Material](#replace-multiple-materials)
  - [Set Fake User](#set-fake-user)
  - [Change Material Link](#change-material-link)
  - [Specials](#specials)
    - [Merge Base Names](#merge-base-names)
    - [Join By Material](#join-by-material)
    - [Assign New PBR Material](#assign-new-pbr-waterial)
    - [Remove Unused Materials](#remove-unused-materials)
    - [Set Auto Smooth](#set-auto-smooth)
- [Material Specials Menu](#material-specials-menu)
- [Preferences](#preferences)

## Popup menu

The default shortcut for Material Utilities is `[Shift + Q]`.
[![Material Utilities - popup menu](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_Menu-e1562975806841.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_Menu.png)

*Tip:* All operators and options have descriptive tooltips

You can set the defaults of several options, such as the default name for new materials, in the [Preferences](#preferences)
(Open Blender Preferences, go to Add-ons, find *Material Utilities*)

### Assign Material

Gives you a list of all available materials (including the option to create a new material).\
It will assign the material you choose to the current selection.
At the top of the menu you have options to Add a new material or "Search" for an existing material \
(you can change when this appears in the preferences),
which can be useful if you have a lot of materials in your project.
Both of these will open the operator panel as a "dialog" in your viewport.\
The `+` (plus) toggle to the right, in the panel, will let you add a new (or search for an existing) material.\
[![Material Assignment](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_AssignMat5-e1564786914277.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_AssignMat5.png)

#### Assignment method

In Object Mode you have the option to select what will happen to the existing material (slots), and where the new material should be placed.
(In Edit mode the material will be appended if it's not already in a material slot).

- **Override all assigned slots**\
Will remove any material previously assigned to the object(s) and add the one you've chosen
- **Assign material to currently selected slot**\
Sets the material you choose to only the currently active material slot (in the *Material Properties* panel).
It will leave the rest of the materials untouched.
- **Assign material to each slot**\
Keeps all the material slots, and their assignment to respective parts of the object.
But will replace each material in those slots with your chosen material.\
(This is recommended when materials are linked to the object)
- **Append material**\
Keeps all materials slots, but appends your chosen material (if it's not already in a slot),
and assigns the whole object to that material slot.\
(This is **not recommended** when materials are linked to object, and there's linked duplicates of the object)

### Select by Material

Gives you a list of all available materials (in Edit mode it only shows the materials assigned to the object).\
When you choose a material all objects (in Object Mode) or faces (in Edit Mode),that have that material assigned, will be selected.\
In the operator panel `[F9]` you can choose to extend your current selection, otherwise what was selected before will be unselected first.\
[![Select By Material](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_SelectByMat_2-e1563064147331.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_SelectByMat_2.png)

### Copy Materials to Selected

- **In Object Mode:** Copies all the materials of the active object to the other selected objects.
- **In Edit Mode:** Copies the material of the active face to the other selected faces
    (works if you have multiple objects in Edit Mode as well).\
    (**NB:** You need to have Face Select enabled to use this)

### Clean Slots

- **Clean Material Slots**\
Removes any material slots that aren't assigned to any part of the object
- **Remove Active Slot** (Object Mode only)\
Will remove the material slot that is currently selected.
You can limit it to only the active object in the operator panel `[F9]`
- **Remove All Material Slots** (Object Mode only)\
Remove all material slots (and thus materials) assigned to the selected object(s).\
You can limit it to only the active object in the operator panel `[F9]`

### Replace Material

Replace any occurrence of one material, **Original**, with another material, **Replacement**.\
In the operator panel you can also choose if you want it done "globally" (for all objects in the file),
or just for selected objects.\
You can also choose to have the objects that were affected by the change selected (objects not affected will be deselected).\
[![Replace Material](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_ReplaceMaterial_2-e1563065836955.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_ReplaceMaterial_2.png)

### Replace Multiple Materials

**NB:** This needs to be enabled in the add-on settings before use!
Use this to replace a list of materials with the matching material in a second list.
This feature is functional, but needs more polish to be more user friendly!
Currently this uses text block(s) (one line per material name/substitute) for the lists:

1. Setup the list(s) in the text editor (or load it in from a text file).
    You have the option to use two text blocks (one for the materials that should be replaced, and one for the materials to replace with).
    Or you can use one text block, where each line contains both the material name and the material that it should be \
    replaced with, separated by, at least, one tab or two spaces (to allow material names with [single] spaces in them)
2. Go to **Replace Multiple Materials** in the Material Utilities menu
3. Select the text blocks that have the materials list for **Original** and **Replacement**.
    If you only have one list that contains both the original material names and replacements, select that for \
    **Original** and leave **Replacement** empty.
4. Select whether only selected objects or all objects should be checked, and whether or not to update the selection \
    (works the same as for **Replace Material**)
5. Run the replacement by clicking **OK**

### Set Fake User

Set the *Fake User flag* (to preserve unused materials) of the materials to either
**On** or **Off**, or **Toggle** their current states (on a per material basis).\
You can limit the action to **Unused** materials (default), **Used** materials, **All** materials,
materials of the **Selected** objects, of the **Active** object, of the **Active Collection**, of a **Selected Collection**, or of all objects in the current **Scene**.\
[![Set Fake User](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_SetFakeUser_2-e1564786813579.png)](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_SetFakeUser_2.png)

### Change Material Link

Change how the material slots are linked, to either the **Data** (i.e. Mesh Data) or to the **Object**,
or **Toggle** what they are currently are linked to (on a per material basis).\
You can limit the action to material slots of the **Selected** objects (default), of the **Active** object,
of the **Active Collection**, of a **Selected Collection**, of all objects in the current **Scene**, or of **All** objects in the file.\
When switching to *Linked to Object* the materials assigned the materials assigned to the slots will be kept intact.\
When switching to *Linked to Data* there's a possibility that there's already an material assigned to the mesh data.\
If there is no material assigned to the data, the material of the object will be kept.\
If there is an material assigned to the data, that material will be used by default, or you can force the use of the material assigned to the object, by enabling **Override Data Material** (Do note that this will affect all objects that share the same mesh data and have materials linked to the data).\
If you enable **Unlink Material From Old Link** the material will be "unlinked" from what it was linked to before when the linking is changed.
[![Change Material Link](https://chris.hindefjord.se/wp-content/uploads/2020/08/MU_MaterialLink_20200801-e1596319891375.png)](https://chris.hindefjord.se/wp-content/uploads/2020/08/MU_MaterialLink_20200801.png)

### Specials

#### Merge Base Names

Finds materials such as `Material`, `Material.001`, `Material.002` and merges them into a single material (`Material`).\
You can select a specific **Material Base Name** (such as `MyMaterial`) to find duplicates of (`MyMaterial.001` etc.).\
By enabling **Auto Rename/Replace** it will find all materials that are "duplicates" and merge them into a single material.\
**Do note** that this only keeps the base material (`MyMaterial`) and ignores the other versions (`MyMaterial.001` etc.)\
You can choose to give the material a new name after all the duplicates have been merged by "checking" the icon
to the right of the material name (a box where you can enter the new name will appear).\

[![Merge Base Names](https://chris.hindefjord.se/wp-content/uploads/2019/11/MU_MergeBaseNames_3-e1572996566823.png)](https://chris.hindefjord.se/wp-content/uploads/2019/11/MU_MergeBaseNames_3.png)

- **Patterns**\
    If you want to merge materials based on another pattern than the the default Blender way (such as `Material_001` instead of `Material.001`)
    you can change the Pattern option to set a custom delimiter (e.g. `.` `_` `,`) or define your own pattern with
    (Python style) Regular Expressions, you can use `%BASE_NAME` to indicate the base part of the name
    (or just make sure it's a group, the operator expects one group matching the base name, e.g `MyMaterial`, and a second group matching the suffix, e.g. `042`)\
    The default regular expression is `^%BASE_NAME\.(\d{1,3})$` which matches materials like `MyMaterial.003` as well as `MyMaterial.2` (The `%BASE_NAME` token just translates to `(.*)`).

#### Join By Material

This is the opposite of "Separate By Material" in Edit mode.
It finds objects that have the same material and join them together.\
You can set a specific **Material**, where all objects that have that material will be joined.\
Or you can choose to **Automatically Join**, where objects that share the same material will be joined (no matter what the material is).\
If there's different types of objects (Mesh, Curves etc.) that shares the same material,
those will be joined according to their type.\
**Do note** that if the objects have multiple materials, the resulting joins might not be as you predicted.\
**Tip:** If you have objects that you don't want to be affected, you can hide them from the viewport first.\
[![Join By Material](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_JoinByMaterial-e1564691922884.png)](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_JoinByMaterial.png)

#### Assign New PBR Material

This function is detailed in the [PBR Texture Set Import documentation](pbr_import.md)

#### Remove Unused Materials

Removes any and all materials that isn't used (i.e. materials that has zero users).
This is similar to *File* > *Clean Up* > *Unused Data-Blocks*, but only looks for unused materials.

#### Set Auto Smooth

Enables the *Auto Smooth* option (otherwise found under *Normals* in the *Object Data* panel) and sets the *Auto Smooth Angle*
to the chosen value for the selected objects (or the objects you choose to affect).\
This is useful when you want to set enable *Auto Smooth* or set the *Auto Smooth Angle* for multiple objects.\
You can choose to *Set Smooth* shading for the affect objects as well. Auto smooth only works on surfaces that has
smooth shading, but **do note** that the *Set Smooth* will override any parts that might have been set to flat shading.\
In the preferences for the Add-on you can set your desired default angle, as well as the default options for *Affect*.\
[![Set Auto Smooth](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_SetAutoSmooth-e1565642419495.png)](https://chris.hindefjord.se/wp-content/uploads/2019/08/MU_SetAutoSmooth.png)

##### Note about Active collection limiting

The *Active collection* isn't necessarily the same as the collection of the active object.
Please check the outliner to verify which collection is active, or choose a specific collection to limit which objects and materials gets affected.

## Material Specials menu

Material Utilities adds some options to the **Material Specials** menu as well (accessible by the small downward pointing arrow to the right of the materials list).\
At the bottom of this menu (below **Paste Material**), most of the options from the popup menu (detailed above) is added.
And at the top two other options are added:

- **Move slot to top**\
  Moves the currently selected material slot to the top of the list
- **Move slot to bottom**\
  Moves the currently selected material slot to the bottom of the list

[![Material Specials menu](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_MaterialSpecials-e1562975670283.png)](https://chris.hindefjord.se/wp-content/uploads/2019/07/MU_MaterialSpecials.png)

## Preferences

The preferences panel have been updated with version 3.0.0 of Material Utilities. The preferences are now structures in three categories/tabs: `Defaults`, `Texture Set Import` and `Miscellaneous`, and each tab is divided into several subcategories (as "pulldowns").

[![Material Utilities preferences](https://chris.hindefjord.se/wp-content/uploads/2023/06/MU_Preferences_3.0.0_Defaults.png)](https://chris.hindefjord.se/wp-content/uploads/2023/06/MU_Preferences_3.0.0_Defaults.png)

### Defaults

This tab lets you set the default options (like the default name used when adding a new material) for several of the operators described above.
Each setting here corresponds directly to the options for the matching operator.

### Texture Set Import

These settings are described in the documentation for [PBR Texture Set Import](pbr_import.md#preferences).

### Miscellaneous

This last tab is for settings that doesn't fit in the other two, divided in two subcategories:

- **Limits**
  - Here you can change when the option to search for materials appears at the the top of the *Assign Material* and *Select By Material* menus. Set `Show 'Search' Limit` to `0` to always show `Search` in the menus (default).
  - `Search` (with `Add new material`) can also appear at the bottom of the menus, given a certain numbers of materials (so you don't have to go to scroll to the top of the menu if Blender happens to align the menu at the bottom). By setting `Show 'Search' at Bottom Limit` you can change when that happens.
  - If you have a file with a lot of materials the use of *Assign Material* and *Select By Material* might become slow (or even hang Blender), so if you have those issues you can change `Material List Menu Limit` to set the number of materials shown (Defaults to 1000 materials).
  (You can still access all the materials via the `Search` option)

- **Extra / Experimental**
  - By default any Grease Pencil materials are excluded from the lists/menus shown by Material Utilities, but you can choose to include them by enabling `Show Grease Pencil materials`
  - By checking `Enable Replace Multiple Materials` you'll be able to use [Replace Multiple Material](#replace-multiple-materials) from the Material Utilities menu. This feature is functional, but perhaps not very polished.
  