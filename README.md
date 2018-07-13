# geoharm utility

## Purpose
The purpose of the geoharm utility is to provide a way to preprocess, geocode, map and group multiple datasets together
for work performed on the Loneliness Metric being developed by the Office for National Statistics. This readme provides
details on how to use the associated scripts.


## unifier.py
unifier.py is a utility script that takes a list of columns present in a DataFrame and merges them into one column called
"ADDRESS". One piece of functionality to note is that any column with a missing field will be ignored in the join, allowing
for the avoidance of issues with constructing longer addresses.


## geocode.py
geocode.py is a utility script that takes a dataset that contains a series of addresses and geocodes them using the Google
Maps API. The script has been designed to be run from the command line mainly although it can be run as a module imported
into another script. The command line arguments are as follows:

> *input* - Filename (including extension, .csv, .xls, .xlsx) that contains addresses. This file should be stored in a ./data/
folder.

> *output* - Filename (including extension, .csv only) that geocodes are written to. This file can be found in the ./results/
folder.

> *column* - Name of column that contains addresses. If also using --*columns* specify this as ADDRESS.

> *--columns* - An optional parameter to specify a .txt file containing a list (comma delimited) of columns to merge into
one ADDRESS column.

An example run is:

```python geocode.py libraries.xls geo_libraries.csv ADDRESS --columns libraries_unify.txt```

Currently there is no automatic way to catch addresses that are geocoded outside the UK although this is a work in progress


## mapping.py
mapping.py is a utility script that takes a geocoded dataset and produces an interactive, HTML map of the locations of each
entity in the dataset. Like geocode.py, the script has been designed to run from the command line. The command line arguments
are as follows:

> *input* - Filename (including extension, must be csv) that has coordinates.

> *output* - Filename (not including extension) for output file.

> *--name* - An optional parameter to specify column name of address if want to include as a popup.

The script will look for columns called "LAT" and "LON" for coordinates, these are the defaults provided by geocode.py.

An example run is:

```python mapping.py geo_libraries.csv libraries_map --name ADDRESS```