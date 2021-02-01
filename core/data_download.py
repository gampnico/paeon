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
import pathlib


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


def extract_database(client_path):
    """Extracts database into client directory.
    
    Author:
        Nicolas Gampierakis

    Args:
        client_path (pathlib.PurePath): the directory path to the client's
        downloaded database
    """
    file_path = client_path + "data.zip"
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(client_path)
    print("\nSuccessfully unzipped and installed database.")


def download_database(server_path, client_path):
    """Downloads and extracts database into client directory.
    
    Author:
        Nicolas Gampierakis

    Args:
        client_path (pathlib.PurePath): the directory path to the client's
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

    extract_database(client_path)

    return data


def determine_timestamp(client_database, server_path):
    """Establishes connection with server and returns server and
    client database modification dates. Can be called by a verify_update()
    if an update check is initiated.

    Author:
        Nicolas Gampierakis

    Args:
       client_database (pathlib.PurePath): the file path to the client's
        database
        server_path (str): the url path to the server database

    Returns:
        client_timestamp (datetime): the last modification date of the
            client database file
        server_timestamp (datetime): the last modification date of the
            server database file
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


def verify_update():
    """Enforces python version is greater than 3.5, sets up client directory
    paths. Checks existence, version, and implementation of client database.
    Calls determine_timestamp() to read and compare the header information of
    server database and client modification date. Calls download_database()
    if a database update is requested by user.
    
    Author:
        Nicolas Gampierakis

    Raises:
        Exception: If Python version is less than 3.5.
        URLError: If errors occur in the connection to the URL path.
        socket.timeout: If the socket timeout defined in download_database()
            occurs during a connection loss.
    """

    # Check and enforce Python version is greater than 3.5
    if sys.version_info.major < 3 or sys.version_info.minor < 5:
        raise Exception(
            "Python 3.5 or greater is required to run the update " "package"
        )

    # Checks existence of and sets up client directories - pathlib is ~10x
    # slower than os.path, but more robust and elegant when dealing with
    # relative path names.
    root = os.path.dirname(os.getcwd())
    client_path = pathlib.PurePath(root).joinpath("data/austria")
    server_path = "https://covid19-dashboard.ages.at/data/data.zip"
    pathlib.Path(client_path).mkdir(exist_ok=True)
    client_zip = client_path / "data.zip"
    client_path = str(client_path) + "/"
    print("\nData provided by AGES.")
    # Checks if database exists. If not, checks if archive exists. Downloads
    # and extracts database if and where appropriate.
    while True:
        try:
            # Check for extracted database.
            if not pathlib.Path(client_zip).is_file():
                if input(
                    "AGES database is missing. Would you like to "
                    "download and extract data?\n(y/n):\n"
                ) in ["y", "Y", "Yes", "yes"]:
                    # Check for archive.
                    print(server_path)
                    print(client_zip)
                    print(client_path)
                    if not pathlib.Path(client_zip).is_file():
                        download_database(server_path, client_path)
                    else:
                        # Extract pre-existing archive.
                        print(
                            "The AGES database was already downloaded. " "Unzipping..."
                        )
                        with zipfile.ZipFile(client_zip, "r") as zip_ref:
                            zip_ref.extractall(client_path)
                        print("Successfully extracted the database.")
                    break
                else:
                    print("Operation cancelled.")
                    break
            else:
                # Application layer.
                print("AGES database already exists locally. Checking for update...")
                # For readability, relegated this to determine_timestamp().
                client_timestamp, server_timestamp = determine_timestamp(
                    client_zip, server_path
                )

                # Equality test of database modification date between server
                # and client.
                if server_timestamp.date() != client_timestamp.date():
                    print("\nDownloading...")
                    download_database(server_path, str(client_path))
                    break
                else:
                    extract_database(client_path)
                    print("The AGES database is up-to-date.")
                    break
        # Transport layer
        except socket.timeout:
            # Handles and warns against connection drop and interruptions.
            print(
                "\nSocket timeout. Please check your Internet connection "
                "and try again."
            )
            break
        except urllib.error.URLError as connection_error:
            # Handles and warns against unresolvable connection issues.
            response_url_error = (
                "\nFile not downloaded because:\n"
                + str(connection_error.reason)
                + ". Please check your connection "
                "and try again."
            )
            print(response_url_error)
        finally:
            # Clean up any temporary files. Connection:Close already included.
            urllib.request.urlcleanup()
            break
