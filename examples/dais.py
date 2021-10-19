#!/usr/bin/python3

import sys
sys.path.append('../lib/')
import req

file = '../Requirements.csv'

print("Loading file:", file, "(last modified:", req.datemodified(file) + ")")
allreqs = req.readall(file)

pocreqs = req.filterstartswith(allreqs, req.Field.ProviderPoC, "PoC")
nopocreqs  = req.union(req.filterby(allreqs, req.Field.ProviderPoC, ""), req.filterby(allreqs, req.Field.ProviderPoC, "not yet identified"))

print("All Reqs (Total):", len(allreqs))
print("Reqs in PoC (Total):", len(pocreqs))
print("Reqs not in PoC (Total):", len(nopocreqs))

print("All Reqs by Provider SC:", req.countby(allreqs, req.Field.ProviderSC))
print()

print("Reqs in PoC:", req.countby(pocreqs, req.Field.ProviderPoC))
print()

print("All Reqs by Lead:", req.countby(allreqs, req.Field.LeadImplementerPartner))
