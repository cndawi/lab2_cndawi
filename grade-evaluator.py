import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                try:
                    score=float(row['score'])
                    weight=float(row['weight'])
                except (ValueError, TypeError):
                    print(f"Error: Invalid number for '{row['assignment']}'. Score and weight must be numbers (score: '{row['score']}', weight: '{row['weight']}').")
                    sys.exit(1)

                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': score,
                    'weight': weight
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    if len(data)==0:
        print("Error: The file has no assignment records. Add grades and try again.")
        sys.exit(1)

    
    # TODO: a) Check if all scores are percentage based (0-100)
    for item in data:
        if item['score'] <0 or item['score'] >100:
            print(f"Error: Invalid score {item['score']} for '{item['assignment']}'. Scores must be between 0 and 100.")
            sys.exit(1)
    # TODO: b) Validate total weights (Total=100, Summative=40, Formative=60)
    total_weight=0
    formative_weight=0
    summative_weight=0
    for item in data:
        total_weight=total_weight + item['weight']
        if item['group'] == 'Formative':
            formative_weight = formative_weight + item['weight']
        elif item['group'] == 'Summative':
            summative_weight = summative_weight + item['weight']
    if total_weight != 100:
        print(f"Error: Total weight is {total_weight}, but it must be 100.")
        sys.exit(1)
    if formative_weight !=60:
        print(f"Error: Formative weight is {formative_weight}, but it must be 60.")
        sys.exit(1)
    if summative_weight !=40:
        print(f"Error: Summative weight is {summative_weight}, but it must be 40.")
        sys.exit(1)

    # TODO: c) Calculate the Final Grade and GPA
    total_grade=0
    for item in data:
        total_grade=total_grade+ item['score']* item['weight']/100
    gpa=(total_grade/100)*5.0
    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    formative_points=0
    summative_points=0
    for item in data:
        points=item['score']* item['weight']/100
        if item['group']=='Formative':
            formative_points=formative_points+points
        else:
            summative_points=summative_points+points
    formative_percent=formative_points/formative_weight*100
    summative_percent=summative_points/summative_weight*100
    if formative_percent>=50 and summative_percent>=50:
        status="PASSED"
    else:
        status="FAILED"
    
    # TODO: e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.
    failed_formative=[]
    for item in data:
        if item['group']=='Formative' and item['score']<50:
            failed_formative.append(item)
    resubmit=[]
    if len(failed_formative) >0:
        highest_weight=failed_formative[0]['weight']
        for item in failed_formative:
            if item['weight']>highest_weight:
                highest_weight=item['weight']
        for item in failed_formative:
            if item['weight']==highest_weight:
                resubmit.append(item)
    print ("Total grade:", round(total_grade,2), "/100")
    print("GPA:", round(gpa,2), "/5.0")
    print("Formative:", round(formative_percent,2), "%")
    print("Summative:", round(summative_percent,2), "%")
    print("\nFinal Status:", status)
    if len(resubmit) >0:
        print("\nEligible for resubmission:")
        for item in resubmit:
            print("-", item['assignment'])
    else:
        print("\nNo resubmission needed.")

    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
