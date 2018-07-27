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
into another script by calling .run(). The command line arguments are as follows:

> *input* - Filename (including extension, .csv, .xls, .xlsx) that contains addresses. This file should be stored in a ./data/
folder.

> *column* - Name of column that contains addresses. If also using --*columns* specify this as ADDRESS.

> *--columns* - An optional parameter to specify a .txt file containing a list (comma delimited) of columns to merge into
one ADDRESS column.

An example run is:

```python geocode.py libraries.xls geo_libraries.csv ADDRESS --columns libraries_unify.txt```


## mapping.py
mapping.py is a utility script that takes a geocoded dataset and produces an interactive, HTML map of the locations of each
entity in the dataset. Like geocode.py, the script has been designed to run from the command line but can be run via .run(). The command line arguments
are as follows:

> *input* - Filename (not including extension, must be csv) that has coordinates.

> *--name* - An optional parameter to specify column name of address if want to include as a popup.

The script will look for columns called "LAT" and "LON" for coordinates, these are the defaults provided by geocode.py.

An example run is:

```python mapping.py geo_libraries.csv libraries_map --name ADDRESS```


## boundarycode.py
boundarycode.py is a utility script that takes a geocoded dataset and a boundary file and merges them together, assigning
a boundary to each datapoint in the geocoded set. In addition there is the option to produce a map image showing what boundaries
contain a datapoint and those that don't. Like geocode.py, the script has been designed to run from the command line but
can be run via .run(). The command line arguments are as follows:

> *data_input* - Filename (not including extension) that contains coordinates.

> *boundary_input* - Filename (not including extension) of Shapefile

> *--map_output* - Flag (Y/N) to specify whether to write debugging maps


## pipeline.py
pipeline.py is script designed to tie all the main stages of the geo-harmonising process together to make running on multiple
datasets easier. The file provides a dictionary whereh multiple datasets and their parameters can be configured before being
run via the command line with no arguments.