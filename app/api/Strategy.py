from typing import Optional

from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from app.core.ports import DocumentExtractorStrategy

# Estrategia concreta para PDFs
class PDFExtractionStrategy(DocumentExtractorStrategy):
    def extract_content(self, file_path: str) -> Optional[str]:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:  # Verifica que se haya extraído texto
                    text += page_text + "\n"  # Agrega un salto de línea entre páginas
            return text.strip()  # Elimina espacios en blanco al inicio y al final
        except Exception as e:
            print(f"Error al extraer contenido del PDF: {e}")
            return None  # Retorna None en caso de error


# Estrategia concreta para DOCX
class DocxExtractionStrategy(DocumentExtractorStrategy):
    def extract_content(self, file_path: str) -> Optional[str]:
        try:
            doc = DocxDocument(file_path)
            # Extraer texto de cada párrafo y unirlos con saltos de línea
            text = "\n".join(para.text for para in doc.paragraphs if para.text)  # Filtrar párrafos vacíos
            return text.strip()  # Eliminar espacios en blanco al inicio y al final
        except Exception as e:
            print(f"Error al extraer contenido del DOCX: {e}")
            return None  # Retorna None en caso de error