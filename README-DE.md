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

PyTranslate ist ein einfaches Programm für das Übersetzen deiner Python Projekte mit dem I18N Standard von [gettext](https://docs.python.org/3/library/gettext.html).
Es kann Übersetzungsvorlagen aus deinen Python Scripts oder Python eingebettete Datein erstellen,
welche du ganz einfach in PyTranslate bearbeiten kannst um sie am Ende zu kompilieren.

![Image of PyTranslate](https://raw.githubusercontent.com/GreenSky-Productions/PyTranslate/master/images/PyTranslate.png)

## Neue Vorlage erstellen

**Momentan noch in arbeit**

Um ein neue Vorlage von Grund auf zu erstellen

Wähle `Datei > Neue Vorlage erstellen` oder drücke `Ctrl+N`.

### Neue Vorlage aus einem Script erstellen

Du kannst ein neue Vorlage aus einem Script heraus erstellen, wo dann alle Einträge ausgelesen werden und zu neuen Vorlage hinzugefügt werden.

Wähle `Datei > Erstelle neue Vorlage aus Script`

## Einträge hinzufügen

Einen neuen Eintrg hinzuzufügen geht mit einen doppel klick auf das `+` in der Linken Spalte oder wähle dieses aus und drücke `Enter`

### Einträge hinzufügen von einem Template

Du kannst Einträge hinzufügen von einer andern Vorlage, falls sich dein Vorlage geändert hat und du diese Einträge zu deiner Übersetzung hinzufügen möchtest.

Wähle `Bearbeiten > Einträge hinzufügen aus Vorlage` oder drücke `Ctrl+I` und wähle dein Vorlage aus.

### Einträge hinzufügen von einem Script

Du kannst auch Einträge aus andern Scripts zu deiener Vorlage oder Übersetzung hinzufügen.

Wähle `Bearbeiten > Einträge hinzufügen aus Script` oder drücke `Shift+Ctrl+I` 

## Einträge bearbeiten

Bearbeite eine Eintrags ID indem du in der linken Spalte doppelklickst oder sie auswählst und `enter` drückst.

Bearbeite den Eintrags Inhalt indem du in der rechten Spalte doppelklickst oder sie auswählst und `enter` drückst.

![Eintragseditor](https://raw.githubusercontent.com/GreenSky-Productions/PyTranslate/master/images/EditEntry.png)

## Einträge Löschen

Wähle ein Eintrag und drücke `Entf` oder
[bearbeite](README-DE.md#edit-entries) es und drücke den Löschen Knopf links unten in der Ecke.

## Übersetzung exportieren
Um deine Überstzung schlussendlich benutzen zu können musst du diese kompielieren.

Wähle `Datei > Exportieren` oder drücke `Ctrl + E`

## Alle Tastenkombinationen

* `Ctrl+N` Erstelle eine neue Vorlage
* `Shift+Ctrl+N` Erstelle eine neue Vorlage aus einem Script
* `Ctrl+S` Speichert die atkuelle Datei
* `Shift+Ctrl+S` Speichert als neue Datei
* `Ctrl+E` Exportiert/Kompieliert deine Datei
* `Ctrl+Q` Beendet das Programm
* `Ctrl+I` Fügt Einträge von einer Vorlage hinzu
* `Shift+Ctrl+I` Fügt Einträge von einem Script hinzu
* `Pfeif-Hoch`und `Pfeil-Runter` Navigieren durch die Eintragsliste
* `Enter` Bearbeitet den angewählten Eintrag

**Eintragseditor Tastenkombinationen**
* `Esc` Abbrechen des Bearbeitens
* `Shift+Enter` Bestätigt und schließt die bearbeitung
* `Shift+Backspace` Löscht Editor Inhalt (nicht den Eintrag als solches)


