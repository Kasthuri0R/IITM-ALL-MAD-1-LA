
# import required lib here
from jinja2 import Template
import sys
import csv
import matplotlib.pyplot as plt

# to read the csv(data.csv) file and store in a list
csv_data = open ('data.csv', newline = '')

# read the csv file
data = list(csv.reader(csv_data))
#print(data)

#store the values from the file
student_course = []
course_marks = []

# take the input from command line
input_list = sys.argv
#to verify the input that is correctly passed
#print(f"sys.argv: {sys.argv}")

#print(input_list)
# 1) input_list[0] = app.py  2)input_list[1] = -s or -c 3) input_list[2] = ID

TOTAL = 0
if input_list[1] == '-s' :
    for row in data :
        if input_list[2] == row[0].strip():
            TOTAL += int(row[2].strip())
            student_course.append(row)

    # if ID is wrong
    if student_course == [] :
        file_content = """
        <html> 
        <body>
            <h1>Wrong Input</h1>
            <p>Something went wrong</p>
        </body>
        </html>"""
        file = open("output.html", 'w')
        file.write(file_content)
        file.close()

    else:
        file_content = """
        <html> 
            <link rel = "stylesheet" href = "style.css">
        <body>
            <h1>Student Details</h1>
            <table>
            <tr>
                <th>Student ID</th>
                <th>Course ID</th>
                <th>Marks</th>
            </tr>
            {% for student in student_course%}
            <tr>
                <td>{{student[0].strip()}}</td>
                <td>{{student[1].strip()}}</td>
                <td>{{student[2].strip()}}</td>   
            </tr>
            {% endfor %}
            <tr>
                <td colspan = "2" > Total Marks </td>
                <td> {{TOTAL}} </td>
            </tr>
            </table>
        </body>
        </html>"""
        
        temp = Template(file_content)
        file_content_with_data = temp.render(student_course = student_course, TOTAL = TOTAL)
        file = open("output.html", 'w')
        file.write(file_content_with_data)
        file.close()

    
elif input_list[1] == '-c' :
    for row in data :
        if input_list[2] == row[1].strip():
            course_marks.append(int(row[2].strip()))
    
    # if ID is wrong
    if course_marks == [] :
        file_content = """
        <html> 
        <body>
            <h1>Wrong Input</h1>
            <p>Something went wrong</p>
        </body>
        </html>"""
        file = open("output.html", 'w')
        file.write(file_content)
        file.close()

    else :
        average_marks = sum(course_marks)/len(course_marks)
        max_marks = max(course_marks)

        file_content = """

        <html>
            <link rel = "stylesheet" href = "style.css">
        <body>
        <h1>Course Details</h1>
        <table> 
            <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
            </tr>
            <tr>
            <td>{{average_marks}}</td>
            <td>{{max_marks}}</td>
            </tr>
        </table>
        <img  src = "hist.png" >
        
        </body>
        </html>"""
        temp = Template(file_content)
        file_content_with_data = temp.render(average_marks = average_marks , max_marks = max_marks)
        # for histogram plotting
        x = course_marks
        plt.hist(x)
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig('hist.png')
        file = open("output.html",'w')
        file.write(file_content_with_data)
        file.close()







