import req

file = 'Requirements-1018.csv'

allreqs = req.readall(file)
sc2reqs = req.filterby(allreqs, req.Field.ProviderSC, "SC2")

print("SC2 Reqs Status:", req.countby(sc2reqs, req.Field.Status))
print()
print("SC2 Reqs by Provider PoC:", req.countby(sc2reqs, req.Field.ProviderPoC))
print()
print("SC2 Contributors:", req.countby(sc2reqs, req.Field.LeadImplementerPartner))