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

import sys
sys.path.append('../lib/')
import req

file = '../Requirements.csv'

print("Loading file:", file, "(last modified:", req.datemodified(file) + ")")
allreqs = req.readall(file)
sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")

count = req.countby(sc2reqs, req.Field.Status)
print("SC2 Reqs Status:", count)
print()
req.plot_counter(count, "SC2-Req-Status.pdf")

count = req.countby(sc2reqs, req.Field.ProviderPoC)
print("SC2 Reqs by Provider PoC:", count)
print()
req.plot_counter(count, "SC2-Req-Provider.pdf")

count = req.countby(sc2reqs, req.Field.LeadImplementerPartner)
print("SC2 Contributors:", count)
req.plot_counter(count, "SC2-Req-Lead.pdf")
