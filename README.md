# Football Table Calendar

Football Table Calendar is a desktop application developed using the PyQt5 framework and the football-data.org API. It allows the user to select a date from a calendar, and will display the
Premier League table based on only data from (and including) that date until the present. For example,
if January 1st were selected, the table would be displayed as if only matches from January 1st to the present count towards table rankings out of all matches played in the league so far.

The main use of this application is to allow followers of the Premier League to analyse the relative
performance of each team based on different timeframes. Displaying the league table restricted to 
a specific timeframe is a common technique used in football analysis in the media to compare a team's 
recent form to their overall standing in the competition.

## Instructions for use

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

After downloading this repository, please make sure that Python 3 is installed on your device. The latest version can be downloaded from https://www.python.org/downloads/.

First, cd into the Football Table Calendar folder in your device's terminal. 

Next, PyQt5 must be installed. This can be achieved through the command: 

```
pip install pyqt5
```

### Running the application

After PyQt5 is installed, to run the Football Table Calendar application type the command: 

```
python -i table.py
```

The application window should now open on your device.

## Built With

* [PyQt5](https://doc.qt.io/qtforpython/) - Framework used
* [football-data.org](https://www.football-data.org/) - API used

## Authors

* **Mark Winch**
