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

import csv
import os
import sys
import time
import subprocess
import glob
import chardet
import re
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
from reqlib import contact as ct
import pandas as pd

class MyField:
	ID = 'ID'
	ShortTitle = 'Short title'
	ProviderSC = 'Provider SC'
	ProviderPoC = 'Provider PoC'
	Description = 'Description'
	Rationale = 'Rationale'
	ConsumerSC = 'Consumer(s) SC'
	ConsumerPoCDemo = 'Consumer(s) PoC/Demo'
	ImplementationRelease = 'Implementation Release'
	LeadImplementerContact = 'Lead implementer contact'
	LeadImplementerPartner = 'Lead implementer partner'
	Status = 'Status'
	Progress = 'Progress (%)'
	ProposedPartner = 'Proposed partner(s)'
	Comments = 'Comments'
	Headers = []

Field =  MyField()

def datemodified(filename):
	return time.ctime(os.path.getmtime(filename))

def readall(filename):
	tmplist = []
	with open(filename, 'rb') as rawdata:
		enc = chardet.detect(rawdata.read(10000))
	with open(filename, encoding=enc['encoding']) as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		Field.Headers = next(csvReader)
		for row in csvReader:
			tmplist.append(row)
	return tmplist

def filterby(lst, field, value):
	field = Field.Headers.index(field)
	tmplist = []
	for row in lst:
		if row[field].lower() == value.lower():
			tmplist.append(row)
	return tmplist	

def filterstartswith(lst, field, value):
	field = Field.Headers.index(field)
	tmplist = []
	for row in lst:
		if row[field].startswith(value):
			tmplist.append(row)
	return tmplist	

def countby(lst, field):
	field = Field.Headers.index(field)
	if len(lst) == 0:
		return None
	group = []
	for item in lst:
		group.append(item[field].lower())
		cn = Counter(group)
	return dict(cn.most_common())

def filterbylist(lst, field, value):
	field = Field.Headers.index(field)
	tmplist = []
	for row in lst:
		raw = row[field].lower()
		rawsplit = raw.split('"')
		while ',' in rawsplit: rawsplit.remove(',')
		while '[' in rawsplit: rawsplit.remove('[')
		while ']' in rawsplit: rawsplit.remove(']')
		if value.lower() in rawsplit:
			tmplist.append(row)
	return tmplist

def filterstartswithlist(lst, field, value):
	field = Field.Headers.index(field)
	tmplist = []
	for row in lst:
		raw = row[field].lower()
		rawsplit = raw.split('"')
		while ',' in rawsplit: rawsplit.remove(',')
		while '[' in rawsplit: rawsplit.remove('[')
		while ']' in rawsplit: rawsplit.remove(']')
		for ri in rawsplit:
			if ri.startswith(value.lower()):
				tmplist.append(row)
				break
	return tmplist

def countbylist(lst, field):
	field = Field.Headers.index(field)
	if len(lst) == 0:
		return None
	group = []
	for item in lst:
		raw = item[field].lower()
		rawsplit = raw.split('"')
		while ',' in rawsplit: rawsplit.remove(',')
		while '[' in rawsplit: rawsplit.remove('[')
		while ']' in rawsplit: rawsplit.remove(']')
		group = group + rawsplit
		cn = Counter(group)
	return dict(cn.most_common())

def printfield(lst, field):
	field = Field.Headers.index(field)
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
		raw = i[Field.Headers.index(Field.ImplementationRelease)]
		raw = raw.replace('M', '')
		rawsplit = raw.split('"')
		while ',' in rawsplit: rawsplit.remove(',')
		while '[' in rawsplit: rawsplit.remove('[')
		while ']' in rawsplit: rawsplit.remove(']')
		for d in rawsplit:
			a.append([
				int(i[Field.Headers.index(Field.ID)]),
				int(i[Field.Headers.index(Field.Progress)].split('%')[0].strip()),
				int(d),
				i[Field.Headers.index(Field.LeadImplementerPartner)].strip()
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
	out = out + r'\begin{document}' + '\n'
	out = out + r'\title{' + title + " (M%d)" % MNOW + footnote +  r'}' + '\n'
	out = out + r'\date{}' + '\n'
	out = out + r'\maketitle' + '\n'
	out = out + r'\begin{verbatim}' + '\n'

	out = out + progress_report(lst)

	out = out + r'\end{verbatim}' + '\n'
	out = out + r'\end{document}'

	with open("tmp.tex", 'w') as f:
		f.write(out)

	try:
		subprocess.call(["latexmk", "-pdf", "tmp.tex"])
		os.rename("tmp.pdf", prefix + "-M%d.pdf" % MNOW)
		for fl in glob.glob("tmp.*"):
			os.remove(fl)
	except FileNotFoundError:
		sys.stderr.write("error: latexmk not found.\n")
		sys.exit(1)

	return prefix + "-M%d.pdf" % MNOW

def plot_counter(cn, title, x_label=None):
	plt.figure()
	plt.rc('axes', axisbelow=True)
	plt.bar(cn.keys(), cn.values(), align='center')
	plt.grid()
	plt.ylabel("Count")
	plt.title(os.path.splitext(title)[0])
	if x_label is not None:
		plt.xlabel(x_label)
	plt.xticks(rotation=90)
	plt.savefig(title, bbox_inches='tight')

def find_emails(lst, contactdf, altnamesdf, flt=''):
	emails = []
	for i in lst:
		contact = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", i[Field.Headers.index(Field.LeadImplementerContact)])
		if contact != []:
			emails = emails + contact
		elif isinstance(contactdf, pd.DataFrame):
			altnames = ct.getaltnames(altnamesdf, i[Field.Headers.index(Field.LeadImplementerPartner)])
			emails = emails + ct.getemails(contactdf, altnames, flt)
	return list(set([x.lower() for x in emails]))
