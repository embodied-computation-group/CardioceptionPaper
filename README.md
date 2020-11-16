# CardioceptionPaper
Data and code for the cardiac interoception method paper.

## Data

Data are stored in the `data` folder:

* `behavior.txt`: summary statisics for group level analysis.

* `merged.txt`: stacked dataframes for trial level analysis.

* `metacognition.txt`: processes metacognition results.

## Code

Scripts and jupyter notebooks are tored in the `code` folder.

### Notebooks

* `1 - Importing Files.ipynb` contains basic files import and summary.

* `2 - Psychophysics.ipynb` description of the psychometric functions.

* `3 - Metacognition.ipynb` analysis of the type 2 task results.

* `4 - HBC.ipynb` Analysis of the Heart Beats Counting task and relation with the Heart Rate Discrimination taks.

* `Hierarchicl Psychophysics.ipynb` for post hoc psychophysics curve fitting and comparison with Psi estimates.

### Scripts

* `importFiles.py` import relevant files from AUX and build a local database.

* `reports.py` generate HTML reports..

* `summary.py` will will extract summary dataframe from local raw data and create the group level summary dataframe (`Behavior.txt`), the merged dataframe (`Merged.txt`) that can be used for trial level analysis and the metacogintion dataframe (`metacognition.txt`).