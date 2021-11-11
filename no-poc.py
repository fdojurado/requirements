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

reqsc1 = req.filterby(allreqs, req.Field.ConsumerPoCDemo, "")
reqsc2 = req.filterby(allreqs, req.Field.ConsumerPoCDemo, "not yet identified")
reqsc = req.union(reqsc1, reqsc2)

reqsp1 = req.filterby(allreqs, req.Field.ProviderPoC, "")
reqsp2 = req.filterby(allreqs, req.Field.ProviderPoC, "not yet identified")
reqsp = req.union(reqsp1, reqsp2)

reqs = req.intersection(reqsc, reqsp)

req.plot_counter(req.countby(reqs, req.Field.ProviderSC), "No-Consumer-Producer-PoC.pdf")
