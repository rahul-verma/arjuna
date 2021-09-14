# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This has to wait. Mimesis 5.0.0 release on Pypi not available yet.
# from mimesis import BinaryFile
#     from mimesis.enums import AudioFile, CompressedFile, DocumentFile, ImageFile, VideoFile

class File:

    @classmethod
    def mp3(cls) -> bytes:
        '''
            Generate an MP3 audio file and return as bytes.
        '''
        return BinaryFile().audio(file_type=AudioFile.MP3)

    @classmethod
    def aac(cls):
        '''
            Generate an AAC audio file and return as bytes.
        '''
        return BinaryFile().audio(file_type=AudioFile.ACC)

    @classmethod
    def zip(cls):
        '''
            Generate a zip compressed file and return as bytes.
        '''
        return BinaryFile().audio(file_type=CompressedFile.ZIP)

    @classmethod
    def gzip(cls):
        '''
            Generate a gzip compressed file and return as bytes.
        '''
        return BinaryFile().audio(file_type=CompressedFile.gzip)

    @classmethod
    def pdf(cls):
        '''
            Generate a PDF document file and return as bytes.
        '''
        return BinaryFile().compressed(file_type=DocumentFile.PDF)

    @classmethod
    def docx(cls):
        '''
            Generate a DOCX document file and return as bytes.
        '''
        return BinaryFile().compressed(file_type=DocumentFile.DOCX)

    @classmethod
    def pptx(cls):
        '''
            Generate a PPTX document file and return as bytes.
        '''
        return BinaryFile().document(file_type=DocumentFile.PPTX)

    @classmethod
    def xlsx(cls):
        '''
            Generate a XLSX document file and return as bytes.
        '''
        return BinaryFile().document(file_type=DocumentFile.XLSX)

    @classmethod
    def gif(cls):
        '''
            Generate a GIF Image file and return as bytes.
        '''
        return BinaryFile().image(file_type=ImageFile.GIF)

    @classmethod
    def png(cls):
        '''
            Generate a PNG Image file and return as bytes.
        '''
        return BinaryFile().image(file_type=ImageFile.PNG)

    @classmethod
    def jpg(cls):
        '''
            Generate a JPG Image file and return as bytes.
        '''
        return BinaryFile().image(file_type=ImageFile.JPG)

    @classmethod
    def mov(cls):
        '''
            Generate a MOV Video file and return as bytes.
        '''
        return BinaryFile().image(file_type=VideoFile.MOV)

    @classmethod
    def mp4(cls):
        '''
            Generate an MP4 Video file and return as bytes.
        '''
        return BinaryFile().image(file_type=VideoFile.MP4)