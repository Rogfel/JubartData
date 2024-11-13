from scrapping.utils import download_image


LINK = 'https://folhetos.paodeacucar.com/minuto/pubs/sv00050541_pa_semanal_minuto_sp/files/large/'



def download_imagens(path='imagens_paodeacucar'):
    for i in range(1,5):
        download_image(LINK + str(i) + '.jpg', path=path)
