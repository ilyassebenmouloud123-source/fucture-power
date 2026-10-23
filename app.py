from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('form.html')
    except Exception as e:
        return f"Erreur form.html: {str(e)}"

@app.route('/facture', methods=['POST'])
def facture():
    try:
        ent_nom = request.form.get('ent_nom','Mon entreprise')
        ent_adresse = request.form.get('ent_adresse','')
        ent_tel = request.form.get('ent_tel','')
        ent_ice = request.form.get('ent_ice','')
        client = request.form.get('client','Client')
        client_tel = request.form.get('client_tel','')
        client_ice = request.form.get('client_ice','')
        
        noms = request.form.getlist('nom')
        qtes = request.form.getlist('qte')
        prixs = request.form.getlist('prix')
        
        html = "<table class='w-full'><tr class='border-b text-xs text-gray-400'><th class='text-left'>Désignation</th><th>Qté</th><th class='text-right'>Prix</th></tr>"
        total = 0
        for i, n in enumerate(noms):
            if not n: continue
            q = int(qtes[i]) if i < len(qtes) and qtes[i] else 1
            p = float(prixs[i]) if i < len(prixs) and prixs[i] else 0
            html += f"<tr class='border-b'><td class='py-2'>{n}</td><td class='text-center'>{q}</td><td class='text-right'>{q*p} DH</td></tr>"
            total += q*p
        html += "</table>"
        
        from datetime import datetime
        return render_template('facture.html',
            numero=datetime.now().strftime("FAC-%Y%m%d-%H%M"),
            date=datetime.now().strftime("%d/%m/%Y"),
            ent_nom=ent_nom, ent_adresse=ent_adresse,
            ent_tel=ent_tel, ent_ice=ent_ice,
            client=client, client_tel=client_tel, client_ice=client_ice,
            items_html=html, sous_total=total, total=total)
    except Exception as e:
        return f"Erreur serveur: {str(e)} <br><a href='/'>Retour</a>"

# Pour Vercel
if __name__ == '__main__':
    app.run()
