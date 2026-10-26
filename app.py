from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form_page():
    return render_template('form.html')

@app.route('/facture')
def facture_page():
    return render_template('facture.html')

@app.route('/generate', methods=['POST'])
def generate():
    # كيخلي الفورم يخدم كيف ما كان
    return render_template('facture.html')

if __name__ == '__main__':
    app.run(debug=True)
