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

SMTP_SERVER = ''
SMTP_PORT = 0
SMTP_USERNAME = ''

import sys
import smtplib
from email.message import EmailMessage
from getpass import getpass
from datetime import datetime

def smtpconf(server, port, username):
	global SMTP_SERVER
	global SMTP_PORT
	global SMTP_USERNAME

	SMTP_SERVER = server
	SMTP_PORT = port
	SMTP_USERNAME = username

def fresh(modified):
	mod = datetime.strptime(modified, "%a %b %d %H:%M:%S %Y")
	diff = datetime.now() - mod
	if diff.days > 0:
		return False
	return True

def email(FROM, TO, SUBJECT, MESSAGE, DATE):

	if SMTP_SERVER == "" or SMTP_PORT == 0 or SMTP_USERNAME == "":
		print("SMTP not configured.")
		sys.exit(1)

	TO.append(FROM)

	msg = EmailMessage()
	msg['From'] = FROM
	msg['Bcc'] = ', '.join(TO)
	msg['Subject'] = SUBJECT
	msg.set_content(MESSAGE) 

	print(msg)

	if not fresh(DATE):
		print("Data are not fresh: %s." % DATE)
		print("Abort.")
		sys.exit(1)

	print("You are about to send an email using %s." % (SMTP_SERVER))
	try:
		password = getpass()
	except KeyboardInterrupt:
		print("Abort.")
		sys.exit(1)

	try:
		mailer = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
		mailer.ehlo()
		mailer.starttls()
		mailer.ehlo()
		mailer.login(SMTP_USERNAME, password)
		mailer.send_message(msg)
		mailer.close()

		with open("sent.log", "a") as myfile:
			myfile.write("***\n")
			myfile.write("Date: %s\n" % datetime.now().ctime())
			myfile.write(str(msg))
	except Exception as e:
		print(getattr(e, 'message', repr(e)))
