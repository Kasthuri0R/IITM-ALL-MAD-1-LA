from flask import Flask , render_template ,request
import csv
import matplotlib.pyplot as plt

app = Flask(__name__)

def render_wrong_html():
    #print('wrong.html will come ')
    return render_template("wrong.html")

def student_information(student_id, rows):
    #print("Function student_information called")
    value = 0
    #print(student_id)
    for row in rows[1:]:
        #print(row)
        if int(row[0].strip()) == int(student_id.strip()):
            value += int(row[2].strip())
    #print('total',value)
    if value == 0:
        student_template = render_wrong_html()
    else:
        student_template = render_template("student.html", student_id = student_id,student_list = rows, total = value)
    return student_template

def course_information(course_id, rows):
    #print('course.html will come')
    count = 0 # storing no of courses
    value = 0 # storing the marks
    max_score = 0 # max_marks
    data = {} 
    for row in rows[1:]:
        try:
            course = int(course_id)
        except:
            break
        if int(row[1].strip()) == course:
            i = int(row[2].strip()) #marks
            value += i
            count += 1
            if i not in data.keys():
                data[i] = 1
            else:
                data[i] += 1
            if i > max_score :
                max_score = i  
    if value == 0 or count == 0 :
        student_template = render_wrong_html()
    else:
        avg = value / count
        courses = list(data.keys())
        values = list(data.values())
        fig = plt.figure(figsize = (10,5))
        plt.bar(courses,values)
        plt.xlabel('Marks')
        plt.ylabel('Frequncy')
        fig.savefig('./static/my_plot.png')
        student_template =  render_template("course.html", course_id = course_id, average = avg , max_marks = max_score)
    return student_template


@app.route('/',methods = ['GET','POST'])
def student_course_selection():
    if request.method == 'GET' :
        return render_template('index.html')
    elif request.method == 'POST':
        file =  open('data.csv','r')
        csv_list = list(csv.reader(file))
        rows = []
        for row in csv_list:
            rows.append(row)
        id_element = request.form.get("ID")
        id_value = request.form.get('id_value')
        if id_element == 'student_id' :
            return student_information(id_value, rows)
        else:
            return course_information(id_value, rows)
    
    else: 
        return render_template('wrong.html')




if __name__ == '__main__':
    app.run(debug =True)