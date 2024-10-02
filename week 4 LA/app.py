from flask import Flask , render_template ,request
import csv
import matplotlib.pyplot as plt

app = Flask(__name__)

f = open('data.csv' , 'r')



@app.route('/' , methods = ['POST' , 'GET'])
def selection_page() :
    if request.method ==  'POST' :
        return render_template('selection_page.html')
    return render_template('selection_page.html')


if __name__ == '__main__':
    app.run(debug =True)