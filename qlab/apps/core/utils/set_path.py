from uuid import uuid4

from django.utils.deconstruct import deconstructible


@deconstructible
class SetPathAndRename(object):
    """
    Upload files under their related sub media directory with renaming
    """

    def __init__(self, path=''):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        return f'{self.sub_path}/{str(uuid4())[:8]}.{ext}'
