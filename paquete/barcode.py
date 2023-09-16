from paquete import models
from CSEPcon.settings import os,MEDIA_ROOT,MEDIA_URL
from barcode.writer import ImageWriter
import barcode
from io import BytesIO

file_folder = f'{MEDIA_ROOT}barCode'

def barcode_Code39(text):
    EAN = barcode.get_barcode_class('Code39')
    my_ean = EAN(text, writer=ImageWriter(),add_checksum=False)
    fullname = f'{text}.png'
    fp = BytesIO()
    my_ean.write(fp)
    folder_barcode=f'{file_folder}/'
    if not os.path.exists(folder_barcode):
        os.makedirs(folder_barcode)
    with open(f"{folder_barcode}{fullname}", "wb") as f:
        my_ean.write(f)
    return f"barCode/{fullname}"


def barcode_2():
    paquete= models.paquete.objects.filter(paq_barCode__isnull= True)
    for i in paquete:
        i.paq_barCode= barcode_Code39(i.paq_numero)
        i.save()
    return None


barcode_2()
