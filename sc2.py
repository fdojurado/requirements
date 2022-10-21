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

from reqlib import req
import myconfig as cfg
import re

print("Loading file:", cfg.reqfile,
      "(last modified:", req.datemodified(cfg.reqfile) + ")")
allreqs = req.readall(cfg.reqfile)
sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")

count = req.countby(sc2reqs, req.Field.Status)
req.plot_counter(count, "SC2-Req-Status.pdf")
print("SC2 Reqs Status:", count)
print()

count = req.countby(sc2reqs, req.Field.ProviderPoC)
req.plot_counter(count, "SC2-Req-Provider.pdf")
print("SC2 Reqs by Provider PoC:", count)
print()

count = req.countby(sc2reqs, req.Field.LeadImplementerPartner)
req.plot_counter(count, "SC2-Req-Lead.pdf")
print("SC2 Contributors:", count)
print()

count = req.countbylist(sc2reqs, req.Field.ConsumerPoCDemo)
req.plot_counter(count, "SC2-Req-Consumer.pdf")
print("SC2 Reqs by Consumer PoC or Demo:", count)

count = req.countbylist(sc2reqs, req.Field.Progress)
count = {int(re.sub(r' [%]$', '', k)): v for (k, v) in count.items()}
sorted_items = dict(sorted(count.items()))
req.plot_counter(sorted_items, "SC2-Req-progress.pdf", 'Progress (%)')
print("SC2 Reqs progress:", count)