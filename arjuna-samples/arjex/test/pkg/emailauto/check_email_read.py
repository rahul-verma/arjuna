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

from arjuna import *

@test
def check_email_temp(request):
    ms = EmailServer.imap()
    mb = ms.get_mailbox()

    # Write code to Trigger the event that leads to sending email(s) to this mailbox.

    # After the event
    emails = mb.new_emails(sender="rv@testmile.com")
    print("After email sending event: ", mb.count)
    for email in emails:
        print(email)

    ms.quit()

@test
def check_email_links(request):
    ms = EmailServer.imap()
    mb = ms.get_mailbox()

    # Write code to Trigger the event that leads to sending email(s) to this mailbox.

    # After the event
    lemail = mb.latest(subject="Docker")
    print(lemail.find_link("confirm-email"))
    
    ms.quit()