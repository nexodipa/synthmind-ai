# streamlit_app.py
# Aplicación web interactiva alternativa basada en Streamlit, lista para Streamlit Community Cloud

import json
import streamlit as st
from gemini_engine import extract_text_from_file, run_gemini_analysis
from report_generator import generate_markdown_report, generate_html_report

# Configuración de página
st.set_page_config(
    page_title="SynthMind AI - Análisis Agéntico Documental",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar créditos en Session State
if "credits" not in st.session_state:
    st.session_state.credits = 3

# Estilos CSS personalizados para mejorar la estética oscura
st.markdown("""
<style>
    .reportview-container {
        background: #05070c;
    }
    .badge {
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-fuerte { background-color: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
    .badge-moderado { background-color: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }
    .badge-debil { background-color: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    
    .badge-alta { background-color: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    .badge-media { background-color: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }
    .badge-baja { background-color: rgba(100, 116, 139, 0.15); color: #94a3b8; border: 1px solid rgba(100, 116, 139, 0.2); }

    .quote-block {
        border-left: 3px solid #10b981;
        padding-left: 10px;
        font-style: italic;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 0 4px 4px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/brain.png", width=64)
    st.title("SynthMind AI")
    
    # Mostrar indicador de créditos
    st.info(f"⚡ **Créditos Gratuitos Restantes:** {st.session_state.credits} / 3")
    
    st.markdown("---")
    
    st.subheader("⚙️ Configuración")
    
    # Entrada de API Key
    api_key_input = st.text_input(
        "Gemini API Key", 
        type="password",
        placeholder="AIzaSy...",
        help="Obtén tu clave de API gratuita en Google AI Studio. Si se deja en blanco, la app intentará leer la variable de entorno GEMINI_API_KEY."
    )
    
    # Selección de Modelo
    model_name = st.selectbox(
        "Modelo Inteligente",
        options=["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
        help="Gemini 2.5 Flash es rápido y económico. Gemini 2.5 Pro es recomendado para razonamientos extensos o complejos."
    )

    # Selección de Especialización
    specialization = st.selectbox(
        "Efoque de Especialización",
        options=[
            ("general", "General (Estándar)"),
            ("academic", "Investigación Académica"),
            ("legal", "Auditoría Jurídica / Legal"),
            ("financial", "Finanzas y Negocios")
        ],
        index=0,
        format_func=lambda x: x[1],
        help="Ajusta las directrices internas del Agente de IA para enfocarse en un área disciplinaria específica."
    )[0]
    
    st.markdown("---")
    st.markdown("💡 [Obtener API Key Gratis](https://aistudio.google.com/)")
    st.markdown("MIT License | © 2026 SynthMind AI")

# --- Cuerpo Principal ---
st.title("🧠 SynthMind AI — Análisis Agéntico Documental")
st.caption("Analiza, sintetiza y audita críticamente reportes y artículos utilizando razonamiento en cadena de pensamiento (Chain-of-Thought) estructurado.")

# Columnas principales
col_left, col_right = st.columns([2, 3])

with col_left:
    st.subheader("📂 Cargar Documento")
    uploaded_file = st.file_uploader("Sube un archivo PDF, de Texto (.txt) o Markdown (.md)", type=["pdf", "txt", "md"])

    st.subheader("⚡ Tarea Agéntica")
    analysis_type = st.radio(
        "Selecciona el tipo de análisis:",
        options=[
            ("concepts", "🔍 Mapeo Conceptual y Argumentos"),
            ("gaps", "⚖️ Auditoría Crítica y Brechas"),
            ("synthesis", "📋 Resumen Ejecutivo y Fichas")
        ],
        format_func=lambda x: x[1]
    )[0]

    # Lógica de Paywall / Botón de análisis
    if st.session_state.credits <= 0:
        st.error("⚠️ **Límite Gratuito Alcanzado**")
        st.markdown("""
        Has agotado tus 3 análisis diarios de cortesía. 
        Para seguir procesando documentos de forma ilimitada y desbloquear las exportaciones automáticas de reportes, adquiere el plan Pro.
        
        👉 **[Suscribirse a SynthMind AI Premium (Stripe)](https://stripe.com)**
        """)
        run_btn = st.button("🚀 Iniciar Análisis Agéntico (Bloqueado)", disabled=True, use_container_width=True)
    else:
        run_btn = st.button("🚀 Iniciar Análisis Agéntico", use_container_width=True)

with col_right:
    st.subheader("📊 Resultados del Análisis")
    
    if run_btn:
        if not uploaded_file:
            st.error("Por favor, sube primero un archivo antes de realizar el análisis.")
        else:
            file_bytes = uploaded_file.read()
            filename = uploaded_file.name
            
            with st.spinner("Ejecutando fases agénticas: Comprensión, Auditoría y Reflexión en la nube..."):
                try:
                    # 1. Extraer texto
                    document_text = extract_text_from_file(file_bytes, filename)
                    
                    if not document_text:
                        st.error("El documento cargado no contiene texto legible.")
                    else:
                        # 2. Ejecutar llamada al motor
                        result_raw = run_gemini_analysis(
                            document_text=document_text,
                            analysis_type=analysis_type,
                            api_key=api_key_input if api_key_input else None,
                            model_name=model_name,
                            specialization=specialization
                        )
                        
                        # 3. Guardar en Session State y restar crédito
                        st.session_state["last_result"] = json.loads(result_raw)
                        st.session_state["last_type"] = analysis_type
                        st.session_state.credits -= 1
                        
                        # Recargar la app para actualizar contador de la barra lateral
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error durante el análisis: {str(e)}")

    # Mostrar resultados guardados en el estado
    if "last_result" in st.session_state and "last_type" in st.session_state:
        data = st.session_state["last_result"]
        dtype = st.session_state["last_type"]
        
        # Botones de exportación avanzada
        st.markdown("### 📥 Exportar Resultados")
        col_j, col_md, col_html = st.columns(3)
        
        with col_j:
            st.download_button(
                "📥 Descargar JSON",
                data=json.dumps(data, indent=2, ensure_ascii=False),
                file_name=f"synthmind_report_{dtype}.json",
                mime="application/json",
                use_container_width=True
            )
            
        with col_md:
            md_report = generate_markdown_report(data, dtype)
            st.download_button(
                "📝 Descargar Word (MD)",
                data=md_report,
                file_name=f"synthmind_report_{dtype}.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with col_html:
            html_report = generate_html_report(data, dtype)
            st.download_button(
                "🖥️ Imprimir Reporte (HTML)",
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

            t1, t2, t3, t4 = st.tabs(["📋 Metadatos", "🔍 Conceptos", "⚖️ Argumentos", "🌳 Taxonomía"])
            
            with t1:
                st.subheader("Metadatos del Documento")
                st.write(f"**Título:** {metadata.get('title', 'N/A')}")
                st.write(f"**Dominio disciplinario:** {metadata.get('domain', 'N/A')}")
                st.write(f"**Tipo de documento:** {metadata.get('document_type', 'N/A')}")
                st.write(f"**Idioma principal:** {metadata.get('language', 'N/A')}")
                st.write(f"**Autores:** {', '.join(metadata.get('authors', []))}")
                
                if quality:
                    st.warning("⚠️ **Observaciones sobre el documento fuente:**\n" + "\n".join([f"- {i}" for i in quality]))

            with t2:
                st.subheader("Conceptos Clave Extraídos")
                for c in concepts:
                    with st.expander(f"{c.get('concept_id')} — {c.get('name')} ({c.get('category')})"):
                        st.markdown(f"**Definición:** {c.get('definition')}")
                        st.markdown(f"**Grado de certeza:** `{c.get('confidence_score')}`")
                        st.markdown("**Evidencia textual:**")
                        st.markdown(f'<div class="quote-block">"{c.get("textual_quote")}"</div>', unsafe_allow_html=True)

            with t3:
                st.subheader("Hilos Argumentativos y Tesis")
                for arg in arguments:
                    rating = arg.get("strength_rating", "Moderado")
                    rating_class = f"badge-{rating.split('/')[0].strip().lower()}"
                    
                    st.markdown(f"""
                    ### {arg.get('argument_id')} — Tesis Principal
                    **Afirmación:** {arg.get('claim_statement')}  
                    <span class="badge {rating_class}">Fuerza: {rating}</span>
                    """, unsafe_allow_html=True)
                    
                    st.write("**Evidencia que lo respalda:**")
                    for ev in arg.get("supporting_evidence", []):
                        st.write(f"- {ev}")
                    
                    if arg.get("counterarguments_mentioned"):
                        st.write("**Objeciones tratadas:**")
                        for ca in arg.get("counterarguments_mentioned", []):
                            st.write(f"- *{ca}*")
                    
                    if arg.get("source_section"):
                        st.caption(f"Sección del origen: {arg.get('source_section')}")
                    st.markdown("---")

            with t4:
                st.subheader("Relación Conceptual (Taxonomía)")
                for tax in taxonomy:
                    st.markdown(f"**Concepto Padre:** `{tax.get('parent_concept')}`")
                    st.markdown(f"**Relación:** *{tax.get('relationship_type')}*")
                    st.markdown(f"**Conceptos derivados:** {', '.join([f'`{i}`' for i in tax.get('child_concepts', [])])}")
                    st.markdown("---")

        elif dtype == "gaps":
            audit = data.get("audit_summary", {})
            contradictions = data.get("internal_contradictions", [])
            gaps = data.get("identified_gaps", [])
            questions = data.get("unanswered_research_questions", [])
            assumptions = data.get("unstated_assumptions", [])

            t1, t2, t3, t4 = st.tabs(["🔬 Rigor Metodológico", "⚠️ Contradicciones", "🔍 Brechas", "❓ Preguntas Abiertas"])

            with t1:
                st.subheader("Auditoría Lógica y Metodológica")
                st.metric("Puntuación de Rigor", f"{audit.get('overall_rigor_score', 0)} / 10")
                st.markdown(f"**Resumen de Robustez:**\n{audit.get('methodological_robustness')}")
                st.markdown(f"**Sesgo Principal Detectado:**\n*{audit.get('primary_bias_detected', 'Ninguno')}*")
                
                if assumptions:
                    st.markdown("---")
                    st.subheader("Supuestos Implícitos del Autor")
                    for a in assumptions:
                        st.write(f"- {a}")

            with t2:
                st.subheader("Contradicciones Internas Detectadas")
                if not contradictions:
                    st.info("No se encontraron contradicciones evidentes dentro del texto.")
                for c in contradictions:
                    st.error(f"**Contradicción {c.get('contradiction_id')}** (Impacto: {c.get('impact_level')})")
                    st.markdown(f"**Punto A:** *\"{c.get('statement_a')}\"*")
                    st.markdown(f"**Punto B (Contrario):** *\"{c.get('statement_b')}\"*")
                    st.info(f"**Análisis de la Brecha:** {c.get('analysis')}")
                    st.markdown("---")

            with t3:
                st.subheader("Brechas de Evidencia Metodológica y Empírica")
                for g in gaps:
                    st.markdown(f"**[{g.get('gap_id')}] — Brecha {g.get('category')}**")
                    st.write(f"**Descripción:** {g.get('description')}")
                    st.write(f"**Evidencia requerida:** *{g.get('missing_evidence')}*")
                    st.markdown("---")

            with t4:
                st.subheader("Líneas de Investigación Abiertas")
                for q in questions:
                    st.markdown(f"**{q.get('question_id')}** — *¿{q.get('question')}?*")
                    st.markdown(f"**Relevancia teórica:** {q.get('relevance')}")
                    st.markdown("---")

        elif dtype == "synthesis":
            summary = data.get("executive_summary", {})
            cards = data.get("synthesis_cards", [])
            recommendations = data.get("strategic_recommendations", [])

            t1, t2, t3 = st.tabs(["⚡ TL;DR y Síntesis", "🗂️ Fichas de Acción", "📋 Plan Estratégico"])

            with t1:
                st.subheader("Resumen Ejecutivo")
                st.info(f"**TL;DR:** {summary.get('tldr')}")
                st.markdown(f"**Narrativa Central:**\n{summary.get('core_narrative')}")
                st.markdown(f"**Perfil de Audiencia:** `{summary.get('target_audience')}`")
                st.markdown("---")
                st.subheader("Puntos de Inflexión Determinantes")
                for item in summary.get("key_takeaways", []):
                    st.markdown(f"✅ {item}")

            with t2:
                st.subheader("Fichas Operativas de Síntesis")
                for card in cards:
                    priority = card.get("priority_level", "Baja")
                    priority_class = f"badge-{priority.lower()}"
                    
                    st.markdown(f"""
                    ### {card.get('card_id')} — {card.get('topic')}
                    **Hallazgo:** {card.get('core_insight')}  
                    <span class="badge {priority_class}">Prioridad: {priority}</span>
                    """, unsafe_allow_html=True)
                    
                    st.info(f"**Implicación de acción:** {card.get('actionable_implication')}")
                    
                    if card.get("key_metrics_or_data"):
                        st.markdown("**Datos clave y Métricas:**")
                        for m in card.get("key_metrics_or_data", []):
                            st.code(m)
                    st.markdown("---")

            with t3:
                st.subheader("Pasos Recomendados Basados en el Análisis")
                for rec in recommendations:
                    st.markdown(f"### {rec.get('step_number')}. {rec.get('action_title')}")
                    st.write(rec.get("description"))
                    st.markdown("---")

    else:
        st.info("Carga un documento y haz clic en 'Iniciar Análisis Agéntico' para ver las visualizaciones estructuradas.")
