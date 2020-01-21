![Logo of PyTranslate](https://raw.githubusercontent.com/GreenSky-Productions/PyTranslate/master/images/SocialPreviewPyTranslate.png)
[[English](README.md) | German]
# PyTranslate

[![Release](https://img.shields.io/github/downloads/GreenSky-Productions/PyTranslate/v1.1/total?color=green)](https://github.com/GreenSky-Productions/PyTranslate/releases/latest)



* [Was ist PyTranslate](README-DE.md#was-istpytranslate)
* [Neue Vorlage erstellen](README-DE.md#neue-vorlage-erstellen)
  * [Neue Vorlage aus einem Script erstellen](README-DE.md#neue-vorlage-aus-einem-script-erstellen)
* [Einträge hinzufügen](README-DE.md#eiträge-hinzufügen)
  * [Einträge hinzufügen von einem Template](README-DE.md#einträge-hinzufügen-von-einem-template)
  * [Einträge hinzufügen von einem Script](README-DE.md#einträge-hinzufügen-von-einem-script)
* [Einträge bearbeiten](README-DE.md#einträge-bearbeiten)
* [Einträge Löschen](README-DE.md#einträge-löschen)
* [Übersetzung exportieren](README-DE.md#übersetzung-exportieren)
* [Alle Tastenkombinationen](README-DE.md#alle-tastenkombinationen)

## Was ist PyTranslate

![Image of PyTranslate](https://raw.githubusercontent.com/GreenSky-Productions/PyTranslate/master/images/PyTranslate.png)


PyTranslate is a easy to use software to translate your Python Project according to the I18N of [gettext](https://docs.python.org/3/library/gettext.html).
It can create a translation template (.pot) from your Python scripts or Python embedded Files. 
Which you can easily edit in PyTranslate and use them to create a compiled Translation File (.mo).

## Create new Template

**Currently Work in Progress**

To create a new Template from scretch Select `File > Create new Template` or press `Ctrl+N`.

### Create your Template from a Script

You can create a new Template from a Script, where all Entries will filterd and Added to the new Template.

Select `File > Create new Template from Script` or press `Shift+Ctrl+N`

Choice you File which will be scanned and you Save File.

## Add Entries

Adding a new Entry will you archive over double clicking the `+` in the left column or select it and press `Enter`

### Add Entries from other Templates

You can add Entries from other Templates for the Case your Template has changed and you want to add the Entries to you Translation.

Select `Edit > Add Entries from a Template` or press `Ctrl+I` and choice you Template File.

### Add Entries from other Scripts

You can also add Entries from other Scripts to your Translation or Template. 

Select `Edit > Add Entries from Script` or press `Shift+Ctrl+I`

## Edit Entries

Editing a Entry ID double click it in the left Column or select it and press `Enter`.

Editing a Entry Value double lcik it in the right Column or select it and press `Enter`.

![Image of PyTranslate](https://raw.githubusercontent.com/GreenSky-Productions/PyTranslate/master/images/EditEntry.png)

## Remove Entries

Select a Entry and press ´Delete`
[Edit](README-DE.md#edit-entries) a Entry and press the Delete Button in the left bottom Corner.

## Export your Translation
For finally use your translation you must in the most cases compile your Translation.
Select `File > export` or press `Ctrl + E`

## All Keybinds

* `Ctrl+N` Create a new Template
* `Shift+Ctrl+N` Create a new Template from a Script
* `Ctrl+S` Save File
* `Shift+Ctrl+S` Save as
* `Ctrl+E` Export
* `Ctrl+Q` Quit
* `Ctrl+I` Add Entries from Template
* `Shift+Ctrl+I` Add Entries from Script
* `Arrow Up` and `Arrow Down` to navigate trought the Entries
* `Enter` Edit a Entry

**Entrie Editor Ekybinds**
* `Esc` Cancel edit
* `Shift+Enter` Confirm change and close Editor
* `Shift+Backspace` Remove Editor content (not the Entry it self)

