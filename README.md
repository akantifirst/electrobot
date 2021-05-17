# Electrobot
## Description

<img align="left" width="150" height="150" src="images/logo.png">

A simple telegram bot that converts electrical power to current and vice versa.
<br>It parses user input automatically. Here are quick examples:
<br>
<br>```12kw  => 12kW 400V cos(φ)=0.95```
<br>```12a 230V 0,8  => 12A 230V cos(φ)=0.80```
<br>```280  => 280kW 400V cos(φ)=0.95```
<br>
<br>
## Installation

No need to install, just start [@nb_electrobot](https://t.me/nb_electrobot) in Telegram.

## Roadmap

in future, this bot will be able to generate electrical schemas based on user input and provide them on the fly as convenient pdf files.

Following problems need to be solved:
1. Mathematical engine for solving cable sections incl. voltage drop, type of cable, way of laying etc.
2. Database storage for user requests
3. VPN access to server
4. Generation of schemas from project database
5. Convertion of schemas to PNG and then to PDF
6. 
