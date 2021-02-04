# Paeon

A rudimentary framework for analysing COVID data for Austria.

This aims to provide a more interactive approach than the [AGES Dashboard]("https://covid19-dashboard.ages.at/"), by allowing the user to compare regional trends and selected time periods, rather than just a national snapshot.

**04.02.2021: AGES appear to have updated their database format. `data_parser()` and `data_plot()` no longer work. A compatibility fix will be issued shortly.**

## Usage

The attached jupyter notebook contains examples of how to use in-built functions.

To download and update AGES data, use the `verify_update()` function in `core/data_download.py`. This function will only download data if an update is available.

## Non-standard Dependencies

* pandas
* numpy
* matplotlib
