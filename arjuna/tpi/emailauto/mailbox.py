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

import email as pyemail

from arjuna.tpi.log import log_info
from arjuna.core.error import EmailBoxNotConnected, EmailNotReceived
from arjuna.interact.email.conditions import MailBoxConditions

from .email import Email, Emails

class MailBox:
    '''
    Represents a named mailbox like Inbox in the email server for a user account.

    Keyword Arguments:
        server: Arjuna's Email Server object.
        name: Name of the mailbox. Default is Inbox.
        readonly: If True, messages can bot be deleted in the mailbox. Default is False.
    '''

    def __init__(self, *, server, name="INBOX", readonly=False):
        self.__server = server
        self.__name = name
        self.__readonly = readonly
        self.__count = None
        self.__saved_count = None

        self.save_state()

    def _select(self):
        status, data = self._server._imap.select(self.name, readonly=self.readonly)
        if status != "OK":
            raise EmailBoxNotConnected(self._server, self.name, data[0].decode())

    def _search(self, sender=None, subject=None, content=None, max=5, latest=True, consider_saved_state=True):
        self._select()

        data = None
        status, data = self._server._imap.search(None, 'ALL')
        if status != "OK":
            raise EmailNotReceived(self._server, self.name, data[0].decode())
        elif not data:
            raise EmailNotReceived(self._server, self.name, "No emails found.")

        email_numbers = data[0].split()
        new_email_count = len(email_numbers)

        if consider_saved_state:
            if new_email_count <= self.__saved_count:
                raise EmailNotReceived(self._server, self.name, "No *new* emails found since last saved state.")
        
        if consider_saved_state:
            new_email_count = new_email_count - self.__saved_count
        if new_email_count < max:
            max = new_email_count
        track = 0
        out_list = []
        if latest:
            email_numbers = reversed(email_numbers)
        for num in email_numbers:
            if track == max:
                break
            email = self.email_at(num.decode())

            if sender and sender.lower() not in email.sender.lower():
                continue

            if subject and subject.lower() not in email.subject.lower():
                continue

            if content:
                found = False
                for c in email.contents:
                    if content in str(c):
                        found = True
                        break
                if not found:
                    continue

            out_list.append(email)
            track += 1

        if out_list:
            return Emails(out_list)

        raise EmailNotReceived(self._server, self.name, "No *new* emails found since last saved state.", sender=sender, subject=subject, content=content)

    def __load(self):
        from arjuna import log_debug
        log_debug("Selecting mailbox: {}".format(self.name))
        if self._server._ready:
            MailBoxConditions(self).Select().wait(max_wait=30)
            _, data = self._server._imap.search(None, 'ALL')
            self.__count = sum(1 for num in data[0].split())
            log_debug("Selected mailbox: {}".format(self.name))
        else:
            raise Exception("A mailbox can be selected only with active connection to IMAP server.")

    def new_emails(self, *, sender=None, subject=None, content=None, max=5, max_wait=None):
        '''
        New emails received since the previous saved state (saved using save_state call), as per provided optional filters.

        Keyword Arguments:
            sender: Filter with Email address from which email is received.
            subject: Filter with Case-insensitive sub-string in subject line.
            content: Filter with Case-insensitive sub-string in content.
            max: Maximum number of emails to be returned. Default is 5.
            max_wait: Maximum time in seconds to re-select mailbox or availablity of emails in the mailbox.

        Note:
            The wait is not a static wait and comes into play if no email meets the filtering criteria.
            When the logic finds the first matching email, it tries to find more, else the wait loop is exited.
        '''
        from arjuna import C
        if max_wait is None:
            max_wait = C("emailauto.max.wait")
        return MailBoxConditions(self).ReceiveEmail(max=max, sender=sender, subject=subject, content=content, latest=True).wait(max_wait=max_wait)

    def latest(self, *, sender=None, subject=None, content=None, max_wait=None):
        '''
        Latest email received since the previous saved state (saved using save_state call), as per provided optional filters.

        This is a shortcut method, and works same as providing max=1 to new_emails.

        Keyword Arguments:
            sender: Filter with Email address from which email is received.
            subject: Filter with Case-insensitive sub-string in subject line.
            content: Filter with Case-insensitive sub-string in content.
            max_wait: Maximum time in seconds to re-select mailbox or availablity of emails in the mailbox.
        '''
        return self.new_emails(max=1, sender=sender, subject=subject, content=content, max_wait=max_wait)[0] 

    def emails(self, *, sender=None, subject=None, content=None, max=5, latest=True):
        '''
        Get Current Emails as per provided optional filters.

        Keyword Arguments:
            sender: Filter with Email address from which email is received.
            subject: Filter with Case-insensitive sub-string in subject line.
            content: Filter with Case-insensitive sub-string in content.
            max: Maximum number of emails to be returned. Default is 5.
            latest: If True, latest emails are considered. Default is True.

        Note:
            If no email is found in current emails that meets the filtering criteria, an automatic wait loop triggers and this method works just like new_emails method in such a context.
            When the logic finds the first matching email, it tries to find more, else the wait loop is exited.
        '''
        from arjuna import C
        max_wait = C("emailauto.max.wait")
        MailBoxConditions(self).Select().wait(max_wait=max_wait)
        return MailBoxConditions(self).ReceiveEmail(max=max, sender=sender, subject=subject, content=content, consider_saved_state=False).wait(max_wait=max_wait)

    @property
    def _server(self):
        return self.__server

    @property
    def name(self):
        '''
        Name of this mailbox.
        '''
        return self.__name

    @property
    def readonly(self):
        '''
        Is it a readonly mailbox selection?
        '''
        return self.__readonly

    @property
    def count(self):
        '''
        Current number of emails present in the mailbox.
        '''
        self.__load()
        return self.__count

    def save_state(self):
        '''
        Save current state information (like email count) before triggering a wait event in subsequent call.
        '''
        self.__load()
        self.__saved_count = self.__count

    def _force_state(self, count):
        '''
        Meant for module testing.
        '''
        self.__saved_count = count

    def email_at(self, ordinal, _reload=True):
        '''
        Email at an ordinal/position - human counted, 1 is the oldest email position.
        '''
        from arjuna import log_debug
        log_debug("Reading email at ordinal >{}< from mailbox {} at email server >{}<".format(
            ordinal, self.name, self._server.host
        ))
        if _reload:
            self.__load()
        _, data = self._server._imap.fetch(str(ordinal), '(RFC822)')
        return Email(pyemail.message_from_string(data[0][1].decode()))