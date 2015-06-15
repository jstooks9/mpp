Python scripts in this folder:
______________________________

labview_parse_3.py raw_file_name num_columns_keep
2d_histogram.py processed_file_name num_bins figure_title
mesytec_process.py
mpp.py raw_file_name num_columns_keep num_bins figure_title
mesytec_process_2.py
mpp.py_2.py raw_file_name input_file_name figure_titles

The arguments for each file are explained in the brief documentation at the top of each file.

labview_parse_3.py takes an output file from the mesytec system and returns a parsed data file. The new file has a column for each MADC output channel (1 - 32)

2d_histogram.py takes a processed file from labview_parse_3.py and creates a 2d histogram (heat map) of the data.

mesytec_process.py combines the contents of the previous 2 files. It holds all of their functionality as python procedures.

mpp.py (mesytec post-process) takes a raw input file and produces a processed file and histogram using the procedures defined in mesytec_process.py.


mesytec_process_2.py this is an updated version of mesytec_process.py. Now, the
functions within are suited to parse and plot data files which contain data
from more than 1 detector.

mpp_2.py is an updated version of mpp.py. Its arguments are a raw data file, an input file, and a title for the plots. Note that the same title will appear on each detector's plot. The filename will reflect detector identity, but the figure title should read something like "5 minute PuBe irradiation". Instructions for input files are included in the notes at the top of the mpp_2.py program file. In this directory, good_example_input.txt and bad_example_input.txt are given as examples. Note that valid delimiters are spaces, tabs, and commas.