from PIL import Image

path_image = "multimedia\logo_card_generator.jpg"
path_logo_ico = "multimedia\logo_card_generator.ico"

img= Image.open(path_image)
img.save(path_logo_ico, format='ICO', sizes= [(64,64)])

print("Conversion reussie ! Fichier crée:", path_logo_ico)