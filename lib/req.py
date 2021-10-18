import csv
import os
import time
from collections import Counter

class MyField:
	ID = 0
	Shorttitle = 1
	ProviderSC = 2
	ProviderPoC = 3
	Description = 4
	Rationale = 5
	ConsumerSC = 6
	ConsumerPoCDemo = 7
	ImplementationRelease = 8
	LeadImplementerContact = 9
	LeadImplementerPartner = 10
	Status = 11
	Progress = 12
	ProposedPartner = 13
	Comments = 14

Field =  MyField()

def readall(filename):
	print("Loading file:", filename, "(last modified:", time.ctime(os.path.getmtime(filename)) + ")")
	tmplist = []
	with open(filename) as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		next(csvReader)
		for row in csvReader:
			tmplist.append(row)
	return tmplist

def filterby(lst, field, value):
	tmplist = []
	for row in lst:
			if row[field].lower() == value.lower():
				tmplist.append(row)
	return tmplist	

def filterstartswith(lst, field, value):
	tmplist = []
	for row in lst:
			if row[field].startswith(value):
				tmplist.append(row)
	return tmplist	

def countby(lst, field):
	if len(lst) == 0:
		return None
	group = []
	for item in lst:
		group.append(item[field].lower())
		cn = Counter(group)
	return dict(cn.most_common())

def printfield(lst, field):
	tmp = []
	for item in lst:
		tmp.append(item[field])
	return tmp

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def union(lst1, lst2):
    lst3 = lst1 + [value for value in lst2 if value not in lst1]
    return lst3

def xor(lst1, lst2):
	lst3 = [value for value in lst1+lst2 if (value not in lst1) or (value not in lst2)]
	return lst3


