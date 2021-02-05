#!/usr/bin/env python3
"""Nicolas Gampierakis (2020). Parses downloaded data files.
"""

import pandas as pd
import numpy as np


def setup_datasets():
    """Parses downloaded AGES datasets.
    
    Returns:
        collated (dict): dictionary of parsed .csv files.
    """
    df_bundesland = pd.read_csv(
        "../data/austria/CovidFaelle_Timeline.csv",
        sep=";",
        index_col=0,
        parse_dates=[0],
        infer_datetime_format=True,
        decimal=",",
    )
    df_districts = pd.read_csv(
        "../data/austria/CovidFaelle_Timeline_GKZ.csv",
        sep=";",
        index_col=0,
        parse_dates=[0],
        infer_datetime_format=True,
        decimal=",",
    )
    df_fz = pd.read_csv(
        "../data/austria/CovidFallzahlen.csv",
        sep=";",
        index_col=0,
        parse_dates=[0],
        dayfirst=True,
        decimal=",",
    )

    # ICU and hospitalisation
    df_fz["PercentHospOcc"] = 100 * df_fz["FZHosp"].div(
        df_fz["FZHosp"] + df_fz["FZHospFree"]
    )
    df_fz["PercentICUOcc"] = 100 * df_fz["FZICU"].div(
        df_fz["FZICU"] + df_fz["FZICUFree"]
    )

    # split datasets
    df_oeste = df_bundesland[df_bundesland["BundeslandID"] == 10]
    df_tirol = df_bundesland[df_bundesland["Bundesland"] == "Tirol"]
    df_wien = df_bundesland[df_bundesland["Bundesland"] == "Wien"]
    df_innsbruck = df_districts[df_districts["Bezirk"] == "Innsbruck-Land"]
    df_innsbruck_city = df_districts[df_districts["Bezirk"] == "Innsbruck-Stadt"]
    df_fz_oeste = df_fz[df_fz["BundeslandID"] == 10]
    df_fz_tirol = df_fz[df_fz["Bundesland"] == "Tirol"]
    df_fz_tirol[df_fz_tirol.index == "2021-01-07"]

    collated = {
        "austria": df_oeste,
        "all_states": df_bundesland,
        "all_districts": df_districts,
        "casualties": df_fz,
        "tirol": df_tirol,
        "wien": df_wien,
        "innsbruck_land": df_innsbruck,
        "innsbruck_city": df_innsbruck_city,
        "casualties_austria": df_fz_oeste,
        "casualties_tirol": df_fz_tirol,
    }

    return collated

