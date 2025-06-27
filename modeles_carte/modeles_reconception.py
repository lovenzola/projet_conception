from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, whitesmoke, honeydew, aliceblue, lightsteelblue, thistle, oldlace
def modele_carte_reconception(resultat,tentative, fond, couleur_nom):
    nom_fichier = f"C:\projet\cartes\carte_reconception\Carte{tentative}_{resultat.nom.title()}_{resultat.matricule.upper()}.pdf"
    carte = canvas.Canvas(nom_fichier, pagesize=(253, 143))
    
    carte.setFillColor(whitesmoke)
    carte.setLineWidth(1)
    carte.setStrokeColor(black)
    carte.rect(1, 1, 251, 141, fill=True, stroke=True)

    carte.drawImage("C:\\projet\\multimedia\\logo.jpg", x=5, y=110.5, width=40, height=30)

    carte.setFillColor(black)
    carte.setFont("Helvetica-Bold", 9)
    carte.drawString(55, 122, "UNIVERSITE PROTESTANTE AU CONGO")

    carte.setFillColor(fond)
    carte.rect(1, 1, 251, 108, fill=True, stroke=True)

    texte = carte.beginText()
    texte.setFillColor(black)
    texte.setTextOrigin(110, 85)
    texte.setFont("Helvetica-Bold", 9)
    texte.textLine(f"{resultat.nom.title()} {(resultat.postnom or "").title()}")
    texte.textLine(f"Prenom: {(resultat.prenom or "").title()}")
    texte.setFont("Helvetica", 9)
    texte.textLine(f"Sexe: {resultat.sexe.upper()}")
    texte.textLine(f"Matricule: {resultat.matricule.upper()}")
    texte.textLine(f"Promotion: {resultat.promotion.upper()}")
    texte.textLine(f"Date de naissance: {resultat.date_naissance}")
    carte.drawText(texte)

    carte.drawImage(resultat.photo_path, x=15, y=25, width=75, height=70)
    carte.setFont("Helvetica-BoldOblique", 9)
    carte.drawString(5, 10, "CARTE D'ETUDIANT")
    carte.drawString(5,100,f"Généré le: {date.today().strftime('%d/%m/%Y')}")
    carte.save()

def modele_fasi_reconception(resultat, tentaive):
    modele_carte_reconception(resultat, tentaive,fond=lightsteelblue, couleur_nom=black)

def modele_fase_reconception(resultat, tentative):
    modele_carte_reconception(resultat, tentative,fond=oldlace, couleur_nom=black)

def modele_droit_reconception(resultat, tentative):
    modele_carte_reconception(resultat,tentative, fond=thistle, couleur_nom=black)

def modele_med_reconception(resultat,tentative):
    modele_carte_reconception(resultat,tentative, fond=honeydew, couleur_nom=black)