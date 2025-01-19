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
* Install setup.py
      * pip install -e <path of  setup.py file
 

## Details about the software
* This application shows SpaceX launch key details, launch tracking with specified inputs, statistics generation.
* The main script is main.py
* Fetched data from API is stored in JSON file as "spacex_cache.json".
* The output result data are exported to Excel file in different sheets as "SpaceX_Launch_Data.xlsx".