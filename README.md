# inkamusic

## NOTE
inkamusic is currently being converted to a github open-source project. 

A first usable version will be available soon.

[![image](https://img.shields.io/pypi/v/inkamusic.svg)](https://pypi.org/project/inkamusic/)
[![image](https://img.shields.io/pypi/l/inkamusic.svg)](https://pypi.org/project/inkamusic/)
[![image](https://img.shields.io/pypi/pyversions/inkamusic.svg)](https://pypi.org/project/inkamusic/)
[![Travis](https://img.shields.io/travis/physicsware/inkamusic/master.svg?logo=travis)](https://travis-ci.org/physicsware/inkamusic)
![Read the Docs](https://img.shields.io/readthedocs/inkamusic)

## Overview
inkamusic creates instrumental music, based on rules. This includes structure, rhythm, melody, harmonization and instrumentation. A simple web interface (with CherryPy) offers the possibility to choose from several options. The output format is a MIDI file that can be played with many applications, e.g. Garageband or VLC on MacOS or Windows Media Player on Windows. Or try https://musescore.org/en, which not only plays the midi files, but also displays the score.


## Installation

You can download and install the latest version of this software from the Python package index (PyPI) as follows:

    pip install --upgrade inkamusic

## Usage

To use the stand alone version run

    inkamusic
  
 This will start a local CherryPy web server. Now open a browser window and enter
 
      http://127.0.0.1:8080
      
  Select options and use the Create button to create a MIDI file. Depending on your browser settings this file will be downloaded or opened. See Overview for additional hints.
  
  inkamusic can also be used as imported module, but this feature is in a preliminary state. More information will be added later.

## Credits

uses the CherryPy Web Framework https://cherrypy.org/
