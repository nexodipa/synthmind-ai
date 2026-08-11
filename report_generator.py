# report_generator.py
# Utilidad para generar reportes estructurados ejecutivos en HTML y Markdown
# Diseño corporativo de alta fidelidad para informes de auditoría y síntesis

def generate_markdown_report(data: dict, analysis_type: str) -> str:
    """
    Genera un informe en formato Markdown profesional sin emojiss, estructurado para uso corporativo y académico.
    """
    md = []

    if analysis_type == "concepts":
        meta = data.get("document_metadata", {})
        md.append(f"# INFORME DE ANÁLISIS: MAPEO CONCEPTUAL Y ARGUMENTOS")
        md.append(f"**Documento:** {meta.get('title', 'Sin Título')}")
        md.append(f"**Autores:** {', '.join(meta.get('authors', []))}")
        md.append(f"**Dominio:** {meta.get('domain', 'N/A')} | **Tipo de Documento:** {meta.get('document_type', 'N/A')}")
        md.append(f"**Idioma Principal:** {meta.get('language', 'N/A')}\n")
        md.append("---")

        # Conceptos clave
        md.append("## 1. Conceptos Clave Extraídos")
        for c in data.get("core_concepts", []):
            md.append(f"### {c.get('concept_id')} — {c.get('name')}")
            md.append(f"* **Categoría:** {c.get('category')}")
            md.append(f"* **Definición:** {c.get('definition')}")
            md.append(f"* **Índice de Certeza de Extracción:** {round(c.get('confidence_score', 0) * 100)}%")
            md.append(f"* **Evidencia Textual Directa:** \"{c.get('textual_quote')}\"\n")

        # Argumentos
        md.append("## 2. Hilos Argumentativos y Tesis Principales")
        for arg in data.get("key_arguments", []):
            md.append(f"### {arg.get('argument_id')} — Tesis: {arg.get('claim_statement')}")
            md.append(f"* **Evaluación de Solidez:** {arg.get('strength_rating')}")
            md.append(f"* **Ubicación en Origen:** {arg.get('source_section', 'N/A')}")
            md.append(f"* **Evidencias de Respaldo:**")
            for ev in arg.get("supporting_evidence", []):
                md.append(f"  - {ev}")
            if arg.get("counterarguments_mentioned"):
                md.append(f"* **Objeciones y Contraargumentos Analizados:**")
                for ca in arg.get("counterarguments_mentioned", []):
                    md.append(f"  - {ca}")
            md.append("")

        # Taxonomía
        md.append("## 3. Taxonomía Jerárquica y Relaciones")
        for tax in data.get("conceptual_taxonomy", []):
            md.append(f"* **Concepto Padre:** `{tax.get('parent_concept')}`")
            md.append(f"  - **Tipo de Relación:** {tax.get('relationship_type')}")
            md.append(f"  - **Conceptos Derivados:** {', '.join([f'`{i}`' for i in tax.get('child_concepts', [])])}")
        
        # Calidad
        quality = data.get("data_quality_issues", [])
        if quality:
            md.append("\n## 4. Observaciones sobre la Calidad de la Fuente")
            for q in quality:
                md.append(f"* {q}")

    elif analysis_type == "gaps":
        audit = data.get("audit_summary", {})
        md.append(f"# INFORME DE AUDITORÍA CRÍTICA Y MATRIZ DE VACÍOS")
        md.append(f"**Puntuación Global de Rigor Lógico:** {audit.get('overall_rigor_score', 0)} / 10")
        md.append(f"**Robustez Metodológica:** {audit.get('methodological_robustness', 'N/A')}")
        md.append(f"**Sesgo Principal Identificado:** {audit.get('primary_bias_detected', 'Ninguno detectado')}\n")
        md.append("---")

        # Contradicciones
        md.append("## 1. Contradicciones Internas Detección")
        contras = data.get("internal_contradictions", [])
        if not contras:
            md.append("No se registraron inconsistencias ni contradicciones explícitas en el cuerpo del texto.")
        for c in contras:
            md.append(f"### {c.get('contradiction_id')} (Nivel de Impacto: {c.get('impact_level')})")
            md.append(f"* **Premisa A:** \"{c.get('statement_a')}\"")
            md.append(f"* **Premisa B (Opuesta):** \"{c.get('statement_b')}\"")
            md.append(f"* **Análisis de Inconsistencia:** {c.get('analysis')}\n")

        # Brechas
        md.append("## 2. Vacíos Empíricos y Limitaciones Metodológicas")
        for g in data.get("identified_gaps", []):
            md.append(f"### {g.get('gap_id')} — Brecha: {g.get('category')}")
            md.append(f"* **Descripción del Vacío:** {g.get('description')}")
            md.append(f"* **Evidencia Faltante Requerida:** {g.get('missing_evidence')}\n")

        # Preguntas sin responder
        md.append("## 3. Líneas de Investigación y Preguntas Abiertas")
        for q in data.get("unanswered_research_questions", []):
            md.append(f"### {q.get('question_id')} — {q.get('question')}")
            md.append(f"* **Relevancia Estratégica:** {q.get('relevance')}\n")

        # Supuestos implícitos
        assumptions = data.get("unstated_assumptions", [])
        if assumptions:
            md.append("## 4. Supuestos Implícitos del Autor")
            for a in assumptions:
                md.append(f"* {a}")

    elif analysis_type == "synthesis":
        summary = data.get("executive_summary", {})
        md.append(f"# SÍNTESIS EJECUTIVA Y FICHAS ESTRATÉGICAS DE ACCIÓN")
        md.append(f"**TL;DR / Resumen Conciso:** \"{summary.get('tldr', 'N/A')}\"\n")
        md.append(f"**Síntesis Narrativa:**\n{summary.get('core_narrative', 'N/A')}\n")
        md.append(f"**Perfil de Audiencia Destino:** {summary.get('target_audience', 'N/A')}\n")
        md.append("---")

        # Puntos clave
        md.append("## 1. Conclusiones Clave de Alto Nivel")
        for t in summary.get("key_takeaways", []):
            md.append(f"* {t}")
        md.append("")

        # Fichas de acción
        md.append("## 2. Fichas de Acción Prioritaria")
        for card in data.get("synthesis_cards", []):
            md.append(f"### {card.get('card_id')} — Área: {card.get('topic')}")
            md.append(f"* **Nivel de Prioridad:** {card.get('priority_level')}")
            md.append(f"* **Hallazgo Clave:** {card.get('core_insight')}")
            md.append(f"* **Implicación Operativa:** {card.get('actionable_implication')}")
            metrics = card.get("key_metrics_or_data", [])
            if metrics:
                md.append(f"* **Métricas y Datos Asociados:** {', '.join(metrics)}")
            md.append("")

        # Recomendaciones
        md.append("## 3. Plan Estratégico Recomendado")
        for rec in data.get("strategic_recommendations", []):
            md.append(f"### Paso {rec.get('step_number')}: {rec.get('action_title')}")
            md.append(f"{rec.get('description')}\n")

    return "\n".join(md)


def generate_html_report(data: dict, analysis_type: str) -> str:
    """
    Genera un informe HTML ejecutivo de alta fidelidad visual (tipo McKinsey/BCG/Big-4).
    Diseño limpio sin emojis, listo para exportar a PDF perfecto vía Ctrl+P.
    """
    markdown_content = generate_markdown_report(data, analysis_type)
    
    html_lines = []
    in_list = False
    
    for line in markdown_content.split('\n'):
        line = line.strip()
        if not line:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue
            
        if line.startswith("# "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h1 class='doc-title'>{line[2:]}</h1>")
        elif line.startswith("## "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h2 class='section-title'>{line[3:]}</h2>")
        elif line.startswith("### "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h3 class='item-title'>{line[4:]}</h3>")
        elif line.startswith("* ") or line.startswith("- "):
            if not in_list:
                html_lines.append("<ul class='content-list'>")
                in_list = True
            content = line[2:]
            content = content.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            content = content.replace("`", "<code>", 1).replace("`", "</code>", 1)
            html_lines.append(f"<li>{content}</li>")
        elif line.startswith("**") and line.endswith("**"):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<p class='highlight-text'><strong>{line[2:-2]}</strong></p>")
        else:
            if in_list: html_lines.append("</ul>"); in_list = False
            content = line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            content = content.replace("`", "<code>", 1).replace("`", "</code>", 1)
            if content.startswith('"') and content.endswith('"'):
                html_lines.append(f"<blockquote class='executive-quote'>{content[1:-1]}</blockquote>")
            else:
                html_lines.append(f"<p class='content-paragraph'>{content}</p>")
                
    if in_list:
        html_lines.append("</ul>")

    body_html = "\n".join(html_lines)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Informe Ejecutivo - SynthMind AI</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&display=swap');
    
    * {{
      box-sizing: border-box;
    }}
    
    body {{
      font-family: 'Merriweather', Georgia, serif;
      font-size: 11pt;
      line-height: 1.7;
      color: #1a202c;
      max-width: 820px;
      margin: 0 auto;
      padding: 50px 40px;
      background: #ffffff;
    }}
    
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #0f172a;
      padding-bottom: 15px;
      margin-bottom: 35px;
    }}
    
    .brand-logo {{
      font-family: 'Inter', sans-serif;
      font-weight: 800;
      font-size: 16px;
      letter-spacing: -0.5px;
      color: #0f172a;
      text-transform: uppercase;
    }}
    
    .brand-tag {{
      font-family: 'Inter', sans-serif;
      font-size: 11px;
      color: #64748b;
      font-weight: 500;
    }}
    
    .doc-title {{
      font-family: 'Inter', sans-serif;
      font-size: 24px;
      font-weight: 700;
      color: #0f172a;
      margin-top: 0;
      margin-bottom: 20px;
      line-height: 1.3;
      letter-spacing: -0.3px;
    }}
    
    .section-title {{
      font-family: 'Inter', sans-serif;
      font-size: 15px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #0f172a;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 6px;
      margin-top: 35px;
      margin-bottom: 15px;
    }}
    
    .item-title {{
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      font-weight: 600;
      color: #1e293b;
      margin-top: 20px;
      margin-bottom: 8px;
      background: #f8fafc;
      padding: 8px 12px;
      border-left: 3px solid #0f172a;
      border-radius: 0 4px 4px 0;
    }}
    
    .content-paragraph {{
      margin-bottom: 12px;
      text-align: justify;
      color: #334155;
    }}
    
    .content-list {{
      margin-top: 6px;
      margin-bottom: 16px;
      padding-left: 24px;
    }}
    
    .content-list li {{
      margin-bottom: 6px;
      color: #334155;
    }}
    
    .executive-quote {{
      font-style: italic;
      background: #f8fafc;
      border-left: 3px solid #3b82f6;
      padding: 12px 18px;
      margin: 18px 0;
      color: #334155;
      font-size: 10.5pt;
      border-radius: 0 4px 4px 0;
    }}
    
    code {{
      font-family: 'Inter', sans-serif;
      font-size: 9.5pt;
      background: #f1f5f9;
      color: #0f172a;
      padding: 2px 6px;
      border-radius: 3px;
      font-weight: 500;
    }}
    
    strong {{
      font-family: 'Inter', sans-serif;
      font-weight: 600;
      color: #0f172a;
    }}
    
    .footer-bar {{
      margin-top: 50px;
      border-top: 1px solid #e2e8f0;
      padding-top: 15px;
      display: flex;
      justify-content: space-between;
      font-family: 'Inter', sans-serif;
      font-size: 10px;
      color: #94a3b8;
    }}
    
    .print-notice {{
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      color: #334155;
      padding: 12px;
      border-radius: 6px;
      margin-bottom: 30px;
      text-align: center;
      font-family: 'Inter', sans-serif;
      font-size: 12px;
    }}

    @media print {{
      body {{
        margin: 0;
        padding: 15mm;
        max-width: 100%;
      }}
      .print-notice {{
        display: none;
      }}
      .item-title {{
        background: none;
        border-left: 2pt solid #0f172a;
        padding-left: 8px;
      }}
      .executive-quote {{
        background: none;
        border-left: 2pt solid #64748b;
      }}
      h1, h2, h3 {{
        page-break-after: avoid;
      }}
    }}
  </style>
</head>
<body>
  <div class="print-notice">
    <strong>Instrucción de Exportación:</strong> Presiona <strong>Ctrl + P</strong> (o CMD + P en Mac) para guardar este reporte como un archivo <strong>PDF Ejecutivo listo para presentación</strong>.
  </div>

  <div class="header-bar">
    <div class="brand-logo">SynthMind AI</div>
    <div class="brand-tag">Auditoría Agéntica & Resumen Ejecutivo</div>
  </div>

  {body_html}

  <div class="footer-bar">
    <span>Documento generado mediante SynthMind AI Engine</span>
    <span>Confidencial | Reservados todos los derechos</span>
  </div>
</body>
</html>
"""
