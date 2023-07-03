# Changelog

<a name="v3.0.0"></a>

## v3.0.0 (2023-07-05)

* Add PBR Texture Set Import (see [README_PBR_Import.md](docs/pbr_import.md))
* Redesign of Add-on preferences panel (this was inspired by [@nutti](https://github.com/nutti) and the preference panel for [Magic UV](https://github.com/nutti/Magic-UV))
* Restructure (and update) of documentation

<a name="v2.4.4"></a>

## v2.4.4 (2023-03-28)

* Fix bug that occures when there's no active object e0603a51312070b1b68b4de170c2af94bf69b7e1

<a name="v2.4.3"></a>

## v2.4.3 (2022-04-15)

* Add "Remove unused materials" (Removes any material with "zero users") eac6bf436165cde1806a8e25f3a6e31f54889fe6
* Add "Replace multiple materials" (Needs to be enabled in the settings before use!) affdbd0755ac2bb2ac7a5c0171eb46789ff5bcfe

<a name="v2.4.2"></a>

## v2.4.2 (2022-04-04)

* Fix issue #10 where a material slot wasn't removed properly when using "Clean material slots" 887ed7012deed6219c7136e29edf6d93b8b0dafd
* Fix problem with Material Icons(/Previews) in Assign Material & Select By Material in Blender 3.x (Mentioned in comment to issue #10) db9522feafa9689162ea6f3453dbea25781d2336

<a name="v2.4.1"></a>

## v2.4.1 (2020-08-01)

* Add options for whether or not to include Grease Pencil materials in the menus
* Add option to unlink from Object/Data for Change Material Link. This addresses issue #8
* Add a limit to how many materials to show in the Assign & Select By menus (Default: 1000), to avoid Blender hanging when there's a big amount of materials in the file. This addresses issue #9
* Add Search & Add New Material options to the bottom of the material menus, when there's more than a certain amount of materials (Default: 50).
This is so it's easier to get to those options when there's more materials than can be shown in one "page" (screen height).

<a name="v2.4.0"></a>

## v2.4.0 (2020-04-10)

* Fix Merge By Base Name to handle missing base names, This addresses issue #6
* Added Collection as a "filter" for which object's materials to affect (similar to "Selected Objects" etc)
  You can either choose a specific Collection or use the Active Collection
  (NB: Active collection isn't necessarily the same as the collection of the active object)
* Add "Copy material to others" in Edit mode. This lets you set the material of the active face to the other selected faces
  (even across multiple selected objects). NB: You need to have Face selection enabled to be able to use it!

<a name="v2.3.1"></a>

## v2.3.1 (2020-04-09)

* Changed the "unregister" method to try to fix #7
* Mark this as a **Stable** version

<a name="v2.3.0"></a>

## v2.3.0-beta (2019-11-05)

* Added Pattern options (Simple/Delimiter choice and Regular Expressions) to Merge Base Names (Works for "Auto Merge" as well)
* Added option to rename the merged material

<a name="v2.2.0"></a>

## v2.2.0-beta (2019-08-12)

* Add "Set Auto Smooth" to Specials
* Fix error when disabling Add-on

<a name="v2.1.1"></a>

## v2.1.1-beta (2019-08-06)

* Add option for affecting selected/active objects to Clean Material slots
* Fix bug with Assign Material menu in Edit mode

<a name="v2.1.0"></a>

## v2.1.0-beta (2019-08-03)

* Add Add-on Preferences (for defaults like new/add material etc)
* Add *Override Current material slot* as an option for *Assign Material*
* Add *Search* as an option at the top of the *Assign Material* and *Select By Material* menus
* Add option/button for adding a new material in the operator panel for *Assign Material*
* *Add New Material* is now at the top of the menu (instead of at the bottom)

<a name="v2.0.0"></a>

## v2.0.0-beta (2019-08-01)
(New feature -> Bump of version)

* Add new operator: Specials > Join By Material

<a name="v1.0.6"></a>

## v1.0.6-beta (2019-08-01)

* Fix (naming of) new/add material (default "Unnamed material"), so it adds numeric suffix if it already exists

<a name="v1.0.5"></a>

## v1.0.5-beta (2019-07-16)

* Fix Issue #4 (Assigning materials when slot is linked to object) bba48ad
* Fix issue #3 (Error if cameras etc are selcted) bba48ad
* Fix issue #2 (Error if there's an Excluded collection) e0a443d
* Fix issue #1 (Exception when no object is selected) 57afffd

<a name="v1.0.4"></a>

## v1.0.4-beta (2019-07-14)

* Fix Select By Material in Edit mode for multiple selected objects dfcdb57
* Fix problem with Assign Material in Edit Mode 70e50f0
* Fix Select By Material menu in Edit Mode 759ee9c

<a name="v1.0.3"></a>

## v1.0.3-beta (2019-07-14)

* Update UI for Replace Material Operator 0f5a4dc
* Update UI for Assign Material Operator d5235fd
* Update UI for Select By Material operator 51710ec

<a name="v1.0.2"></a>

## v1.0.2-beta (2019-07-14)

* Update UI for Change Material Link operator c359798
* Fix Change Material Link operator 0d462cb
* Fix wrongly named unregister function 8be1de0

<a name="1.0.1"></a>

## v1.0.1-beta (2019-07-13)

* Add "Copy material to ohers" for Object mode 90808e6
* Add Assign material operators 26e083a
* Add Change Material Link b260335
* Add Clean Material Slots (for Curve/Surface objects) 762a357
* Add Clean Material Slots (for mesh objects) 2defaaf
* Add different override types for Assign material d3588aa
* Add Extend Selection option 06fbc23
* Add material operators to the Material Context Menu 1d2dd84
* Add Material Slot Move 08cb7aa
* Add Remove Material slots operators 46ee0c3
* Add Replace Material d0e8653
* Add Select material operator for edit Mode 29ee3f0
* Add Select material operator for object mode 3f7d1b1
* Add selection for Curves in Edit mode (Bezier) 5ef05ad
* Add Set Fake User f03c6d2
* Add Specials > Merge Base Names 9dbb609
* Append Material works for objects with one material d3273ff
* Disable Remove Material Slots in Edit mode 74370ea
* Fix "No objects found" message c85faee
* Fix Assign material for Curves (etc) in Edit mode df74948
* Fix broken reference in documentation 9881905
* Fix grammar mistake add4beb
* Fix labels in the UI 05ea11e
* Fix menu references due to API change. 8ebdfde
* Fix problem where assigned materials weren't connected to faces 1f2c7bb
* Improve selection by material, in Edit mode, for "not mesh" objects 5645192
* Move functions to separate file and name the main file __init__.py 607ed18
* Move menus to seperate file 0bc32b9
* Move operators to separate file (and put enums separately) 7f3bd8d
* Move return value e72d7a4
* Remove Move slot up/domn. e990722
* Update icon for Clean Material Slots 4fba3af
* Update menu API references 916a0d1
* Update version in init-file 4c8d33d
* Use material previews as icons in the Assign & Select menus 527bc40
