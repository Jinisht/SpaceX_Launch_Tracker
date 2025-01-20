# SpaceX-Launch-Tracker

## About
This repository contains a Python application that tracks and analyzes SpaceX launches using their public API. The application should help users understand launch history, track statistics, and monitor mission details.
 
## Operating system
Windows 10

## Python 
Python 3.10.16

## PIP Packages             
* requests 2.32.3
* pandas 2.2.3
* openpyxl 3.1.5

## Installation
* Create virtual environment.
* Clone the GitHub repo
* Install setup.py- 
      pip install -e <path of  setup.py file
 

## Details about the application
* This application shows SpaceX launch key details, launch tracking with specified inputs, statistics generation.
* The files in the application are main.py and module_features.py
* The main script is main.py
* The input details such as date range, rocket name, success = True/false, and launch site should be given in the main.py
* Fetched data from API is stored in JSON file as "spaceX_cache.json".
* The output result data are exported to Excel file in different sheets as "SpaceX_launch_data.xlsx".
* Unittest files are added.