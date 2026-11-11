from flask import Flask, render_template, request
import urllib.request, json

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/facture', methods=['POST'])
def facture():
    data = request.form.to_dict()
    return render_template('facture.html', d=data)

@app.route('/chhal-dkhlo')
def chhal_dkhlo():
    try:
        url = "https://abacus.jasoncameron.dev/info/facture-power-ilyasse/visits"
        data = json.loads(urllib.request.urlopen(url, timeout=5).read())
        total = data.get("value", 0)
        return f"<h1 style='text-align:center;font-family:Arial;margin-top:100px'>Dkhel 3andek : {total} wahed</h1><p style='text-align:center'>Hado homa nass l 7qi9iyin li dkhlou</p>"
    except:
        return "<h1 style='text-align:center'>Mazal 0 wahed</h1>"

if __name__ == '__main__':
    app.run(debug=True)
