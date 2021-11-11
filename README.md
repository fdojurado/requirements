# Requirements Processor

This is a collection of scripts that process requirements, send reminder emails, and generate automatic progress reports. The processor is able to read, filter, classify and plot requirements by various fields. It is also able to generate progress reports in `pdf` format, and generate and send automatic reminder emails.

The scripts have only been tested on macOS but should work with any major operating system.

## Requirements

The scripts assume Python 3 and have been tested in Python 3.9.1.

The automatic report generation requires a Latex installation with [Latexmk](https://mg.readthedocs.io/latexmk.html).

## Structure

* `reqlib/req.py` requirement processor library
* `reqlib/contact.py` contact list processor library
* `reqlib/spam.py` reminder email processor library
* `myconfig.py` configuration file
* `*.py` various usage examples

## Usage

### Download the data

The first step to use the library is to download from Sharepoint [the list of requirements](https://risecloud.sharepoint.com/sites/85db9cd852424a279ac607e87f0fb0a6/Lists/Requirements%20list/AllItems.aspx) in CSV format: `'Requirements.csv'`. Make sure that all fields are visible before you extract the requirements.

To use the email functionality, you shall also download [the contact list](https://risecloud.sharepoint.com/:x:/r/sites/85db9cd852424a279ac607e87f0fb0a6/_layouts/15/Doc.aspx?sourcedoc=%7B4A4C0C40-C35E-4E4D-8329-910EF888BEC7%7D&file=DAIS%20contacts%20and%20email%20lists%202021-11-04.xlsx&action=default&mobileredirect=true): `'DAIS contacts and email lists YYYY-MM-DD.xlsx'`. To address the challenge that organisations use different variants of their name in various places, you shall also download [the alternative names list](https://risecloud.sharepoint.com/:x:/r/sites/85db9cd852424a279ac607e87f0fb0a6/_layouts/15/Doc.aspx?sourcedoc=%7B7CC67EAC-D7C4-49C3-A8E7-19E56B19F058%7D&file=dais-altnames.xlsx&action=default&mobileredirect=true): `dais-altnames.xlsx`.

All these files get updated regularly, so make sure you download a fresh version. Indeed, the email engine does not permit sending reminder emails with outdated data.

### Update the config file

The next step is to update the configuration file: `myconfig.py`. Comments in the file explain the purpose of each field when not self-explanatory.

### Reading, Filtering and Plotting Requirements

All relevant functions are in `reqlib/req.py`.

First, you can read all the requirements using the `readall()` function.

Functions `filterby()` and `filterstartswith()` filter requirements that have a single value, whilst functions `filterbylist()` and `filterstartswithlist()` filter requirements that have multiple values. Functions `interesection()`, `union()` and `xor()` can be then used to manipulate sets of requirements.

Functions `printfield()`, `countby()` and `countbylist()` print fields and classify the requirements respectively. Function `plot_counter()` plots the output of `countby()` in a bar chart.

See `dais.py`, `sc2.py`, `no-poc.py` and `inconsistencies.py` in root directory for various usage examples.

### Progress Reports

Function `generate_report()` in `reqlib/req.py` automatically generates progress reports in `pdf` format ordered by deadline and with progress bars for each individual requirement. It also marks unfinished requirements with a yellow, orange and red alert when the implementation deadline approaches.

See `progress.py` in root directory for an example.

### Get contact emails

All relevant functions are in `reqlib/req.py`.

To get the emails of a specific organisation, you first need to load the contacts list and alternative names list using the `loaddata()` function. The function has as optional argument the sheet of the spreadsheet, which unless specified otherwise, defaults to `2` that is the relevant sheet in the contacts file.

You can get the alternative names of a specific organisation using the `getaltname()` function.

You can get all the emails of the organisation using the `getemails()` function. The function has an optional argument for filtering by a specific WP or SC.

See `partner-emails.py` in root directory for an example.

### Generate reminder emails

You can extract emails from a list of requirements by using the `find_emails()` function in `reqlib/req.py`.

Unfortunately, some emails have typos. The function `fixemails()` in `reqlib/contact.py` can fix most of those typos by looking for the closes match in the contacts file.

You can then send a reminder email to those recipients by specifying the subject and body of the email.

In turn, you can configure the email engine using the function `smtpconf()` and send the email by using the function `email()` in `reqlib/spam.py`.

The `email()` function will abort if the requirements are not fresh. Otherwise, it will prompt for your email account's password and, upon a successful authentication will send the email. The function also previews the email before sending it. To preview an email without sending it, simply `ctrl+c` at the password prompt.

All sent emails are also forwarded to the sender and saved in a local log file: `sent.log`.

See `email-proposed.py` and `email-no-demo.py` in root directory for various usage examples.

## Contributions

Contributions are welcome.
