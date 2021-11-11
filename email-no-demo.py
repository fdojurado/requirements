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

print("Loading file:", cfg.reqfile, "(last modified:", req.datemodified(cfg.reqfile) + ")")
allreqs = req.readall(cfg.reqfile)
sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")

reqsc1 = req.filterby(sc2reqs, req.Field.ConsumerPoCDemo, "")
reqsc2 = req.filterby(sc2reqs, req.Field.ConsumerPoCDemo, "not yet identified")
reqsc = req.union(reqsc1, reqsc2)

withdemo = req.filterstartswithlist(sc2reqs, req.Field.ConsumerPoCDemo, "Demo")
nodemo = req.xor(sc2reqs, withdemo)
emails = req.find_emails(nodemo, contactdf, altnamesdf, 'SC2')

TO = ct.fixemails(contactdf, emails)

DATE = req.datemodified(cfg.reqfile)

SUBJECT = "[DAIS-SC2] Requirements without consumer demo"

MESSAGE = """Dear DAIS lead implementers,

This is a kind reminder that the status of some of your requirements do not have a consumer demonstrator.
Each requirement shall be preferably consumed by a demostrator (but can also be consumed by a PoC only exceptionally).

If your requirements do not have a Consumer PoC or Demonstrator, please identify one and add it to the 'Consumer(s) PoC/Demo' field.

If your requirements have a Consumer PoC, please identify the most suitable demonstrator and add it to the 'Consumer(s) PoC/Demo' field. The field can have multiple values, so no need to remove the Consumer PoC.

The requirements with no consumer demonstrator are: %s

The requirements with neither consumer demonstrator nor PoC are: %s

Thanks in advance for addressing this issue.

This email is based on a snapshot of the requirements table downloaded on %s.
If you have updated your requirements after that time, please ignore this email.

Cheers,
%s
""" % (req.printfield(nodemo, req.Field.ID), req.printfield(reqsc, req.Field.ID), DATE, cfg.NAME)

spam.smtpconf(cfg.SMTP_SERVER, cfg.SMTP_PORT, cfg.SMTP_USERNAME)
spam.email(cfg.FROM, TO, SUBJECT, MESSAGE, DATE)
