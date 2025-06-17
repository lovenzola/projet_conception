# Connexion a la base de donnee
from sqlalchemy.orm import sessionmaker
from base_donnees.etudiant import etudiants, engine
# Lancement d'une session de manipulation de données de la base
Session = sessionmaker(bind=engine)
session= Session()
etu= session.query(etudiants).all()
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, whitesmoke 
for etus in etu[:2]:
    carte= canvas.Canvas(f"Carte_{etus.nom}.pdf",pagesize=(243,153))
    carte.setFillColor(whitesmoke)
    carte.setStrokeColor(black)
    carte.setLineWidth(0.5)
    carte.rect(1,1,241,151, stroke=True,fill=True)
    carte.drawImage("C:\projet\multimedia\logo.jpg",10,108,width=50,height=35, preserveAspectRatio=True )
    carte.drawImage(etus.photo_path, 150,32,width=80,height=80,preserveAspectRatio=True)
    carte.setFont("Helvetica",9)
    carte.setFillColor(black)
    carte.drawString(120,10,"Fait a kinshasa 12/06/2025")
    carte.setFont("Helvetica-Bold",12)
    carte.setFillColor(black)
    carte.drawString(70,127,"CARTE D'ETUDIANT")
    texte= carte.beginText()
    texte.setTextOrigin(10,96)
    texte.setFont("Helvetica-Bold",10)
    texte.setFillColor(black)
    texte.textLine(f"Nom : {etus.nom.title()} ")
    texte.textLine(f"Post-nom : {etus.postnom.title()}")
    texte.textLine(f"Prenom : {etus.prenom.title()}")
    texte.textLine(f"Matricule :{etus.matricule.upper()}")
    texte.textLine(f"Promotion :{etus.promotion.upper()}")
    carte.drawText(texte)
    carte.save()
