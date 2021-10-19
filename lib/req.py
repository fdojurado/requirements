import csv
import os
import time
from datetime import datetime
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

def datemodified(filename):
	return time.ctime(os.path.getmtime(filename))

def readall(filename):
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

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def progress_report(lst):
	a = []
	for i in lst:
		a.append([
			int(i[Field.ID]),
			int(i[Field.Progress].split('%')[0].strip()),
			int(i[Field.ImplementationRelease].split('"')[1].split("M")[1]),
			i[Field.LeadImplementerPartner]
		])
	a = sorted(a,key=lambda x: (x[2],x[1]))

	MNOW = diff_month(datetime.now(), datetime(2021,4,1))

	out = ""
	steps = 20
	for i in a:
		prog = "["
		for j in range(0, int(i[1]*steps/100)):
			prog = prog + '='
		for j in range(int(i[1]*steps/100), steps):
			prog = prog + ' '
		prog = prog + "]"

		alert = ""
		if i[1] < 100 and MNOW > i[2]:
			alert = "RED ALERT"
		elif i[1] < 100 and MNOW >= i[2]:
			alert = "ORANGE ALERT"
		elif i[1] < 100 and MNOW >= i[2] - 1:
			alert = "YELLOW ALERT"

		out = out + "%3d %20s %s %3d%%   M%.2d %s\n" % (i[0], i[3], prog, i[1], i[2], alert)

	return out

def generate_report(lst, title, date, prefix):

	footnote = r'\footnote{Requirements downloaded from Sharepoint: ' + date + r'}'
	MNOW = diff_month(datetime.now(), datetime(2021,4,1))

	out = r'\documentclass[a4paper]{article}' + '\n'
	out = out + r'\title{' + title + " (M%d)" % MNOW + footnote +  r'}' + '\n'
	out = out + r'\date{}' + '\n'
	out = out + r'\maketitle' + '\n'
	out = out + r'\begin{document}' + '\n'
	out = out + r'\begin{verbatim}' + '\n'

	out = out + progress_report(lst)

	out = out + r'\end{verbatim}' + '\n'
	out = out + r'\end{document}'

	return out