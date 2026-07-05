# This is not my Add-On!

This is a fork of glitchingdot/UltraPattern because the original creator didn't seem to be active anymore.

For now I've added support for stairs, which was the reason I forked it.

In the future I'm gonna add support for Jump Pads.

Original Description (with small changes by me):

# UltraPattern (1.1.1)
A Blender add-on to import, create, modify, and export Cyber Grind Pattern files for ULTRAKILL

Use UltraPattern to build and visualize new patterns fast, set up animation environments quickly, and debug broken patterns!

## Features
* Importing and exporting Cyber Grind patterns 📦
* Create new patterns 💡
* Prefab editing 📝
* Visualze prefabs with custom colors 🌈
  
*And more to come!*

## Requirements
UltraPattern was built using Blender **3.6.1**, but it is compatible with most modern versions of Blender  
*hopefully*, compatibility cannot be 100% ensured

## Installation
* Download the add-on from the Releases page: [UltraPattern](https://github.com/kommeleon/UltraPattern/releases/latest)
   * Do **NOT** unzip the file
* In Blender, go to *Edit > Preferences > Add-ons* and click on *Install*
* Select the downloaded file, press *Install Add-on*
* Click on the check box next to the text

Congrats, you've just installed UltraPattern! 🎉

## Usage
* In the 3D View, press N to open the sidebar
* Click on the tab labled "UltraPattern"
* To get started, either import a pattern with *Import CGP* or create a blank pattern with *Create Blank Pattern*  
  * Patterns can be found in `Cybergrind/Patterns/` in your game folder
  * The Default Patterns can be found in the latest release [UltraPattern](https://github.com/kommeleon/UltraPattern/releases/latest) as Default_Patterns.zip
* To edit a pillar's prefab, click on it, and you will see a new panel named "Pillar" appear
  * If you want to update multiple pillars at the same time, make sure to click *Update All Selected Pillars*  
* To generate a material for rendering, click *Generate Material*, browse to the texture, and confirm it  
  * Cyber Grind textures are found in `Cybergrind/Textures/` in your game folder
  * The Default textures can be found in the latest release [UltraPattern](https://github.com/kommeleon/UltraPattern/releases/latest) as Default_Textures.zip
* To export, select the pattern's collection and click *Export CGP*
