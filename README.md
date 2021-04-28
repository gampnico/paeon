# Paeon

A rudimentary, trend-driven framework for analysing COVID-19 trends in Austria.

This aims to provide a more trend-driven approach than the [AGES Dashboard]("https://covid19-dashboard.ages.at/"), by allowing the user to compare state and district trends for selected time periods, rather than a static, national snapshot.

It also allows basic data analysis of ECDC vaccination data, and a **very** rudimentary way of estimating vaccine waiting times for a given age.

## Usage

The jupyter notebooks in the `notebooks/` folder contains in-depth instructions and examples on how to use this framework. 

To download and update AGES and ECDC data, use the `verify_update()` function in `core/data_download.py`. This function will only download data if an update is available.

## Non-standard Dependencies

* pandas
* numpy
* matplotlib
* jupyter-notebook -- but only to access the notebook.