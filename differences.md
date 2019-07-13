# What's the difference - Material Utilities vs Material Utils

## Table of Contents

- [Introduction](#introduction)
  - [Author](#author)
  - [Short Background](#shortbackground)
- [Naming](#naming)
- [Blender Internal and material conversions](#blenderinternalandmaterialconversions)
- [Texture Renamer](#texturerenamer)
- [Preview Active Material](#previewactivematerial)
- [Icons](#icons)
- [Material Preview in menus](#materialpreviews)
- [Change Material Link](#changemateriallink)
- [Added options for operators](#addedoptionsforoperators)
- [Possible additions](#possibleadditions)
- [More technical changes](#moretechnicalchanges)

## Introduction

It should be noted that this is not a Changelog!
This is a document that describes what's included or, mainly, not included, from the original Add-on *Material Utils*,
for both users and developers.\
This document might not include every little change, but ther has been an effort to be as thorough as possible.

### Author

This document (as well as the Add-on it details) was authored by Christopher Hindefjord
(ChrisHinde / https://chris.hindefjord.se) July 2019.

### Short Background

The goal with the Add-on *Material Utilities* is to bring the functionality of *Material Utils* from 2.79 to 2.8x.\
Wdhen I started using 2.80 (in beta) I was instanly missing several of the functions that *Material Utils* provided
(mainly material assignment and selection in the 3D viewport), as I couldn't find a port for 2.80 (or one in development)
I started porting it myself. While porting the code I decided to add some functionality to it that I thought could be useful.\
Most of it are now ported, some are missing due to: not being relevant anymore, me thinking it's not that useful (rare),
or just will take a bit more effort (i.e. could be added later).

## Naming

A, slightly, different name was choosen to, primarily, indicate that this isn't *Material Utils* - it's done by another
developer and whilst it mainly has the same functionality, it's not a 1:1 port.

## Blender Internal and material conversions - Removed

Since 2.80 dropped the "Blender Internal"/"Blender Render" engine, none of the functionality that relates to Blener Render was included.

#### Examples:

- Conversions between Blender Render and Cycles
- Texface to Material and v.v.
- Transparent Back (This might be interesting to add for Cycles/Eevee instead)

## Texture Renamer - Not added

This is a bit of a special case in the switch from 2.79 to 2.80.\
Textures doesn't work in the same way in 2.8x as in 2.7x, mainly because of the exclusion of Blender Render.
While textures exists in a similar way as before, they are used for brushes and modifiers, but not for materials.\
The question is then if, helpful as it might be, be included in an Add-on as *Material Utilities*.

## Preview Active Material - Not added

The Material Preview hasn't yet been implemented in *Material Utilities*, and there's some questions about if it should be included.
We now have "LookDev", as well as rendered view, in 2.8x, which gives a better preview of the material than the preview.
But even so, it could exist some uses cases where a material preview, accessible via a shortcut, could be useful.
The ability to see all available materials in a grid view is pretty nice as well.

## Icons - Changed

Some icons have been changed in an attempt to have them be more descriptive (like a Pen instead of a rhombus for Merge Base Names).

## Material Preview in menus - Added

Instead of using the "generic material icon" in the material lists (Assign material & Select by material)
the material previews are used instead (which reflects the selected preview type).\
This make it's a bit easier to find the right material at a glance.

## Change Material Link - Added

This operator lets the user change the material link directly from the viewport and for several material slots and objects
directly from the viewport. It has options to set the links to Object or Data, or Toggle what's currently used.
Personally, I tend to switch the material link somewhat frequently, and this will help in those cases.\
*(This UI might change some)*

## Added options for operators

Some operators have gotten some more options (accessible through the *Adjust last operation* panel `[F9]`):

- *Assign Material* (Object mode) - User can now choose to override all material slots, assign material to each slot,
  and append material (keep other slots) (assigns the whole object to that slot). There are times when being able to
  keep material slots assignments to the mesh is useful, as well as keeping the original material referenced
- *Select By Material* - This now have an option to extend the current selection (or just override the selection),
  useful when you want to select several parts with different materials etc.
- *Clean Material Slots* - Extended to work with Curves/Surfaces (only worked with Meshes before), might add more types in the future
- *Remove Active Slot*, *Remove All Material Slots* - Now have the option to only affect the active object
- *Set Fake User* - Now have the option to toggle the Fake User flag

## Possible additions

Here's a (short) list of things that might be added in the future

- Conversions from/to Cycles/Eeeve and other render engines
- Material templates
- Rename Material
- Copy materials to others in Edit mode (gives the selected faces the same material as the active face)
- Node tools
- Tweak material

## More technical changes

- In 2.7x the "popup menu" (Shift+Q) was labeled *Material Specials Menu*, that has been changed to *Material Utilities*.\
  This was the internal name for the menu accessible via the "Down arrow" to the right of the material list (in 2.7x).
  But in 2.8x that's also how that menu is labeled in the UI (in the tooltip) and we shouldn't risk confusing the user
  by using the same label.

- The option to remove separators in the menus was not added.\
  The use for it (especially with todays screen resolutions etc) is questionable, more so weighted against the added
  readability. It also breaks the convention used by every other menu in Blender (where menu items are separated by category).

- The warning/message system isn't implemented. Maybe not entirely an bad idea, but here's some reasons why it isn't included:
  - I started with (by accident..) an older (2010) versions of Material Utils, which didn't have that utility (the main reason)
  - I find such systems a bit to rigid sometimes
  - As it was, it only supported INFO messages, but I think there are some valid reasons to mark certain messages
    as "warnings" and some as "info" (or even "error" etc)

- The operators and menus now have the "id" `materialutilities` in their bl_idname's,
  mainly because there was some conflicts with menus that existed within Blender with the same names.

- The return values (eg. `return {'FINISHED'}`) was moved from the operator's `execute` methods to the called functions
  (in the cases where there is such a function). This means that, if the operator fails etc, a proper return value
  (eg. `{'ERROR'}` or `{'CANCELLED'}`) will be returned.
