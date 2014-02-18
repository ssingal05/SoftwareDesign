# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014
firework
@author: ssingal
"""

# Import needed libraries
from random import randint
import math
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
        if i<3:
            return [functions[i],build_random_function(min_depth-1,max_depth-1)]
        else:
            return [functions[i],build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]
            
    # If we are not required to have more nested functions and...
    else:
        
        # ...if we still allowed to have more nested functions, probabistically
        # decide if we should***
        if max_depth>1:
            stop = randint(0,max_depth-min_depth)
            # ***add more functions
            if stop!=0:
                i = randint(0,len(functions)-3)
                if i<3:
                    return [functions[i],build_random_function(min_depth,max_depth-1)]
                else:
                    return [functions[i],build_random_function(min_depth,max_depth-1),build_random_function(min_depth,max_depth-1)]
            # ***or end with a variable
            else:
                i = randint(1,2)
                return [functions[len(functions)-i]]
                
        # ...if we aren'y allowed to have more nested functions, then end with
        # a variable
        else:
            i = randint(1,2)
            return [functions[len(functions)-i]]

    
def evaluate_random_function(f, x, y):
    """
    evaulate_random_function will evaluate a given function with the given
    input variables
    
    inputs:     f: The function
                x: The value of the x variables in the function
                y: The value of the y variables in the function
                
    outputs:    A number representing the value of the evaluated function
    """

    # If there is only one value in the list representing the function, then
    # the function is just a variable and we should substitute and return a value
    if len(f)==1:
        # Return the x value for x variables
        if f[0]=='x':
            return 1.0*x
            print 'hello'
        # Return the y value for y variables
        else:
            return 1.0*y
            print 'suck'
    # If there is more than one value in this list representing the function,
    # then we need to evaluate this function based on the following mathematical
    # operations
    else:
        # Take the sine of the function
        if f[0] == 'sin_pi':
            return math.sin(math.pi*evaluate_random_function(f[1],x,y))
        # Take the cosine of the function
        elif f[0] == 'cos_pi':
            return math.cos(math.pi*evaluate_random_function(f[1],x,y))
        # Square the function
        elif f[0] == 'sqr':
            return math.pow(evaluate_random_function(f[1],x,y),2)
        # Find the product of the functions
        elif f[0] == 'prod':
            return evaluate_random_function(f[1],x,y)*evaluate_random_function(f[2],x,y)
        # Find the average of the functions
        else:
            return (evaluate_random_function(f[1],x,y)+evaluate_random_function(f[2],x,y))/2
            

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
            unscaledr = evaluate_random_function(redf,fscalei,fscalej)
            unscaledg = evaluate_random_function(greenf,fscalei,fscalej)
            unscaledb = evaluate_random_function(bluef,fscalei,fscalej)
            
            # Find correct R, G, and B values for current pixel
            r=int(remap_interval(unscaledr,-1,1,0,255))
            g=int(remap_interval(unscaledg,-1,1,0,255))
            b=int(remap_interval(unscaledb,-1,1,0,255))
            
            # Set the color of the current pixel
            edit[i,j]=(r,g,b)
    
    # Save the image        
    im.save("pic2.png")