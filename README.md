# Electrobot
## Description

<img align="left" width="150" height="150" src="images/logo.png">

A simple telegram bot that converts electrical power to current and vice versa.
<br>It parses user input automatically. Here are quick examples:
<br>
<br>```12kw  => 12kW 400V cos(φ)=0.95```
<br>```12kw 1% => limit dU factor to 1%```
<br>```12kw NYCWY => specify cable type.```
<br>```12a 230V 0,8  => 12A 230V cos(φ)=0.80```
<br>```UV-AV-01 12kw => 12kW, Switchboard name: UV-AV-01```
<br>```12kw e1 30m => 12kW, laying in cable channel, length 30m```
<br>
<br>
## Installation

No need to install, just start [@nb_electrobot](https://t.me/nb_electrobot) in Telegram.
<br>In case you want to run it locally, clone to your Linux server and add ```config.py``` file 
with ```TOKEN="your-token-from-telegram-botfather"```
<br>You can also run the script as a service.

## Roadmap

In future, this bot will be able to generate electrical schemas based on user input and provide them on the fly as convenient pdf files.

Following problems need to be solved:
1. Database storage for user requests
2. Generation of schemas from project database
3. Convertion of schemas to PNG and then to PDF

##Limitations

<br>Currently only german language is supported.
<br>Available cable types are NYM, NYY, NYCWY, N2XH.
<br>Available circuit breaker makers are ABB, Hager, Siemens.
<br>Currently only circuit breakers are supported (fuses are not supported).
<br>This program doesn't concider circuit breaker selectivity.
