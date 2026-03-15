#!/bin/bash

CRON_CMD="/usr/bin/updatedb"

echo "Cronjob für updatedb erstellen"
echo "--------------------------------"

PS3="Bitte wählen Sie eine Option: "
options=("Stündlich" "Täglich" "Wöchentlich" "Monatlich" "Abbrechen")

select opt in "${options[@]}"
do
    case $opt in
        "Stündlich")
            read -p "Alle wie viele Stunden? (z.B. 1,2,4): " hours
            cron="0 */$hours * * * $CRON_CMD"
            break
            ;;
        "Täglich")
            read -p "Uhrzeit (HH:MM): " time
            hour=$(echo $time | cut -d: -f1)
            minute=$(echo $time | cut -d: -f2)
            cron="$minute $hour * * * $CRON_CMD"
            break
            ;;
        "Wöchentlich")
            read -p "Wochentag (0=Sonntag ... 6=Samstag): " weekday
            read -p "Uhrzeit (HH:MM): " time
            hour=$(echo $time | cut -d: -f1)
            minute=$(echo $time | cut -d: -f2)
            cron="$minute $hour * * $weekday $CRON_CMD"
            break
            ;;
        "Monatlich")
            read -p "Tag im Monat (1-31): " day
            read -p "Uhrzeit (HH:MM): " time
            hour=$(echo $time | cut -d: -f1)
            minute=$(echo $time | cut -d: -f2)
            cron="$minute $hour $day * * $CRON_CMD"
            break
            ;;
        "Abbrechen")
            echo "Abgebrochen."
            exit 0
            ;;
        *)
            echo "Ungültige Auswahl."
            ;;
    esac
done

echo
echo "Folgender Cronjob wird hinzugefügt:"
echo "$cron"

read -p "Bestätigen? (y/n): " confirm
if [[ "$confirm" == "y" ]]; then
    (crontab -l 2>/dev/null; echo "$cron") | crontab -
    echo "Cronjob erfolgreich hinzugefügt."
else
    echo "Keine Änderungen vorgenommen."
fi