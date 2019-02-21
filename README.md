# D&D Infinity

Practicing Domain-Driven Design (DDD) using 5e Dungeons & Dragons (D&D). Please see the wiki for more info!

## What is D&D Infinity?

This project is a fun side project with the purpose of learning how to build a scalable, maintainable codebase
from scratch. I chose D&D as the model of choice because of my relatively deep understanding of the domain itself.
Of course, I may find that I have some underlying misunderstandings along the way. :)

A good project to start is a D&D Beyond replica - a website where you can create and maintain your
D&D character. This allows me to explore different frameworks and libraries out in the WWW, and also learn
how to integrate these tools together.

Of course, I don't plan to make money off this project - this project is here simply to learn. :)

## Unit Tests

To run the project's unit tests, simply run:
```bash
python -m unittest discover
```

## Web Application

The web application currently serves as a testing ground to view the PC model in a web browser.

To run the web application, run the following commands:
```bash
# Windows Powershell
$env:FLASK_APP = "app"
$env:FLASK_DEBUG = "development"
flask run
```

## Character Sheet PDF Generator (WIP)

The character sheet PDF generator creates a PDF from the PC model in LaTeX.

While there is a working version of the generator, the LaTeX document format is still being
worked on to make it more tabletop-friendly.

## Awesome Sauce

For the sake of making the project more awesome, I've added a picture of the dragonborn squad.

![Dragonborn Squad](static/images/dragonborn_squad.png)
