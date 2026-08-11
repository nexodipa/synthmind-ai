# gemini_engine.py
# Motor Agéntico de Análisis Documental utilizando la API de Gemini 2.5 (Google GenAI SDK)
# Implementación estricta con Pydantic, Chain-of-Thought y salida JSON formal

import io
import os
from typing import List, Optional
from pydantic import BaseModel, Field
from pypdf import PdfReader
from google import genai
from google.genai import types

# =====================================================================
# 1. Esquemas JSON Tipados con Pydantic
# =====================================================================

class DocumentMetadata(BaseModel):
    title: str = Field(description="Título principal identificado del documento.")
    authors: List[str] = Field(default_factory=list, description="Lista de autores o entidad emisora.")
    domain: str = Field(description="Dominio del conocimiento (ej. Biotecnología, Finanzas, Derecho).")
    document_type: str = Field(description="Tipo de documento (ej. Artículo Científico, Contrato, Reporte Financiero).")
    language: str = Field(description="Idioma principal del texto.")

class CoreConcept(BaseModel):
    concept_id: str = Field(description="Identificador único del concepto (ej. C01, C02).")
    name: str = Field(description="Nombre preciso del concepto clave.")
    category: str = Field(description="Categoría o tipo (ej. Metodología, Definición, Métrica).")
    definition: str = Field(description="Definición o síntesis conceptual procesada.")
    confidence_score: float = Field(description="Índice de certeza de la extracción entre 0.0 y 1.0.")
    textual_quote: str = Field(description="Cita textual exacta extraída del documento que sirve de evidencia.")

class KeyArgument(BaseModel):
    argument_id: str = Field(description="Identificador único (ej. ARG01, ARG02).")
    claim_statement: str = Field(description="Tesis central o afirmación principal planteada por el autor.")
    supporting_evidence: List[str] = Field(description="Lista de evidencias textuales o cuantitativas que respaldan la afirmación.")
    counterarguments_mentioned: List[str] = Field(default_factory=list, description="Objeciones o contraargumentos abordados en el texto.")
    strength_rating: str = Field(description="Evaluación de solidez del argumento: 'Fuerte', 'Moderado' o 'Débil'.")
    source_section: Optional[str] = Field(default=None, description="Sección o página aproximada donde se ubica.")

class ConceptualTaxonomyNode(BaseModel):
    parent_concept: str = Field(description="Concepto o categoría superior.")
    child_concepts: List[str] = Field(description="Lista de subconceptos o derivados.")
    relationship_type: str = Field(description="Tipo de relación (ej. 'Jerárquica', 'Causal', 'Complementaria').")

class ConceptAndArgumentMapSchema(BaseModel):
    document_metadata: DocumentMetadata
    core_concepts: List[CoreConcept]
    key_arguments: List[KeyArgument]
    conceptual_taxonomy: List[ConceptualTaxonomyNode]
    data_quality_issues: List[str] = Field(default_factory=list, description="Problemas detectados como OCR fragmentado o texto incompleto.")


class InternalContradiction(BaseModel):
    contradiction_id: str = Field(description="Identificador único (ej. ERR01).")
    statement_a: str = Field(description="Primera afirmación identificada en el texto.")
    statement_b: str = Field(description="Segunda afirmación en el texto que contradice a la primera.")
    analysis: str = Field(description="Explicación detallada de la incompatibilidad lógica.")
    impact_level: str = Field(description="Nivel de impacto: 'Crítico', 'Moderado' o 'Menor'.")

class IdentifiedGap(BaseModel):
    gap_id: str = Field(description="Identificador único (ej. GAP01).")
    category: str = Field(description="Tipo de vacío: 'Empírico', 'Metodológico', 'Teórico' o 'Normativo'.")
    description: str = Field(description="Descripción clara de la omisión o falta de evidencia.")
    missing_evidence: str = Field(description="Especifique qué datos o pruebas adicionales se requerirían.")

class UnansweredQuestion(BaseModel):
    question_id: str = Field(description="Identificador único (ej. Q01).")
    question: str = Field(description="Pregunta de investigación relevante que el texto omite o deja abierta.")
    relevance: str = Field(description="Justificación de la importancia de esta pregunta.")

class CriticalAnalysisAndGapsSchema(BaseModel):
    audit_summary: dict = Field(description="Resumen global de rigor lógico, puntuación de 1 a 10 y sesgo identificado.")
    internal_contradictions: List[InternalContradiction]
    identified_gaps: List[IdentifiedGap]
    unanswered_research_questions: List[UnansweredQuestion]
    unstated_assumptions: List[str] = Field(description="Supuestos implícitos no expresados explícitamente por el autor.")


class ExecutiveSummary(BaseModel):
    tldr: str = Field(description="Resumen de máximo 2 oraciones (TL;DR).")
    core_narrative: str = Field(description="Síntesis narrativa ejecutiva de alto nivel (2-3 párrafos).")
    target_audience: str = Field(description="Público o perfil profesional a quien está dirigido el reporte.")
    key_takeaways: List[str] = Field(description="De 3 a 5 conclusiones de alto impacto.")

class SynthesisCard(BaseModel):
    card_id: str = Field(description="Identificador único (ej. CARD01).")
    topic: str = Field(description="Tema o área de enfoque.")
    priority_level: str = Field(description="Prioridad: 'Alta', 'Media' o 'Baja'.")
    core_insight: str = Field(description="Hallazgo sintético clave.")
    actionable_implication: str = Field(description="Implicación directa para la toma de decisiones.")
    key_metrics_or_data: List[str] = Field(default_factory=list, description="Cifras o datos clave asociados.")

class StrategicRecommendation(BaseModel):
    step_number: int = Field(description="Número de secuencia ejecutiva.")
    action_title: str = Field(description="Título formal de la recomendación.")
    description: str = Field(description="Detalle del plan de acción sugerido.")

class ExecutiveSynthesisCardsSchema(BaseModel):
    executive_summary: ExecutiveSummary
    synthesis_cards: List[SynthesisCard]
    strategic_recommendations: List[StrategicRecommendation]


# =====================================================================
# 2. System Prompt Oficial (Chain-of-Thought + Protocolo Formal)
# =====================================================================

SYSTEM_PROMPT = """
Eres SynthMind AI, un motor agéntico de nivel enterprise diseñado para el análisis crítico, extracción estructurada de conocimientos y auditoría formal de documentos densos.

INSTRUCCIONES DE RAZONAMIENTO Y ESTILO:
- Tono Formal y Corporativo: Utiliza un lenguaje preciso, riguroso y objetivo. No uses emoticonos, lenguaje informal ni giros coloquiales en tus respuestas.
- Proceso de Razonamiento (Chain-of-Thought): 
  1. Escanea el texto fuente identificando la arquitectura de argumentos, metodología y evidencia presentada.
  2. Evalúa la solidez de las afirmaciones contrastándolas con la evidencia proporcionada.
  3. Estructura los hallazgos en un formato jerárquico impecable y libre de redundancias.
- Respaldo Riguroso: Toda cita o evidencia textual debe ser extraída fielmente del documento original sin fabricar información.

Debes devolver ÚNICAMENTE el objeto JSON estricto correspondiente al esquema configurado.
"""


# =====================================================================
# 3. Funciones de Extracción y Generación
# =====================================================================

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """
    Extrae el contenido textual de archivos PDF, TXT y MD.
    """
    if filename.lower().endswith('.pdf'):
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    else:
        try:
            return file_content.decode('utf-8').strip()
        except UnicodeDecodeError:
            return file_content.decode('latin-1').strip()


def run_gemini_analysis(
    document_text: str,
    analysis_type: str,
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash",
    specialization: str = "general"
) -> str:
    """
    Llama a la API de Gemini aplicando el esquema estructurado Pydantic y las directrices del nicho.
    """
    resolved_api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not resolved_api_key:
        raise ValueError("API Key de Gemini no encontrada. Configúrela en el entorno o proporciónela en la interfaz.")

    client = genai.Client(api_key=resolved_api_key)

    if analysis_type == "concepts":
        schema = ConceptAndArgumentMapSchema
        prompt_instruction = "Ejecute la extracción estructurada de conceptos clave, tesis y taxonomía del siguiente texto:"
    elif analysis_type == "gaps":
        schema = CriticalAnalysisAndGapsSchema
        prompt_instruction = "Ejecute la auditoría crítica de consistencia lógica, vacíos empíricos e inconsistencias del siguiente texto:"
    elif analysis_type == "synthesis":
        schema = ExecutiveSynthesisCardsSchema
        prompt_instruction = "Ejecute la síntesis ejecutiva, fichas operativas y recomendaciones del siguiente texto:"
    else:
        raise ValueError(f"Tipo de análisis no válido: {analysis_type}")

    system_instruction = SYSTEM_PROMPT
    if specialization == "academic":
        system_instruction += "\nDIRECTRIZ DISCIPLINARIA (ACADÉMICA Y CIENTÍFICA): Priorice la evaluación de hipótesis empíricas, metodología experimental, validez de muestra y contribuciones teóricas al estado del arte."
    elif specialization == "legal":
        system_instruction += "\nDIRECTRIZ DISCIPLINARIA (JURÍDICA Y CUMPLIMIENTO): Concéntrese en la asignación de responsabilidades, cláusulas de riesgo, contradicciones normativas y grado de cumplimiento regulatorio."
    elif specialization == "financial":
        system_instruction += "\nDIRECTRIZ DISCIPLINARIA (FINANCIERA Y NEGOCIOS): Enfoque el análisis en métricas operativas (ROI, EBITDA, ingresos), hipótesis de mercado, consistencia en balances y proyecciones de riesgo comercial."

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.1,
        response_mime_type="application/json",
        response_schema=schema,
    )

    response = client.models.generate_content(
        model=model_name,
        contents=f"{prompt_instruction}\n\n{document_text}",
        config=config,
    )

    return response.text
