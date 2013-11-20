from flask import Flask, render_template, request
app = Flask(__name__)

app.vars = {}

@app.route('/index',methods=['GET','POST']) # form in template
def index():
    if request.method == 'GET':
        return render_template('datainput.html')
    else:  # request was POST
        app.vars['name'] = request.form['pagename']
        return render_template('results.html',checkname=app.vars['name'])

if __name__ == "__main__":
    app.run(debug=True)
