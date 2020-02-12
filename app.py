# user defined scripts
from scripts import scrapper

#python imports
import os

# flask imports
from flask import Flask, render_template, request, send_file, after_this_request
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = {
            'year': int(request.form['year']),
            'sem': int(request.form['sem']),
            'dept': request.form['dept'],
            'start': int(request.form['start']),
            'end': int(request.form['end'])
        }

        # script where all the scraping and zip creation is happening
        filename = scrapper.get_result(data)

        @after_this_request
        def remove_file(response):
            try:
                os.remove(filename)
            except Exception as error:
                app.log_exception(error)
            return response
        
        # sends the zip file. as_attachment parameters specify that the original name of the zip will be the 
        return send_file(filename)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/howtouse')
def howtouse():
    return render_template('howtouse.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
