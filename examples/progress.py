#!/usr/bin/python3

import sys
sys.path.append('../lib/')
import req

file = '../Requirements.csv'
report_prefix = "SC2-Report"

print("Loading file:", file, "(last modified:", req.datemodified(file) + ")")
allreqs = req.readall(file)

sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")

prog = req.generate_report(report_prefix, sc2reqs, 'SC2 Progress Report', req.datemodified(file))

print(prog)
