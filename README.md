Scraper package was build using pep 660 package distribution standards.


Create a virtual environment for the project.

If pip is not installed on your system, you can install it by running the following command:

$ sudo apt-get install python-pip

Then, install virtualenv by running the command:
$ pip install virtualenv

Verify your installation by checking the version of virtualenv:
$ virtualenv --version

Create a virtual environment using the following command:

$ python3 -m venv venv

Activate the virtual environment.
On macOS, run the command:
$ . venv/bin/activate

On Windows, run the command:
$ .\venv\Scripts\activate

Build the Scraper Python package by running the command:
Oepen your terminal confirm you are in project directory
$ pip install -e .

Run the Upwork Scraper package using the following command:
$ upwork_scraper main