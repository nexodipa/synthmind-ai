# gemini_engine.py
# Motor Agéntico de Análisis y Síntesis de Documentos utilizando el SDK google-genai

import os
import io
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from pypdf import PdfReader
from google import genai
from google.genai import types

# =====================================================================
# 1. Definición de Esquemas JSON Estructurados vía Pydantic
# =====================================================================

# --- ESQUEMA A: Mapeo Conceptual y Argumentos ---
class DocumentMetadata(BaseModel):
    title: str = Field(description="Título principal o tema central del documento.")
    authors: List[str] = Field(default=[], description="Lista de autores o entidad creadora.")
    domain: str = Field(description="Dominio disciplinario (ej. Psicología Organizacional, Neurociencia, Finanzas, etc.).")
    document_type: str = Field(description="Tipo de documento (ej. Artículo Científico, Reporte Técnico, Ensayo, Whitepaper).")
    language: str = Field(description="Idioma principal del texto analizado.")

class CoreConcept(BaseModel):
    concept_id: str = Field(description="Identificador único (ej. CON-001).")
    name: str = Field(description="Nombre del concepto o término especializado.")
    definition: str = Field(description="Definición dada por el autor o deducida del contexto.")
    category: str = Field(description="Categoría o nodo taxonómico al que pertenece.")
    textual_quote: str = Field(description="Cita textual que respalda o define el concepto.")
    confidence_score: float = Field(description="Grado de certeza del modelo sobre la extracción (0.0 a 1.0).")

class KeyArgument(BaseModel):
    argument_id: str = Field(description="Identificador único (ej. ARG-001).")
    claim_statement: str = Field(description="Declaración o tesis del argumento.")
    supporting_evidence: List[str] = Field(default=[], description="Datos, estudios o razonamientos que respaldan la tesis.")
    counterarguments_mentioned: List[str] = Field(default=[], description="Objeciones o posturas contrarias abordadas en el texto.")
    strength_rating: str = Field(description="Evaluación del rigor y respaldo del argumento. Debe ser: Fuerte, Moderado o Débil / Especulativo")
    source_section: Optional[str] = Field(default=None, description="Sección, capítulo o número de página aproximado.")

class ConceptualTaxonomy(BaseModel):
    parent_concept: str = Field(description="Concepto o categoría superior.")
    child_concepts: List[str] = Field(default=[], description="Subconceptos o componentes derivados.")
    relationship_type: str = Field(description="Tipo de relación (ej. 'es un tipo de', 'causa', 'contradice', 'complementa').")

class ConceptAndArgumentMapSchema(BaseModel):
    document_metadata: DocumentMetadata
    core_concepts: List[CoreConcept]
    key_arguments: List[KeyArgument]
    conceptual_taxonomy: List[ConceptualTaxonomy]
    data_quality_issues: List[str] = Field(default=[], description="Observaciones sobre fragmentación, imprecisiones u OCR defectuoso en la fuente.")


# --- ESQUEMA B: Auditoría Crítica y Gaps ---
class AuditSummary(BaseModel):
    overall_rigor_score: float = Field(description="Puntaje general de rigor y coherencia (0.0 a 10.0).")
    methodological_robustness: str = Field(description="Resumen del rigor metodológico o empírico.")
    primary_bias_detected: str = Field(description="Sesgo principal identificado en la perspectiva del autor o estudio.")

class InternalContradiction(BaseModel):
    contradiction_id: str = Field(description="Identificador (ej. CTR-001).")
    statement_a: str = Field(description="Primera afirmación o dato presente en el texto.")
    statement_b: str = Field(description="Segunda afirmación o dato que la contradice dentro del texto.")
    analysis: str = Field(description="Explicación de la inconsistencia detectada.")
    impact_level: str = Field(description="Impacto de la contradicción en la tesis global. Debe ser: Crítico, Moderado o Menor")

class IdentifiedGap(BaseModel):
    gap_id: str = Field(description="Identificador (ej. GAP-001).")
    category: str = Field(description="Categoría de la brecha. Debe ser: Metodológica, Empírica, Teórica, Muestral o Contextual")
    description: str = Field(description="Detalle explícito de lo que omite o no justifica el texto.")
    missing_evidence: str = Field(description="Tipo de dato o prueba que se requeriría para validar la afirmación.")

class UnansweredResearchQuestion(BaseModel):
    question_id: str = Field(description="Identificador (ej. REQ-001).")
    question: str = Field(description="Pregunta de investigación formulada.")
    relevance: str = Field(description="Por qué esta pregunta es vital para el desarrollo del área.")

class CriticalAnalysisAndGapsSchema(BaseModel):
    audit_summary: AuditSummary
    internal_contradictions: List[InternalContradiction]
    identified_gaps: List[IdentifiedGap]
    unanswered_research_questions: List[UnansweredResearchQuestion]
    unstated_assumptions: List[str] = Field(default=[], description="Supuestos implícitos no demostrados que da por sentados el autor.")


# --- ESQUEMA C: Resumen Ejecutivo y Síntesis Accionable ---
class ExecutiveSummary(BaseModel):
    tldr: str = Field(description="Resumen ejecutivo en 2-3 oraciones clave.")
    core_narrative: str = Field(description="Síntesis estructurada del argumento central y contexto.")
    key_takeaways: List[str] = Field(default=[], description="Puntos de inflexión o hallazgos más determinantes (4-6 ítems).")
    target_audience: str = Field(description="Perfil o rol para el cual esta síntesis es relevante (ej. Directivos, Investigadores, etc.).")

class SynthesisCard(BaseModel):
    card_id: str = Field(description="Identificador (ej. CRD-001).")
    topic: str = Field(description="Tema o módulo de conocimiento de la tarjeta.")
    core_insight: str = Field(description="Hallazgo clave condensado.")
    actionable_implication: str = Field(description="Qué se debe hacer o cómo aplicar este hallazgo en la práctica.")
    priority_level: str = Field(description="Grado de urgencia o relevancia práctica. Debe ser: Alta, Media o Baja")
    key_metrics_or_data: List[str] = Field(default=[], description="Cifras, métricas o referencias de respaldo si existen.")

class StrategicRecommendation(BaseModel):
    step_number: int = Field(description="Orden secuencial de la recomendación.")
    action_title: str = Field(description="Título breve de la acción recomendada.")
    description: str = Field(description="Detalle de ejecución sugerido basado en el análisis del documento.")

class ExecutiveSynthesisCardsSchema(BaseModel):
    executive_summary: ExecutiveSummary
    synthesis_cards: List[SynthesisCard]
    strategic_recommendations: List[StrategicRecommendation]


# =====================================================================
# 2. System Prompt de Producción
# =====================================================================
SYSTEM_PROMPT = """
ROL Y MISIÓN PRINCIPAL:
Eres SynthMind AI, un motor agéntico de investigación y análisis vertical de documentos complejos (artículos científicos, reportes financieros, consultoría, literatura técnica y académica). Tu objetivo principal es descomponer textos densos en conocimiento estructurado, identificar incoherencias o vacíos lógicos con precisión quirúrgica, y generar síntesis altamente accionables sin pérdida de rigor.

INSTRUCCIONES DE RAZONAMIENTO AGÉNTICO (CHAIN-OF-THOUGHT & REFLECTION):
Antes de emitir cualquier salida estructurada, debes ejecutar internamente las siguientes fases agénticas:
1. FASE DE COMPRENSIÓN Y DESGLOSE (Parse & Deconstruct): Escanea el documento completo identificando la tesis principal, metodología, hipótesis y conceptos clave.
2. FASE DE AUDITORÍA CRÍTICA (Critical Audit & Gap Spotting): Evalúa la solidez de los argumentos. Busca contradicciones, afirmaciones sin respaldo empírico y sesgos.
3. FASE DE SÍNTESIS Y ACCIONABILIDAD (Synthesis & Mapping): Condensa la información en estructuras jerárquicas y tarjetas operativas con citas de respaldo.
4. FASE DE AUTO-CORRECCIÓN Y REVISIÓN (Self-Correction & Schema Verification): Valida que las afirmaciones estén fundamentadas. Toda afirmación debe estar respaldada por citas.

MANEJO DE CASOS LÍMITE:
- OCR Defectuoso/Texto Fragmentado: Registra problemas en 'data_quality_issues' y analiza lo inteligible.
- Contradicciones: No las reconcilies arbitrariamente, reporta ambas posturas.
- Cero Alucinaciones: Usa estrictamente citas directas o paráfrasis fieles del texto original.
- Idioma: Responde siempre en el idioma principal del documento fuente (o en el idioma solicitado por el usuario).

Debes devolver ÚNICAMENTE un objeto JSON válido conforme al esquema requerido.
"""

# =====================================================================
# 3. Funciones del Motor Agéntico
# =====================================================================

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """
    Extrae el texto de un archivo PDF, de texto plano (.txt) o Markdown (.md).
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
        # Asumir texto plano/UTF-8 para txt y md
        try:
            return file_content.decode('utf-8').strip()
        except UnicodeDecodeError:
            return file_content.decode('latin-1').strip()


def run_gemini_analysis(
    document_text: str,
    analysis_type: str,
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash"
) -> str:
    """
    Realiza la llamada a la API de Gemini configurando la salida estructurada
    según el tipo de análisis solicitado.
    """
    # 1. Resolver API Key (Entorno o parámetro dinámico)
    resolved_api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not resolved_api_key:
        raise ValueError("No se ha configurado la API Key de Gemini. Configúrala en el entorno o pásala como parámetro.")

    # 2. Inicializar cliente
    client = genai.Client(api_key=resolved_api_key)

    # 3. Seleccionar el esquema correspondiente
    if analysis_type == "concepts":
        schema = ConceptAndArgumentMapSchema
        prompt_instruction = "Realiza la extracción estructurada de conceptos y argumentos del siguiente documento:"
    elif analysis_type == "gaps":
        schema = CriticalAnalysisAndGapsSchema
        prompt_instruction = "Realiza la auditoría crítica de brechas, contradicciones e inconsistencias del siguiente documento:"
    elif analysis_type == "synthesis":
        schema = ExecutiveSynthesisCardsSchema
        prompt_instruction = "Genera el resumen ejecutivo y las tarjetas de síntesis accionable del siguiente documento:"
    else:
        raise ValueError(f"Tipo de análisis no válido: {analysis_type}")

    # 4. Configurar la llamada
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.1,  # Temperatura baja para máxima precisión
        response_mime_type="application/json",
        response_schema=schema,
    )

    # 5. Ejecutar generación
    response = client.models.generate_content(
        model=model_name,
        contents=f"{prompt_instruction}\n\n{document_text}",
        config=config,
    )

    return response.text
