#!/usr/bin/env python3
"""Nicolas Gampierakis (2020). Downloads external databases from given url.
"""

import socket
import sys
import time
import urllib.error
import urllib.request
import datetime
import os
import zipfile


def progress_bar(packet_number, packet_size, total_size):
    """Custom reporthook for displaying download progress bar. Called as a
    default keyword argument by download_database().
    Adapted from:
    https://blog.shichao.io/2012/10/04/progress_speed_indicator_for_urlretrieve_in_python.html # noqa

    Author:
        Sichao An, minor edits Nicolas Gampierakis

    Args:
        packet_number (int): number of data packets transferred from server
            to client
        packet_size (int): size of data packet
        total_size (int): total database file size reported by Content-Length
            header
    """

    # Create timer to calculate download speed

    global start_tick
    if packet_number == 0:
        start_tick = time.time()
        return
    elapsed_time = time.time() - start_tick
    # Track total downloaded data
    packet_progress = packet_number * packet_size
    # Use min() to avoid percentage overshoot
    percentage_downloaded = min(packet_number * packet_size * 100 / total_size, 100)
    bandwidth = int(packet_progress / (1024 * elapsed_time))
    # Using write instead of print to avoid automatic \n
    sys.stdout.write(
        "\rDownloading data ...%d%%, %d MB, %d KB/s"
        % (percentage_downloaded, packet_progress / (1024 * 1024), bandwidth)
    )
    # Flushes buffer to terminal to avoid lag in output
    sys.stdout.flush()


def download_database(server_path, client_path):
    """Downloads and extracts database into client directory.

    Args:
        client_path (pathlib.PurePath): the file path to the client's
        downloaded database
        server_path (str): the url path to the server database
    """

    # Timeout value recommended by NN/g before user loses attention
    if sys.version_info.major < 3 or sys.version_info.minor < 5:
        raise Exception(
            "Python 3.5 or greater is required to run the update " "package"
        )
    file_path = client_path + "data.zip"
    print(file_path)
    socket.setdefaulttimeout(10)
    data = urllib.request.urlretrieve(server_path, file_path, reporthook=progress_bar)
    print("\nDatabase successfully downloaded.")
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(client_path)
    print("\nSuccessfully unzipped and installed database.")

    return data


def determine_timestamp(client_database, server_path):
    """Establishes connection with GeoNames server and returns server and
    client database modification dates. Called by verify_update() if an update
    check is initiated.

    Author:
        Nicolas Gampierakis

    Args:
       client_database (pathlib.PurePath): the file path to the client's database
        server_path (str): the url path to the server database

    Returns
    -------
    client_timestamp : datetime
        the last modification date of the client database file
    server_timestamp : datetime
        the last modification date of the server database file
    """

    connection = urllib.request.urlopen(server_path, timeout=20)
    # Parse control information and get server database modification date
    server_timestamp = connection.headers["last-modified"].replace(",", "")
    server_timestamp = datetime.datetime.strptime(
        server_timestamp, "%a %d %b %Y %H:%M:%S %Z"
    )
    # Get client database modification date, convert to UTC in case user
    # changed time zone.
    client_timestamp = datetime.datetime.strptime(
        str(datetime.datetime.utcfromtimestamp(os.path.getmtime(client_database))),
        "%Y-%m-%d %H:%M:%S.%f",
    )
    return client_timestamp, server_timestamp


def download_pipeline(country="austria", data_path="../data/"):
    if country == "austria":
        dl_path = data_path + "austria/"
        download_database(
            server_path="https://covid19-dashboard.ages.at/data/data.zip",
            client_path=dl_path,
        )
