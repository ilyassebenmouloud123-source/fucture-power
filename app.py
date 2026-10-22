from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'client': request.form.get('client'),
            'ice': request.form.get('ice'),
            'date': request.form.get('date'),
            'produits': [],
            'total': 0
        }
        noms = request.form.getlist('nom[]')
        qtes = request.form.getlist('qte[]')
        prixs = request.form.getlist('prix[]')
        
        for n,q,p in zip(noms, qtes, prixs):
            if n:
                try:
                    total_ligne = float(q or 0) * float(p or 0)
                    data['produits'].append({'nom': n, 'qte': q, 'prix': p, 'total': total_ligne})
                    data['total'] += total_ligne
                except:
                    pass
        
        data['tva'] = data['total'] * 0.20
        data['ttc'] = data['total'] + data['tva']
        data['num'] = f"FAC-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
        return render_template('facture.html', data=data)
    
    return render_template('form.html', today=datetime.date.today())

if __name__ == '__main__':
    app.run(debug=True)