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
# Very useful information on emails in Python: https://coderzcolumn.com/tutorials/python/email-how-to-represent-an-email-message-in-python


from .server import ImapServer


class EmailServer:

    @classmethod
    def imap(cls, *, host=None, port=None, user=None, password=None, use_ssl=None):
        '''
        Create an IMAP Server supporting IMAP4 protocol for reading emails.

        Keyword Arguments:
            host: IP or domain name of Email IMAP Server. Default is localhost. Default is configurable with emailauto.imap.host option.
            port: Port of the IMAP Server. Default is 143 for non-SSL Mode and 993 for SSL-Mode. Default is configurable with emailauto.imap.port option.
            user: Email address to open mailbox. Default is configurable with emailauto.user option.
            password: Password corresponding to the email account. Default is configurable with emailauto.password option.
            use_ssl: Should IMAPS (SSL-mode) be used? Default is True.
        '''
        return ImapServer(host=host, port=port, user=user, password=password, use_ssl=use_ssl)