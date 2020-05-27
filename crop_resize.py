


from PIL import Image
import os, sys




# Crops the image and saves it as "new_filename"
def crop_image(img, crop_area, new_filename):
    cropped_image = img.crop(crop_area)
    cropped_image.save(new_filename)

# The x, y coordinates of the areas to be cropped. (x1, y1, x2, y2)
crop_areas = [(500, 1200, 150, 640)]

image_name = 'ani_0000.png'
img = Image.open(image_name)

# Loops through the "crop_areas" list and crops the image based on the coordinates in the list
for i, crop_area in enumerate(crop_areas):
    filename = os.path.splitext(image_name)[0]
    ext = os.path.splitext(image_name)[1]
    new_filename = filename + '_cropped' + str(i) + ext

    crop_image(img, crop_area, new_filename)

"""
dirs = os.listdir(path);

path = '/home/ralap/GSS_presentation/Python_code/ani_pngs/'

def resize():
     for item in dirs:
         if os.path.isfile(path+item):
             im = Image.open(path+item)
             f, e = os.path.splitext(path+item)
             imResize = im.resize((500,300), Image.ANTIALIAS)
             imResize.save(f + ' resized.png', 'png', quality=200)
 
resize()
"""
