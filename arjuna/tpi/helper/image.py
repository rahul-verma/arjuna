import os
import base64

from arjuna.tpi.tracker import track

@track("trace")
class Image:
    '''
        An image object.

        Keyword Arguments:
            fpath: (Mandatory) Absolute path of the Image file.
            b64: Base64 representation of the image.
    '''

    def __init__(self, *, fpath: str, b64: str=None):
        self.__fpath = fpath
        self.__b64 = b64

    @property
    def file_name(self) -> str:
        '''
            File Name of screenshot file.
        '''

        return os.path.basename(self.__fpath)

    @property
    def full_path(self) -> str:
        '''
           Absolute path of screenshot file.
        '''

        return self.__fpath

    @property
    def base64(self) ->str:
        '''
            Base64 string for the image.
        '''
        if self.__b64:
            return self.__b64

        with open(self.__fpath, "rb") as f:
            content = f.read()
            return base64.b64encode(content)

