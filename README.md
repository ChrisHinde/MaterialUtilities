# Material utilities v0.1
An add-on for Blender 2.8x that lets the user assign materials directly in the 3D viewport (via a keyboard shortcut and a pop up menu), as well as select by material and more!

**This ALPHA, and still under development, you're welcome to use it, but be aware that it might not work smoothly!**

## Table of Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [Known issues](#knownissues)
- [Support](#support)
- [Contributing](#contributing)

## Background

This is based on the Add-on Material Utils by Michael Williamson (michaelw), originally written for Blender 2.4 (and then ported to 2.6, 2.7x).
I was really missing this Add-on when I started using Blender 2.80. But I couldn't find any ports of it (or even any in development),
so I decided to port it myself, and this is the result!

The goal is to include (almost?) every feature it had in 2.7x, but I'm also adding some features that I think (and hope others will as well)
will be useful!

Some examples:
- Some functions (like "Clean Material Slots") now also work on Curve and Surface objects
- The Select By Material have the option to extend the current selecction
- Assign Material have options to override or append materials in Object Mode

## Installation

1. Download the Add-on as a ZIP-file.
2. In Blender 2.8x go to *Edit* > *Preferences*, select *Add-ons* in the left panel, and then *Install* in the upper right.
3. Browse to where you saved the ZIP-file, select it and click on *Install Add-on from File*.
4. Click the checkbox to the left to enable the Add-on.
5. (Click the menu icon in the lower left and select *Save Current State*, unless you have Auto-save Preferences on)

## Usage

The default shortcut for Material Utilities (henceforth MU) is `Shift + Q`


## Known issues

- The selection by material only works for the active object in Edit mode.
  If you have multiple objects selected and "open" in Edit mode, it won't select any of the faces,
  with the selected material, of the other objects.
- The assignment of material when you have multiple objects selected in Edit mode doesn't work correctly
  and give Unexpected results.
- **CRASHES:** Blender crashes (8 out of 10 times) when the user try to assign a material to a Curve object
  that has more than one material (slot) in Object mode. This has only been experienced during those conditions.
  (i.e A Curve object, with more than one material, and only in Object mode [it works fine in Edit mode])

## Support



## Contributing

Please contribute!
