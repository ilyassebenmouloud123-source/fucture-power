from flask import Flask, render_template, request
from datetime import datetime
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/facture', methods=['POST'])
def facture():
    try:
        # 1. ENTREPRISE
        ent_nom = request.form.get('ent_nom', 'Mon Entreprise').strip()
        ent_ice = request.form.get('ent_ice', '').strip()
        ent_rc = request.form.get('ent_rc', '').strip()
        ent_adresse = request.form.get('ent_adresse', '').strip()
        ent_tel = request.form.get('ent_tel', '').strip()
        ent_email = request.form.get('ent_email', '').strip()

        # 2. CLIENT
        client = request.form.get('client', 'Client').strip()
        client_tel = request.form.get('client_tel', '').strip()
        client_ice = request.form.get('client_ice', '').strip()

        # 3. ITEMS - LUXURY FORMAT
        noms = request.form.getlist('nom')
        qtes = request.form.getlist('qte')
        prixs = request.form.getlist('prix')

        items_html = ""
        sous_total = 0

        for i in range(len(noms)):
            n = noms[i].strip()
            if not n:
                continue
            try:
                q = int(qtes[i]) if i < len(qtes) and qtes[i] else 1
                p = float(prixs[i]) if i < len(prixs) and prixs[i] else 0
            except:
                q = 1
                p = 0
            
            ligne_total = q * p
            sous_total += ligne_total

            # LUXURY ROW - متوافق مع facture.html luxury
            items_html += f"""
            <div class='grid grid-cols-[1fr_70px_110px] p-4 items-center hover:bg-[#fcfbf7] transition'>
                <span class='font-medium text-[14px] text-black capitalize'>{n}</span>
                <span class='text-center text-[13px] text-zinc-600'>{q}</span>
                <span class='text-right font-bold text-[14px] text-black'>{ligne_total:.2f} DH</span>
            </div>
            """

        if not items_html:
            items_html = "<div class='p-4 text-center text-zinc-400 text-sm'>Aucun article</div>"

        # 4. CALCULS
        remise = float(request.form.get('remise', 0) or 0)
        tva_pct = float(request.form.get('tva', 0) or 0)
        
        remise_val = sous_total * remise / 100
        base_ht = sous_total - remise_val
        tva_val = base_ht * tva_pct / 100
        total = base_ht + tva_val

        # 5. NUMERO + DATE
        now = datetime.now()
        numero = f"FAC-{now.strftime('%Y%m%d-%H%M')}"
        date = now.strftime('%d/%m/%Y')
        
        notes = request.form.get('notes', '').strip()
        paiement = request.form.get('paiement', 'Espèces')

        # Nettoyage tel pour WhatsApp
        def clean_tel(t):
            return re.sub(r'[^0-9]', '', t)

        return render_template('facture.html',
            numero=numero,
            date=date,
            ent_nom=ent_nom,
            ent_ice=ent_ice,
            ent_rc=ent_rc,
            ent_adresse=ent_adresse,
            ent_tel=ent_tel,
            ent_email=ent_email,
            client=client,
            client_tel=clean_tel(client_tel),
            client_ice=client_ice,
            items_html=items_html,
            sous_total=f"{sous_total:.2f}",
            total=f"{total:.2f}",
            notes=notes if notes else f"Paiement: {paiement}. Merci pour votre confiance.",
            paiement=paiement
        )

    except Exception as e:
        return f"""
        <h1>Erreur: {str(e)}</h1>
        <p>Vérifie app.py et facture.html</p>
        <a href='/'>Retour</a>
        <pre>{str(e)}</pre>
        """

# Pour Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)
