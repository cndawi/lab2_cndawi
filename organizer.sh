#!/bin/bash
if [ ! -d "archive" ]; then
	mkdir archive
fi
if [ ! -f "grades.csv" ]; then
	echo "Error: grades.csv not found. Nothing to archive."
	exit 1
fi
timestamp=$(date +"%Y%m%d-%H%M%S")
mv grades.csv archive/grades_$timestamp.csv
touch grades.csv
echo "Timestamp:" $timestamp "| Original: grades.csv | Archived as: archive/grades_$timestamp.csv" >> organizer.log
echo "Archived grades.csv as archive/grades_$timestamp.csv"
