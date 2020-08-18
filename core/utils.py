import uuid
import os.path

def get_filename(filename):
    discard, ext = os.path.splitext(filename)
    basename = str(uuid.uuid4())
    return ''.join([basename, ext])
