# TwitOff
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fun web application for comparing and predicting Tweets. Using logistic regression as 
a model and NES.css as a template.

## Installation

### From source
```bash
# make a local copy of directoy
git clone https://github.com/andronikmk/TwitOff.git

# cd into correct directoy
cd TwitOff

# create enviornment
pipenv install

# activate enviornment
pipenv shell

# deploy
gunicorn twitoff:APP -t 120
```

## Interactive U.I. made with NES-style CSS Framework.

<p align="center">
  <h4>Home Page</h4>
  <img src="https://raw.githubusercontent.com/andronikmk/TwitOff/master/img/img1.png">
</p>

<p align="center">
  <h4>Predictions Page</h4>
  <img src="https://raw.githubusercontent.com/andronikmk/TwitOff/master/img/prediction.png">
</p>