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


def askedToCheck(listofstrings):
    l = len(listofstrings)
    if l == 1:
        return listofstrings[0]
    elif l <= 4:
        return ", ".join(listofstrings)
    elif l > 4:
        return "%s phrases: %s, %s... %s, %s" % (l, listofstrings[0], listofstrings[1], listofstrings[-2], listofstrings[-1])


@app.route('/index', methods=['GET', 'POST'])  # form in template
def index():
    if request.method == 'GET':
        print "we did a get"
        return render_template('datainput.html')
    else:  # request was POST
        print "we did a POST!"
        if 'pagename' in request.form:
            print type(request.form['pagename'])
            namestocheck, language = request.form['pagename'].encode('utf-8'), request.form['langname']
            namestocheck = namestocheck.split('\r\n')
        else:
            namefilestorage, language = request.files[('fileofnames')].stream, request.form['langname']
            namestocheck = [line.strip('\n').decode('utf-8') for line in namefilestorage]
        orig, checkresult, statistics = onWikipedia(namestocheck, language)
        return render_template('results.html', checkname=askedToCheck(orig), result=checkresult, stats=statistics, target_lang=language)


if __name__ == "__main__":
    app.run(debug=True)
