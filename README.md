# Electrobot
## Description

<img align="left" width="150" height="150" src="images/logo.png">

This telegram bot is able to generate electrical schemes based on user input and provide them on the fly as convenient CAD/PDF files. It parses user input automatically. Here are quick examples:
<br>
<br>```12kw 1% => 12kW 400V cos(φ)=0.95, limit dU factor to 1%```
<br>```UV-AV-01 12a NYCWY 0,8 => 12A, specify cable type, cos(φ)=0.80, switchboard name: UV-AV-01```
<br>```12kw e1 30m => 12kW, laying in cable channel (see laying types), length 30m```
<br>
<br>
## Deployment

Simple use: just start [@nb_electrobot](https://t.me/nb_electrobot) in Telegram.
<br>In case you want to run it locally, follow the instructions described in Deployment section in Wiki.

## Roadmap

1. Add text files support. Use case: user sends previously prepared text file with the list of feeders. This will allow to fill in the data faster from desktop.
2. Add Excel/PDF files read/write possible to make feeder lists editable and reusable.
3. Add possibility to create user templates (add-on)
4. Add internationalization options such as language switch, local norms, regulations, makers and cable types.

## Limitations

Currently, only german language is supported.
<br>Available cable types are NYM, NYY, NYCWY, N2XH.
<br>Available circuit breaker makers are ABB, Hager, Siemens.
<br>Currently only circuit breakers are supported (fuses are not supported).
<br>This program doesn't consider circuit breaker selectivity.
