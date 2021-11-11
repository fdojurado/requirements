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

print("Loading file:", cfg.reqfile, "(last modified:", req.datemodified(cfg.reqfile) + ")")
allreqs = req.readall(cfg.reqfile)

sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")
poc2xreqs = req.filterstartswith(sc2reqs, req.Field.ProviderPoC, "PoC2.")
poc2xreqs2 = req.filterstartswith(allreqs, req.Field.ProviderPoC, "PoC2.")
inconsistentreqs = req.xor(poc2xreqs, poc2xreqs2)

print("Total PoC2.x Reqs:", req.countby(poc2xreqs2, req.Field.ProviderSC))
print("ID of PoC2.x Reqs not in SC2:", req.printfield(inconsistentreqs, req.Field.ID))

nopoc = req.union(
	req.filterby(sc2reqs, req.Field.ProviderPoC, "not yet identified"),
	req.filterby(sc2reqs, req.Field.ProviderPoC, "")
)
rq = req.xor(sc2reqs, poc2xreqs)
rq = req.xor(rq, nopoc)
print("SC2 Reqs not in PoC2.x:", req.countby(rq, req.Field.ProviderPoC))
print("ID of SC2 Reqs not in PoC2.x:", req.printfield(rq, req.Field.ID))
