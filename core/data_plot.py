#!/usr/bin/env python3
"""Nicolas Gampierakis (2020). Plots downloaded data.
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def plot_seven_day_incidence(
    data_dict,
    time_interval=0,
    austria="yes",
    tirol="yes",
    innsbruck_land="yes",
    innsbruck_city="yes",
    vienna="no",
):
    """Plots 7-day incidence rates per 100,000 people.

    Args:
        data_dict (dict): collated parsed datasets from
            data_parser.setup_datasets()
        time_interval (int): the index from which to start plotting data
        austria (str): choose whether to plot data for Austria
    """

    if austria == "yes":
        plt.plot(
            data_dict["austria"]["SiebenTageInzidenzFaelle"][time_interval:-1],
            label="Austria",
            color="gray",
            linestyle="dashed",
            linewidth=2.5,
        )
    if tirol == "yes":
        plt.plot(
            data_dict["tirol"]["SiebenTageInzidenzFaelle"][time_interval:-1],
            label="Tyrol",
            color="brown",
            linewidth=2,
        )
    if vienna == "yes":

        plt.plot(
            data_dict["wien"]["SiebenTageInzidenzFaelle"][time_interval:-1],
            label="Vienna",
            color="blue",
            linewidth=2,
        )
    if innsbruck_land == "yes":

        plt.plot(
            data_dict["innsbruck_land"]["SiebenTageInzidenzFaelle"][time_interval:-1],
            label="Innsbruck-Land",
            color="black",
            linewidth=2,
        )
    if innsbruck_city == "yes":
        plt.plot(
            data_dict["innsbruck_city"]["SiebenTageInzidenzFaelle"][time_interval:-1],
            label="Innsbruck-Stadt",
            color="red",
            linewidth=2,
        )
    plt.title("7-Day Incidence Rate (per 100,000)")
    plt.legend()
    plt.show()


def plot_icu_incidence(data_dict, time_interval=0):
    """Plots ICU incidence rate per 100,000 people.

    Args:
        data_dict (dict): collated parsed datasets from
            data_parser.setup_datasets()
        time_interval (int): the index from which to start plotting data
    """

    plt.plot(
        data_dict["casualties_austria"]["FZICU"][time_interval:-1]
        / data_dict["austria"]["AnzEinwohner"][time_interval:-1]
        * 100000,
        label="Austria",
        color="gray",
        linestyle="dashed",
        linewidth=2.5,
    )
    plt.plot(
        data_dict["casualties_tirol"]["FZICU"][time_interval:-1]
        / data_dict["tirol"]["AnzEinwohner"][time_interval:-1]
        * 100000,
        label="Tyrol",
        color="red",
        linewidth=2,
    )

    plt.plot(
        data_dict["casualties"][data_dict["casualties"]["Bundesland"] == "Wien"][
            "FZICU"
        ][time_interval:-1]
        / data_dict["all_states"][data_dict["all_states"]["Bundesland"] == "Wien"][
            "AnzEinwohner"
        ][-1]
        * 100000,
        label="Vienna",
        color="blue",
        linewidth=2,
    )
    plt.title("COVID-19 ICU Incidence Rate (per 100,000)")
    plt.legend()
    plt.show()


def plot_icu_percentages(data_dict, time_interval=0):
    """Plots the percentage of ICU beds that are allocated to COVID patients.

    Args:
        data_dict (dict): collated parsed datasets from
            data_parser.setup_datasets()
        time_interval (int): the index from which to start plotting data
    """

    plt.plot(
        data_dict["casualties_austria"]["PercentICUOcc"][time_interval:-1],
        label="Austria",
        color="gray",
        linestyle="dashed",
        linewidth=2.5,
    )

    plt.plot(
        data_dict["casualties_tirol"]["PercentICUOcc"][time_interval:-1],
        label="Tyrol",
        color="red",
        linewidth=2,
    )

    plt.plot(
        data_dict["casualties"][data_dict["casualties"]["Bundesland"] == "Wien"][
            "PercentICUOcc"
        ][time_interval:-1],
        label="Vienna",
        color="blue",
        linewidth=2,
    )
    plt.title("Percentage of Total Active ICU Stations Allocated to COVID-19 Patients")
    plt.legend()
    plt.show()
