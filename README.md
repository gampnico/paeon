# Paeon

A rudimentary framework for analysing COVID data for Austria.

This aims to provide a more interactive approach than the [AGES Dashboard]("https://covid19-dashboard.ages.at/"), by allowing the user to compare regional trends and selected time periods, rather than just a national snapshot.

## Usage

The attached jupyter notebook contains examples of how to use in-built functions.

To download and update AGES data, use the `verify_update()` function in `core/data_download.py`. This function will only download data if an update is available.

## Non-standard Dependencies

* pandas
* numpy
* matplotlib
