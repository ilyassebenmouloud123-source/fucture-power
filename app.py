from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/facture', methods=['GET', 'POST'])
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('form.html')
    
    client = request.form.get('client', 'Client')
    numero = request.form.get('numero', f'FAC-{datetime.now().year}-001')
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    noms = request.form.getlist('nom[]')
    qtes = request.form.getlist('qte[]')
    prixs = request.form.getlist('prix[]')
    
    items = []
    sous_total = 0
    
    for i in range(len(noms)):
        if noms[i].strip() == '':
            continue
        try:
            q = float(qtes[i]) if i < len(qtes) and qtes[i] else 1
            p = float(prixs[i]) if i < len(prixs) and prixs[i] else 0
            total_ligne = q * p
            sous_total += total_ligne
            items.append({
                'nom': noms[i],
                'qte': q,
                'prix': p,
                'total': total_ligne
            })
        except:
            continue
    
    if not items:
        items = [{'nom': 'Prestation', 'qte': 1, 'prix': 1500, 'total': 1500}]
        sous_total = 1500
    
    tva_pct = 20
    tva_val = sous_total * 0.2
    total = sous_total + tva_val
    
    return render_template('facture.html',
        client=client,
        numero=numero,
        date=date,
        items=items,
        sous_total=sous_total,
        tva=f"{tva_pct}%",
        total=total
    )

if __name__ == '__main__':
    app.run(debug=True)
