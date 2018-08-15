# Content Migration For Syncplicity

This program will walk through a local file tree and replicate it to Syncplicity. Note: empty folders are not replicated.

It can create a new syncpoint (top level folder) in Syncplicity
and store the file tree under that syncpoint
or create the exact same tree with current top lever folder as the syncpoint.

## System Requirements

Supported OSs: Windows (tested on Windows10), Linux (tested on Ubuntu)

Requirements: Python3, requests module, requests-toolbelt module.

## Getting started

### Installation guide

In order to install modules with Python, you must have PIP (Python's modules installer).
PIP usually comes with Python.
In case you do not have PIP installed, use the link below, it includes instructions for all different OSs:

<https://www.makeuseof.com/tag/install-pip-for-python/>

Once PIP is installed, open a CLI (cmd or shell) and issue the following commands:

    pip install requests
    pip install requests-toolbelt

### First run

Before using the program, please enter your credentials in `Services\ConfigurationFile`:

* App Key
* App Secret
* Application Token

In case you do not have the credentials and would like to learn how to obtain these,
please go to <https://developer.syncplicity.com/overview>.

## Usage

    Main.py [-h] -s SYNCPOINT -f FOLDER [--as-user AS_USER] [--create-syncpoint]

Note: `--create-syncpoint` flag is required in order to allow syncpoint creation.
Without the flag, the program stops if no syncpoint with the specified name exists.

### Content Migration API Options

Arguments:

    -h, --help - show this help message and exit

    -s SYNCPOINT, --syncpoint SYNCPOINT - enter syncpoint name

    -f FOLDER, --folder FOLDER - enter path to the local folder to be migrated to Syncplicity

    --as-user AS_USER - enter user email in order to commit in name of a certain user

    --create-syncpoint - create syncpoint using the entered syncpoint name and upload content of chosen folder under created syncpoint

    --just-content - migrate only the content under the specified top level folder (in folder flag)

### Examples

    ./Main.py -s "Test Syncpoint" -f C:\Test\TestFolder
    ./Main.py -s "Test Syncpoint" -f C:\Test\TestFolder --as-user user@email.com
    ./Main.py -s "Test Syncpoint" -f "C:\Test\Test Folder" --create-syncpoint
    ./Main.py -s TestSyncpoint -f C:\Test\TestFolder --create-syncpoint --as-user user@email.com

### Caveats

* HTTP 500 is treated as success due to a bug. This is a workaround and should not be used in production.
* If 2 Syncpoints exist with the same name, one will randomly be chosen.

### Fiddler Usage Instructions

  1. Obtain Fiddler Root Certificate the following way: Tools -> Options -> HTTPS -> Actions -> Export Root Certificate to Desktop.
  2. Verify Fiddler port the following way: Tools -> Options -> Connections -> Fiddler listens on port: PORT. This port is for both HTTP & HTTPS.
  3. In AuthenticationClass.py & API_Caller.py, uncomment the commented requests lines (and comment out the uncommented ones).
     Replace PORT with the port number & replace PATH\TO\CERTIFICATE with the full path to the root certificate.

## Team

![alt text][Axwaylogo] Axway Syncplicity Team

[Axwaylogo]: https://github.com/Axway-syncplicity/Assets/raw/master/AxwayLogoSmall.png "Axway logo"

## License

Apache License 2.0