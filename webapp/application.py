# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import missing

app = Flask(__name__)

# take in names from datainput.html form
# run massagenames (implicitly chunks into 50 titles per request) and leftout
# return result to user in results.html form

def onWikipedia(names, lang):
    names = missing.massagenames(names)
    resultlist = missing.leftout(names, lang)
    stats = missing.generate_statistics(resultlist, names)
    return names, resultlist, stats

@app.route('/index',methods=['GET','POST']) # form in template
def index():
    if request.method == 'GET':
        print "we are in get"
        return render_template('datainput.html')
    else:  # request was POST
        print "we did a POST!"
        if 'pagename' in request.form:
            namestocheck, language = request.form['pagename'], request.form['langname']
            namestocheck = namestocheck.split('\r\n')
        else:
            namefilestorage, language = request.files[('fileofnames')].stream, request.form['langname']
            namestocheck = [line.strip() for line in namefilestorage]
        orig, checkresult, statistics = onWikipedia(namestocheck, language)
        import pdb
        pdb.set_trace()
        return render_template('results.html', checkname=orig, result=checkresult, stats=statistics)


if __name__ == "__main__":
    app.run(debug=True)
