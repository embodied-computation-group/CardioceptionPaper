# CardioceptionPaper
Data and code for the cardiac interoception method paper.

## Data

Data are stored in the `data` folder:

* `behavior.txt`

* `merged.txt`

* `metacognition.txt`

## Code

Scripts and jupyter notebooks are tored in the `code` folder.

### Notebooks

* `GroupSummary.ipynb` contains basic goupd level summary analysis.

* `Hierarchicl Psychophysics.ipynb` for post hoc psychophysics curve fitting and comparison with Psi estimates.

### SCripts

* `importFiles.py` import relevant files from AUX and build a local database.

* `summary.py` will will extract summary dataframe from local raw data and create the group level summary dataframe (`Behavior.txt`), the merged dataframe (`Merged.txt`) that can be used for trial level analysis and the metacogintion dataframe (`metacognition.txt`).