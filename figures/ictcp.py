#!/usr/bin/env python3

import colour
import numpy as np
import sys

def rgb_to_ictcp(rgb):
    BT2020 = colour.RGB_to_RGB(rgb, input_colourspace='sRGB', output_colourspace='ITU-R BT.2020')
    return colour.RGB_to_ICtCp(BT2020)

def ictcp_to_rgb(ictcp):
    return colour.RGB_to_RGB(colour.ICtCp_to_RGB(ictcp), input_colourspace='ITU-R BT.2020', output_colourspace='sRGB')

if __name__ == '__main__':
    RGB = colour.read_image(sys.argv[1])

    I, Ct, Cp = np.split(rgb_to_ictcp(RGB), 3, axis=2)

    Zero = np.zeros_like(I)
    # sRGB gray to ICtCp (mimicking YCbCr's midpoint of Y=0 == luma 128)
    I_half, _, _ = np.split(rgb_to_ictcp(np.dstack((np.full_like(Ct, 1), Zero, Zero))), 3, axis=2)

    I_as_RGB = ictcp_to_rgb(np.dstack((I, Zero, Zero)))
    Ct_as_RGB = ictcp_to_rgb(np.dstack((I_half, Ct, Zero)))
    Cp_as_RGB = ictcp_to_rgb(np.dstack((I_half, Zero, Cp)))

    components = np.concatenate((I_as_RGB, Ct_as_RGB, Cp_as_RGB), axis=0)

    colour.write_image(components, 'ICtCp_components.tif')

    I_as_RGB = ictcp_to_rgb(np.dstack((I, Zero, Zero)))
    Ct_as_RGB = ictcp_to_rgb(np.dstack((I, Ct, Zero)))
    Cp_as_RGB = ictcp_to_rgb(np.dstack((I, Zero, Cp)))

    components = np.concatenate((I_as_RGB, Ct_as_RGB, Cp_as_RGB), axis=0)

    colour.write_image(components, 'ICtCp_components_contrib.tif')

    # After this, convert the images to 8-bit in your editor of choice,
    # making sure gamma 2.2 is properly applied
