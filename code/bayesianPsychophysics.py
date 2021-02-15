import numpy as np
import pandas as pd
import pymc3 as pm
import os
from theano import tensor as tt


def comulative_normal(x, alpha, beta, s=np.sqrt(2)):
    # Cumulative distribution function for the standard normal distribution
    return 0.5 + 0.5 * tt.erf((x - alpha) / (beta * s))


def singleSubject(this_df):

    # ---------------
    # Preprocess data
    # ---------------
    x, n, r = np.zeros(163), np.zeros(163), np.zeros(163)

    for ii, intensity in enumerate(np.arange(-40.5, 41, 0.5)):
        x[ii] = intensity
        n[ii] = sum(this_df.Alpha == intensity)
        r[ii] = sum((this_df.Alpha == intensity) & (this_df.Decision == "More"))

    nstim2 = np.shape(x)
    xmean = np.nanmean(x)
    xmeanvect = np.repeat(xmean, nstim2)

    # remove nans
    validmask = np.isnan(x.flatten()) == False
    xij2, nij2, rij2 = x.flatten(), n.flatten(), r.flatten()
    xij, nij, rij = xij2[validmask], nij2[validmask], rij2[validmask]
    xvect = xmeanvect[validmask]

    # psi estimates
    slope = this_df.EstimatedSlope.iloc[-1]
    threshold = this_df.EstimatedThreshold.iloc[-1]

    # ------------------------------
    # Cumulative normal distribution
    # ------------------------------
    with pm.Model():

        alpha = pm.Uniform("alpha", lower=-40.5, upper=40.5)
        beta = pm.Uniform("beta", lower=0, upper=40)

        thetaij = pm.Deterministic(
            "thetaij", comulative_normal(xij - xvect, alpha, beta)
        )

        rij_ = pm.Binomial("rij", p=thetaij, n=nij, observed=rij)
        trace = pm.sample(
            chains=2, cores=2, tune=2000, draws=2000, return_inferencedata=True
        )

    stats = pm.summary(trace, ["alpha", "beta"])
    bayesThreshold = stats["mean"]["alpha"]
    bayesSlope = stats["mean"]["beta"]
    r_hat_alpha = stats["r_hat"]["alpha"]
    r_hat_beta = stats["r_hat"]["beta"]

    return slope, threshold, bayesThreshold, bayesSlope, r_hat_alpha, r_hat_beta


for session in ["Del1", "Del2"]:

    merged_df = pd.read_csv(os.getcwd() + f"/{session}_merged.txt")
    merged_df = merged_df[~merged_df.Alpha.isnull()]
    merged_df = merged_df[~merged_df.Decision.isnull()]
    merged_df = merged_df[merged_df.HeartRateOutlier == 0]

    summary_df = pd.DataFrame([])
    for subject in merged_df.Subject.unique():

        for modality in ["Intero", "Extero"]:

            this_df = merged_df[
                (merged_df.Subject == subject) & (merged_df.Modality == modality)
            ]

            # Drop trials with decision time < 100 ms
            this_df = this_df[~(this_df.DecisionRT < 0.1)]

            # Remove HR outliers
            this_df = this_df[this_df.HeartRateOutlier == 0]

            (
                slope,
                threshold,
                bayesThreshold,
                bayesSlope,
                r_hat_alpha,
                r_hat_beta,
            ) = singleSubject(this_df)

            summary_df = summary_df.append(
                pd.DataFrame(
                    {
                        "Subject": subject,
                        "Modality": modality,
                        "Threshold": [threshold],
                        "Slope": [slope],
                        "BayesianThreshold": [bayesThreshold],
                        "BayesianSlope": [bayesSlope],
                        "r_hat_alpha": [r_hat_alpha],
                        "r_hat_beta": [r_hat_beta],
                    }
                ),
                ignore_index=True,
            )

    summary_df.to_csv(f"{session}_psychophysics.txt", index=False)
