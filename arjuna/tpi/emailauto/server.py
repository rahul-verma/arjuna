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

import imaplib

from .mailbox import MailBox


class ImapServer:
    '''
    IMAP Server supporting IMAP4 protocol for reading emails.

    Keyword Arguments:
        host: IP or domain name of Email IMAP Server. Default is localhost. Default is configurable with emailauto.imap.host option.
        port: Port of the IMAP Server. Default is 143 for non-SSL Mode and 993 for SSL-Mode. Default is configurable with emailauto.imap.port option.
        user: Email address to open mailbox. Default is configurable with emailauto.user option.
        password: Password corresponding to the email account. Default is configurable with emailauto.password option.
        use_ssl: Should IMAPS (SSL-mode) be used? Default is True.
    '''

    def __init__(self, *, host=None, port=None, user=None, password=None, use_ssl=None):
        from arjuna import C
        cport = C("emailauto.imap.port")
        self.__host = host is None and C("emailauto.imap.host") or host
        if use_ssl is None:
            self.__use_ssl = C("emailauto.imap.usessl")
        else:
            self.__use_ssl = use_ssl
        if port is None:
            if cport != "not_set":
                self.__port = cport
            else:
                self.__port = self.__use_ssl and 993 or 143
        self.__user = user and user or C("emailauto.user")
        if self.__user == "not_set":
            raise Exception("One must provide IMAP server user in the constructor or in the reference configuration value for emailauto.user option.")

        self.__password = password and password or C("emailauto.password")
        if self.__password == "not_set":
            raise Exception("One must provide IMAP server password in the constructor or in the reference configuration value for emailauto.password option.")

        self.__imap = None
        self.__connected = False
        self.__loggedin = False
        self.__mailbox = None
        self.__ready = False

        self.connect()

    def connect(self, reconnect=False):
        '''
        Connect to the server and login using the provided account details.

        Keyword Arguments:
            reconnect: If already connected, force a reconnect. Default is False.
        '''
        if self.__ready:
            if not reconnect:
                return
            else:
                self.quit()
        from arjuna import log_info
        log_info("Connecting to IMAP server >{}< at port >{}< (Using SSL: {}) for user: >{}<.".format(
            self.host, self.port, self.uses_ssl, self.user
        ))
        if not self.__connected:
            if self.uses_ssl:
                self.__imap = imaplib.IMAP4_SSL(self.host, self.port)
            else:
                self.__imap = imaplib.IMAP4(self.host, self.port)
            self.__connected = True

        if not self.__loggedin:
            self._imap.login(self.user, self.password)
            self.__loggedin = True

        # By default connects to Inbox.
        self.__ready = True
        log_info("Connected to IMAP Server >{}<.".format(self.host))

    def quit(self):
        '''
        Disconnect from the server and logout.
        '''
        from arjuna import log_info
        log_info("Disconnecting from IMAP Server >{}<.".format(self.host))
        if self.__ready:
            # Select should be done atleast once before closing. So this line takes care of that.
            self.__imap.select("INBOX")
            self._imap.close()
            self.__msg_count = None
            if self.__loggedin:
                self._imap.logout()
                self.__loggedin = False
            log_info("Disconnected from IMAP Server >{}<.".format(self.host))
            self.__connected = False
            return
        log_info("Quit called without active connection to IMAP Server >{}<. Ignored.".format(self.host))

    def get_mailbox(self, name="INBOX", *, readonly=False):
        '''
        Get a MailBox object.

        Arguments:
            name: Name of the mailbox. Default is Inbox.

        Keyword Arguments:
            readonly: If True, messages can bot be deleted in the mailbox. Default is False.
        '''
        return MailBox(server=self, name=name, readonly=readonly)

    @property
    def host(self):
        '''
        Domain/IP Address of the server.
        '''
        return self.__host

    @property
    def uses_ssl(self):
        '''
        Does it use SSL?
        '''
        return self.__use_ssl

    @property
    def port(self):
        '''
        Network port of the server.
        '''
        return self.__port

    @property
    def user(self):
        '''
        Email account to open mailbox.
        '''
        return self.__user

    @property
    def password(self):
        '''
        Email account password to open mailbox.
        '''
        return self.__password

    @property
    def _imap(self):
        return self.__imap

    @property
    def _ready(self):
        return self.__ready

    @property
    def _mailbox(self):
        return self.__mailbox