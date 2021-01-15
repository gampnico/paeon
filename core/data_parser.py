#!/usr/bin/env python3
"""Nicolas Gampierakis (2020). Parses downloaded data files.
"""

import pandas as pd
import numpy as np

df_lux = pd.read_csv(
    "../data/luxembourg/datapublic-covid19.csv",
    names=[
        "Date",
        "Normal Care",
        "Intensive Care",
        "IC Without GE",
        "Cumulative Deaths",
        "Hospital Discharge",
        "Cumulative Infections",
        "People Tested",
        "Total Tests",
    ],
    skiprows=1,
)


