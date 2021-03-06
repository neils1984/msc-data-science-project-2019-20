import os
import glob
from PIL import Image


img_path = 'images/*.png'
img_out_path = 'images/cropped_images128/'

for img in glob.glob(img_path):
    im_name = os.path.basename(img)
    im = Image.open(img)
    new_im = im.resize((128, 128))
    new_im.save(f'{img_out_path}{im_name}')