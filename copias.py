from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from io import BytesIO
import pandas as pd

def lee_frases():
    """
    Lee las frases desde un archivo CSV y las devuelve como una lista de listas.
    """
    df = pd.read_csv('frases.csv')
    return df.values.tolist()

def create_overlay(text1, x1, y1, text2, x2, y2, text3, x3, y3):
    """
    Crea un PDF en memoria con tres textos en las coordenadas especificadas.
    """
    packet = BytesIO()
    can = canvas.Canvas(packet)

    # Configuración de las fuentes
    can.setFont("Helvetica", 12)  # Tamaño para los números
    can.drawString(x1, y1, text1)  # Primer número
    can.drawString(x2, y2, text2)  # Segundo número

    can.setFont("Helvetica", 8)   # Tamaño más pequeño para la frase
    can.drawString(x3, y3, text3)  # Frase

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

        # Crear la capa con los textos y números
        text1 = str((i * 2) - 1)  # Número impar
        text2 = str(i * 2)        # Número par
        text3 = str(frases[i - 1]).replace("]", "").replace("[", "").replace("'", "")  # Frase

        x1, y1 = positions[0]     # Coordenadas para el primer número
        x2, y2 = positions[1]     # Coordenadas para el segundo número
        x3, y3 = positions[2]     # Coordenadas para la frase

        overlay = create_overlay(text1, x1, y1, text2, x2, y2, text3, x3, y3)
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
copies = input(f"Ingrese el número de copias. Valor por defecto: 40, (80 fichas): ")
copies = int(copies) if copies.isdigit() else 40
# 


# Crear el PDF con portada, páginas numeradas y 
# trasera, incluyendo una linea de pie con frases del archivo frases csv
# en A5 paraka EOI
create_numbered_pdf(input_pdf_path, portada_path, trasera_path, output_pdf_path, copies, positions)
print(f"PDF generado: {output_pdf_path}")
