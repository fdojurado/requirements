#!/usr/bin/python3
 
import sys
sys.path.append('../lib/')
import req

file = '../Requirements.csv'

print("Loading file:", file, "(last modified:", req.datemodified(file) + ")")
allreqs = req.readall(file)

sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")
poc2xreqs = req.filterstartswith(sc2reqs, req.Field.ProviderPoC, "PoC2.")
poc2xreqs2 = req.filterstartswith(allreqs, req.Field.ProviderPoC, "PoC2.")
inconsistentreqs = req.xor(poc2xreqs, poc2xreqs2)

print("Total PoC2.x Reqs:", req.countby(poc2xreqs2, req.Field.ProviderSC))
print("ID of PoC2.x Reqs not in SC2:", req.printfield(inconsistentreqs, req.Field.ID))