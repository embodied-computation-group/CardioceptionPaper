# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

import papermill as pm
import subprocess
import os
import multiprocessing as mp


def reportHRD(
    sub,
    datapath="C:/Users/au646069/ECG/1_VPN_aux/",
    reportPath="C:/Users/au646069/github/CardioceptionPaper/reports/",
    session="Del1",
):

    try:
        report_subpath = "HRD" if session == "Del1" else "HRD2"
        pm.execute_notebook(
            "C:/Users/au646069/github/CardioceptionPaper/code/HeartRateDiscrimination.ipynb",
            f"{reportPath}HRD/{sub}.ipynb",
            parameters=dict(subject=sub, path=datapath, session=session),
        )
        command = f"jupyter nbconvert --to html --execute --TemplateExporter.exclude_input=True {reportPath}{report_subpath}/{sub}.ipynb --output {reportPath}{report_subpath}/{sub}_report.html"
        subprocess.call(command)
        os.remove(reportPath + report_subpath + "/" + sub + ".ipynb")
    except:
        print(f"Subject {sub} not found.")


if __name__ == "__main__":
    datapath = "C:/Users/au646069/ECG/1_VPN_aux/"
    subList = os.listdir(datapath)
    pool = mp.Pool(processes=4)
    pool.map(reportHRD, subList)
