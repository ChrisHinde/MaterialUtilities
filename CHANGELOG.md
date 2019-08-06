# Changelog

<a name="v2.1.1"></a>
# v2.1.1-beta (2019-08-06)

* Add option for affecting selected/active objects to Clean Material slots
* Fix bug with Assign Material menu in Edit mode

<a name="v2.1.0"></a>
# v2.1.0-beta (2019-08-03)

* Add Add-on Preferences (for defaults like new/add material etc)
* Add *Override Current material slot* as an option for *Assign Material*
* Add *Search* as an option at the top of the *Assign Material* and *Select By Material* menus
* Add option/button for adding a new material in the operator panel for *Assign Material*
* *Add New Material* is now at the top of the menu (instead of at the bottom)

<a name="v2.0.0"></a>
# v2.0.0-beta (2019-08-01)
(New feature -> Bump of version)

* Add new operator: Specials > Join By Material

<a name="v1.0.6"></a>
# v1.0.6-beta (2019-08-01)

* Fix (naming of) new/add material (default "Unnamed material"), so it adds numeric suffix if it already exists

<a name="v1.0.5"></a>
# v1.0.5-beta (2019-07-16)

* Fix Issue #4 (Assigning materials when slot is linked to object) bba48ad
* Fix issue #3 (Error if cameras etc are selcted) bba48ad
* Fix issue #2 (Error if there's an Excluded collection) e0a443d
* Fix issue #1 (Exception when no object is selected) 57afffd

<a name="v1.0.4"></a>
# v1.0.4-beta (2019-07-14)

* Fix Select By Material in Edit mode for multiple selected objects dfcdb57
* Fix problem with Assign Material in Edit Mode 70e50f0
* Fix Select By Material menu in Edit Mode 759ee9c

<a name="v1.0.3"></a>
# v1.0.3-beta (2019-07-14)

* Update UI for Replace Material Operator 0f5a4dc
* Update UI for Assign Material Operator d5235fd
* Update UI for Select By Material operator 51710ec

<a name="v1.0.2"></a>
# v1.0.2-beta (2019-07-14)

* Update UI for Change Material Link operator c359798
* Fix Change Material Link operator 0d462cb
* Fix wrongly named unregister function 8be1de0

<a name="1.0.1"></a>
# v1.0.1-beta (2019-07-13)

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
