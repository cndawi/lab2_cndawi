# Lab 2: ALU Transcript Generator

A Python program that works out a student's final academic standing from a CSV of course grades, plus a Bash script that archives the grades file and logs the action.

## Files
- grade-evaluator.py: validates the data, calculates the total grade and GPA, decides PASSED or FAILED, and lists assignments eligible for resubmission.
- organizer.sh: archives grades.csv with a timestamp, creates a fresh empty grades.csv and appends an entry to organizer.log.
- grades.csv: the course data.
- README.md: this file.

## Requirements
- Python 3, standard library only (csv, sys, os). No external packages.
- A Bash shell (Linux, macOS, WSL or Git Bash).

## Input format
grades.csv has one row per assignment with these columns:

    assignment,group,score,weight
    Quiz,Formative,85,20
    Group Exercise,Formative,40,20
    Functions and Debugging Lab,Formative,45,20
    Midterm Project - Simple Calculator,Summative,70,20
    Final Project - Text-Based Game,Summative,60,20

- group must be Formative or Summative.
- score is a percentage from 0 to 100.
- weight is the assignment's share of the course. All weights add up to 100: Formative 60 and Summative 40.

## How to run

### 1. Evaluate the grades
Command: `python3 grade-evaluator.py`

When prompted, enter the CSV file name, for example grades.csv. Output for the sample data:

    --- Processing Grades ---
    Total grade: 60.0 /100
    GPA: 3.0 /5.0
    Formative: 56.67 %
    Summative: 65.0 %

    Final Status: PASSED

    Eligible for resubmission:
    - Group Exercise
    - Functions and Debugging Lab

If nothing needs resubmission, it prints "No resubmission needed." instead of the list.

### 2. Archive the grades
Command: `bash organizer.sh`

The script:
1. creates the archive folder if it does not exist
2. moves grades.csv to archive/grades_YYYYMMDD-HHMMSS.csv
3. creates a new empty grades.csv, ready for the next batch
4. appends a line to organizer.log, which keeps entries from every run

Example organizer.log line:

    Timestamp: 20261110-235214 | Original: grades.csv | Archived as: archive/grades_20261110-235214.csv

If grades.csv does not exist, it prints an error and exits with code 1. Run the evaluator first, because the organizer empties grades.csv.

## Grading rules
- Each assignment adds score x weight / 100 points to the total grade.
- GPA = (total grade / 100) x 5.0.
- A category percentage is its points divided by its weight, times 100.
- PASSED needs at least 50% in both Formative and Summative. Otherwise the status is FAILED, even if the total grade is above 50.
- Resubmission is for Formative assignments scoring below 50. Only the failed Formative assignment(s) with the highest weight are eligible, and if several share that weight, all are listed.

## Worked example (sample grades.csv)
- Total grade: 60.0, so GPA = 3.0
- Formative: 34 out of 60 = 56.67%
- Summative: 26 out of 40 = 65%
- Both are at least 50%, so the status is PASSED
- Group Exercise (40) and Functions and Debugging Lab (45) both failed and both weigh 20, so both are eligible for resubmission

## Error handling
The program stops with a clear message, and exit code 1, in these cases:
- File not found: Error: The file 'x.csv' was not found.
- Empty file: Error: The file has no assignment records. Add grades and try again.
- Non-numeric or blank score or weight: Error: Invalid number for 'Quiz'. Score and weight must be numbers (score: 'abc', weight: '20').
- Score outside 0-100: Error: Invalid score 150.0 for 'Quiz'. Scores must be between 0 and 100.
- Weights that do not add up: Error: Total weight is 110.0, but it must be 100. The same check is made for Formative (60) and Summative (40), which also catches a misspelled group name.

## Testing
Checked with the sample data and with edited copies of grades.csv:
- good data gives PASSED, GPA 3.0 and two resubmission items (tie on weight 20)
- a lower Formative percentage below 50 gives FAILED even when the total grade is above 50
- one failed assignment with a higher weight lists only that assignment
- no failed Formative assignments prints "No resubmission needed."
- an empty file, a score of abc, a blank score, a score of 150 and weights that do not total 100 each print the matching error
- organizer.sh run twice adds two lines to organizer.log, and run without grades.csv exits with code 1
