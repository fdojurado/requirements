#!/usr/bin/python3
#
# Copyright (C) 2021  Xenofon Fafoutis <xefa@dtu.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from reqlib import spam
from reqlib import req
from reqlib import contact as ct
import myconfig as cfg

contactdf = ct.loaddata(cfg.contactsfile)
altnamesdf = ct.loaddata(cfg.altnamesfile, 0)

allreqs = req.readall(cfg.reqfile)
sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")
proposed = req.filterby(sc2reqs, req.Field.Status, 'Proposed')
emails = req.find_emails(proposed, contactdf, altnamesdf, 'SC2')

TO = ct.fixemails(contactdf, emails)

DATE = req.datemodified(cfg.reqfile)

SUBJECT = "[DAIS-SC2] Requirements not yet accepted/rejected by lead implementer"

MESSAGE = """Dear DAIS lead implementers,

This is a kind reminder that the status of some of your requirements is still 'Proposed', waiting for your approval. Please, review the requirements and change the status to 'Accepted by lead implementer' or 'Rejected by lead implementer' accordingly.

The 'Proposed' requirements are: %s

Thanks in advance for addressing this issue.

This email is based on a snapshot of the requirements table downloaded on %s.
If you have updated your requirements after that time, please ignore this email.

Cheers,
%s
""" % (req.printfield(proposed, req.Field.ID), DATE, cfg.NAME)

spam.smtpconf(cfg.SMTP_SERVER, cfg.SMTP_PORT, cfg.SMTP_USERNAME)
spam.email(cfg.FROM, TO, SUBJECT, MESSAGE, DATE)
