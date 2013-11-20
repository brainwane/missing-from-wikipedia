from flask import Flask, render_template, request
import missing

app = Flask(__name__)

# take in names from datainput.html form
# massagenames
#### chunknames - someday! when I actually have a bunch
# leftout
# return result to user in results.html form

def onWikipedia(name):
    names = [name]
    names = missing.massagenames(names)
    resultlist = missing.leftout(names, "en")
    return resultlist != []

@app.route('/index',methods=['GET','POST']) # form in template
def index():
    if request.method == 'GET':
        return render_template('datainput.html')
    else:  # request was POST
        nametocheck = request.form['pagename']
        checkresult = onWikipedia(nametocheck)
        return render_template('results.html', checkname=nametocheck, result=checkresult)

if __name__ == "__main__":
    app.run(debug=True)
