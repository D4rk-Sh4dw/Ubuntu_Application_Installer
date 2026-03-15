#!/bin/bash
echo "=== Interactive Cronjob Generator ==="
echo "Cron format: MINUTE HOUR DOM MON DOW COMMAND"
read -p "Enter Minute (0-59, or *): " c_min
read -p "Enter Hour (0-23, or *): " c_hour
read -p "Enter Day of Month (1-31, or *): " c_dom
read -p "Enter Month (1-12, or *): " c_mon
read -p "Enter Day of Week (0-7, or *): " c_dow
read -p "Enter the command to execute: " c_cmd

if [ -z "$c_cmd" ]; then
    echo "Error: Command cannot be empty."
    exit 1
fi

CRON_JOB="$c_min $c_hour $c_dom $c_mon $c_dow $c_cmd"

echo "Generated Cronjob: $CRON_JOB"
read -p "Do you want to add this to your crontab? (y/n): " confirm

if [[ "$confirm" == [yY] || "$confirm" == [yY][eE][sS] ]]; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Success! The cronjob has been installed."
else
    echo "Aborted."
fi
