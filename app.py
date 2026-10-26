from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form_page():
    return render_template('form.html')

@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

@app.route('/facture')
def facture_page():
    return render_template('facture.html')
@app.route('/google0e59c1123d53e92c.html')
def google_verify():
    return 'google-site-verification: google0e59c1123d53e92c.html'

if __name__ == '__main__':
    app.run(debug=True)
