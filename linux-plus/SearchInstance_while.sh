#!/bin/bash

while true; do
	read -p  "Enter file name to process: " FILENAME

	if [[ ! -f "$FILENAME" ]]; then 
		echo "Filename:  $FILENAME does not exist. Retry."
		

	else
		#file is found 
		break 

	fi

done

OUTPUTFILE="TerminatedInstances.txt"

#we are using regular expression to look  for instance of type "i-0c127ab5cdf997cf4" 
grep "serdar" event_history.csv |grep "Term" |grep -oE 'i-[a-zA-Z0-9']+ > $OUTPUTFILE

echo "see your terminated instances in $OUTPUTFILE."



