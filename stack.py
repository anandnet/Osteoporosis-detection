import cv2
import numpy as np

def basic_changes(scale,img):
    #change into bgr,scaling of images
    shape=img.shape
    if (len(shape)==2):
        img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    new_img=cv2.resize(img,(width,height))
    return new_img

def blank_img(height,width):
    blank_image = np.zeros((height,width,3), np.uint8)
    return blank_image
    



def image_matrix(matrix,scale=1):
    """
    This function takes three args(Matrix,Scale)
    1. Matrix of images is list of images (height,width of every image should be same)
            ex: [[img1,img2,img3],[[],img4,img5]]
        for blank image [ ] can be used.
        first image should not be blank image.
    2. Scale which is for scaling of img,defult value is 1
    """
    collage_img=None
    for i,rows in enumerate(matrix):
        collage_row_img=basic_changes(scale,rows[0])
        shape=collage_row_img.shape
        for j,image in enumerate(rows):
            if j==0:
                continue
            else:
                if(image==[]):
                    collage_row_img=np.hstack((collage_row_img,blank_img(shape[0],shape[1])))
                else:
                    collage_row_img=np.hstack((collage_row_img,basic_changes(scale,image)))
        if (i==0):
            collage_img=collage_row_img
        else:
            collage_img=np.vstack((collage_img,collage_row_img))
    return collage_img
    