import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def raincloud(
    data,
    x,
    y,
    palette=["#4c72b0", "#c44e52"],
    levels=None,
    ax=None,
    alpha=0.6,
    show_outliers=True,
    stripplot={},
    lines={},
    boxplot={},
    violin={},
):
    """Repeated measure raincloud plot."""
    if levels is None:
        level1 = data[x].unique()[0]
        level2 = data[x].unique()[1]
    else:
        level1, level2 = levels

    df = pd.DataFrame(
        {
            level1: data[y][data[x] == level1].to_numpy(),
            level2: data[y][data[x] == level2].to_numpy(),
        }
    )

    if ax is None:
        fig, ax = plt.subplots()

    ###########
    # Stripplot
    ###########
    jitter = 0.02
    df_x_jitter = pd.DataFrame(
        np.random.normal(loc=0, scale=jitter, size=df.values.shape), columns=df.columns
    )
    df_x_jitter += np.array([0.25, 0.75])
    for col, c in zip(df, palette):
        ax.plot(
            df_x_jitter[col],
            df[col],
            "o",
            alpha=0.2,
            zorder=1,
            ms=6,
            mew=1,
            color=c,
            **stripplot
        )

    #######
    # Lines
    #######
    for idx in df.index:
        ax.plot(
            df_x_jitter.loc[idx, [level1, level2]],
            df.loc[idx, [level1, level2]],
            color="grey",
            linewidth=0.5,
            linestyle="-",
            zorder=-1,
            alpha=0.6,
            **lines
        )

    #########
    # Boxplot
    #########
    sns.boxplot(
        data=df,
        width=0.1,
        notch=True,
        palette=palette,
        ax=ax,
        showfliers=False,
        **boxplot
    )

    ############
    # Violinplot
    ############

    # Outliers detection
    if show_outliers is False:
        violin_vec = []
        for vec in [df[level1], df[level2]]:

            Q1 = vec.quantile(0.25)
            Q3 = vec.quantile(0.75)
            IQR = Q3 - Q1  # IQR is interquartile range.

            filter = (vec >= Q1 - 1.5 * IQR) & (vec <= Q3 + 1.5 * IQR)
            violin_vec.append(vec.loc[filter])
    else:
        violin_vec = [df[level1], df[level2]]

    vl = ax.violinplot(violin_vec, showextrema=False, widths=0.5, **violin)

    # Left plot
    paths = vl["bodies"][0].get_paths()[0]
    paths.vertices[:, 0][paths.vertices[:, 0] >= 1] = 1
    paths.vertices[:, 0] -= 1.1
    vl["bodies"][0].set_edgecolor("k")
    vl["bodies"][0].set_facecolor(palette[0])
    vl["bodies"][0].set_alpha(alpha)

    # Right plot
    paths = vl["bodies"][1].get_paths()[0]
    paths.vertices[:, 0][paths.vertices[:, 0] <= 2] = 2
    paths.vertices[:, 0] -= 0.9
    vl["bodies"][1].set_edgecolor("k")
    vl["bodies"][1].set_facecolor(palette[1])
    vl["bodies"][1].set_alpha(alpha)

    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels(df.columns)
    ax.set_xlim(-0.5, len(df.columns) - 0.5)

    return ax
