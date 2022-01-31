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

from email.header import decode_header

from arjuna.tpi.log import log_info


class Email:
    '''
    Represents an Email.

    Keyword Arguments:
        pyemail: Python's builtin email object.
    '''

    def __init__(self, pyemail):
        self.__email = pyemail
        self.__metadata = {}
        for k in self.__email.keys():
            value, encoding = decode_header(self.__email.get(k))[0]
            if isinstance(value, bytes):
                self.__metadata[k] = value.decode(encoding)
            else:
                self.__metadata[k] = value
        self.__contents = []
        self.__load_content()

    def __str__(self):
        return str(self.__email)

    def get_header(self, name):
        '''
        Get value for an email-header.
        '''
        return self.__metadata[name]

    @property
    def sender(self):
        '''
        Sender email-address (From)
        '''
        return self.get_header("From")

    @property
    def recipient(self):
        '''
        Recipient email-address (To)
        '''
        return self.get_header("To")

    @property
    def date(self):
        '''
        Date of receipt of this email.
        '''
        return self.get_header("Date")

    @property
    def subject(self):
        '''
        Subject line of this email.
        '''
        return self.get_header("Subject")

    @property
    def content_type(self):
        '''
        Content-Type of this email.
        '''
        return self.get_header("Content-Type")

    @property
    def is_multipart(self):
        '''
        Is it a multi-part email?
        '''
        return self.__email.is_multipart()

    def _load_part_content(self, part):
        # Code heavily taken from https://www.thepythoncode.com/article/reading-emails-in-python
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))
        try:
            # Email body
            body = part.get_payload(decode=True).decode()
        except:
            return
        if "attachment" not in content_disposition:
            if content_type == "multipart/alternative":
                pass
            elif content_type =="text/plain":
                from arjuna.tpi.parser.text import Text
                self.__contents.append(Text(body))
            elif content_type =="text/html":
                from arjuna.tpi.parser.html import Html
                self.__contents.append(Html.from_str(body))
            else:
                print("Unsupported email content type.", content_type)
                # Unsupported content type
                pass  
        else:
            pass
            # Currently Arjuna does not handle email attachments

    def _walk(self, email):
        for index, part in enumerate(email.walk()):
            self._load_part_content(part)

    def __load_content(self):
        if self.is_multipart:
            self._walk(self.__email)
        else:
            self._load_part_content(self.__email)

    @property
    def contents(self):
        '''
        Contents of this email as a list of objects representing different parts. Currently attachments are not processed.
        '''
        return self.__contents

    def find_links(self, *, unique=True, contain=""):
        '''
        All hyperlinks in the email content.

        Keyword Arguments:
            unique: Only unique hyperlinks are included in result.
            contain: Only hyperlinks that contain the provided substring are included in the result.
        '''
        outlist = []
        for content in self.contents:
            out = content.find_links(unique=unique, contain=contain)
            if out:
                outlist.extend(out)

        if unique:
            return tuple(set(outlist))
        else:
            return tuple(outlist) 

    def find_link(self, contains):
        '''
        Returns first hyperlink that contains the provided URI part as a sub-string.

        Arguments:
            contains: A sub-string which should be present in the hyperlink.
        '''
        links = self.find_links(contain=contains)
        if links:
            return links[0]
        else:
            raise Exception("No Hyperlink was found with sub-string >{}<".format(contains))


    @property
    def links(self):
        '''
        All hyperlinks in the email content.
        '''
        return self.find_links(unique=False)

    @property
    def unique_links(self):
        '''
        All unique hyperlinks in the email content.
        '''
        return self.find_links()


class Emails:
    '''
    Represents a sequence of one or more Arjuna's Email objects.

    Keyword Arguments:
        email_list: Sequence of Arjuna's email objects.

    Note:
        You can loop over this object like a Python-list.

        .. code-block:: python

            for email in emails:
                print(email)
    '''


    def __init__(self, email_list):
        self.__emails = email_list

    @property
    def count(self):
        '''
        Number of emails in this list.
        '''
        return len(self.__emails)

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        return self.__emails[index]

    def __iter__(self):
        return iter(self.__emails)