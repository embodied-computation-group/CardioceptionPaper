# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

import papermill as pm
import subprocess
import os
import multiprocessing as mp


def reportHBC(
    sub,
    datapath="C:/Users/au646069/github/CardioceptionPaper/data/raw/HBC/",
    reportPath="C:/Users/au646069/github/CardioceptionPaper/reports/",
):

    pm.execute_notebook(
        "C:/Users/au646069/github/CardioceptionPaper/code/HeartBeatCounting.ipynb",
        reportPath + "HBC/" + sub + ".ipynb",
        parameters=dict(subject=sub, path=datapath),
    )
    command = f"jupyter nbconvert --to html --execute --TemplateExporter.exclude_input=True {reportPath}HBC/{sub}.ipynb --output {reportPath}HBC/{sub}_report.html"
    subprocess.call(command)
    os.remove(reportPath + "HBC/" + sub + ".ipynb")


if __name__ == "__main__":
    datapath = "C:/Users/au646069/github/CardioceptionPaper/data/raw/HBC/"
    subList = os.listdir(datapath)
    pool = mp.Pool(processes=4)
    pool.map(reportHBC, subList)
    pool.close()
    pool.join()
