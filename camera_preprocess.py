# This function performs initial preprocess 
from PIL import Image

def preprocess(image_file_name):
    sub_image = Image.open(image_file_name).crop((1370, 830, 1520, 980))
    new_file_name = image_file_name+"sub.jpg"
    sub_image.save(new_file_name)
    
    return new_file_name