#!/usr/bin/python3

import sys
sys.path.append('../lib/')
import req

file = '../Requirements.csv'
report_prefix = "SC2-Report"

print("Loading file:", file, "(last modified:", req.datemodified(file) + ")")
allreqs = req.readall(file)

sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")

status, out = req.generate_report(sc2reqs, 'SC2 Progress Report', req.datemodified(file), report_prefix)
if status == 1:
	print(out)
else:
	print("report created: " + out)
