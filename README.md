
# pymta

Python toolbox for market technical analysis ( at the moment heavily relying on Yahoo Finance data )



##Interface

I've started working on different interfaces to the core libraries. 

### GUI

Module **mainw.py** provide a python-tk interface to the main functions. With this module you can:

- open/create a database
- load EoD data from Yahoo Finance
- plot EoD data


### Console

**console.py** module provide some basic functionality to interact with

- open/create a database
- load EoD data from Yahoo Finance


### Web (Flask)

This module provide a simple interface to visualize EoD data using [techan.js](http://techanjs.org/) library.
  
Refer to the README.md inside the folder for setup instructions

### Web (Django)

This is nothing more than a stub. You better ignore it.
