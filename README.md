# Practicing DDD with D&D

Practicing Domain-Driven Design (DDD) using 5e Dungeons & Dragons (D&D) as the domain, AKA try to replicate D&D Beyond.

This project is currently written in Python 3.5. I'm writing this in Python for its flexibility to prototype
while modelling, and also because I just want to practice Python.

## Project hit list
* Move the project hit list to GitHub issues and/or a project management system
* Clean up saving throw/skill proficiency hashmap usage
* Restructure equipment (rely on class inheritance vs. use properties)
    * Have functions to ask whether something is simple/martial, STR/DEX-based, etc.
    * Work on determining proficiencies for specific weapons vs. simple/martial
* Clean up traits/features across race/class/background (consistency?)
* Have a cleaner separation between cantrips and cast spells
* Add feats into the mix
* Find a way to aggregate additions to attacks/spellcasting (i.e. sneak attack)
* Rename PC class because it gets confusing that it was once meant for multiclassing
* Don't throw error within object if verification doesn't pass, let outside program determine
    * As in, let the verify function return the object containing the list of required things
    * Hmmm perhaps that the JSON stuff is more of a display thing than actually a feature
    * AKA I don't necessarily need the JSON to work in order to allow the verification to work
* Build a character to level 20

## Domain goals
* Build a nicely-modelled player character (PC)
* Build a nicely-modelled monster
* Build a character sheet generator to a PDF
* Build an initiative tracker
* Build a PC creation module

# Tech goals
* Learn Python
* Learn MongoDB or a relational database
* Learn Flask with a side of Javascript
* Learn how to fit and use this in a 7" touchscreen

![Dragonborn Squad](static/images/dragonborn_squad.png)
