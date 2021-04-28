#!/usr/bin/env python3
"""Nicolas Gampierakis (2020). Data processing backend.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["figure.figsize"] = (16, 5)
import sys

sys.path.append("../core/")
import data_download as dd
import data_plot as dp
import data_parser as parse
import math

# Line of best fit
def line_of_best_fit(df, y_values, poly_degree=1):
    """Creates data matrix for a line of best fit.
    
    Author:
        Nicolas Gampierakis

    Args:
        df (pandas.DataFrame): ECDC formatted dataset, parsed using
            ``data_parser.vaccine_region()``.
        y_values (pandas.core.series.Series): univariate time series
            of interest.
        poly_degree (int): degree of fitted polynomial.

    Return:
        y_hat (numpy.ndarray): array of polynomial coefficients.
    """

    x_values = np.linspace(0, 1, len(y_values))
    coeffs = np.polyfit(x_values, y_values, poly_degree)
    poly_eqn = np.poly1d(coeffs)
    y_hat = poly_eqn(x_values)

    return y_hat


def vaccine_uptake(df, region="LU", age=25):
    """Given a specified age, roughly estimates the number of people ahead
    in the vaccine queue. Assumes population is evenly distributed within
    age brackets, and that all vulnerable people in lower age groups have
    already been vaccinated, so is not representative of earlier stages of
    the vaccine rollout. Not all ECDC regions are supported by this function.
    
    Author:
        Nicolas Gampierakis
    
    Args:
        df (pandas.core.frame.DataFrame): ECDC formatted dataset,
            parsed using ``data_parser.vaccine_region()``.
        region (str): EU/EEA country code.
        age (int): age of interest.

    Returns:
        tuple (tuple):{
            vaccinated_dict (dict): number of vaccinated per age
                bracket.
            unvaccinated_dict (dict): number of unvaccinated per age
                bracket.
            num_in_queue (int): given age, estimated number of people
                in vaccine queue.
            x_values (numpy.ndarray): evenly spaced normalised vector
                of same length as time series.
            y_hat_dict (dict): contains tuples of ``numpy.ndarray``
                returned by ``numpy.polyfit()``.
            coeffs_dict (dict): coefficients used for a line of best
                fit.
        }
    """

    include_list = [
        "FirstDose",
        "FirstDoseRefused",
        "SecondDose",
        "UnknownDose",
        "NumberDosesReceived",
    ]

    exclude_list = []
    # overwriting is easier to deal with when using exclude_list later
    if age <= 24:
        age_group = "Age18_24"
        age_range_min = [6, 18]
    if age > 24:
        age_group = "Age25_49"
        age_range_min = [24, 25]
        exclude_list.append("Age18_24")
    if age > 49:
        age_group = "Age50_59"
        age_range_min = [9, 50]
        exclude_list.append("Age25_49")
    if age > 59:
        age_group = "Age60_69"
        age_range_min = [9, 60]
        exclude_list.append("Age50_59")
    if age > 69:
        age_group = "Age70_79"
        age_range_min = [9, 70]
        exclude_list.append("Age60_69")
    if age > 79:
        age_group = "Age80+"
        age_range_min = [15, 80]
        exclude_list.append("Age70_79")

    df_region = df.loc[(df["Region"] == region)]
    denom_dict = (
        df_region.groupby("TargetGroup")["Denominator"].apply(set).map(list).to_dict()
    )

    vaccinated_dict = {}
    coeffs_dict = {}
    y_hat_dict = {}

    for key in denom_dict.keys():
        df_region_key = df[(df["Region"] == region) & (df["TargetGroup"] == key)]
        df_region_key_sum = (
            df_region_key.loc[:, df_region_key.columns.isin(include_list)]
            .resample("W")
            .sum()
        )
        df_region_key_sum = pd.DataFrame.join(
            df_region_key_sum,
            (
                df_region_key.loc[:, ~df_region_key.columns.isin(include_list)]
                .resample("W")
                .last()
            ),
        )
        df_region_key_sum["FirstCumSum"] = df_region_key_sum["FirstDose"].cumsum()
        df_region_key_sum["SecondCumSum"] = df_region_key_sum["SecondDose"].cumsum()
        vaccinated_dict[key] = [
            (df_region_key_sum["FirstCumSum"]),
            (df_region_key_sum["SecondCumSum"]),
            len(df_region_key_sum["FirstCumSum"]),
        ]

        # Generate fitting data
        x_values = np.linspace(0, 1, len(df_region_key_sum["FirstDose"]))
        poly_degree = 1

        coeffs_list = []
        y_hat_list = []

        for frame in [df_region_key_sum["FirstDose"], df_region_key_sum["SecondDose"]]:
            coeffs = np.polyfit(x_values, frame, poly_degree)
            poly_eqn = np.poly1d(coeffs)
            y_hat = poly_eqn(x_values)

            coeffs_list.append(coeffs)
            coeffs_dict[key] = coeffs_list
            y_hat_list.append(y_hat)
            y_hat_dict[key] = y_hat_list

    # Number of unvaccinated people in selected age bracket, divided
    # evenly into age groups (inaccurate demographics)
    unvaccinated_dict = {}
    for key in vaccinated_dict.keys():
        unvaccinated_dict[key] = denom_dict[key][0] - vaccinated_dict[key][1]

    # average unvaccinated people per age per bracket
    unvaccinated_current_age = math.floor(
        unvaccinated_dict[age_group][-1] / age_range_min[0]
    )

    # discount everyone who has received a first dose
    num_in_queue = denom_dict["ALL"][0] - (vaccinated_dict["ALL"][1])
    # discount everyone in age bracket who is unvaccinated and younger
    num_in_queue -= unvaccinated_current_age * (age - age_range_min[1])
    # discount everyone else who is unvaccinated and younger
    for group in exclude_list:
        num_in_queue -= unvaccinated_dict[group]

    return (
        vaccinated_dict,
        unvaccinated_dict,
        int(num_in_queue[-1]),
        x_values,
        y_hat_dict,
        coeffs_dict,
    )


# x_values, y_hats, coeffs, vaccinated, unvaccinated, numq = number_in_queue(df, "LU", 57)
def time_to_vaccination(vaccine_array, num_weeks=2):
    """Very roughly estimates days to first dose vaccination based on
    the vaccination rate of the last specified number of weeks, and the
    estimated number of people ahead in vaccine queue. Assumes all
    vulnerable population has already been vaccinated, vaccines are
    distributed by decreasing age, and that vaccine distribution remains
    constant into the future. Does not account for drops in distribution.
    
    Author:
        Nicolas Gampierakis
    
    Args:
        vaccine_array (tuple): datasets returned by ``vaccine_uptake()``.
        num_weeks (int): number of previous weeks considered for
            vaccination rate.

    Returns:
        tuple (tuple):{
            latest_vaccination_rate (float): vaccinations per day.
            days_left (float): estimated days left before first dose
                available.
        }
    """
    if num_weeks >= vaccine_array[0]["ALL"][2]:
        num_weeks = vaccine_array[0]["ALL"][2] - 1
        print("Number of weeks is capped at %.0f weeks." % (vaccine_array[0]["ALL"][2]))
    # Linear gradient from previous two weeks vaccination numbers (first dose).
    latest_vaccination_rate = (
        (vaccine_array[0]["ALL"][0][-1] - vaccine_array[0]["ALL"][0][-(num_weeks + 1)])
        / num_weeks
    ) / 7
    days_left = vaccine_array[2] / latest_vaccination_rate

    print(
        "At the current rate of %.0f vaccinations per day, \nthere are possibly %.0f days left before an available vaccination."
        % (latest_vaccination_rate, days_left)
    )
    return latest_vaccination_rate, days_left
