import pygame
import os


def create_img_list_from_dir(directory):
    img_list = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            # print(f)
            img_list.append(pygame.image.load(f))

    return img_list


def merge_img_list(img_list):
    """merge images in list to single flat image"""
    # merge images
    merge_img = None
    for img in img_list:
        if merge_img == None:
            merge_img = img
        else:
            merge_img.blit(img, (0, 0))

    return merge_img
