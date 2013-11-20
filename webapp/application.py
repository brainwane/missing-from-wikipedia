from flask import Flask, render_template, request
import missing

app = Flask(__name__)

# take in names from datainput.html form
# run massagenames (implicitly chunks into 50 titles per request) and leftout
# return result to user in results.html form

def onWikipedia(names, lang):
    names = names.split('\r\n')
    names = missing.massagenames(names)
    resultlist = missing.leftout(names, lang)
    return names, resultlist

@app.route('/index',methods=['GET','POST']) # form in template
def index():
    if request.method == 'GET':
        return render_template('datainput.html')
    else:  # request was POST
        namestocheck, language = request.form['pagename'], request.form['langname']
        orig, checkresult = onWikipedia(namestocheck, language)
        return render_template('results.html', checkname=orig, result=checkresult)

if __name__ == "__main__":
    app.run(debug=True)
