# streamlit_app.py
# Aplicación web interactiva profesional basada en Streamlit para SynthMind AI

import json
import streamlit as st
from gemini_engine import extract_text_from_file, run_gemini_analysis
from report_generator import generate_markdown_report, generate_html_report

# Configuración de página
st.set_page_config(
    page_title="SynthMind AI Enterprise Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar créditos en Session State
if "credits" not in st.session_state:
    st.session_state.credits = 3

# Estilos CSS de nivel corporativo
st.markdown("""
<style>
    .reportview-container {
        background: #090d16;
    }
    .badge {
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
        font-family: monospace;
    }
    .badge-fuerte { background-color: rgba(16, 185, 129, 0.12); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.25); }
    .badge-moderado { background-color: rgba(245, 158, 11, 0.12); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.25); }
    .badge-debil { background-color: rgba(239, 68, 68, 0.12); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.25); }
    
    .badge-alta { background-color: rgba(239, 68, 68, 0.12); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.25); }
    .badge-media { background-color: rgba(245, 158, 11, 0.12); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.25); }
    .badge-baja { background-color: rgba(148, 163, 184, 0.12); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.25); }

    .quote-block {
        border-left: 3px solid #10b981;
        padding: 8px 14px;
        font-style: italic;
        background-color: rgba(255, 255, 255, 0.02);
        margin: 8px 0;
        border-radius: 0 4px 4px 0;
        font-family: serif;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("SynthMind AI")
    st.caption("Enterprise Document Intelligence Engine")
    
    # Créditos
    st.info(f"Créditos de Evaluación Restantes: {st.session_state.credits} / 3")
    
    st.markdown("---")
    
    st.markdown("### Parámetros del Sistema")
    
    api_key_input = st.text_input(
        "Clave de API Gemini", 
        type="password",
        placeholder="AIzaSy...",
        help="Clave de API de Google AI Studio. Si se omite, se intentará usar la variable de entorno GEMINI_API_KEY."
    )
    
    model_name = st.selectbox(
        "Modelo de Lenguaje",
        options=["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
        help="Gemini 2.5 Flash para respuestas ultrarrápidas. Gemini 2.5 Pro para máxima capacidad analítica."
    )

    specialization = st.selectbox(
        "Enfoque Disciplinario",
        options=[
            ("general", "General / Corporativo"),
            ("academic", "Investigación Científica y Académica"),
            ("legal", "Auditoría Legal y Cumplimiento"),
            ("financial", "Análisis Financiero y Riesgo")
        ],
        index=0,
        format_func=lambda x: x[1],
        help="Modifica las directrices internas del motor agéntico según el dominio del texto."
    )[0]
    
    st.markdown("---")
    st.markdown("[Obtener API Key en Google AI Studio](https://aistudio.google.com/)")
    st.caption("SynthMind AI v2.0 | Licencia MIT")

# --- Cuerpo Principal ---
st.title("SynthMind AI — Plataforma de Análisis Agéntico Documental")
st.caption("Extracción de taxonomías, auditoría de inconsistencias y síntesis ejecutiva estructurada con Gemini 2.5.")

col_left, col_right = st.columns([2, 3])

with col_left:
    st.subheader("Carga de Fuente")
    uploaded_file = st.file_uploader("Documentos admitidos: PDF, TXT, MD", type=["pdf", "txt", "md"])

    st.subheader("Protocolo de Análisis")
    analysis_type = st.radio(
        "Seleccione la tarea a ejecutar:",
        options=[
            ("concepts", "Mapeo Conceptual y Tesis"),
            ("gaps", "Auditoría Crítica y Vacíos Empíricos"),
            ("synthesis", "Síntesis Ejecutiva y Fichas de Acción")
        ],
        format_func=lambda x: x[1]
    )[0]

    if st.session_state.credits <= 0:
        st.error("Límite de Evaluación Gratuita Alcanzado")
        st.markdown("""
        Ha consumido sus 3 créditos diarios de evaluación. 
        Para procesamiento ilimitado y exportación de informes ejecutivos, active la suscripción corporativa.
        
        [Activar Licencia Comercial (Stripe)](https://stripe.com)
        """)
        run_btn = st.button("Ejecutar Análisis Agéntico", disabled=True, use_container_width=True)
    else:
        run_btn = st.button("Ejecutar Análisis Agéntico", use_container_width=True)

with col_right:
    st.subheader("Consola de Resultados")
    
    if run_btn:
        if not uploaded_file:
            st.error("Debe cargar primero un archivo en formato PDF, TXT o MD.")
        else:
            file_bytes = uploaded_file.read()
            filename = uploaded_file.name
            
            with st.spinner("Procesando documento y ejecutando cadena de pensamiento agéntica..."):
                try:
                    document_text = extract_text_from_file(file_bytes, filename)
                    
                    if not document_text:
                        st.error("El documento no contiene texto legible.")
                    else:
                        result_raw = run_gemini_analysis(
                            document_text=document_text,
                            analysis_type=analysis_type,
                            api_key=api_key_input if api_key_input else None,
                            model_name=model_name,
                            specialization=specialization
                        )
                        
                        st.session_state["last_result"] = json.loads(result_raw)
                        st.session_state["last_type"] = analysis_type
                        st.session_state.credits -= 1
                        
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error durante el procesamiento: {str(e)}")

    if "last_result" in st.session_state and "last_type" in st.session_state:
        data = st.session_state["last_result"]
        dtype = st.session_state["last_type"]
        
        st.markdown("#### Opciones de Exportación")
        col_j, col_md, col_html = st.columns(3)
        
        with col_j:
            st.download_button(
                "Exportar JSON Raw",
                data=json.dumps(data, indent=2, ensure_ascii=False),
                file_name=f"synthmind_report_{dtype}.json",
                mime="application/json",
                use_container_width=True
            )
            
        with col_md:
            md_report = generate_markdown_report(data, dtype)
            st.download_button(
                "Exportar Word (MD)",
                data=md_report,
                file_name=f"synthmind_report_{dtype}.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with col_html:
            html_report = generate_html_report(data, dtype)
            st.download_button(
                "Reporte PDF (HTML)",
                data=html_report,
                file_name=f"synthmind_report_{dtype}.html",
                mime="text/html",
                use_container_width=True
            )

        st.markdown("---")

        if dtype == "concepts":
            metadata = data.get("document_metadata", {})
            concepts = data.get("core_concepts", [])
            arguments = data.get("key_arguments", [])
            taxonomy = data.get("conceptual_taxonomy", [])
            quality = data.get("data_quality_issues", [])

            t1, t2, t3, t4 = st.tabs(["Metadatos Fuente", "Conceptos Clave", "Hilos Argumentativos", "Taxonomía"])
            
            with t1:
                st.write(f"**Título:** {metadata.get('title', 'N/A')}")
                st.write(f"**Dominio:** {metadata.get('domain', 'N/A')}")
                st.write(f"**Tipo de Documento:** {metadata.get('document_type', 'N/A')}")
                st.write(f"**Idioma:** {metadata.get('language', 'N/A')}")
                st.write(f"**Autores:** {', '.join(metadata.get('authors', []))}")
                
                if quality:
                    st.warning("Observaciones sobre la fuente original:\n" + "\n".join([f"- {i}" for i in quality]))

            with t2:
                for c in concepts:
                    with st.expander(f"{c.get('concept_id')} — {c.get('name')} ({c.get('category')})"):
                        st.markdown(f"**Definición:** {c.get('definition')}")
                        st.markdown(f"**Índice de Certeza:** `{c.get('confidence_score')}`")
                        st.markdown("**Cita Textual:**")
                        st.markdown(f'<div class="quote-block">"{c.get("textual_quote")}"</div>', unsafe_allow_html=True)

            with t3:
                for arg in arguments:
                    rating = arg.get("strength_rating", "Moderado")
                    rating_class = f"badge-{rating.split('/')[0].strip().lower()}"
                    
                    st.markdown(f"""
                    ### {arg.get('argument_id')} — Tesis Principal
                    **Afirmación:** {arg.get('claim_statement')}  
                    <span class="badge {rating_class}">Solidez: {rating}</span>
                    """, unsafe_allow_html=True)
                    
                    st.write("**Evidencias de Respaldo:**")
                    for ev in arg.get("supporting_evidence", []):
                        st.write(f"- {ev}")
                    
                    if arg.get("counterarguments_mentioned"):
                        st.write("**Objeciones Consideradas:**")
                        for ca in arg.get("counterarguments_mentioned", []):
                            st.write(f"- *{ca}*")
                    
                    if arg.get("source_section"):
                        st.caption(f"Ubicación en fuente: {arg.get('source_section')}")
                    st.markdown("---")

            with t4:
                for tax in taxonomy:
                    st.markdown(f"**Concepto Padre:** `{tax.get('parent_concept')}`")
                    st.markdown(f"**Relación:** *{tax.get('relationship_type')}*")
                    st.markdown(f"**Conceptos Derivados:** {', '.join([f'`{i}`' for i in tax.get('child_concepts', [])])}")
                    st.markdown("---")

        elif dtype == "gaps":
            audit = data.get("audit_summary", {})
            contradictions = data.get("internal_contradictions", [])
            gaps = data.get("identified_gaps", [])
            questions = data.get("unanswered_research_questions", [])
            assumptions = data.get("unstated_assumptions", [])

            t1, t2, t3, t4 = st.tabs(["Auditoría Metodológica", "Contradicciones", "Vacíos Empíricos", "Preguntas Abiertas"])

            with t1:
                st.metric("Puntuación Global de Rigor", f"{audit.get('overall_rigor_score', 0)} / 10")
                st.markdown(f"**Resumen de Robustez:**\n{audit.get('methodological_robustness')}")
                st.markdown(f"**Sesgo Principal Identificado:**\n*{audit.get('primary_bias_detected', 'Ninguno detectado')}*")
                
                if assumptions:
                    st.markdown("---")
                    st.markdown("#### Supuestos Implícitos del Autor")
                    for a in assumptions:
                        st.write(f"- {a}")

            with t2:
                if not contradictions:
                    st.info("No se identificaron contradicciones internas en el documento.")
                for c in contradictions:
                    st.error(f"Contradicción {c.get('contradiction_id')} (Impacto: {c.get('impact_level')})")
                    st.markdown(f"**Premisa A:** *\"{c.get('statement_a')}\"*")
                    st.markdown(f"**Premisa B (Opuesta):** *\"{c.get('statement_b')}\"*")
                    st.info(f"**Análisis de la Inconsistencia:** {c.get('analysis')}")
                    st.markdown("---")

            with t3:
                for g in gaps:
                    st.markdown(f"**[{g.get('gap_id')}] — Brecha: {g.get('category')}**")
                    st.write(f"**Descripción:** {g.get('description')}")
                    st.write(f"**Evidencia requerida:** *{g.get('missing_evidence')}*")
                    st.markdown("---")

            with t4:
                for q in questions:
                    st.markdown(f"**{q.get('question_id')}** — *{q.get('question')}*")
                    st.markdown(f"**Relevancia:** {q.get('relevance')}")
                    st.markdown("---")

        elif dtype == "synthesis":
            summary = data.get("executive_summary", {})
            cards = data.get("synthesis_cards", [])
            recommendations = data.get("strategic_recommendations", [])

            t1, t2, t3 = st.tabs(["Resumen TL;DR", "Fichas de Acción", "Plan Estratégico"])

            with t1:
                st.info(f"**TL;DR:** {summary.get('tldr')}")
                st.markdown(f"**Narrativa Central:**\n{summary.get('core_narrative')}")
                st.markdown(f"**Audiencia Objetivo:** `{summary.get('target_audience')}`")
                st.markdown("---")
                st.markdown("#### Conclusiones Clave")
                for item in summary.get("key_takeaways", []):
                    st.markdown(f"- {item}")

            with t2:
                for card in cards:
                    priority = card.get("priority_level", "Baja")
                    priority_class = f"badge-{priority.lower()}"
                    
                    st.markdown(f"""
                    ### {card.get('card_id')} — {card.get('topic')}
                    **Hallazgo Clave:** {card.get('core_insight')}  
                    <span class="badge {priority_class}">Prioridad: {priority}</span>
                    """, unsafe_allow_html=True)
                    
                    st.info(f"**Implicación Operativa:** {card.get('actionable_implication')}")
                    
                    if card.get("key_metrics_or_data"):
                        st.markdown("**Métricas Asociadas:**")
                        for m in card.get("key_metrics_or_data", []):
                            st.code(m)
                    st.markdown("---")

            with t3:
                for rec in recommendations:
                    st.markdown(f"### Paso {rec.get('step_number')}: {rec.get('action_title')}")
                    st.write(rec.get("description"))
                    st.markdown("---")

    else:
        st.info("Cargue un documento y ejecute el análisis agéntico para visualizar los resultados.")
