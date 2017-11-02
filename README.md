# FKAnimGenForBlender
A Blender scene and packaged python script for generating 3D animations of forward kinematics transformations.

This tool is intended for educators teaching students about moving and fixed axes approaches for computing coordinate frame transformations.
Using the open source software Blender, the included scene generates an animation of Coordinate Frame A transformed to Coordinate Frame B using a fixed-axes approach.
A python API is also included in the scene itself (and in this repo for easy reading) to allow users to generate animations of any MOVING-AXIS or FIXED-AXIS transformation
using simple rot and trans commands.

# Getting Started
1. Download Blender at blender.org
2. Download this repo, and open forwardKinematicsAnimSetting.blend in Blender.
3. The current script has already been run for the example scene. Press [alt a] to play the animation, or click the play button in the timeline view on the left middle of the window.
# Modifying the Animation/Script
1. The script comes preloaded in the blender scene. At the bottom of the window, you should see the script in the text editor window.
2. The bottom of the script (after the API) shows the code used to generate the sample animation.
3. Where the code has ```frame.trans((2,1,-3))
frame.rot_z(-1 * math.pi / 2)
frame.rot_y(-1 * math.pi / 2)``` written, you can modify the instructions to any sequence of rot_x,rot_y,rot_z, and trans. The example script has documentation to show exactly what it is doing with the API so that you can tweak every step. 
4. When you've modified your script, press the 'Run Script' button at the bottom of the text editor. This script does not run the animation itself, but generates an animation inside of the blender scene that you can run with [alt a] or the timeline window.

# Contributing to this Repository
If you make changes to this repository that could be beneficial to other users, please feel free to make a pull request after doing the following:
1. Ensuring that all API methods and script changes are sufficiently documented (similar to the current level of documentation)
2. Test a few different configurations of animations (both moving and fixed axis) to make sure they still work. 
3. Ensure that your changes to the python script are reflected both in the internal python file of the scene as well as the external file in the repo. (Use save as in the text editor to save to the external file, and then use make internal in the text editor to make the file the scene references the internal version again)
