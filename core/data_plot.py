#!/usr/bin/env python3
"""Nicolas Gampierakis (2020). Plots downloaded data.
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import string


def district_seven_day_incidence(
    dataframe,
    district_name,
    time_start=0,
    time_end=-1,
    line_color=None,
    background="no",
):
    """Plots 7-day incidence rates per 100,000 people for Austrian districts.

    Args:
        dataframe (dict): collated parsed datasets from
            data_parser.setup_datasets().
        district_name (str or int): the district name or first three
            digits of its GKZ number. The name must be correctly spelt 
            and capitalised.
        time_start (int): the index from which to start plotting data.
        time_end (int): the index from which to end plotting data.
        line_color (str): overrides default line colours chosen by
            matplotlib.
        background (str): set to "yes" if passing national data.
    """
    if background == "yes":
        plt.plot(
            dataframe["austria"]["SiebenTageInzidenzFaelle"][time_start:time_end],
            label="Austria",
            color="gray",
            linestyle="dashed",
            linewidth=2.5,
        )
    else:
        if type(district_name) is str:
            district_data = dataframe["all_districts"][
                dataframe["all_districts"]["Bezirk"] == district_name
            ]
        elif type(district_name) is int:
            district_data = dataframe["all_districts"][
                dataframe["all_districts"]["GKZ"] == district_name
            ]
            district_name = district_data["Bezirk"][0]

        plt.plot(
            district_data["SiebenTageInzidenzFaelle"][time_start:time_end],
            label=str(district_name),
            color=line_color,
            linewidth=2,
        )
    plt.title("Trend in 7-Day Incidence per 100,000 people")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("7-Day Incidence per 100,000")


def state_seven_day_incidence(
    data_dict,
    time_start=0,
    time_end=-1,
    state_list=["austria", "tirol", "innsbruck-stadt", "innsbruck-land"],
):
    """Plots 7-day incidence per 100,000 people for Austrian states.

    Args:
        data_dict (dict): collated parsed datasets from
            data_parser.setup_datasets().
        time_start (int): the index from which to start plotting data.
        time_end (int): the index from which to end plotting data.
        place_list (list): list of strings of state names for which to
            plot data.
    """

    whitelist = string.punctuation + string.whitespace
    for place in state_list:
        if type(place) is not int:
            for char in whitelist:
                place = place.lower().replace(char, "")

        if place in ["austria", "österreich", "oesterreich", "osterreich", 10]:
            plt.plot(
                data_dict["austria"]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Austria",
                color="gray",
                linestyle="dashed",
                linewidth=2.5,
            )

        if place in ["tirol", "tyrol", 7]:
            plt.plot(
                data_dict["tirol"]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Tyrol",
                color="brown",
                linewidth=2,
            )

        if place in [
            "innsbruckland",
        ]:
            plt.plot(
                data_dict["innsbruck_land"]["SiebenTageInzidenzFaelle"][
                    time_start:time_end
                ],
                label="Innsbruck-Land",
                color="black",
                linewidth=2,
            )

        if place in [
            "innsbruckstadt",
            "innsbruckcity",
            "innsbruck",
            "stadtinnsbruck",
        ]:
            plt.plot(
                data_dict["innsbruck_city"]["SiebenTageInzidenzFaelle"][
                    time_start:time_end
                ],
                label="Innsbruck (city)",
                color="red",
                linewidth=2,
            )
        if place in ["salzburg", 5]:
            plt.plot(
                data_dict["all_states"][
                    data_dict["all_states"]["Bundesland"] == "Salzburg"
                ]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Salzburg",
                color="green",
                linewidth=2,
            )
        if place in ["vienna", "wien", 9]:
            plt.plot(
                data_dict["wien"]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Vienna",
                color="blue",
                linewidth=2,
            )

        if place in ["burgenland", 1]:
            plt.plot(
                data_dict["all_states"][
                    data_dict["all_states"]["Bundesland"] == "Burgenland"
                ]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Burgenland",
                linewidth=2,
            )
        if place in ["kärnten", "karnten", "kaernten", "carinthia", 2]:
            plt.plot(
                data_dict["all_states"][
                    data_dict["all_states"]["Bundesland"] == "Kärnten"
                ]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Kärnten",
                linewidth=2,
            )
        if place in [
            "niederösterreich",
            "niederosterreich",
            "niederoesterreich",
            "loweraustria",
            3,
        ]:
            plt.plot(
                data_dict["all_states"][
                    data_dict["all_states"]["Bundesland"] == "Niederösterreich"
                ]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Lower Austria",
                linewidth=2,
            )
        if place in [
            "oberrösterreich",
            "oberosterreich",
            "oberoesterreich",
            "upperaustria",
            4,
        ]:
            plt.plot(
                data_dict["all_states"][
                    data_dict["all_states"]["Bundesland"] == "Oberösterreich"
                ]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Upper Austria",
                linewidth=2,
            )
        if place in ["steiermark", "styria", 6]:
            plt.plot(
                data_dict["all_states"][
                    data_dict["all_states"]["Bundesland"] == "Steiermark"
                ]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Styria",
                linewidth=2,
            )
        if place in ["vorarlberg", 8]:
            plt.plot(
                data_dict["all_states"][
                    data_dict["all_states"]["Bundesland"] == "Vorarlberg"
                ]["SiebenTageInzidenzFaelle"][time_start:time_end],
                label="Vorarlberg",
                linewidth=2,
            )

        else:
            pass

    plt.title("Trend in 7-Day Incidence (per 100,000)")
    plt.xlabel("Date")
    plt.ylabel("7-Day Incidence per 100,000")
    plt.legend()


def plot_icu_incidence(data_dict, time_start=0, time_end=-1):
    """Plots ICU incidence per 100,000 people.

    Args:
        data_dict (dict): collated parsed datasets from
            data_parser.setup_datasets().
        time_start (int): the index from which to start plotting data.
        time_end (int): the index from which to end plotting data.
    """

    plt.plot(
        data_dict["casualties_austria"]["FZICU"][time_start:time_end]
        / data_dict["austria"]["AnzEinwohner"][time_start:time_end]
        * 100000,
        label="Austria",
        color="gray",
        linestyle="dashed",
        linewidth=2.5,
    )
    plt.plot(
        data_dict["casualties_tirol"]["FZICU"][time_start:time_end]
        / data_dict["tirol"]["AnzEinwohner"][time_start:time_end]
        * 100000,
        label="Tyrol",
        color="red",
        linewidth=2,
    )

    plt.plot(
        data_dict["casualties"][data_dict["casualties"]["Bundesland"] == "Wien"][
            "FZICU"
        ][time_start:time_end]
        / data_dict["all_states"][data_dict["all_states"]["Bundesland"] == "Wien"][
            "AnzEinwohner"
        ][-1]
        * 100000,
        label="Vienna",
        color="blue",
        linewidth=2,
    )
    plt.title("Trend in COVID-19 ICU Incidence Rate (per 100,000)")
    plt.xlabel("Date")
    plt.ylabel("Incidence per 100,000")
    plt.legend()
    plt.show()


def plot_icu_percentages(data_dict, time_start=0, time_end=-1):
    """Plots the percentage of ICU beds that are allocated to COVID patients.

    Args:
        data_dict (dict): collated parsed datasets from
            data_parser.setup_datasets().
        time_start (int): the index from which to start plotting data.
        time_end (int): the index from which to end plotting data.

    """

    plt.plot(
        data_dict["casualties_austria"]["PercentICUOcc"][time_start:time_end],
        label="Austria",
        color="gray",
        linestyle="dashed",
        linewidth=2.5,
    )

    plt.plot(
        data_dict["casualties_tirol"]["PercentICUOcc"][time_start:time_end],
        label="Tyrol",
        color="red",
        linewidth=2,
    )

    plt.plot(
        data_dict["casualties"][data_dict["casualties"]["Bundesland"] == "Wien"][
            "PercentICUOcc"
        ][time_start:time_end],
        label="Vienna",
        color="blue",
        linewidth=2,
    )
    plt.title("Percentage of Occupied ICU Stations Allocated to COVID-19 Patients")
    plt.xlabel("Date")
    plt.ylabel("Percent [%]")
    plt.legend()
    plt.show()
