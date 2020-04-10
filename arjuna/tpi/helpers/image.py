import os
import base64

class Image:

    def __init__(self, *, fpath: str, b64: str=None):
        self.__fpath = fpath
        self.__b64 = b64

    @property
    def file_name(self):
        '''
            File Name of screenshot file.
        '''

        return os.path.basename(self.__fpath)

    @property
    def full_path(self):
        '''
           Abolsute path of screenshot file.
        '''

        return self.__fpath

    @property
    def base64(self):
        '''
            Base64 string for the image.
        '''
        if self._b64:
            return self.__b64

        with open(self.__fpath, "rb") as f:
            content = f.read()
            return base64.b64encode(content)

