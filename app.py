# app.py
# Servidor FastAPI para SynthMind AI con SPA (HTML5 + Tailwind CSS) integrada

import json
import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from gemini_engine import extract_text_from_file, run_gemini_analysis

app = FastAPI(title="SynthMind AI API", version="1.0.0")

# Permitir CORS para desarrollo local fácil
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SPA HTML integrada para despliegue de archivo único
HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SynthMind AI - Análisis Agéntico Documental</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            display: ['Outfit', 'sans-serif'],
          }
        }
      }
    }
  </script>
  <style>
    /* Estilos personalizados oscuros y de vidrio */
    body {
      background-color: #05070c;
      color: #e2e8f0;
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.06) 0%, transparent 40%);
    }
    .glass-card {
      background: rgba(13, 18, 30, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.2);
    }
  </style>
</head>
<body class="min-height-screen flex flex-col font-sans antialiased">

  <!-- Header -->
  <header class="w-full border-b border-white/5 py-4 px-6 flex justify-between items-center glass-card sticky top-0 z-50">
    <div class="flex items-center gap-3">
      <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-indigo-600 flex justify-center items-center text-white shadow-lg shadow-emerald-500/10">
        <i data-lucide="brain-circuit" class="h-6 w-6"></i>
      </div>
      <div>
        <h1 class="font-display font-bold text-xl tracking-tight text-white flex items-center gap-2">
          SynthMind <span class="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent text-sm font-semibold tracking-wider px-2 py-0.5 rounded border border-emerald-500/20 bg-emerald-500/5">AI</span>
        </h1>
        <p class="text-xs text-slate-400">Motor de Síntesis y Análisis Crítico Agéntico</p>
      </div>
    </div>
    <div class="flex items-center gap-4">
      <a href="https://aistudio.google.com/" target="_blank" class="text-xs text-emerald-400 hover:text-emerald-300 hover:underline flex items-center gap-1">
        <i data-lucide="key" class="h-3 w-3"></i> Consigue tu API Key
      </a>
    </div>
  </header>

  <!-- Main Layout -->
  <main class="flex-1 w-full max-w-7xl mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 overflow-hidden">
    
    <!-- Panel Izquierdo: Inputs (4 Cols) -->
    <section class="lg:col-span-4 flex flex-col gap-6">
      
      <!-- API Key & Modelo Card -->
      <div class="glass-card rounded-2xl p-5 flex flex-col gap-4">
        <h2 class="font-display font-semibold text-white flex items-center gap-2 text-md">
          <i data-lucide="settings" class="text-emerald-400 h-4 w-4"></i> Configuración Inicial
        </h2>
        
        <!-- API Key Input -->
        <div class="flex flex-col gap-1.5">
          <label class="text-xs text-slate-300 font-medium flex justify-between">
            <span>Gemini API Key</span>
            <span class="text-slate-500">(Opcional si usas variables de entorno)</span>
          </label>
          <div class="relative">
            <input type="password" id="api-key" placeholder="AIzaSy..." class="w-full bg-black/40 border border-white/10 rounded-xl py-2 px-3 pl-8 text-sm focus:outline-none focus:border-emerald-500 text-white transition-all">
            <i data-lucide="lock" class="absolute left-2.5 top-2.5 h-4 w-4 text-slate-500"></i>
            <button onclick="togglePassword()" class="absolute right-2.5 top-2.5 text-slate-500 hover:text-slate-300">
              <i data-lucide="eye" id="eye-icon" class="h-4 w-4"></i>
            </button>
          </div>
        </div>

        <!-- Modelo Select -->
        <div class="flex flex-col gap-1.5">
          <label class="text-xs text-slate-300 font-medium">Modelo Inteligente</label>
          <select id="model-select" class="w-full bg-black/40 border border-white/10 rounded-xl py-2 px-3 text-sm focus:outline-none focus:border-emerald-500 text-white transition-all">
            <option value="gemini-2.5-flash" selected>Gemini 2.5 Flash (Ultra Rápido y Eficiente)</option>
            <option value="gemini-2.5-pro">Gemini 2.5 Pro (Razonamiento Complejo y Extenso)</option>
          </select>
        </div>
      </div>

      <!-- File Uploader & Tipo de Análisis -->
      <div class="glass-card rounded-2xl p-5 flex-1 flex flex-col gap-4">
        <h2 class="font-display font-semibold text-white flex items-center gap-2 text-md">
          <i data-lucide="file-text" class="text-emerald-400 h-4 w-4"></i> Carga y Análisis
        </h2>

        <!-- Drag & Drop Uploader -->
        <div class="flex flex-col gap-1.5">
          <label class="text-xs text-slate-300 font-medium">Documento Fuente</label>
          <div id="drop-zone" class="border-2 border-dashed border-white/10 hover:border-emerald-500/50 rounded-2xl p-6 text-center cursor-pointer transition-all flex flex-col items-center gap-2 bg-white/[0.01]">
            <input type="file" id="file-input" accept=".pdf,.txt,.md" class="hidden">
            <div class="h-10 w-10 rounded-full bg-emerald-500/10 text-emerald-400 flex justify-center items-center" id="upload-icon-container">
              <i data-lucide="upload-cloud" class="h-5 w-5"></i>
            </div>
            <span class="text-xs text-slate-300 font-semibold" id="file-name-text">Arrastra un archivo o haz clic</span>
            <span class="text-[10px] text-slate-500">PDF, TXT, MD (Máx. 15MB)</span>
          </div>
        </div>

        <!-- Tipo de Análisis Select -->
        <div class="flex flex-col gap-2">
          <label class="text-xs text-slate-300 font-medium">Tipo de Tarea Agéntica</label>
          
          <!-- Concept Map Option -->
          <label class="flex items-start gap-3 p-3 rounded-xl border border-white/10 hover:border-emerald-500/30 cursor-pointer bg-black/10 select-none transition-all" for="analysis-concepts">
            <input type="radio" name="analysis_type" id="analysis-concepts" value="concepts" checked class="mt-1 accent-emerald-500">
            <div>
              <span class="text-xs font-semibold text-white block">Mapeo Conceptual</span>
              <span class="text-[10px] text-slate-400">Extrae taxonomías, conceptos estructurados y argumentos lógicos del texto.</span>
            </div>
          </label>

          <!-- Gaps Option -->
          <label class="flex items-start gap-3 p-3 rounded-xl border border-white/10 hover:border-emerald-500/30 cursor-pointer bg-black/10 select-none transition-all" for="analysis-gaps">
            <input type="radio" name="analysis_type" id="analysis-gaps" value="gaps" class="mt-1 accent-emerald-500">
            <div>
              <span class="text-xs font-semibold text-white block">Auditoría Crítica y Brechas</span>
              <span class="text-[10px] text-slate-400">Encuentra contradicciones internas, sesgos teóricos y preguntas abiertas.</span>
            </div>
          </label>

          <!-- Synthesis Option -->
          <label class="flex items-start gap-3 p-3 rounded-xl border border-white/10 hover:border-emerald-500/30 cursor-pointer bg-black/10 select-none transition-all" for="analysis-synthesis">
            <input type="radio" name="analysis_type" id="analysis-synthesis" value="synthesis" class="mt-1 accent-emerald-500">
            <div>
              <span class="text-xs font-semibold text-white block">Resumen Ejecutivo y Fichas</span>
              <span class="text-[10px] text-slate-400">Crea síntesis estratégicas, TL;DR y tarjetas accionables de prioridad.</span>
            </div>
          </label>
        </div>

        <!-- Submit Button -->
        <button id="analyze-btn" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-semibold py-3 px-4 rounded-xl text-sm transition-all shadow-md shadow-emerald-500/10 hover:shadow-emerald-500/25 flex justify-center items-center gap-2">
          <i data-lucide="zap" class="h-4 w-4"></i> Iniciar Análisis Agéntico
        </button>
      </div>

    </section>

    <!-- Panel Derecho: Resultados (8 Cols) -->
    <section class="lg:col-span-8 flex flex-col min-h-[500px]">
      
      <!-- Contenedor Resultados -->
      <div class="glass-card rounded-2xl flex-1 flex flex-col overflow-hidden">
        
        <!-- Header Resultados con Pestañas -->
        <div class="border-b border-white/5 bg-black/30 py-3 px-5 flex justify-between items-center">
          <div class="flex items-center gap-3">
            <div class="h-2 w-2 rounded-full bg-emerald-500" id="status-indicator"></div>
            <span class="text-xs font-semibold uppercase tracking-wider text-slate-400" id="status-text">Panel de Visualización</span>
          </div>
          
          <div class="flex items-center gap-2" id="export-actions" style="display: none;">
            <button onclick="copyRawJson()" class="text-xs bg-white/5 hover:bg-white/10 px-2.5 py-1.5 rounded-lg border border-white/10 text-slate-300 hover:text-white flex items-center gap-1.5 transition-all">
              <i data-lucide="copy" class="h-3 w-3"></i> Copiar JSON
            </button>
            <button onclick="downloadJsonReport()" class="text-xs bg-emerald-500/10 hover:bg-emerald-500/20 px-2.5 py-1.5 rounded-lg border border-emerald-500/20 text-emerald-400 hover:text-emerald-300 flex items-center gap-1.5 transition-all">
              <i data-lucide="download" class="h-3 w-3"></i> Descargar
            </button>
          </div>
        </div>

        <!-- Cuerpo Dinámico -->
        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar flex flex-col" id="result-workspace">
          
          <!-- Placeholder Inicial -->
          <div class="my-auto flex flex-col items-center text-center gap-3 py-10" id="placeholder-container">
            <div class="h-16 w-16 rounded-full bg-white/[0.02] border border-white/5 flex justify-center items-center text-slate-500">
              <i data-lucide="folder-search" class="h-8 w-8"></i>
            </div>
            <div>
              <h3 class="text-white font-display font-semibold text-sm">Esperando Documento</h3>
              <p class="text-xs text-slate-500 max-w-sm mt-1">Carga tu PDF e introduce tu API Key para ejecutar las fases agénticas de Chain-of-Thought y reflexión estructurada.</p>
            </div>
          </div>

          <!-- Loading Container -->
          <div class="my-auto flex flex-col items-center gap-5 py-10" id="loading-container" style="display: none;">
            <div class="relative flex items-center justify-center">
              <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-emerald-500"></div>
              <i data-lucide="sparkles" class="absolute h-6 w-6 text-emerald-400 animate-pulse"></i>
            </div>
            <div class="text-center">
              <h3 class="text-white font-display font-semibold text-sm" id="loading-title">Iniciando Análisis</h3>
              <p class="text-xs text-slate-400 mt-1 max-w-xs mx-auto" id="loading-step">Estableciendo flujo de lectura del documento...</p>
            </div>
            
            <!-- Simulador de Pasos del Agente -->
            <div class="w-full max-w-xs space-y-2 mt-2 text-left">
              <div class="flex items-center gap-2 text-xs text-emerald-400" id="step-ocr">
                <i data-lucide="check" class="h-3.5 w-3.5 hidden"></i>
                <div class="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping"></div>
                <span>Fase 1: Extracción del documento (Python)</span>
              </div>
              <div class="flex items-center gap-2 text-xs text-slate-500" id="step-cot">
                <i data-lucide="check" class="h-3.5 w-3.5 hidden"></i>
                <div class="h-1.5 w-1.5 rounded-full bg-slate-600"></div>
                <span>Fase 2: Razonamiento y Reflexión (Gemini CoT)</span>
              </div>
              <div class="flex items-center gap-2 text-xs text-slate-500" id="step-json">
                <i data-lucide="check" class="h-3.5 w-3.5 hidden"></i>
                <div class="h-1.5 w-1.5 rounded-full bg-slate-600"></div>
                <span>Fase 3: Auditoría y Validación de Esquema</span>
              </div>
            </div>
          </div>

          <!-- Contenedor Final de Datos (Se dibuja dinámicamente) -->
          <div id="data-container" class="space-y-6" style="display: none;"></div>

        </div>
      </div>

    </section>

  </main>

  <!-- Footer -->
  <footer class="w-full border-t border-white/5 py-4 px-6 text-center text-xs text-slate-500">
    <p>© 2026 SynthMind AI - Licencia MIT. Construido para Google AI Studio y Gemini 2.5.</p>
  </footer>

  <!-- Scripts Logic -->
  <script>
    let activeFile = null;
    let lastAnalysisResult = null;

    // Inicializar iconos
    document.addEventListener('DOMContentLoaded', () => {
      lucide.createIcons();
      setupFileUploader();
    });

    function togglePassword() {
      const input = document.getElementById('api-key');
      const icon = document.getElementById('eye-icon');
      if (input.type === 'password') {
        input.type = 'text';
        icon.setAttribute('data-lucide', 'eye-off');
      } else {
        input.type = 'password';
        icon.setAttribute('data-lucide', 'eye');
      }
      lucide.createIcons();
    }

    function setupFileUploader() {
      const dropZone = document.getElementById('drop-zone');
      const fileInput = document.getElementById('file-input');
      const fileNameText = document.getElementById('file-name-text');
      const uploadIconContainer = document.getElementById('upload-icon-container');

      dropZone.addEventListener('click', () => fileInput.click());

      fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
          handleFile(e.target.files[0]);
        }
      });

      dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-emerald-500');
        dropZone.classList.add('bg-emerald-500/5');
      });

      ['dragleave', 'drop'].forEach(event => {
        dropZone.addEventListener(event, () => {
          dropZone.classList.remove('border-emerald-500');
          dropZone.classList.remove('bg-emerald-500/5');
        });
      });

      dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        if (e.dataTransfer.files.length > 0) {
          handleFile(e.dataTransfer.files[0]);
        }
      });

      function handleFile(file) {
        activeFile = file;
        fileNameText.textContent = file.name;
        fileNameText.classList.remove('text-slate-300');
        fileNameText.classList.add('text-emerald-400');
        uploadIconContainer.className = "h-10 w-10 rounded-full bg-emerald-500/20 text-emerald-300 flex justify-center items-center";
        uploadIconContainer.innerHTML = '<i data-lucide="file-check" class="h-5 w-5"></i>';
        lucide.createIcons();
      }
    }

    // Listener para el botón de analizar
    document.getElementById('analyze-btn').addEventListener('click', async () => {
      const apiKey = document.getElementById('api-key').value;
      const model = document.getElementById('model-select').value;
      const analysisType = document.querySelector('input[name="analysis_type"]:checked').value;

      if (!activeFile) {
        alert('Por favor, selecciona un documento PDF o de texto para comenzar.');
        return;
      }

      // Preparar UI de carga
      document.getElementById('placeholder-container').style.display = 'none';
      document.getElementById('data-container').style.display = 'none';
      document.getElementById('export-actions').style.display = 'none';
      const loadingContainer = document.getElementById('loading-container');
      loadingContainer.style.display = 'flex';
      
      updateLoadingUI('Fase 1: Extracción del documento', 'Leyendo el contenido del archivo local en el servidor...', 'ocr');

      // Crear FormData
      const formData = new FormData();
      formData.append('file', activeFile);
      formData.append('analysis_type', analysisType);
      formData.append('model', model);
      if (apiKey) {
        formData.append('api_key', apiKey);
      }

      try {
        // Simular transiciones de carga
        setTimeout(() => {
          updateLoadingUI('Fase 2: Razonamiento Agéntico', 'Gemini está ejecutando la cadena de pensamiento y auditoría...', 'cot');
        }, 1500);

        setTimeout(() => {
          updateLoadingUI('Fase 3: Estructuración y Control', 'Validando la estructura JSON de acuerdo con el esquema estricto...', 'json');
        }, 4000);

        const response = await fetch('/api/analyze', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || 'Error en el servidor durante el procesamiento.');
        }

        const data = await response.json();
        lastAnalysisResult = data;
        
        // Dibujar resultados
        loadingContainer.style.display = 'none';
        document.getElementById('export-actions').style.display = 'flex';
        const dataContainer = document.getElementById('data-container');
        dataContainer.style.display = 'block';
        
        document.getElementById('status-indicator').className = 'h-2 w-2 rounded-full bg-emerald-400';
        document.getElementById('status-text').textContent = 'Análisis Completado';

        renderResult(analysisType, data);

      } catch (err) {
        loadingContainer.style.display = 'none';
        document.getElementById('placeholder-container').style.display = 'flex';
        document.getElementById('status-indicator').className = 'h-2 w-2 rounded-full bg-red-500';
        document.getElementById('status-text').textContent = 'Error';
        alert('Error analizando documento: ' + err.message);
      }
    });

    function updateLoadingUI(title, stepText, activeStep) {
      document.getElementById('loading-title').textContent = title;
      document.getElementById('loading-step').textContent = stepText;

      const steps = {
        'ocr': { id: 'step-ocr', next: ['step-cot', 'step-json'] },
        'cot': { id: 'step-cot', complete: 'step-ocr', next: ['step-json'] },
        'json': { id: 'step-json', complete: ['step-ocr', 'step-cot'] }
      };

      const activeObj = steps[activeStep];
      
      // Marcar activo como parpadeando
      const activeEl = document.getElementById(activeObj.id);
      activeEl.className = "flex items-center gap-2 text-xs text-emerald-400 font-semibold";
      activeEl.querySelector('.h-1.5').className = "h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping";
      activeEl.querySelector('i').classList.add('hidden');

      // Marcar anteriores como completados
      if (activeObj.complete) {
        const completes = Array.isArray(activeObj.complete) ? activeObj.complete : [activeObj.complete];
        completes.forEach(cId => {
          const el = document.getElementById(cId);
          el.className = "flex items-center gap-2 text-xs text-emerald-500";
          el.querySelector('.h-1.5').className = "h-1.5 w-1.5 rounded-full bg-emerald-500 hidden";
          el.querySelector('i').classList.remove('hidden');
        });
      }

      // Marcar futuros como pendientes
      if (activeObj.next) {
        activeObj.next.forEach(nId => {
          const el = document.getElementById(nId);
          el.className = "flex items-center gap-2 text-xs text-slate-500";
          el.querySelector('.h-1.5').className = "h-1.5 w-1.5 rounded-full bg-slate-600";
          el.querySelector('i').classList.add('hidden');
        });
      }
      lucide.createIcons();
    }

    function renderResult(type, data) {
      const container = document.getElementById('data-container');
      container.innerHTML = '';

      if (type === 'concepts') {
        const metadata = data.document_metadata || {};
        const concepts = data.core_concepts || [];
        const argumentsList = data.key_arguments || [];
        const taxonomy = data.conceptual_taxonomy || [];
        const qualityIssues = data.data_quality_issues || [];

        // Dibujar Metadatos
        let metadataHTML = `
          <div class="p-5 rounded-2xl bg-white/[0.02] border border-white/5">
            <h4 class="text-xs text-slate-500 font-bold uppercase tracking-wider mb-3">Metadatos del Documento</h4>
            <h3 class="font-display font-bold text-white text-lg">${metadata.title || 'Sin Título'}</h3>
            <div class="flex flex-wrap gap-2 mt-3">
              <span class="text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 py-1 px-2.5 rounded-full">Disciplina: ${metadata.domain}</span>
              <span class="text-xs bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 py-1 px-2.5 rounded-full">Tipo: ${metadata.document_type}</span>
              <span class="text-xs bg-slate-500/10 border border-white/10 text-slate-300 py-1 px-2.5 rounded-full">Idioma: ${metadata.language}</span>
            </div>
            ${metadata.authors && metadata.authors.length > 0 ? `
              <p class="text-xs text-slate-400 mt-3"><strong>Autores:</strong> ${metadata.authors.join(', ')}</p>
            ` : ''}
          </div>
        `;

        // Conceptos Clave
        let conceptsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs text-slate-500 font-bold uppercase tracking-wider">Conceptos Clave Extraídos</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${concepts.map((concept, index) => {
                const confPercent = Math.round(concept.confidence_score * 100);
                const confColor = confPercent >= 80 ? 'text-emerald-400 bg-emerald-500/10' : (confPercent >= 60 ? 'text-yellow-400 bg-yellow-500/10' : 'text-red-400 bg-red-500/10');
                return `
                  <div class="p-4 rounded-xl border border-white/5 bg-white/[0.01] hover:bg-white/[0.02] transition-all flex flex-col gap-2 relative">
                    <span class="absolute top-3 right-3 text-[10px] py-0.5 px-2 rounded-full font-semibold ${confColor}">
                      Certeza: ${confPercent}%
                    </span>
                    <span class="text-[10px] text-slate-500 uppercase tracking-widest font-mono font-semibold">${concept.concept_id} - ${concept.category}</span>
                    <h5 class="font-display font-semibold text-white text-sm">${concept.name}</h5>
                    <p class="text-xs text-slate-400 line-clamp-3">${concept.definition}</p>
                    
                    <!-- Cita expandible -->
                    <details class="mt-2 text-[11px] border-t border-white/5 pt-2">
                      <summary class="text-emerald-400 hover:text-emerald-300 cursor-pointer outline-none select-none font-semibold">Ver evidencia textual</summary>
                      <blockquote class="bg-black/30 p-2 rounded border-l-2 border-emerald-500 text-slate-300 italic mt-1 font-sans">
                        "${concept.textual_quote}"
                      </blockquote>
                    </details>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;

        // Argumentos Principales
        let argumentsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs text-slate-500 font-bold uppercase tracking-wider">Hilos Argumentativos & Evidencias</h4>
            <div class="space-y-4">
              ${argumentsList.map(arg => {
                const ratingBadge = arg.strength_rating === 'Fuerte' 
                  ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' 
                  : (arg.strength_rating === 'Moderado' ? 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400' : 'bg-red-500/10 border-red-500/20 text-red-400');
                return `
                  <div class="p-5 rounded-2xl border border-white/5 bg-white/[0.01] flex flex-col gap-3">
                    <div class="flex justify-between items-start gap-4">
                      <div>
                        <span class="text-[10px] text-slate-500 uppercase font-mono font-semibold">${arg.argument_id}</span>
                        <h5 class="text-white text-sm font-semibold mt-0.5">${arg.claim_statement}</h5>
                      </div>
                      <span class="text-xs border py-0.5 px-2.5 rounded-full font-medium ${ratingBadge}">
                        ${arg.strength_rating}
                      </span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                      <div>
                        <h6 class="text-[10px] uppercase font-bold text-slate-500 tracking-wider mb-1.5">Evidencias de Respaldo</h6>
                        <ul class="list-disc pl-4 space-y-1 text-xs text-slate-300">
                          ${arg.supporting_evidence.map(ev => `<li>${ev}</li>`).join('')}
                        </ul>
                      </div>
                      ${arg.counterarguments_mentioned && arg.counterarguments_mentioned.length > 0 ? `
                        <div>
                          <h6 class="text-[10px] uppercase font-bold text-slate-500 tracking-wider mb-1.5">Objeciones / Contraargumentos</h6>
                          <ul class="list-disc pl-4 space-y-1 text-xs text-slate-400">
                            ${arg.counterarguments_mentioned.map(ca => `<li>${ca}</li>`).join('')}
                          </ul>
                        </div>
                      ` : ''}
                    </div>
                    ${arg.source_section ? `
                      <span class="text-[10px] text-slate-500 mt-2 block self-end">Ubicación aproximada: ${arg.source_section}</span>
                    ` : ''}
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;

        // Calidad de datos
        let qualityHTML = '';
        if (qualityIssues && qualityIssues.length > 0) {
          qualityHTML = `
            <div class="p-4 rounded-xl border border-yellow-500/10 bg-yellow-500/5 text-yellow-400/90 text-xs flex gap-3">
              <i data-lucide="alert-triangle" class="h-5 w-5 flex-shrink-0 mt-0.5"></i>
              <div>
                <span class="font-semibold block mb-1">Problemas de Calidad del Documento:</span>
                <ul class="list-disc pl-4 space-y-1">
                  ${qualityIssues.map(issue => `<li>${issue}</li>`).join('')}
                </ul>
              </div>
            </div>
          `;
        }

        container.innerHTML = metadataHTML + conceptsHTML + argumentsHTML + qualityHTML;

      } else if (type === 'gaps') {
        const audit = data.audit_summary || {};
        const contradictions = data.internal_contradictions || [];
        const gaps = data.identified_gaps || [];
        const questions = data.unanswered_research_questions || [];
        const assumptions = data.unstated_assumptions || [];

        // Resumen Auditoría
        let auditHTML = `
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="p-5 rounded-2xl bg-white/[0.02] border border-white/5 text-center flex flex-col items-center justify-center">
              <span class="text-xs text-slate-500 font-bold uppercase tracking-wider mb-1">Rigor Lógico</span>
              <span class="text-3xl font-display font-bold text-white">${audit.overall_rigor_score}/10</span>
              <div class="w-24 bg-white/10 h-1.5 rounded-full mt-2 overflow-hidden">
                <div class="bg-emerald-400 h-full" style="width: ${audit.overall_rigor_score * 10}%"></div>
              </div>
            </div>
            <div class="p-5 rounded-2xl bg-white/[0.02] border border-white/5 md:col-span-2">
              <span class="text-xs text-slate-500 font-bold uppercase tracking-wider block mb-1">Solidez Metodológica</span>
              <p class="text-xs text-slate-300 leading-relaxed">${audit.methodological_robustness}</p>
              ${audit.primary_bias_detected ? `
                <div class="mt-2.5 text-xs text-yellow-400/90 flex items-center gap-1.5">
                  <i data-lucide="eye-off" class="h-4 w-4"></i>
                  <span><strong>Sesgo Principal:</strong> ${audit.primary_bias_detected}</span>
                </div>
              ` : ''}
            </div>
          </div>
        `;

        // Contradicciones Internas
        let contradictionsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs text-slate-500 font-bold uppercase tracking-wider">Contradicciones Internas Identificadas</h4>
            ${contradictions.length === 0 ? `
              <p class="text-xs text-slate-500 italic p-4 bg-white/[0.01] rounded-xl border border-white/5">No se detectaron contradicciones internas evidentes en el documento.</p>
            ` : `
              <div class="space-y-4">
                ${contradictions.map(c => {
                  const impactColor = c.impact_level === 'Crítico' ? 'text-red-400 bg-red-500/10 border-red-500/20' : (c.impact_level === 'Moderado' ? 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20' : 'text-slate-300 bg-white/5 border-white/10');
                  return `
                    <div class="p-5 rounded-2xl border border-white/5 bg-white/[0.01] flex flex-col gap-3">
                      <div class="flex justify-between items-center">
                        <span class="text-[10px] text-slate-500 font-mono font-semibold">${c.contradiction_id}</span>
                        <span class="text-xs border py-0.5 px-2 rounded-full font-medium ${impactColor}">Impacto: ${c.impact_level}</span>
                      </div>
                      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-black/20 p-3.5 rounded-xl border border-white/5">
                        <div class="space-y-1">
                          <span class="text-[9px] uppercase font-bold text-slate-500">Afirmación A</span>
                          <p class="text-xs text-slate-300 italic">"${c.statement_a}"</p>
                        </div>
                        <div class="space-y-1 border-t md:border-t-0 md:border-l border-white/5 pt-2.5 md:pt-0 md:pl-4">
                          <span class="text-[9px] uppercase font-bold text-slate-500">Afirmación B (Contradictoria)</span>
                          <p class="text-xs text-slate-300 italic">"${c.statement_b}"</p>
                        </div>
                      </div>
                      <div>
                        <h6 class="text-[10px] uppercase font-bold text-slate-500 mb-1">Análisis Crítico</h6>
                        <p class="text-xs text-slate-300 leading-relaxed">${c.analysis}</p>
                      </div>
                    </div>
                  `;
                }).join('')}
              </div>
            `}
          </div>
        `;

        // Brechas y Vacíos
        let gapsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs text-slate-500 font-bold uppercase tracking-wider">Vacíos Empíricos y Metodológicos</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${gaps.map(g => `
                <div class="p-4 rounded-xl border border-white/5 bg-white/[0.01] hover:bg-white/[0.02] flex flex-col gap-2">
                  <div class="flex justify-between items-center">
                    <span class="text-[10px] text-slate-500 font-mono font-semibold">${g.gap_id}</span>
                    <span class="text-[10px] bg-indigo-500/10 text-indigo-400 py-0.5 px-2 rounded border border-indigo-500/20 font-semibold">${g.category}</span>
                  </div>
                  <p class="text-xs text-slate-200 mt-1 font-semibold">${g.description}</p>
                  <div class="bg-black/20 p-2.5 rounded border-l-2 border-indigo-500/50 mt-1">
                    <span class="text-[9px] uppercase font-bold text-slate-500 block mb-0.5">Evidencia Faltante Necesaria</span>
                    <p class="text-[11px] text-slate-400 italic">${g.missing_evidence}</p>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;

        // Preguntas Abiertas
        let questionsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs text-slate-500 font-bold uppercase tracking-wider">Líneas de Investigación Futura / Preguntas Abiertas</h4>
            <div class="space-y-3">
              ${questions.map(q => `
                <div class="p-4 rounded-xl border border-white/5 bg-white/[0.01] flex flex-col gap-1.5">
                  <span class="text-[10px] text-slate-500 font-mono font-semibold">${q.question_id}</span>
                  <p class="text-xs text-emerald-400 font-semibold font-display">"¿${q.question.replace(/^\?|\?$/g, '')}?"</p>
                  <p class="text-xs text-slate-400 leading-relaxed"><strong class="text-slate-300">Relevancia teórica:</strong> ${q.relevance}</p>
                </div>
              `).join('')}
            </div>
          </div>
        `;

        container.innerHTML = auditHTML + contradictionsHTML + gapsHTML + questionsHTML;

      } else if (type === 'synthesis') {
        const summary = data.executive_summary || {};
        const cards = data.synthesis_cards || [];
        const recommendations = data.strategic_recommendations || [];

        // Resumen Ejecutivo
        let summaryHTML = `
          <div class="p-5 rounded-2xl bg-gradient-to-br from-indigo-500/5 to-emerald-500/5 border border-white/5 flex flex-col gap-3">
            <h4 class="text-xs text-emerald-400 font-bold uppercase tracking-wider">Resumen Ejecutivo (TL;DR)</h4>
            <p class="font-display font-medium text-white text-md italic leading-relaxed">"${summary.tldr}"</p>
            <div class="border-t border-white/5 my-2 pt-3">
              <h5 class="text-xs text-slate-500 font-bold uppercase tracking-wider mb-2">Análisis de Síntesis</h5>
              <p class="text-xs text-slate-300 leading-relaxed">${summary.core_narrative}</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2 border-t border-white/5 pt-3">
              <div>
                <h5 class="text-xs text-slate-500 font-bold uppercase tracking-wider mb-2">Puntos Clave Clave</h5>
                <ul class="list-disc pl-4 space-y-1 text-xs text-slate-300">
                  ${summary.key_takeaways.map(t => `<li>${t}</li>`).join('')}
                </ul>
              </div>
              <div>
                <h5 class="text-xs text-slate-500 font-bold uppercase tracking-wider mb-1">Audiencia Objetivo</h5>
                <span class="text-xs inline-block bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 py-1 px-3 rounded-full mt-1">
                  ${summary.target_audience}
                </span>
              </div>
            </div>
          </div>
        `;

        // Synthesis Cards
        let cardsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs text-slate-500 font-bold uppercase tracking-wider">Fichas de Síntesis y Acción</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${cards.map(card => {
                const priorityClass = card.priority_level === 'Alta' 
                  ? 'text-red-400 bg-red-500/10 border-red-500/20' 
                  : (card.priority_level === 'Media' ? 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20' : 'text-slate-300 bg-white/5 border-white/10');
                return `
                  <div class="p-4 rounded-xl border border-white/5 bg-white/[0.01] hover:bg-white/[0.02] flex flex-col gap-2">
                    <div class="flex justify-between items-center">
                      <span class="text-[9px] text-slate-500 font-mono font-semibold">${card.card_id} - ${card.topic}</span>
                      <span class="text-[10px] border py-0.5 px-2 rounded-full font-semibold ${priorityClass}">Prioridad: ${card.priority_level}</span>
                    </div>
                    <h5 class="text-xs font-semibold text-white mt-1">${card.core_insight}</h5>
                    
                    <div class="bg-emerald-500/5 p-2.5 rounded border-l-2 border-emerald-500/50 mt-1">
                      <span class="text-[9px] uppercase font-bold text-emerald-400 block mb-0.5">Implicación Práctica</span>
                      <p class="text-[11px] text-slate-300 leading-relaxed">${card.actionable_implication}</p>
                    </div>

                    ${card.key_metrics_or_data && card.key_metrics_or_data.length > 0 ? `
                      <div class="mt-2 text-[10px] text-slate-400">
                        <strong>Métricas / Datos de Respaldo:</strong>
                        <ul class="list-disc pl-4 space-y-0.5 mt-1 font-mono">
                          ${card.key_metrics_or_data.map(m => `<li>${m}</li>`).join('')}
                        </ul>
                      </div>
                    ` : ''}
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;

        // Recomendaciones Estratégicas
        let recsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs text-slate-500 font-bold uppercase tracking-wider">Pasos Recomendados / Plan Estratégico</h4>
            <div class="relative pl-6 space-y-5 border-l border-white/10 ml-3">
              ${recommendations.map(r => `
                <div class="relative">
                  <!-- Bullet Circle -->
                  <div class="absolute -left-[31px] top-0 h-4.5 w-4.5 rounded-full bg-emerald-500 text-white flex justify-center items-center text-[10px] font-bold border-2 border-[#05070c] shadow">
                    ${r.step_number}
                  </div>
                  <h5 class="text-xs font-semibold text-white font-display">${r.action_title}</h5>
                  <p class="text-xs text-slate-400 mt-1 leading-relaxed">${r.description}</p>
                </div>
              `).join('')}
            </div>
          </div>
        `;

        container.innerHTML = summaryHTML + cardsHTML + recsHTML;
      }

      lucide.createIcons();
    }

    function copyRawJson() {
      if (!lastAnalysisResult) return;
      const strJson = JSON.stringify(lastAnalysisResult, null, 2);
      navigator.clipboard.writeText(strJson).then(() => {
        alert('Código JSON copiado al portapapeles con éxito.');
      });
    }

    function downloadJsonReport() {
      if (!lastAnalysisResult) return;
      const blob = new Blob([JSON.stringify(lastAnalysisResult, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `synthmind_report_${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  </script>
</body>
</html>
"""

# =====================================================================
# API Endpoints
# =====================================================================

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """
    Sirve la interfaz web SPA interactiva en la ruta raíz.
    """
    return HTMLResponse(content=HTML_CONTENT)


@app.post("/api/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    analysis_type: str = Form(...),
    api_key: Optional[str] = Form(None),
    model: str = Form("gemini-2.5-flash")
):
    """
    API POST para cargar documentos y ejecutar análisis agénticos estructurados.
    """
    # 1. Validar tipos de archivos permitidos
    allowed_extensions = {".pdf", ".txt", ".md"}
    filename = file.filename
    _, ext = os.path.splitext(filename)
    if ext.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de archivo no permitido. Solo se aceptan extensiones: {', '.join(allowed_extensions)}"
        )

    # 2. Leer contenido binario
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo leer el archivo cargado: {str(e)}")

    # 3. Extraer texto del documento
    try:
        document_text = extract_text_from_file(content, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extrayendo texto del documento: {str(e)}")

    if not document_text:
        raise HTTPException(status_code=400, detail="El documento cargado no contiene texto legible.")

    # 4. Enviar a Gemini Engine y obtener respuesta estructurada en JSON
    try:
        raw_json_response = run_gemini_analysis(
            document_text=document_text,
            analysis_type=analysis_type,
            api_key=api_key,
            model_name=model
        )
        
        # Parsear para devolver el objeto JSON formateado
        parsed_data = json.loads(raw_json_response)
        return parsed_data
        
    except ValueError as val_err:
        # Error al resolver la API Key u otros argumentos locales
        raise HTTPException(status_code=400, detail=str(val_err))
    except json.JSONDecodeError:
        # Falla al decodificar la salida estructurada de Gemini
        raise HTTPException(
            status_code=502, 
            detail="Fallo crítico al validar la salida estructurada. La respuesta de Gemini no se ajusta al esquema JSON requerido."
        )
    except Exception as gen_err:
        # Cualquier otro error genérico de API o Red
        raise HTTPException(
            status_code=500, 
            detail=f"Fallo del motor agéntico de Gemini: {str(gen_err)}"
        )
