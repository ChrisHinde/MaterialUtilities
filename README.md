# Material utilities v3.0.2 (Dev)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

An add-on for Blender 2.8x, and 3.x+, that lets the user assign materials directly in the 3D viewport
(via a keyboard shortcut and a pop up menu), as well as select by material and more!

Each part is tested thoroughly during development, but we can't guarantee that there in't a special case where a problem might occur!\
Please read the list of [Known issues](#known-issues) below, if your problem isn't listed, please leave a bug report.

## Version

The current stable version of Material Utilities is [**v3.0.2**](CHANGELOG.md#v3.0.2)\
(Major version indicates big changes or feature adds, Minor version bigger bugfixes and changes to existing features,
  Patch version [last number] indicates small changes and fixes)

## Disclaimer (want to help out?)

I (Chris Hindefjord) am not really in a position where I can actively develop and maintain this add-on. I will do my best\
to respond to new issues, but I (sadly) can't guarantee a quick response.
I don't want this project to die, and neither do I think that creating forks (just to keep it maintained in another repository) is the best idea!
So I welcome anyone that is willing to help, either by:

- Patching and making pull request
- Be added to this repository as a collaborators (and so having a more direct access to the project)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y3O0EEE)

## Table of Contents

- [Background](#background)
- [Information](#information)
- [Installation](#installation)
- [Usage](#usage--documentation)
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

If you want to know what's different (including code wise), take a look at the [Differences](docs/differences.md) document.\
But here are some examples:

- Some functions (like "Clean Material Slots") now also work on Curve and Surface objects
- The Select By Material have the option to extend the current selection
- Assign Material have options to override or append materials in Object Mode

## Information

This Add-on is now included with the official Blender Builds (since 2.81), just go the *Preferences* > *Add-ons* > Select the *Material* category, or search for "Material", and then enable it.\
**NB:** The version included with Blender might be, slightly, older than the latest version found in this repository.
Please visit the [Changelog](CHANGELOG.md) to compare the difference in the versions.\
Thanks to Meta-Androcto for handling the inclusion into the Blender repository.

## Installation

1. Download the Add-on as a ZIP-file.
2. In Blender 4.x go to *Edit* > *Preferences*, select *Add-ons* in the left panel, and then *Install* in the upper right.
3. Browse to where you saved the ZIP-file, select it and click on *Install Add-on from File*.
4. Click the checkbox to the left to enable the Add-on.
5. Click the menu icon in the lower left and select *Save Current State*

## Usage / Documentation

The default shortcut for Material Utilities is `[Shift + Q]` (in the 3D Viewport and Shader Editor).
You can find more usage documentation in the [documentation](docs/) ([3D Viewport Menu](docs/usage.md), [Shader Editor Menu](docs/pbr_import.md))

## Known issues

There's currently no known issues.  

(**Do note** that each spline/curve in Curve Objects can only have one material,
  so you can't assign different materials to different parts of a spline)

## Support

Support is given when time is available, you can ask for support via <https://chris.hindefjord.se/contact/>. \
If you think you've find a bug, please
[report it by creating an issue](https://github.com/ChrisHinde/MaterialUtilities/issues)!\
Bug reports takes precedence over other support requests!
(Also see [Disclaimer](#disclaimer-want-to-help-out) above)

## Contributing

You're welcome to contribute to this Add-on.\
If you want to know where to start, take a look at the [TODO](TODO) file.
(Also see [Disclaimer](#disclaimer-want-to-help-out) above)

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgements

This Add-on is based on and uses (some) code by the following awesome people:\
Michael Williamson (michaelw) (original author)\
Meta-Androcto\
Sybren\
Saidenka\
lijenstina\
CoDEmanX\
SynaGl0w\
ideasman42\
nutti

(If you think your code is used in this add-on, but you're not listed here,
please contact ChrisHinde so correct attribution can be given)
