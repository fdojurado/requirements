#!/usr/bin/python3

import sys
sys.path.append('../lib/')
import req

file = '../Requirements.csv'

allreqs = req.readall(file)
sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")

print(req.progress_report(sc2reqs))
