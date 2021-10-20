# Requirements Processor

This is a collection of scripts that process requirements and generate automatic progress reports. The processor is able to read, filter, classify and plot requirements by various fields. It is also able to generate progress reports in `pdf` format.

The scripts have only been tested on macOS.

## Requirements

The scripts assume Python 3 and have been tested in Python 3.9.1.

The automatic report generation requires a Latex installation with [Latexmk](https://mg.readthedocs.io/latexmk.html).

## Structure

* `lib/req.py` requirement processor library
* `examples/` various usage examples

## Usage

The first step to use the library is to download from Sharepoint the list of requirements in CSV format: `Requirements.csv`. In turn, you can read all the requirements using the `readall()` function.

Functions `filterby()`, `filterstartswith()`, `interesection()`, `union()` and `xor()` can be then used to filter and manipulate sets of requirements.

Functions `printfield()` and `countby()` print fields and classify the requirements respectively. Function `plot_counter()` plots the output of `countby()` in a bar chart.

Finally, function `generate_report()` automatically generates progress reports in `pdf` format ordered by deadline and with progress bars for each individual requirement. It also marks unfinished requirements with a yellow, orange and red alert when the implementation deadline approaches.

See `examples/` for various usage examples.

## Contributions

Contributions are welcome.