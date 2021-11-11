#!/usr/bin/python3

from reqlib import contact as ct
import myconfig as cfg

ORG = 'DTU'

altnames = ct.loaddata(cfg.altnamesfile, 0)
altnames = ct.getaltnames(altnames, ORG)

df = ct.loaddata(cfg.contactsfile)
df = ct.getemails(df, altnames, 'SC2')

print(df)
