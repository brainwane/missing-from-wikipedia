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
        print "request.form is " + str(request.form)
        print "request.files is " + str(request.files)
        if request.form['pagename']:
            print "they typed in a list of names"
            namestocheck, language = request.form['pagename'], request.form['langname']
            namestocheck = namestocheck.split('\r\n')
        else:
            print "file upload"
            namefile, language = request.files['fileofnames'], request.form['langname']
            namestocheck = missing.getnamefile(namefile)
        # orig, checkresult, statistics = onWikipedia(namestocheck, language)
        # return render_template('results.html', checkname=orig, result=checkresult, stats=statistics)
        return render_template('results.html', checkname=["yo"], result=["yo"], stats={"original":5,"ratio":90.0,"missing":3})

if __name__ == "__main__":
    app.run(debug=True)
