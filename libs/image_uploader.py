import os,re 
from typing import Union 
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet,IMAGES 

image_set = UploadSet("images",IMAGES)


def save_images(image: FileStorage,folder: str=None,name: str=None) ->str:
    return image_set.save(image,folder,name)


def get_image_path(filename: str=None,folder: str=None) ->str:
    return image_set.path(filename,folder) 

def find_image_format(filename: str,folder: str) ->Union[str,None]:
    for format in IMAGES:
        image=f"{filename}.{format}"
        image_path = image_set.path(filename=image,folder=folder)
        if os.path.isfile(image_path):
            return image_path
        return None
        

def retrieve_filename(file: Union[str,FileStorage]) ->str:
    if isinstance(file,FileStorage):
        return file.filename
    return file

def is_filename_safe(file: Union[str,FileStorage]):
    filename = retrieve_filename(file)

    formats = "|".join(IMAGES)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.{{formats}}$"
    return re.match(regex,filename)  is not None 

def get_basename(file: Union[str,FileStorage]):
    filename= retrieve_filename(file)
    return os.path.split(filename)[1]

def get_extension():
    filename= retrieve_filename(file)
    return os.path.splittext(filename)[1] 