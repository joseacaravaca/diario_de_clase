from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import A5

def lee_frases():
    """
    Lee las frases desde un archivo CSV y las devuelve como una lista de listas.
    """
    df = pd.read_csv('frases.csv')
    return df.values.tolist()

def create_overlay(page_number):
    """
    Crea un PDF en memoria con el número de página en la esquina superior izquierda.
    """
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A5)  # Tamaño de página A5

    # Número de página en la esquina superior izquierda
    can.setFont("Helvetica", 10)
    can.drawString(110,568, str(page_number))  # Coordenadas para el número de página en A5

    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def create_numbered_pdf(input_pdf_path, portada_path, trasera_path, output_pdf_path, copies, positions):
    """
    Crea un PDF con portada, páginas numeradas y trasera.
    """
    reader = PdfReader(input_pdf_path)
    portada = PdfReader(portada_path).pages[0]
    trasera = PdfReader(trasera_path).pages[0]
    writer = PdfWriter()
    frases = lee_frases()

    # Añadir la portada
    writer.add_page(portada)

    # Repetir y numerar las páginas
    for i in range(1, copies + 1):
        original_page = reader.pages[0]
        new_page = PageObject.create_blank_page(
            width=original_page.mediabox.width, height=original_page.mediabox.height
        )
        new_page.merge_page(original_page)

        # Crear la capa con el número de página
        page_number = i  # Número de página

        overlay = create_overlay(page_number)
        new_page.merge_page(overlay)

        # Agregar la página numerada al PDF final
        writer.add_page(new_page)

    # Añadir la página trasera
    writer.add_page(trasera)

    # Guardar el PDF resultante
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

# Configuración
input_pdf_path = "cuerpo.pdf"  # Ruta al PDF original
portada_path = "portada.pdf"            # Ruta al PDF de la portada
trasera_path = "trasera.pdf"            # Ruta al PDF de la trasera
output_pdf_path = "diario_de_clase.pdf"  # Ruta al PDF resultante
positions = [(110, 565), (110, 270), (30, 15)]  # Coordenadas (x, y) para los textos
# 
# Preguntar por el número de páginas
copies = input(f"Ingrese el número de copias. Valor por defecto: 40: ")
copies = int(copies) if copies.isdigit() else 40
# 


# Crear el PDF con portada, páginas numeradas y 
# trasera, incluyendo una linea de pie con frases del archivo frases csv
# en A5 para la EOI
create_numbered_pdf(input_pdf_path, portada_path, trasera_path, output_pdf_path, copies, positions)
print(f"PDF generado: {output_pdf_path}")
