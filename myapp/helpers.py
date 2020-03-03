import os
import uuid


# def get_uuid_filename(filename):

#     ext = filename.split('.')[-1]
#     return "{}.{}".format(uuid.uuid4().hex, ext)


# def get_upload_path(instance, filename):
#     return os.path.join(f"uploads/{instance.__class__.__name__.lower()}",
#                         get_uuid_filename(filename))

class DummyObject:
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
