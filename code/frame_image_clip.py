import os
import natsort
from PIL import Image

# 폴더를 지정해서 그 안에 있는 이미지를 순서대로 나열
original_path = './frame_image'
cutted_path = './frame_image_crop/'
img_list = os.listdir(original_path)
img_list = natsort.natsorted(img_list, reverse=False)

# 하나씩 읽어와서 crop하고 저장하는 부분
for i, filename in enumerate(img_list):
    im = Image.open(original_path + '/' + filename)
    area = (0, 26, 1280, 666)
    crop_image = im.crop(area)
    savename = './frame_image_crop/' + 'crop_{0}'.format(i) + '.jpg'
    print(savename)
    crop_image.save(savename)
