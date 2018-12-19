# -*- coding:utf-8 -*-

"""

@author:Michael Ji
@file:coco2yolo.py
@time:2018/12/1712:40 PM

"""
import os
import shutil

from pycocotools.coco import COCO

annFile = '/Users/southdom/DeepLearningDoc/coco dataset/annotations/instances_train2017.json'
imgFile = '/Users/southdom/DeepLearningDoc/coco dataset/train2017/%s.jpg'
destFile = '/Users/southdom/DeepLearningDoc/coco dataset/yolo-train/%s.jpg'
destTextFile = '/Users/southdom/DeepLearningDoc/coco dataset/yolo-train/%s.txt'

coco = COCO (annFile)
#
# carIds = coco.getCatIds(catNms=['car'])
# motorcycleIds = coco.getCatIds(catNms=['motorcycle'])
# busIds = coco.getCatIds(catNms=['bus'])
# trainIds = coco.getCatIds(catNms=['train'])
# truckIds = coco.getCatIds(catNms=['truck'])
#
# carImgIds = coco.getImgIds(catIds=carIds)
# motorcycleImgIds = coco.getImgIds(catIds=motorcycleIds)
# busImgIds = coco.getImgIds(catIds=busIds)
# trainImgIds = coco.getImgIds(catIds=trainIds)
# truckImgIds = coco.getImgIds(catIds=truckIds)

anns = {}
for v in coco.anns.values ():
    img = v['image_id']
    cat = v['category_id']
    if cat not in [3, 6, 7, 8]:
        continue
    if img in anns:
        anns[img].append (v)
    else:
        anns[img] = [v]

for k, vs in anns.items ():

    imageId = str (k).zfill (12)
    file = imgFile % imageId
    if os.path.exists (file):
        shutil.copy (file, destFile % (imageId))
        yoloAnnotiation = '%s %s %s %s %s\n'
        with open (destTextFile % (imageId), "w") as f:
            img = coco.loadImgs (k)[0]
            width = img["width"]
            height = img["height"]
            for v in vs:
                cat = v["category_id"]

                bbox = v["bbox"]
                f.write (yoloAnnotiation % (
                    cat, (bbox[0] + (bbox[2] / 2)) / width, (bbox[1] + (bbox[3] / 2)) / height, bbox[2] / width,
                    bbox[3] / height))
