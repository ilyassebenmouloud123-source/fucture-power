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
    
    # Entreprise
    ent_nom = request.form.get('ent_nom','FACTURE POWER')
    ent_ice = request.form.get('ent_ice','')
    ent_tel = request.form.get('ent_tel','')
    ent_adresse = request.form.get('ent_adresse','')
    
    # Client
    client = request.form.get('client','Client')
    client_tel = request.form.get('client_tel','')
    numero = request.form.get('numero', f'FAC-{datetime.now().strftime("%Y%m%d")}-001')
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Options
    tva_pct = float(request.form.get('tva','20'))
    remise_pct = float(request.form.get('remise','0'))
    paiement = request.form.get('paiement','Espèces')
    notes = request.form.get('notes','')
    
    noms = request.form.getlist('nom[]')
    qtes = request.form.getlist('qte[]')
    prixs = request.form.getlist('prix[]')
    
    items=[]
    sous_total=0
    for i in range(len(noms)):
        if not noms[i].strip(): continue
        try:
            q=float(qtes[i]) if qtes[i] else 1
            p=float(prixs[i]) if prixs[i] else 0
            total_l=q*p
            sous_total+=total_l
            items.append({'nom':noms[i],'qte':int(q) if q.is_integer() else q,'prix':int(p) if p.is_integer() else p,'total':int(total_l) if total_l.is_integer() else total_l})
        except: continue
    
    if not items:
        items=[{'nom':'Prestation','qte':1,'prix':400,'total':400}]
        sous_total=400
    
    remise_val = sous_total * (remise_pct/100)
    base = sous_total - remise_val
    tva_val = base * (tva_pct/100)
    total = base + tva_val
    
    def clean(n): return int(n) if float(n).is_integer() else round(n,2)
    
    return render_template('facture.html',
        ent_nom=ent_nom, ent_ice=ent_ice, ent_tel=ent_tel, ent_adresse=ent_adresse,
        client=client, client_tel=client_tel, numero=numero, date=date,
        items=items, sous_total=clean(sous_total), remise_pct=remise_pct,
        remise_val=clean(remise_val), tva=tva_pct, tva_val=clean(tva_val),
        paiement=paiement, notes=notes, total=clean(total)
    )

if __name__ == '__main__':
    app.run(debug=True)
