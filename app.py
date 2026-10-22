from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# باش نحتافظو بالفواتير مؤقتا للتحميل
FACTURES = {}

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/create', methods=['POST'])
def create():
    # 1 - INFOS ENTREPRISE (PRIVÉ)
    ent_nom = request.form.get('ent_nom','').strip()
    ent_ice = request.form.get('ent_ice','')
    ent_tel = request.form.get('ent_tel','')
    ent_adresse = request.form.get('ent_adresse','')
    ent_logo_data = request.form.get('ent_logo_data','')  # <-- LOGO BASE64

    # 2 - CLIENT
    client = request.form.get('client','').strip()
    client_tel = request.form.get('client_tel','')
    numero = request.form.get('numero','FAC-2026-001')
    date = request.form.get('date','')
    if not date:
        date = datetime.now().strftime('%d/%m/%Y')

    # 3 - ARTICLES
    noms = request.form.getlist('nom[]')
    qtes = request.form.getlist('qte[]')
    prixs = request.form.getlist('prix[]')

    items = []
    sous_total = 0
    for n,q,p in zip(noms,qtes,prixs):
        if not n: continue
        try:
            q = int(q) if q else 1
            p = float(p) if p else 0
        except:
            q=1; p=0
        total = q * p
        sous_total += total
        items.append({'nom':n,'qte':q,'prix':p,'total':total})

    # 4 - CALCULS
    try:
        tva = float(request.form.get('tva','20'))
    except:
        tva = 20
    remise = request.form.get('remise','0')
    try:
        remise_pct = float(remise)
    except:
        remise_pct = 0

    tva_montant = sous_total * (tva/100)
    remise_montant = sous_total * (remise_pct/100)
    total = sous_total + tva_montant - remise_montant

    paiement = request.form.get('paiement','Espèces')
    notes = request.form.get('notes','')

    data = {
        'ent_nom':ent_nom,'ent_ice':ent_ice,'ent_tel':ent_tel,'ent_adresse':ent_adresse,
        'ent_logo_data':ent_logo_data,
        'client':client,'client_tel':client_tel,'numero':numero,'date':date,
        'items':items,'sous_total':round(sous_total,2),
        'tva':tva,'tva_montant':round(tva_montant,2),
        'remise':remise,'remise_montant':round(remise_montant,2),
        'total':round(total,2),'paiement':paiement,'notes':notes
    }

    FACTURES[numero] = data

    return render_template('facture.html', **data)

@app.route('/download/<numero>')
def download(numero):
    data = FACTURES.get(numero)
    if not data:
        return "Facture non trouvée, retourne créer une nouvelle", 404
    # كنرجعو نفس الصفحة، المتصفح يقدر يدير Print to PDF
    # إلا بغيتي PDF حقيقي، غادي نزيدو WeasyPrint من بعد
    return render_template('facture.html', **data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
