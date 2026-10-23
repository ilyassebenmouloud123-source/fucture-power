from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/facture', methods=['POST'])
def facture():
    # Infos pro
    ent_nom = request.form.get('ent_nom', '')
    ent_ice = request.form.get('ent_ice', '')
    ent_rc = request.form.get('ent_rc', '')
    ent_adresse = request.form.get('ent_adresse', '')
    ent_tel = request.form.get('ent_tel', '')
    ent_email = request.form.get('ent_email', '')
    
    # Client
    client = request.form.get('client', '')
    client_tel = request.form.get('client_tel', '')
    client_ice = request.form.get('client_ice', '')
    
    # Items
    noms = request.form.getlist('nom')
    qtes = request.form.getlist('qte')
    prixs = request.form.getlist('prix')
    
    items_html = ""
    sous_total = 0
    for i in range(len(noms)):
        try:
            q = int(qtes[i]) if qtes[i] else 1
            p = float(prixs[i]) if prixs[i] else 0
            total_ligne = q * p
            sous_total += total_ligne
            items_html += f"<tr class='border-b border-zinc-50'><td class='py-4 text-sm'>{noms[i]}</td><td class='text-center text-sm'>{q}</td><td class='text-right text-sm'>{p} DH</td><td class='text-right font-bold text-sm'>{total_ligne} DH</td></tr>"
        except:
            continue
    
    remise = float(request.form.get('remise', 0) or 0)
    tva = float(request.form.get('tva', 20) or 20)
    
    remise_montant = sous_total * remise / 100
    base = sous_total - remise_montant
    tva_montant = base * tva / 100
    total = base + tva_montant
    
    numero = f"FAC-{datetime.now().strftime('%Y%m%d-%H%M')}"
    date = datetime.now().strftime('%d/%m/%Y')
    
    return render_template('facture.html',
        ent_nom=ent_nom, ent_ice=ent_ice, ent_rc=ent_rc,
        ent_adresse=ent_adresse, ent_tel=ent_tel, ent_email=ent_email,
        client=client, client_tel=client_tel, client_ice=client_ice,
        items_html=items_html, sous_total=sous_total,
        total=total, numero=numero, date=date,
        notes=request.form.get('notes',''))

if __name__ == '__main__':
    app.run(debug=True)
