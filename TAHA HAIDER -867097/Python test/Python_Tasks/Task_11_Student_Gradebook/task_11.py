# Task 11 – Student Gradebook

import csv

students = {}
scores = {}

# Read students
with open("students.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        students[row["student_id"]] = row["name"]
        scores[row["student_id"]] = []


# Read scores
with open("scores.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        sid = row["student_id"]
        subject = row["subject"]
        marks = float(row["marks"])

        if sid not in students:
            continue

        if marks < 0 or marks > 100:
            continue

        duplicate = False

        for item in scores[sid]:

            if item[0] == subject:
                duplicate = True

        if duplicate:
            continue

        scores[sid].append((subject, marks))


result = []

# Calculate average and grade
for sid in students:

    total = 0

    for item in scores[sid]:
        total += item[1]

    if len(scores[sid]) == 0:
        average = 0
    else:
        average = total / len(scores[sid])

    if average >= 85:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 55:
        grade = "C"
    elif average >= 40:
        grade = "D"
    else:
        grade = "F"

    result.append({
        "id": sid,
        "name": students[sid],
        "average": average,
        "grade": grade
    })


# Sort by average
for i in range(len(result)):

    for j in range(i + 1, len(result)):

        if result[j]["average"] > result[i]["average"]:
            result[i], result[j] = result[j], result[i]

        elif result[j]["average"] == result[i]["average"]:

            if result[j]["id"] < result[i]["id"]:
                result[i], result[j] = result[j], result[i]


# Add rank and print
for i in range(len(result)):
    result[i]["rank"] = i + 1

    print("Student:", result[i]["name"])
    print("Average:", result[i]["average"])
    print("Grade:", result[i]["grade"])
    print("Rank:", result[i]["rank"])
    print("----------------")


# Export report
with open("report.csv", "w", newline="") as file:

    fields = ["id", "name", "average", "grade", "rank"]

    writer = csv.DictWriter(file, fieldnames=fields)

    writer.writeheader()
    writer.writerows(result)
