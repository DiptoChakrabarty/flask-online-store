from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity

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
            image_path = image_uploader.save_images(data["image"],folder-folder)
            basename =  image_uploader.get_basename(image_path)
            return {"msg": "image uploaded {}".format(basename)},201
        except UploadNotAllowed:
            ext = image_uploader.get_extension(data["image"])
            return {"msg": "Image format incorrect"},400