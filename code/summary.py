import pandas as pd
import numpy as np
from metadPy.sdt import rates, dprime, criterion
from metadPy.utils import trials2counts, discreteRatings
from systole.detection import rr_artefacts
import os

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
datapath = "C:/Users/au646069/ECG/1_VPN_aux/"
subjects = os.listdir(datapath)


def groupLevel(datapath, subjects, verbose=True):
    """Extract summary statistics"""

    ####################
    # Summary statistics
    ####################
    group_df = pd.DataFrame([])  # Group level summary
    for session in ["Del1", "Del2"]:
        sess = "_del2" if session == "Del2" else ""
        for sub in subjects:

            # Heart Rate Discrimination
            try:
                df = pd.read_csv(f"{datapath}{sub}/HRD{sess}/HRD{sess}_final.txt")
                taskDuration = (
                    df["StartListening"].iloc[-1] - df["StartListening"].iloc[0]
                ) / 60

                if "StartListening" in df.columns:
                    df = df.drop("StartListening", axis=1)

                resp = "Estimation" if session == "Del1" else "Decision"

                for modality in ["Intero", "Extero"]:
                    if session == "Del1":
                        this_df = df[df.Modality == modality]
                    else:
                        this_df = df[
                            (df.Modality == modality) & (df.TrialType == "psi")
                        ]

                    threshold, slope = (
                        this_df.EstimatedThreshold.iloc[-1],
                        this_df.EstimatedSlope.iloc[-1],
                    )
                    estimationRT, confidenceRT = (
                        this_df[f"{resp}RT"].median(),
                        this_df.ConfidenceRT.median(),
                    )
                    accuracy, confidence = (
                        this_df["ResponseCorrect"].mean() * 100,
                        this_df["Confidence"].mean(),
                    )

                    # SDT
                    this_df.loc[:, "stimuli"] = this_df.responseBPM > this_df.listenBPM
                    this_df.loc[:, "responses"] = this_df[resp] == "More"
                    d, c = this_df.dprime(), this_df.criterion()

                    group_df = group_df.append(
                        {
                            "Subject": sub,
                            "Session": session,
                            "Modality": modality,
                            "Accuracy": accuracy,
                            "Confidence": confidence,
                            "Threshold": threshold,
                            "Slope": slope,
                            "TaskDuration": taskDuration,
                            "DecisionRT": estimationRT,
                            "ConfidenceRT": confidenceRT,
                            "dPrime": d,
                            "Criterion": c,
                        },
                        ignore_index=True,
                    )
            except:
                if verbose:
                    print(f"Subject: {sub} not found")

    ##################
    # Concatenate data
    ##################
    merged_df = pd.DataFrame([])  # Concatenated raw data
    for sub in subjects:
        for session in ["Del1", "Del2"]:
            sess = "_del2" if session == "Del2" else ""
            # Heart Rate Discrimination
            try:
                df = pd.read_csv(f"{datapath}{sub}/HRD{sess}/HRD{sess}_final.txt")
                if "StartListening" in df.columns:
                    df = df.drop("StartListening", axis=1)
                df["Subject"] = sub
                df["Session"] = session
                merged_df = merged_df.append(df, ignore_index=True)
            except:
                if verbose:
                    print(f"Error with subject: {sub}")

    return group_df, merged_df
