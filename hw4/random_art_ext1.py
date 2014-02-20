# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014
firework
@author: ssingal
"""

# Import needed libraries
from random import randint
from math import sin,cos,pi
import Image

# Make a list of all available functions and variables
functions = ['sin_pi','cos_pi','sqr','prod','avg','x','y']

def build_random_function(min_depth, max_depth):
    """
    build_random_function will build a random function based on a minimum nesting
    limit a maximum nesting limit.
    
    inputs:     min_depth: Minimum nesting limit
                max_depth: Maximum nesting limit
                
    outputs:    List containing a randomly built function
    """
    
    # Test to see if we are required to have more nested functions due to
    # the limitations of min_depth
    if min_depth>0:
        
        # Randomly choose a function and recursively call this method for the
        # input of the chosen functions
        i = randint(0,len(functions)-3)
        if functions[i] == 'sin_pi':
            return lambda x,y: sin(pi*build_random_function(min_depth-1,max_depth-1)(x,y))
        elif functions[i] == 'cos_pi':
            return lambda x,y: cos(pi*build_random_function(min_depth-1,max_depth-1)(x,y))
        elif functions[i] == 'sqr':
            return lambda x,y: pow(build_random_function(min_depth-1,max_depth-1)(x,y),2)
        elif functions[i] == 'prod':
            return lambda x,y: build_random_function(min_depth-1,max_depth-1)(x,y)*build_random_function(min_depth-1,max_depth-1)(x,y)
        else:
            return lambda x,y: (build_random_function(min_depth-1,max_depth-1)(x,y)+build_random_function(min_depth-1,max_depth-1)(x,y))/2
            
    # If we are not required to have more nested functions and...
    else:
        
        # ...if we still allowed to have more nested functions, probabistically
        # decide if we should***
        if max_depth>1:
            stop = randint(0,max_depth-min_depth)
            # ***add more functions
            if stop!=0:
                i = randint(0,len(functions)-3)
                if functions[i] == 'sin_pi':
                    return lambda x,y: sin(pi*build_random_function(min_depth-1,max_depth-1)(x,y))
                elif functions[i] == 'cos_pi':
                    return lambda x,y: cos(pi*build_random_function(min_depth-1,max_depth-1)(x,y))
                elif functions[i] == 'sqr':
                    return lambda x,y: pow(build_random_function(min_depth-1,max_depth-1)(x,y),2)
                elif functions[i] == 'prod':
                    return lambda x,y: build_random_function(min_depth-1,max_depth-1)(x,y)*build_random_function(min_depth-1,max_depth-1)(x,y)
                else:
                    return lambda x,y: (build_random_function(min_depth-1,max_depth-1)(x,y)+build_random_function(min_depth-1,max_depth-1)(x,y))/2
            # ***or end with a variable
            else:
                i = randint(1,2)
                if functions[len(functions)-i]=='x':
                    return lambda x,y:x
                else:
                    return lambda x,y:y
                
        # ...if we aren'y allowed to have more nested functions, then end with
        # a variable
        else:
            i = randint(1,2)
            if functions[len(functions)-i]=='x':
                return lambda x,y:x
            else:
                return lambda x,y:y

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ 
    Maps the input value that is in the interval [input_interval_start, input_interval_end]
    to the output interval [output_interval_start, output_interval_end].  The mapping
    is an affine one (i.e. output = input*c + b).
    
    inputs:     val: The value to scale
                input_interval_start: Minimum of scale corresponding to given value
                input_interval_end: Maximum of scale corresponding to given value
                output_interval_start: Minimum of scale corresponding to needed value
                output_interval_end: Maximum of scale corresponding to needed value
                
    outputs:    A number representing the rescaled value
    """
    
    # Find the amount of scaling needed based on the interval ranges
    c = (1.0*output_interval_end - 1.0*output_interval_start)/(1.0*input_interval_end-1.0*input_interval_start)
    
    # Return the rescaled value
    return c*(1.0*val-1.0*input_interval_start)+1.0*output_interval_start
    
# Main method
if __name__ == "__main__":
    
    # Set minimum and maximum depths
    mindep =10
    maxdep = 15
    
    # Set image size
    imgwidth = 500;
    imgheight = 500;
    
    # Create functions for red, green, and blue channels
    redf=build_random_function(mindep,maxdep)
    greenf=build_random_function(mindep,maxdep)
    bluef=build_random_function(mindep,maxdep)
    print str(redf)
    # Create a new image and set it up for editing
    im = Image.new("RGB",(imgwidth,imgheight))
    edit = im.load()
    
    # Traverse through every pixel
    for i in range(imgwidth):
        for j in range(imgheight):
            
            # Find a scaled value from -1 to 1 to plug into function based on
            # pixel position
            fscalei=remap_interval(i,0,imgwidth-1,-1,1)
            fscalej=remap_interval(j,0,imgheight-1,-1,1)
            
            # Find unscaled value of R, G, and B values
            unscaledr = redf(fscalei,fscalej)
            unscaledg = greenf(fscalei,fscalej)
            unscaledb = bluef(fscalei,fscalej)
            
            # Find correct R, G, and B values for current pixel
            r=int(remap_interval(unscaledr,-1,1,0,255))
            g=int(remap_interval(unscaledg,-1,1,0,255))
            b=int(remap_interval(unscaledb,-1,1,0,255))
            
            # Set the color of the current pixel
            edit[i,j]=(r,g,b)
    
    # Save the image        
    im.save("pic3.png")