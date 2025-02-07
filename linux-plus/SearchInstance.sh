#!/bin/bash


read -p  "Enter file name to process: " FILENAME

if [[ ! -f "$FILENAME" ]]; then 
	echo "Filename:  $FILENAME does not exist. Exiting."
	exit 1
fi



OUTPUTFILE="TerminatedInstances.txt"

grep "serdar" event_history.csv |grep "Term" |grep -oE 'i-[a-zA-Z0-9']+ > $OUTPUTFILE

echo "see your terminated instances in $OUTPUTFILE."



