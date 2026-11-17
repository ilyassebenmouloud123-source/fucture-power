from flask import Flask, render_template, request
import random
from datetime import date

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/facture', methods=['POST'])
def facture():
    # Infos entreprise / client
    d = request.form.to_dict()
    # Les lignes dyal facture (kayjibo ga3 les lignes, machi ghir wehda)
    noms = request.form.getlist('nom')
    qtes = request.form.getlist('qte')
    prixs = request.form.getlist('prix')

    items = []
    total_ht = 0
    for n, q, p in zip(noms, qtes, prixs):
        if n.strip() == "":
            continue
        q = int(q or 1)
        p = float(p or 0)
        sous_total = q * p
        total_ht += sous_total
        items.append({"nom": n, "qte": q, "prix": p, "total": sous_total})

    remise = float(request.form.get('remise') or 0)
    tva = float(request.form.get('tva') or 0)

    apres_remise = total_ht - (total_ht * remise / 100)
    montant_tva = apres_remise * tva / 100
    total_ttc = apres_remise + montant_tva

    return render_template('facture.html',
        d=d, items=items,
        numero=random.randint(1000, 9999),
        date_aujourd=date.today().strftime("%d/%m/%Y"),
        total_ht=round(total_ht, 2),
        remise=remise, tva=tva,
        montant_tva=round(montant_tva, 2),
        total_ttc=round(total_ttc, 2))

if __name__ == '__main__':
    app.run(debug=True)
