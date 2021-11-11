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

import pandas as pd
from fuzzywuzzy import fuzz

def loaddata(file, sheet=2):
	return pd.read_excel(file, sheet_name=sheet)
	
def filterby(df, field, value):
	return df[df[field] == value]

def isin(df, field, lst):
	return df[df[field].isin(lst)]

def getfield(df, field):
	return df[field]

def getlist(df):
	return df.values.tolist()

def lowerall(df):
	df = df.apply(lambda x: x.astype(str).str.lower())
	df = df.apply(lambda x: x.astype(str).str.strip())
	return df

def getaltnames(df, org):
	df = lowerall(df)
	df = df[df.eq(org.lower().strip()).any(1)]
	if not df.empty:
		df = df.values[0].tolist()
		while 'nan' in df:
			df.remove('nan')
		return df
	else:
		return [org]

def getemails(df, lst, flt=""):
	df = lowerall(df)
	lst = [x.lower() for x in lst]
	df = isin(df, 'Organization', lst)
	if flt != "":
		dftemp = filterby(df, flt, 'x')
		if not dftemp.empty:
			df = dftemp
	df = getfield(df, 'Email')
	df = getlist(df)
	return df

def fixemails(df, lst):
	df = getfield(df, 'Email')
	emails = []
	for i in lst:
		if i in df.values:
			emails.append(i)
		mx = 0
		idx = 0
		for j in df.values:
			if fuzz.ratio(i,j) > mx:
				mx = fuzz.ratio(i,j)
				idx = j
		emails.append(idx)
	return list(set(emails))
