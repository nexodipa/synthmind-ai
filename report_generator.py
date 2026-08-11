# report_generator.py
# Utilidad para generar reportes estructurados imprimibles en HTML y Markdown

def generate_markdown_report(data: dict, analysis_type: str) -> str:
    """
    Genera un informe en formato Markdown legible a partir del JSON del análisis.
    """
    md = []

    if analysis_type == "concepts":
        meta = data.get("document_metadata", {})
        md.append(f"# Reporte de Análisis: Mapeo Conceptual y Argumentos")
        md.append(f"**Documento:** {meta.get('title', 'Sin Título')}")
        md.append(f"**Autores:** {', '.join(meta.get('authors', []))}")
        md.append(f"**Disciplina:** {meta.get('domain', 'N/A')} | **Tipo:** {meta.get('document_type', 'N/A')}")
        md.append(f"**Idioma:** {meta.get('language', 'N/A')}\n")
        md.append("---")

        # Conceptos clave
        md.append("## 🔍 Conceptos Clave")
        for c in data.get("core_concepts", []):
            md.append(f"### {c.get('concept_id')} - {c.get('name')}")
            md.append(f"*   **Categoría:** {c.get('category')}")
            md.append(f"*   **Definición:** {c.get('definition')}")
            md.append(f"*   **Certeza de extracción:** {c.get('confidence_score') * 100}%")
            md.append(f"*   **Evidencia Textual:** *\"{c.get('textual_quote')}\"*\n")

        # Argumentos
        md.append("## ⚖️ Argumentos Principales & Evidencias")
        for arg in data.get("key_arguments", []):
            md.append(f"### {arg.get('argument_id')} - Tesis: {arg.get('claim_statement')}")
            md.append(f"*   **Fuerza del Argumento:** {arg.get('strength_rating')}")
            md.append(f"*   **Ubicación:** {arg.get('source_section', 'N/A')}")
            md.append(f"*   **Evidencias de Respaldo:**")
            for ev in arg.get("supporting_evidence", []):
                md.append(f"    *   {ev}")
            if arg.get("counterarguments_mentioned"):
                md.append(f"*   **Objeciones / Contraargumentos:**")
                for ca in arg.get("counterarguments_mentioned", []):
                    md.append(f"    *   {ca}")
            md.append("")

        # Taxonomía
        md.append("## 🌳 Taxonomía Jerárquica")
        for tax in data.get("conceptual_taxonomy", []):
            md.append(f"*   **Categoría Superior:** `{tax.get('parent_concept')}`")
            md.append(f"    *   **Relación:** *{tax.get('relationship_type')}*")
            md.append(f"    *   **Conceptos derivados:** {', '.join([f'`{i}`' for i in tax.get('child_concepts', [])])}")
        
        # Problemas de calidad
        quality = data.get("data_quality_issues", [])
        if quality:
            md.append("\n## ⚠️ Observaciones sobre la Calidad del Origen")
            for q in quality:
                md.append(f"*   {q}")

    elif analysis_type == "gaps":
        audit = data.get("audit_summary", {})
        md.append(f"# Reporte de Auditoría Crítica e Inconsistencias")
        md.append(f"**Puntuación de Rigor Lógico:** {audit.get('overall_rigor_score', 0)} / 10")
        md.append(f"**Robustez Metodológica:** {audit.get('methodological_robustness', 'N/A')}")
        md.append(f"**Sesgo Principal Detectado:** {audit.get('primary_bias_detected', 'N/A')}\n")
        md.append("---")

        # Contradicciones
        md.append("## ⚠️ Contradicciones Internas")
        contras = data.get("internal_contradictions", [])
        if not contras:
            md.append("No se detectaron contradicciones explícitas en el texto.")
        for c in contras:
            md.append(f"### {c.get('contradiction_id')} (Impacto: {c.get('impact_level')})")
            md.append(f"*   **Afirmación A:** *\"{c.get('statement_a')}\"*")
            md.append(f"*   **Afirmación B:** *\"{c.get('statement_b')}\"*")
            md.append(f"*   **Análisis:** {c.get('analysis')}\n")

        # Brechas
        md.append("## 🔍 Vacíos Empíricos e Inconsistencias")
        for g in data.get("identified_gaps", []):
            md.append(f"### {g.get('gap_id')} - Brecha {g.get('category')}")
            md.append(f"*   **Descripción:** {g.get('description')}")
            md.append(f"*   **Evidencia faltante recomendada:** {g.get('missing_evidence')}\n")

        # Preguntas sin responder
        md.append("## ❓ Preguntas de Investigación Abiertas")
        for q in data.get("unanswered_research_questions", []):
            md.append(f"### {q.get('question_id')} - ¿{q.get('question')}?")
            md.append(f"*   **Relevancia teórica/práctica:** {q.get('relevance')}\n")

        # Supuestos implícitos
        assumptions = data.get("unstated_assumptions", [])
        if assumptions:
            md.append("## 💡 Supuestos Implícitos del Autor")
            for a in assumptions:
                md.append(f"*   {a}")

    elif analysis_type == "synthesis":
        summary = data.get("executive_summary", {})
        md.append(f"# Resumen Ejecutivo y Fichas Estratégicas")
        md.append(f"**TL;DR:** *\"{summary.get('tldr', 'N/A')}\"*\n")
        md.append(f"**Narrativa Central:**\n{summary.get('core_narrative', 'N/A')}\n")
        md.append(f"**Público Objetivo:** `{summary.get('target_audience', 'N/A')}`\n")
        md.append("---")

        # Puntos clave
        md.append("## 📌 Puntos de Inflexión Clave")
        for t in summary.get("key_takeaways", []):
            md.append(f"*   {t}")
        md.append("")

        # Fichas de acción
        md.append("## 🗂️ Fichas de Acción y Prioridades")
        for card in data.get("synthesis_cards", []):
            md.append(f"### {card.get('card_id')} - Tema: {card.get('topic')}")
            md.append(f"*   **Prioridad:** {card.get('priority_level')}")
            md.append(f"*   **Hallazgo Clave:** {card.get('core_insight')}")
            md.append(f"*   **Implicación de Acción:** {card.get('actionable_implication')}")
            metrics = card.get("key_metrics_or_data", [])
            if metrics:
                md.append(f"*   **Datos y Métricas:** {', '.join(metrics)}")
            md.append("")

        # Recomendaciones
        md.append("## 📋 Pasos Recomendados (Plan Estratégico)")
        for rec in data.get("strategic_recommendations", []):
            md.append(f"### {rec.get('step_number')}. {rec.get('action_title')}")
            md.append(f"{rec.get('description')}\n")

    return "\n".join(md)


def generate_html_report(data: dict, analysis_type: str) -> str:
    """
    Genera una página HTML estructurada e independiente con CSS print-friendly (@media print)
    para que al abrirse en navegador e imprimir (Ctrl+P) se guarde en PDF perfecto.
    """
    markdown_content = generate_markdown_report(data, analysis_type)
    
    # Simple parseo de Markdown a HTML para evitar dependencias
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
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h2 class='section-title'>{line[3:]}</h2>")
        elif line.startswith("### "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("* ") or line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = line[2:]
            # Pequeña conversión de negritas y comillas
            content = content.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            content = content.replace("`", "<code>", 1).replace("`", "</code>", 1)
            html_lines.append(f"<li>{content}</li>")
        elif line.startswith("**") and line.endswith("**"):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<p><strong>{line[2:-2]}</strong></p>")
        else:
            if in_list: html_lines.append("</ul>"); in_list = False
            # Reemplazar negritas
            content = line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            content = content.replace("`", "<code>", 1).replace("`", "</code>", 1)
            if content.startswith('"') and content.endswith('"'):
                html_lines.append(f"<blockquote class='quote'>{content[1:-1]}</blockquote>")
            else:
                html_lines.append(f"<p>{content}</p>")
                
    if in_list:
        html_lines.append("</ul>")

    body_html = "\n".join(html_lines)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reporte de Análisis SynthMind AI</title>
  <style>
    body {{
      font-family: 'Georgia', 'Times New Roman', serif;
      line-height: 1.6;
      color: #2d3748;
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      background: #ffffff;
    }}
    h1, h2, h3, h4 {{
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #1a202c;
    }}
    h1 {{
      font-size: 2.25rem;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 12px;
      margin-bottom: 30px;
      text-align: center;
    }}
    .section-title {{
      font-size: 1.5rem;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 6px;
      margin-top: 40px;
      color: #2b6cb0;
    }}
    h3 {{
      font-size: 1.15rem;
      margin-top: 24px;
      color: #2d3748;
      background: #f7fafc;
      padding: 8px 12px;
      border-left: 3px solid #4299e1;
      border-radius: 0 4px 4px 0;
    }}
    p, li {{
      font-size: 1.05rem;
      margin-bottom: 12px;
      text-align: justify;
    }}
    ul {{
      margin-bottom: 20px;
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 6px;
    }}
    .quote {{
      font-style: italic;
      background: #f7fafc;
      border-left: 3px solid #48bb78;
      padding: 10px 16px;
      margin: 15px 0;
      color: #4a5568;
    }}
    code {{
      font-family: monospace;
      background: #edf2f7;
      padding: 2px 4px;
      border-radius: 3px;
      font-size: 0.9em;
    }}
    strong {{
      color: #1a202c;
    }}
    
    /* Configuración especial para impresión (Ctrl+P) */
    @media print {{
      body {{
        margin: 20mm;
        padding: 0;
        font-size: 11pt;
        color: #000;
        background: #fff;
      }}
      h1, h2, h3, h4 {{
        page-break-after: avoid;
      }}
      h1 {{
        font-size: 20pt;
        margin-bottom: 20pt;
      }}
      .section-title {{
        font-size: 14pt;
        margin-top: 25pt;
        border-bottom: 1pt solid #000;
      }}
      h3 {{
        font-size: 12pt;
        background: none;
        border-left: 2pt solid #000;
        padding-left: 8pt;
      }}
      .quote {{
        background: none;
        border-left: 1.5pt solid #555;
        padding-left: 10pt;
      }}
      .no-print {{
        display: none;
      }}
      a {{
        text-decoration: none;
        color: #000;
      }}
    }}
  </style>
</head>
<body>
  <div class="no-print" style="background:#ebf8ff; border:1px solid #bee3f8; color:#2b6cb0; padding:15px; border-radius:8px; margin-bottom:30px; text-align:center; font-family:sans-serif; font-size:13px;">
    <strong>💡 Vista de Reporte de SynthMind AI:</strong> Presiona <strong>Ctrl + P</strong> en tu teclado (o CMD + P en Mac) para guardar este documento como un archivo <strong>PDF limpio de alta calidad</strong>.
  </div>

  {body_html}

</body>
</html>
"""
