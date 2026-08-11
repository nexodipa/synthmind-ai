# test_app.py
# Suite de pruebas unitarias para SynthMind AI

import pytest
from unittest.mock import MagicMock, patch
from gemini_engine import extract_text_from_file, run_gemini_analysis
from fastapi.testclient import TestClient
from app import app

client_test = TestClient(app)

# =====================================================================
# 1. Pruebas de Extracción de Texto
# =====================================================================

def test_extract_text_txt():
    """
    Prueba que se extraiga texto correctamente de archivos de texto plano.
    """
    sample_text = b"Hola, este es un texto de prueba para SynthMind AI."
    extracted = extract_text_from_file(sample_text, "test.txt")
    assert extracted == "Hola, este es un texto de prueba para SynthMind AI."


def test_extract_text_md():
    """
    Prueba que se extraiga texto correctamente de archivos Markdown.
    """
    sample_text = b"# Titulo\nEste es un documento markdown."
    extracted = extract_text_from_file(sample_text, "document.md")
    assert "# Titulo\nEste es un documento markdown." in extracted


@patch('gemini_engine.PdfReader')
def test_extract_text_pdf(mock_pdf_reader):
    """
    Prueba la extracción de texto en PDFs simulando (mocking) el PdfReader.
    """
    # Configurar mock de página de pypdf
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Texto extraido de la pagina PDF."
    
    mock_reader_instance = MagicMock()
    mock_reader_instance.pages = [mock_page]
    mock_pdf_reader.return_value = mock_reader_instance
    
    extracted = extract_text_from_file(b"dummy_pdf_bytes", "test.pdf")
    assert extracted == "Texto extraido de la pagina PDF."
    mock_pdf_reader.assert_called_once()

# =====================================================================
# 2. Pruebas del Motor de Gemini (Mockeando el Cliente GenAI)
# =====================================================================

@patch('gemini_engine.genai.Client')
def test_run_gemini_analysis(mock_genai_client):
    """
    Prueba que el motor haga las llamadas a Gemini con el esquema correcto.
    """
    # Configurar mock de respuesta
    mock_response = MagicMock()
    mock_response.text = '{"document_metadata": {"title": "Test doc", "domain": "Science", "document_type": "Report", "language": "es"}, "core_concepts": [], "key_arguments": [], "conceptual_taxonomy": [], "data_quality_issues": []}'
    
    mock_client_instance = MagicMock()
    mock_client_instance.models.generate_content.return_value = mock_response
    mock_genai_client.return_value = mock_client_instance
    
    res = run_gemini_analysis(
        document_text="Este es el texto del documento para analizar.",
        analysis_type="concepts",
        api_key="TEST_API_KEY",
        model_name="gemini-2.5-flash"
    )
    
    assert "Test doc" in res
    mock_genai_client.assert_called_once_with(api_key="TEST_API_KEY")
    mock_client_instance.models.generate_content.assert_called_once()

# =====================================================================
# 3. Pruebas de Endpoints de FastAPI
# =====================================================================

def test_fastapi_index_endpoint():
    """
    Prueba que la ruta raiz devuelva la SPA HTML.
    """
    response = client_test.get("/")
    assert response.status_code == 200
    assert "SynthMind AI" in response.text
    assert "tail" in response.text  # Tailwind import

@patch('app.run_gemini_analysis')
def test_fastapi_analyze_endpoint_invalid_file(mock_run_analysis):
    """
    Prueba que el endpoint falle si el archivo no tiene la extensión correcta.
    """
    response = client_test.post(
        "/api/analyze",
        files={"file": ("test.png", b"dummy_content", "image/png")},
        data={"analysis_type": "concepts", "model": "gemini-2.5-flash"}
    )
    assert response.status_code == 400
    assert "Tipo de archivo no permitido" in response.json()["detail"]
    mock_run_analysis.assert_not_called()
