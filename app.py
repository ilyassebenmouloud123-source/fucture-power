from flask import Flask, render_template, request, redirect, url_for, send_file
import io
from datetime import datetime
import random

app = Flask(__name__)

# Kan-khezeno l fawatir hna bach l download y-khdem
FACTURES = {}

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/facture', methods=['GET', 'POST'])
def facture():
    # HADA HOWA L FIX DYAL METHOD NOT ALLOWED
    if request.method == 'GET':
        return redirect('/')

    ent_nom = request.form.get('ent_nom', '')
    ent_adresse = request.form.get('ent_adresse', '')
    ent_tel = request.form.get('ent_tel', '')
    ent_ice = request.form.get('ent_ice', '')
    ent_logo_data = request.form.get('ent_logo_data', '')

    client = request.form.get('client', '')
    client_tel = request.form.get('client_tel', '')
    client_ice = request.form.get('client_ice', '')
    notes = request.form.get('notes', '')
    paiement = request.form.get('paiement', 'Espèces')

    noms = request.form.getlist('nom')
    qtes = request.form.getlist('qte')
    prixs = request.form.getlist('prix')

    items = []
    sous_total = 0
    for n, q, p in zip(noms, qtes, prixs):
        if not n.strip():
            continue
        try:
            q = int(q) if q else 1
            p = float(p) if p else 0
        except:
            q, p = 1, 0
        total_ligne = q * p
        sous_total += total_ligne
        items.append({'nom': n, 'qte': q, 'prix': f"{p:.2f}", 'total': f"{total_ligne:.2f}"})

    try:
        tva = float(request.form.get('tva', 0) or 0)
        remise = float(request.form.get('remise', 0) or 0)
    except:
        tva, remise = 0, 0

    remise_montant = sous_total * remise / 100
    sous_apres_remise = sous_total - remise_montant
    tva_montant = sous_apres_remise * tva / 100
    total = sous_apres_remise + tva_montant

    numero = f"FP-{datetime.now().strftime('%Y%m%d')}-{random.randint(100,999)}"
    date = datetime.now().strftime('%d/%m/%Y')

    data = {
        'numero': numero, 'date': date,
        'ent_nom': ent_nom, 'ent_adresse': ent_adresse, 'ent_tel': ent_tel,
        'ent_ice': ent_ice, 'ent_logo_data': ent_logo_data,
        'client': client, 'client_tel': client_tel, 'client_ice': client_ice,
        'items': items, 'notes': notes, 'paiement': paiement,
        'sous_total': f"{sous_total:.2f}",
        'tva': str(int(tva)) if tva == int(tva) else str(tva),
        'tva_montant': f"{tva_montant:.2f}",
        'remise': str(int(remise)) if remise == int(remise) else str(remise),
        'remise_montant': f"{remise_montant:.2f}",
        'total': f"{total:.2f}",
    }
    FACTURES[numero] = data
    return render_template('facture.html', **data)

@app.route('/download/<numero>')
def download(numero):
    data = FACTURES.get(numero)
    if not data:
        return redirect('/')
    # PDF b tariqa khfifa b reportlab
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, 800, data['ent_nom'])
    c.setFont("Helvetica", 10)
    c.drawString(40, 780, f"Facture: {data['numero']} - {data['date']}")
    c.drawString(40, 765, f"Client: {data['client']} - {data['client_tel']}")
    y = 730
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Designation")
    c.drawRightString(550, y, "Total")
    y -= 20
    c.setFont("Helvetica", 10)
    for it in data['items']:
        c.drawString(40, y, f"{it['nom']}  x{it['qte']}  -  {it['prix']} DH")
        c.drawRightString(550, y, f"{it['total']} DH")
        y -= 18
    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(550, y, f"TOTAL: {data['total']} DH")
    c.setFont("Helvetica", 9)
    c.drawString(40, 60, "FACTURE POWER PRO - Merci pour votre confiance")
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"facture-{numero}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
