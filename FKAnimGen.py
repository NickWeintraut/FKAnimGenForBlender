##################---------------########################
############# AUTHOR: Nick Weintraut   ##################
###############  Rowan University  ######################
################  Nov. 2nd, 2017  #######################
##################---------------########################
###### FK Animation Generation API for Blender 2.79 #####
#############-------------------------###################
#############        Contents         ###################
#############    1. API LIBRARY       ###################
#############    2. EXAMPLE SCRIPT    ###################
##################---------------########################
### TERMS OF USE:                ########################
### Use, distribute, modify, as long as you Credit Me ###

##################---------------########################
############### BEGIN - API LIBRARY #####################
##################---------------########################

import bpy
import math
"""
    Helper function to just clear the Blender Scene
"""
def clear_scene():
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
"""
    Class CoordFrame defines a coordinate frame object in 3d space that will show up in the 3d view.
    Creating a CoordFrame object places the frame object into the scene and initializes its animation
"""
class CoordFrame:
    """
        Constructor for a CoordFrame. Takes as input:
            The suffix for the name of the CoordFrame (e.g. A,B...)
            A tuple (x,y,z) representing the location of the coordinate frame in world coordinates
    """
    def __init__(self, suffix, location, x=None, y=None, z=None, startFrame=0):
        bpy.ops.object.empty_add(type='ARROWS', view_align=False, location=location, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        self.frame_arrows = bpy.context.object
        self.frame_arrows.name = "frame" + suffix
        bpy.ops.object.empty_add(type='SPHERE', view_align=False, location=location, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        self.root = bpy.context.object
        self.root.name = "frame" + suffix + "_root"
        self.root.empty_draw_size = 0.05
        self.root.select=True
        self.frame_arrows.select=True
        bpy.context.scene.objects.active = self.root
        bpy.ops.object.parent_set(keep_transform=False)
        self.align_to_dirs(x,y,z)
        self.set_movement_type("FIXED_AXIS")
        self.curr_frame = startFrame
        #Hack to remove a weird keyframing bug due to keyframing the initial position after rotation
        #End hack
        self.move_frames = 30
        self.pause_frames = 15
        #HackFix
        self.calibrateForAnimation()
    
    """
        Called before any animation operations are called. This function is literally just to accomodate some
        very strange behaviour due to the initial keyframing that doesnt like FIXED_AXIS
    """
    def calibrateForAnimation(self):
        #Hack to remove a weird keyframing bug due to keyframing the initial position after rotation caused by 
        #initializing keyframes before setting move type to FIXED_AXIS
        moveType = self.move_type
        self.set_movement_type("FIXED_AXIS")
        self.set_pause_frames(0)
        self.add_pause()
        self.set_movement_frames(0)
        self.trans((0,0,0))
        self.set_movement_type(moveType)
        #End hack
        
    """
        Rotates this CoordFrame along one of its axes by the given radians value
        (Does not generate animation)
        ex: coordFrame.rot(math.pi / 2, x=True) will rotate coordFrame by 90 degrees on its x axis
    """
    def rot(self, radians, x=False, y=False, z=False):
        bpy.ops.transform.rotate(value=radians, axis=(1 if x else 0, 1 if y else 0, 1 if z else 0), constraint_axis=(x, y, z), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    
    """
        Helper function which aligns this CoordFrame's scene object to the given directions using the right hand rule. 
        Does not generate animation.
    """
    def align_to_dirs(self, x=None, y=None, z=None):
        #First, if the direction is not calculated in y and x, calculate the missing direction
        #These to cases (y!=None and z!=None AND x!=None and Z!= None) represent the cases where we needed to calculate x or y
        #We do this as the next step in the code is to use the x and y directions to calculate the actual rotation of the object in blenders rotation coordinates
        if y != None and z!= None:
            if y == "RIGHT" and z == "OUT":
                x="DOWN"
            elif y == "RIGHT" and z == "IN":
                x="UP"
            elif y == "RIGHT" and z == "DOWN":
                x="IN"
            elif y == "RIGHT" and z == "UP":
                x="OUT"
            elif y == "LEFT" and z == "OUT":
                x="UP"
            elif y == "LEFT" and z == "IN":
                x="DOWN"
            elif y == "LEFT" and z == "DOWN":
                x="OUT"
            elif y == "LEFT" and z == "UP":
                x="IN"
            elif y == "UP" and z == "OUT":
                x="RIGHT"
            elif y == "UP" and z == "IN":
                x="LEFT"
            elif y == "UP" and z == "LEFT":
                x="OUT"
            elif y == "UP" and z == "RIGHT":
                x="IN"
            elif y == "DOWN" and z == "OUT":
                x="LEFT"
            elif y == "DOWN" and z == "IN":
                x="RIGHT"
            elif y == "DOWN" and z == "LEFT":
                x="IN"
            elif y == "DOWN" and z == "RIGHT":
                x="OUT"
            elif y == "IN" and z == "UP":
                x="RIGHT"
            elif y == "IN" and z == "DOWN":
                x="LEFT"
            elif y == "IN" and z == "LEFT":
                x="UP"
            elif y == "IN" and z == "RIGHT":
                x="DOWN"
            elif y == "OUT" and z == "UP":
                x="LEFT"
            elif y == "OUT" and z == "DOWN":
                x="RIGHT"
            elif y == "OUT" and z == "LEFT":
                x="DOWN"
            elif y == "OUT" and z == "RIGHT":
                x="UP"
        elif z!= None and x != None:
            if z == "RIGHT" and x == "OUT":
                y="DOWN"
            elif z == "RIGHT" and x == "IN":
                y="UP"
            elif z == "RIGHT" and x == "DOWN":
                y="IN"
            elif z == "RIGHT" and x == "UP":
                y="OUT"
            elif z == "LEFT" and x == "OUT":
                y="UP"
            elif z == "LEFT" and x == "IN":
                y="DOWN"
            elif z == "LEFT" and x == "DOWN":
                y="OUT"
            elif z == "LEFT" and x == "UP":
                y="IN"
            elif z == "UP" and x == "OUT":
                y="RIGHT"
            elif z == "UP" and x == "IN":
                y="LEFT"
            elif z == "UP" and x == "LEFT":
                y="OUT"
            elif z == "UP" and x == "RIGHT":
                y="IN"
            elif z == "DOWN" and x == "OUT":
                y="LEFT"
            elif z == "DOWN" and x == "IN":
                y="RIGHT"
            elif z == "DOWN" and x == "LEFT":
                y="IN"
            elif z == "DOWN" and x == "RIGHT":
                y="OUT"
            elif z == "IN" and x == "UP":
                y="RIGHT"
            elif z == "IN" and x == "DOWN":
                y="LEFT"
            elif z == "IN" and x == "LEFT":
                y="UP"
            elif z == "IN" and x == "RIGHT":
                y="DOWN"
            elif z == "OUT" and x == "UP":
                y="LEFT"
            elif z == "OUT" and x == "DOWN":
                y="RIGHT"
            elif z == "OUT" and x == "LEFT":
                y="DOWN"
            elif z == "OUT" and x == "RIGHT":
                y="UP"
                
        #Now that we have x and y guaranteed to be set (unless only one direction was supplied)
        #Actually rotate our coordFrame object in the scene so it matches those directions
        bpy.ops.object.select_all(action="DESELECT")
        self.root.select = True
        #Now to set rotations based on < 6 * 5 combinations
        if x == "RIGHT" and y == "OUT":
            z="DOWN"
            self.rot(math.pi / 2, z=True)
            self.rot(math.pi, x=True)
        elif x == "RIGHT" and y == "IN":
            z="UP"
            self.rot(math.pi / 2, z=True)
        elif x == "RIGHT" and y == "DOWN":
            z="IN"
            self.rot(math.pi / 2, z=True)
            self.rot(-1 * math.pi / 2, x=True)
        elif x == "RIGHT" and y == "UP":
            z="OUT"
            self.rot(math.pi / 2, z=True)
            self.rot(math.pi / 2, x=True)
        elif x == "LEFT" and y == "OUT":
            z="UP"
            self.rot(-1 * math.pi / 2, z=True)
        elif x == "LEFT" and y == "IN":
            z="DOWN"
            self.rot(-1 * math.pi / 2, z=True)
            self.rot(math.pi, x=True)
        elif x == "LEFT" and y == "DOWN":
            z="OUT"
            self.rot(-1 * math.pi / 2, z=True)
            self.rot(-1 * math.pi / 2, x=True)
        elif x == "LEFT" and y == "UP":
            z="IN"
            self.rot(-1 * math.pi / 2, z=True)
            self.rot(math.pi / 2, x=True)
        elif x == "UP" and y == "OUT":
            z="RIGHT"
            self.rot(-1 * math.pi / 2, y=True)
            self.rot(-1 * math.pi / 2, x=True)
        elif x == "UP" and y == "IN":
            z="LEFT"
            self.rot(-1 * math.pi / 2, y=True)
            self.rot(math.pi / 2, x=True)
        elif x == "UP" and y == "LEFT":
            z="OUT"
            self.rot(-1 * math.pi / 2, y=True)
            self.rot(math.pi, x=True)
        elif x == "UP" and y == "RIGHT":
            z="IN"
            self.rot(-1 * math.pi / 2, y=True)
        elif x == "DOWN" and y == "OUT":
            z="LEFT"
            self.rot(math.pi / 2, y=True)
            self.rot(math.pi / 2, x=True)
        elif x == "DOWN" and y == "IN":
            z="RIGHT"
            self.rot(math.pi / 2, y=True)
            self.rot(-1 * math.pi / 2, x=True)
        elif x == "DOWN" and y == "LEFT":
            z="IN"
            self.rot(math.pi / 2, y=True)
            self.rot(math.pi, x=True)
        elif x == "DOWN" and y == "RIGHT":
            z="OUT"
            self.rot(math.pi / 2, y=True)
        elif x == "IN" and y == "UP":
            z="RIGHT"
            self.rot(math.pi, z=True)
            self.rot(math.pi / 2, x=True)
        elif x == "IN" and y == "DOWN":
            z="LEFT"
            self.rot(math.pi, z=True)
            self.rot(-1 * math.pi / 2, x=True)
        elif x == "IN" and y == "LEFT":
            z="UP"
            self.rot(math.pi, z=True)
        elif x == "IN" and y == "RIGHT":
            z="DOWN"
            self.rot(math.pi, z=True)
            self.rot(math.pi, x=True)
        elif x == "OUT" and y == "UP":
            z="LEFT"
            self.rot(math.pi / 2, x=True)
        elif x == "OUT" and y == "DOWN":
            z="RIGHT"
            self.rot(-1 * math.pi / 2, x=True)
        elif x == "OUT" and y == "LEFT":
            z="DOWN"
            self.rot(math.pi, x=True)
        elif x == "OUT" and y == "RIGHT":
            z="UP"
        else:
            print("alignment not found") #will be printed if incorrect directions are supplied or only one or zero directions are supplied
        bpy.ops.object.select_all(action="DESELECT")
        
    """
        Helper function that moves the time scrubber ahead a certain number of animation frames (think frames per second)
        Used to generate the animation in the scene.
    """
    def add_frames(self, frames):
        self.curr_frame += frames
        bpy.context.scene.frame_set(self.curr_frame)
    
    """
        Adds a pause to our generated animation for the number of animation frames specified by 
        this CoordFrame object's pause_frames attribute (self.pause_frames)
    """
    def add_pause(self):
        self.add_frames(self.pause_frames)
        self.insert_keyframe()
    
    """
        Helper function for 'keyframing' this object - keyframing marks 
        the the exact position and rotation at this animation frame as a 'key' frame;
        Position and rotation of objects is calculated as an interpolation of key frames
        for every animation frame.
        Used in animation generation functions.
    """
    def insert_keyframe(self):
        self.root.select = True
        self.frame_arrows.select = True
        bpy.ops.anim.keyframe_insert(type='BUILTIN_KSI_LocRot')
        bpy.context.scene.frame_end = self.curr_frame

    """
        Helper function used by all animation api functions to move the 
        current animation frame to the next animation frame we will want to keyframe.
    """
    def setup_move(self):
        bpy.ops.object.select_all(action="DESELECT")
        self.add_frames(self.move_frames)
    
    """
        Sets the movement type field of this CoordFrame
        type is a String that should be equal to either 'MOVING_AXIS' or 'FIXED_AXIS'
    """
    def set_movement_type(self, type):
        self.move_type = type
        if type == "MOVING_AXIS":
            self.root.empty_draw_type = "SPHERE"
            self.root.empty_draw_size = 0.05
        else:
            self.root.empty_draw_type = "ARROWS"
            self.root.empty_draw_size = 1.0
        
    """
        Set the number of animation frames used for each movement(every trans/rotx/roty/rotz is a movement).
        For example - this blender scene is calibrated to run at 60 frames per second,
        so plugging in 120 for the value of frames will make every operation take 2 seconds.
    """
    def set_movement_frames(self, frames):
        self.move_frames = frames
    
    """
        Set the number of animation frames used for each pause(every trans/rotx/roty/rotz has a pause after it).
        For example - this blender scene is calibrated to run at 60 frames per second,
        so plugging in 60 for the value of frames will make every pause take 1 second.
        INVARIANT - Never set pause_frames lower than 1 
        (As in order to make the fixed axis rotation smooth, I steal a frame from its pause frames)
    """
    def set_pause_frames(self, frames):
        self.pause_frames = frames
    
    """
        Constructs an animation move which rotates the CoordFrame by the given radians on the given axis
        if move_type is set to 'MOVING_AXIS' on the CoordFrame, this will simply rotate the frame.
        if move_type is set to 'FIXED_AXIS' on the CoordFrame, this will rotate the frame 
        around the axis of its original frame (as well as the original frame to show the relation), 
        then snap the original frame back to its rotation before the animation.
    """
    def rotate(self, radians, x=False, y=False, z=False):
        self.setup_move()
        #do rotation
        self.root.select = True
        bpy.ops.transform.rotate(value=radians, axis=(1 if x else 0, 1 if y else 0, 1 if z else 0), constraint_axis=(x, y, z), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        self.insert_keyframe()
        self.add_frames(1)
        if self.move_type == "FIXED_AXIS":
            #unparent the frame root
            self.root.select = False
            self.frame_arrows.select = True
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            #move the frame root back to original rotation
            self.frame_arrows.select = False
            self.root.select = True
            bpy.ops.transform.rotate(value=-1 * radians, axis=(1 if x else 0, 1 if y else 0, 1 if z else 0), constraint_axis=(x, y, z), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            #reparent
            self.frame_arrows.select=True
            bpy.context.scene.objects.active = self.root
            bpy.ops.object.parent_set(keep_transform=True)
        self.insert_keyframe()
        self.add_frames(self.pause_frames - 1)
        self.insert_keyframe()
    
    """
        Wrapper for the rotate function which rotates around the x-axis
    """
    def rot_x(self, radians):
        self.rotate(radians, x=True)

    """
        Wrapper for the rotate function which rotates around the y-axis
    """
    def rot_y(self, radians):
        self.rotate(radians, y=True)
       
    """
        Wrapper for the rotate function which rotates around the z-axis
    """ 
    def rot_z(self, radians):
        self.rotate(radians, z=True)
        
    """
        Constructs an animation move which translates the CoordFrame a tuple movement=(x,y,z) of 3d distance.
        If move_type is set to 'MOVING_AXIS' then this simply translates the CoordFrame (x,y,z) according to its local axes
        If move_type is set to 'FIXED_AXIS' then this translates the CoordFrame (x,y,z) according to its original frame's axes
    """
    def trans(self, movement):
        self.setup_move()
        self.root.select = True
        origFrameLocation = (self.root.location.x, self.root.location.y, self.root.location.z)
        bpy.ops.transform.translate(value=movement, constraint_axis=(True, True, True), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)
        if self.move_type == "FIXED_AXIS":
            #unparent the frame root
            self.root.select = False
            self.frame_arrows.select = True
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            #move the frame root back to original position
            self.root.location = origFrameLocation
            #reparent
            self.root.select=True
            self.frame_arrows.select=True
            bpy.context.scene.objects.active = self.root
            bpy.ops.object.parent_set(keep_transform=True)
        self.insert_keyframe()
        self.add_frames(self.pause_frames)
        self.insert_keyframe()
        
##################-------------#######################
############### END - API LIBRARY ####################
##################-------------#######################



###################----------#########################
################ BEGIN - SCRIPT ######################
###################----------#########################

# Clear all previous objects from the scene (this will clear animation as well
# -----------------------------------------------------------------
clear_scene()

# Initializing the coordinate frames
# -----------------------------------------------------------------

# This will be the CoordFrame we will be animating for this example
frame = CoordFrame("A",(0,0,0), y="DOWN", z="RIGHT")

# We can use the CoordFrame constructor to show our target in the animation as well (we won't animate this)
target = CoordFrame("B",(3,1,2), x="UP", y="RIGHT")

# Set animation settings for the coordinate frame we will be moving
# -----------------------------------------------------------------

# The frames we will move for (this scene is currently running at 60fps, so this is two seconds)
frame.set_movement_frames(120)

# The frames we will pause for in between moves (keep it above 1 please, as I add an extra keyframe for rotation moves, which i steal from the pause time)
frame.set_pause_frames(60)

# options: MOVING_AXIS or FIXED_AXIS - this must be set before calling calibrateForAnimation if you want a FIXED_AXIS animation
frame.set_movement_type("FIXED_AXIS")

# Build the animation!
#------------------------------------------------------------------

#Instructions to move the coordinate frame:

frame.trans((2,1,-3))
frame.rot_z(-1 * math.pi / 2)
frame.rot_y(-1 * math.pi / 2)

###################--------#########################
################ END - SCRIPT ######################
###################--------#########################

################ Author: Nick Weintraut ############
################## Rowan University ################