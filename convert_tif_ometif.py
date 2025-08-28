import tifffile as tf
import sys
import numpy as np
import cv2

image = tf.imread(sys.argv[1])

if image.shape[2] > image.shape[0]:
    image = np.transpose(image,(1,2,0))

filename = sys.argv[1].rsplit('.',1)[0]

def img_resize(img,scale_factor):
    width = int(np.floor(img.shape[1] * scale_factor))
    height = int(np.floor(img.shape[0] * scale_factor))
    return cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)

def write_ome_tif(filename, image, subresolutions = 7, pixelsize = 0.2125):
    subresolutions = subresolutions
    pixelsize = pixelsize
    fn = filename + ".ome.tif"
    with tf.TiffWriter(fn, bigtiff=True) as tif:
        metadata={
            'SignificantBits': 8,
            'PhysicalSizeX': pixelsize,
            'PhysicalSizeXUnit': 'µm',
            'PhysicalSizeY': pixelsize,
            'PhysicalSizeYUnit': 'µm',
            'Channel': {'Name': ['newname1', 'newname2', 'newname3']} # Use this line to edit channel names for multi-channel images
        }
        options = dict(
            photometric='minisblack',
            tile=(1024, 1024),
            compression='jpeg2000',
            resolutionunit='CENTIMETER'
        )
        tif.write(
            np.moveaxis(image,-1,0),
            subifds=subresolutions,
            resolution=(1e4 / pixelsize, 1e4 / pixelsize),
            metadata=metadata,
            **options
        )

        scale = 1
        for i in range(subresolutions):
            scale /= 2
            downsample = img_resize(image,scale),
            tif.write(
                np.moveaxis(downsample,-1,0),
                subfiletype=1,
                resolution=(1e4 / scale / pixelsize,1e4 / scale / pixelsize),
                **options
            )

write_ome_tif(filename, image, subresolutions = 7, pixelsize = 0.2125)
