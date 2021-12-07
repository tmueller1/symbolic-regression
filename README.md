# Symbolic Regression <!-- omit in toc -->

A symbolic regression is an algorithm for fitting analytic relationships between features $\bm{x}$ and targets $y$ based on training data. This repository contains an implementation of a symbolic regression in Python with a GUI. The implementation is based on the DEAP library, see https://deap.readthedocs.io/en/master/.

# Table of Contents <!-- omit in toc -->
- [Installation](#installation)
- [Supported Training Data Format](#supported-training-data-format)

# Installation 

To run this implementation of a symbolic regression, a Python interpreter is required. While this code was optimized for Python 3.8,  most likely other versions of Python 3 will also work. The code is reported to work on Windows and Linux. 

In addition to a Python interpreter, the packages in "requirements.txt" are needed. They can be installed automatically with the Python package-manager pip by running the command `pip install -r requirements.txt`.

# Supported Training Data Format

The training data has to be an ".xls" file with the following format:

![format of training data](./figures_for_readme/format_of_training_data.png)

The first row is a header that describes the content of each column. The first column contains the target values for every measurement, while the other columns are the corresponding features.

