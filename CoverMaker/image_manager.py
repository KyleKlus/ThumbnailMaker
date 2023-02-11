from PIL import Image
import numpy as np


def read_image(path):
    '''
    Loads the image from a path and handles the exceptions
    :param path : Sourcepath of the image
    :return Loaded image
    '''
    try:
        image_src = Image.open(path)
        return image_src
        
    except Exception as e:
        print(e)



def get_bar_width(img, vertical = True, color = [0, 0, 0], c_deviation = 12):
    '''
    Determines the width of the bars in the image
    :param img : image to be analyzed
    :param vertical : option, which determines the direction of the bars
    :param color : option, which determines the color of the bars
    :param c_deviation : maximum deviation from the original color
    :return width of the plainly colured bars in pixels
    '''
    pix = np.array(img)
    width = 0
    
    if vertical:
        for p in [0.20, 0.50, 0.80]:  # take a sample from the top, middle and bottom
            x = 0
            for i in pix[int(img.height * p)]: # check if pixel is a bar pixel
                if i[0] < color[0] + c_deviation and i[1] < color[1] + c_deviation and i[2] < color[2] + c_deviation:
                    x += 1
                else:
                    break
            
            if x < width or p == 0.20: # check if x is a better value
                width = x
    
    else:
        for p in [0.20, 0.50, 0.80]:  # take a sample from the left, middle and right
            x = 0
            for i in pix: # check if pixel is a bar pixel
                if i[int(img.width * p)][0] < color[0] + c_deviation and i[int(img.width * p)][1] < color[1] + c_deviation and i[int(img.width * p)][2] < color[2] + c_deviation:
                    x += 1
                else:
                    break
            
            if x < width or p == 0.20: # check if x is a better value
                width = x
    
    return width

def add_bars(img, min_size = 1, bar_color = (1, 1, 1)):
    '''
    Creates a new image containing the original one and 
    two black bars on top of the larger sides.
    :param img : image to be modified
    :param bar_color : color of the new bars
    :return new_image : black image with the correct size
    '''
    if img.width < min_size: # handle low res images
            bar = Image.new(mode = 'RGB', size = ((min_size - img.width) // 2, img.height), color = bar_color)
            new_img = Image.new('RGB', (min_size, img.height))
            new_img.paste(bar, (0, 0))
            new_img.paste(img, (bar.width, 0))
            new_img.paste(bar, (bar.width + img.width, 0))
            img = new_img
    
    if img.height < min_size: # handle low res images
            bar = Image.new(mode = 'RGB', size = (img.width, (min_size - img.height) // 2), color = bar_color)
            new_img = Image.new('RGB', (img.width, min_size))
            new_img.paste(bar, (0, 0))
            new_img.paste(img, (0, bar.height))
            new_img.paste(bar, (0, bar.height + img.height))
            img = new_img
    
    if img.width > img.height: # get the proportions and execute the code which keeps the proportions
        bar = Image.new(mode = 'RGB', size = (img.width, (img.width - img.height) // 2), color = bar_color)
        new_img = Image.new('RGB', (img.width, img.height + 2 * bar.height))
        new_img.paste(bar, (0, 0))
        new_img.paste(img, (0, bar.height))
        new_img.paste(bar, (0, bar.height + img.height))
        
    elif img.height > img.width: # get the proportions and execute the code which keeps the proportions
        bar = Image.new(mode = 'RGB', size = ((img.height - img.width) // 2, img.height), color = bar_color)
        new_img = Image.new('RGB', (img.width + 2 * bar.width, img.height))
        new_img.paste(bar, (0, 0))
        new_img.paste(img, (bar.width, 0))
        new_img.paste(bar, (bar.width + img.width, 0))
    else:
        new_img = img;
    
    return new_img


def generate_cover(img_path, size):
    '''
    Generates a new image containing the original one and 
    two black bars with the correct size, so that the image has the specified size
    :param img_path : path of the image to be modified
    :param size : size of the new image
    :return img : image with the correct size
    '''
    img = read_image(img_path) # fetch the image
    
    # cut of any vertical bars
    bar_width = get_bar_width(img, vertical = True)
    if bar_width > 0:
        img = img.crop((bar_width, 0, img.width - bar_width, img.height))
    
    # cut of any horizontal bars
    bar_width = get_bar_width(img, vertical = False)
    if bar_width > 0:
        img = img.crop((0, bar_width, img.width, img.height - bar_width))
    
    img = add_bars(img, size) # add new bars if needed, so that the image is square
    
    if not img.width == size: # resize to the specified size 
        img = img.resize((size, size))
    
    return img
