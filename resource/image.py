from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request,send_file
from flask_jwt_extended import jwt_required,get_jwt_identity
import os,traceback

from libs import image_uploader
from schemas.image import ImageSchema

image_schema = ImageSchema()

class ImageUpload(Resource):
    @jwt_required
    def post(self):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            image_path = image_uploader.save_images(data["image"],folder=folder)
            basename =  image_uploader.get_basename(image_path)
            return {"msg": "image uploaded {}".format(basename)},201
        except UploadNotAllowed:
            ext = image_uploader.get_extension(data["image"])
            return {"msg": "Image format incorrect"},400

class Images(Resource):
    @jwt_required
    def get(self,filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_uploader.is_filename_safe(filename):
            return {"msg": "Incorrect file type requested"},400
        try:
            return send_file(image_uploader.get_path(filename,folder=folder))
        except FileNotFoundError:
            return {"msg": "Image not found"},404
    
    @jwt_required
    def delete(self,filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_uploader.is_filename_safe(filename):
            return {"msg": "Incorrect file type requested"},400
        try:
            return os.remove(image_uploader.get_path(filename,folder=folder))
        except FileNotFoundError:
            return {"msg": "Image not found"},404
        except:
            return {"msg": "Image could not be deleted"},400
