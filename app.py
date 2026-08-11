# app.py
# Servidor FastAPI para SynthMind AI con SPA corporativa de alta fidelidad integrada

import json
import os
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from gemini_engine import extract_text_from_file, run_gemini_analysis
from report_generator import generate_markdown_report, generate_html_report

app = FastAPI(title="SynthMind AI API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReportRequest(BaseModel):
    data: dict
    analysis_type: str

# SPA HTML de diseño corporativo y minimalista (Vercel / Stripe Aesthetic)
HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SynthMind AI — Plataforma de Análisis Agéntico Documental</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
            display: ['Outfit', 'sans-serif'],
          }
        }
      }
    }
  </script>
  <style>
    body {
      background-color: #090d16;
      color: #cbd5e1;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.04) 0%, transparent 50%),
        radial-gradient(circle at 100% 100%, rgba(99, 102, 241, 0.03) 0%, transparent 50%);
    }
    .glass-panel {
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.07);
    }
    .glass-input {
      background: rgba(3, 7, 18, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .glass-input:focus {
      border-color: #10b981;
      box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.15);
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.12);
      border-radius: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.25);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col font-sans antialiased">

  <!-- Header Superior -->
  <header class="w-full border-b border-white/10 py-3.5 px-6 flex justify-between items-center glass-panel sticky top-0 z-50">
    <div class="flex items-center gap-3">
      <div class="h-9 w-9 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex justify-center items-center text-emerald-400">
        <i data-lucide="cpu" class="h-5 w-5"></i>
      </div>
      <div>
        <h1 class="font-display font-bold text-lg tracking-tight text-white flex items-center gap-2">
          SynthMind <span class="text-xs font-mono font-medium px-2 py-0.5 rounded border border-emerald-500/30 text-emerald-400 bg-emerald-500/10 tracking-normal">Enterprise 2.5</span>
        </h1>
      </div>
    </div>
    
    <div class="flex items-center gap-4">
      <div class="hidden sm:flex items-center gap-2 bg-white/[0.03] border border-white/10 px-3 py-1.5 rounded-lg text-xs text-slate-300">
        <i data-lucide="shield-check" class="h-3.5 w-3.5 text-emerald-400"></i>
        <span>Créditos de Evaluación: <span id="credits-counter" class="font-semibold text-white">3</span> / 3</span>
      </div>
      
      <a href="https://aistudio.google.com/" target="_blank" class="text-xs text-slate-400 hover:text-white transition-colors flex items-center gap-1.5">
        <i data-lucide="key" class="h-3.5 w-3.5 text-slate-400"></i> API Key
      </a>
    </div>
  </header>

  <!-- Layout Principal -->
  <main class="flex-1 w-full max-w-7xl mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
    
    <!-- Columna Izquierda: Configuración (4 Cols) -->
    <section class="lg:col-span-4 flex flex-col gap-5">
      
      <!-- Panel Parámetros -->
      <div class="glass-panel rounded-xl p-5 flex flex-col gap-4">
        <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
          <i data-lucide="sliders" class="h-3.5 w-3.5 text-emerald-400"></i> Parámetros de Análisis
        </h2>
        
        <!-- API Key Input -->
        <div class="flex flex-col gap-1.5">
          <label class="text-xs text-slate-300 font-medium flex justify-between">
            <span>Clave de API Gemini</span>
            <span class="text-[10px] text-slate-500">Opcional si usa entorno</span>
          </label>
          <div class="relative">
            <input type="password" id="api-key" placeholder="AIzaSy..." class="w-full glass-input rounded-lg py-2 px-3 pl-8 text-xs text-white focus:outline-none transition-all font-mono">
            <i data-lucide="lock" class="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-500"></i>
            <button onclick="togglePassword()" class="absolute right-2.5 top-2.5 text-slate-500 hover:text-slate-300">
              <i data-lucide="eye" id="eye-icon" class="h-3.5 w-3.5"></i>
            </button>
          </div>
        </div>

        <!-- Modelo -->
        <div class="flex flex-col gap-1.5">
          <label class="text-xs text-slate-300 font-medium">Modelo de Lenguaje</label>
          <select id="model-select" class="w-full glass-input rounded-lg py-2 px-3 text-xs text-white focus:outline-none transition-all">
            <option value="gemini-2.5-flash" selected>Gemini 2.5 Flash (Alta Velocidad)</option>
            <option value="gemini-2.5-pro">Gemini 2.5 Pro (Razonamiento Complejo)</option>
          </select>
        </div>

        <!-- Especialización -->
        <div class="flex flex-col gap-1.5">
          <label class="text-xs text-slate-300 font-medium">Enfoque Disciplinario</label>
          <select id="specialization-select" class="w-full glass-input rounded-lg py-2 px-3 text-xs text-white focus:outline-none transition-all">
            <option value="general" selected>General / Corporativo</option>
            <option value="academic">Investigación Científica y Académica</option>
            <option value="legal">Auditoría Legal y Cumplimiento Normativo</option>
            <option value="financial">Análisis Financiero y Evaluación de Riesgo</option>
          </select>
        </div>
      </div>

      <!-- Panel Carga y Selección -->
      <div class="glass-panel rounded-xl p-5 flex-1 flex flex-col gap-4">
        <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
          <i data-lucide="file-up" class="h-3.5 w-3.5 text-emerald-400"></i> Documento y Protocolo
        </h2>

        <!-- Uploader -->
        <div class="flex flex-col gap-1.5">
          <label class="text-xs text-slate-300 font-medium">Archivo Fuente</label>
          <div id="drop-zone" class="border border-dashed border-white/15 hover:border-emerald-500/50 rounded-xl p-5 text-center cursor-pointer transition-all flex flex-col items-center gap-2 bg-black/20">
            <input type="file" id="file-input" accept=".pdf,.txt,.md" class="hidden">
            <div class="h-8 w-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex justify-center items-center" id="upload-icon-container">
              <i data-lucide="upload" class="h-4 w-4"></i>
            </div>
            <span class="text-xs text-slate-300 font-medium" id="file-name-text">Seleccionar o arrastrar documento</span>
            <span class="text-[10px] text-slate-500">PDF, TXT, MD (Hasta 15 MB)</span>
          </div>
        </div>

        <!-- Modalidad de Análisis -->
        <div class="flex flex-col gap-2">
          <label class="text-xs text-slate-300 font-medium">Protocolo Agéntico</label>
          
          <label class="flex items-start gap-3 p-3 rounded-lg border border-white/10 hover:border-emerald-500/30 cursor-pointer bg-black/20 transition-all" for="analysis-concepts">
            <input type="radio" name="analysis_type" id="analysis-concepts" value="concepts" checked class="mt-0.5 accent-emerald-500">
            <div>
              <span class="text-xs font-semibold text-white block">Mapeo Conceptual & Tesis</span>
              <span class="text-[10px] text-slate-400 block mt-0.5">Extrae jerarquías conceptuales, taxonomías y argumentos respaldados.</span>
            </div>
          </label>

          <label class="flex items-start gap-3 p-3 rounded-lg border border-white/10 hover:border-emerald-500/30 cursor-pointer bg-black/20 transition-all" for="analysis-gaps">
            <input type="radio" name="analysis_type" id="analysis-gaps" value="gaps" class="mt-0.5 accent-emerald-500">
            <div>
              <span class="text-xs font-semibold text-white block">Auditoría Crítica & Vacíos</span>
              <span class="text-[10px] text-slate-400 block mt-0.5">Identifica contradicciones internas, sesgos y preguntas abiertas.</span>
            </div>
          </label>

          <label class="flex items-start gap-3 p-3 rounded-lg border border-white/10 hover:border-emerald-500/30 cursor-pointer bg-black/20 transition-all" for="analysis-synthesis">
            <input type="radio" name="analysis_type" id="analysis-synthesis" value="synthesis" class="mt-0.5 accent-emerald-500">
            <div>
              <span class="text-xs font-semibold text-white block">Síntesis Ejecutiva & Fichas</span>
              <span class="text-[10px] text-slate-400 block mt-0.5">Genera TL;DR, directrices estratégicas y tarjetas operativas.</span>
            </div>
          </label>
        </div>

        <!-- Botón Ejecutar -->
        <button id="analyze-btn" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2.5 px-4 rounded-lg text-xs transition-all flex justify-center items-center gap-2 shadow-lg shadow-emerald-950/40">
          <i data-lucide="play" class="h-3.5 w-3.5"></i> Ejecutar Análisis Agéntico
        </button>
      </div>

    </section>

    <!-- Columna Derecha: Resultados (8 Cols) -->
    <section class="lg:col-span-8 flex flex-col min-h-[550px]">
      
      <div class="glass-panel rounded-xl flex-1 flex flex-col overflow-hidden">
        
        <!-- Barra de Estado y Exportación -->
        <div class="border-b border-white/10 bg-black/40 py-3 px-5 flex justify-between items-center">
          <div class="flex items-center gap-2.5">
            <div class="h-2 w-2 rounded-full bg-slate-600" id="status-indicator"></div>
            <span class="text-xs font-mono text-slate-400 uppercase tracking-wider" id="status-text">Consola de Resultados</span>
          </div>
          
          <div class="flex items-center gap-2" id="export-actions" style="display: none;">
            <button onclick="copyRawJson()" class="text-xs bg-white/5 hover:bg-white/10 px-2.5 py-1.5 rounded-md border border-white/10 text-slate-300 hover:text-white flex items-center gap-1.5 transition-all">
              <i data-lucide="code" class="h-3.5 w-3.5"></i> JSON Raw
            </button>
            <button onclick="downloadReport('markdown')" class="text-xs bg-white/5 hover:bg-white/10 px-2.5 py-1.5 rounded-md border border-white/10 text-slate-300 hover:text-white flex items-center gap-1.5 transition-all">
              <i data-lucide="file-text" class="h-3.5 w-3.5"></i> Word (MD)
            </button>
            <button onclick="downloadReport('html')" class="text-xs bg-emerald-500/10 hover:bg-emerald-500/20 px-2.5 py-1.5 rounded-md border border-emerald-500/30 text-emerald-400 flex items-center gap-1.5 transition-all">
              <i data-lucide="printer" class="h-3.5 w-3.5"></i> Reporte PDF
            </button>
          </div>
        </div>

        <!-- Área de Trabajo -->
        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar flex flex-col" id="result-workspace">
          
          <!-- State 1: Standby -->
          <div class="my-auto flex flex-col items-center text-center gap-3 py-12" id="placeholder-container">
            <div class="h-12 w-12 rounded-xl bg-white/[0.02] border border-white/10 flex justify-center items-center text-slate-500">
              <i data-lucide="file-search" class="h-6 w-6"></i>
            </div>
            <div>
              <h3 class="text-white font-medium text-sm">Esperando Documento</h3>
              <p class="text-xs text-slate-500 max-w-sm mt-1">Cargue un documento fuente y seleccione un protocolo para desplegar la síntesis estructurada.</p>
            </div>
          </div>

          <!-- State 2: Processing -->
          <div class="my-auto flex flex-col items-center gap-5 py-12" id="loading-container" style="display: none;">
            <div class="relative flex items-center justify-center">
              <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500"></div>
              <i data-lucide="cpu" class="absolute h-5 w-5 text-emerald-400"></i>
            </div>
            <div class="text-center">
              <h3 class="text-white font-medium text-sm" id="loading-title">Procesando Documento</h3>
              <p class="text-xs text-slate-400 mt-1 max-w-xs mx-auto" id="loading-step">Ejecutando fase de extracción...</p>
            </div>
            
            <div class="w-full max-w-xs space-y-2 mt-2 text-left">
              <div class="flex items-center gap-2 text-xs text-emerald-400" id="step-ocr">
                <i data-lucide="check" class="h-3.5 w-3.5 hidden"></i>
                <div class="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping"></div>
                <span>Fase 1: Parsing y Lectura Estructurada</span>
              </div>
              <div class="flex items-center gap-2 text-xs text-slate-500" id="step-cot">
                <i data-lucide="check" class="h-3.5 w-3.5 hidden"></i>
                <div class="h-1.5 w-1.5 rounded-full bg-slate-600"></div>
                <span>Fase 2: Razonamiento Agéntico & Auditoría</span>
              </div>
              <div class="flex items-center gap-2 text-xs text-slate-500" id="step-json">
                <i data-lucide="check" class="h-3.5 w-3.5 hidden"></i>
                <div class="h-1.5 w-1.5 rounded-full bg-slate-600"></div>
                <span>Fase 3: Validación Estricta de Esquema</span>
              </div>
            </div>
          </div>

          <!-- State 3: Output Render -->
          <div id="data-container" class="space-y-6" style="display: none;"></div>

        </div>
      </div>

    </section>

  </main>

  <!-- Modal Paywall Corporativo -->
  <div id="paywall-overlay" class="fixed inset-0 bg-black/80 backdrop-blur-md z-[1000] flex justify-center items-center opacity-0 pointer-events-none transition-opacity duration-200">
    <div class="glass-panel rounded-2xl p-8 max-w-md w-[90%] text-center border border-white/15 flex flex-col items-center gap-5 shadow-2xl">
      <div class="h-12 w-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex justify-center items-center text-emerald-400">
        <i data-lucide="shield-alert" class="h-6 w-6"></i>
      </div>
      <div>
        <h3 class="font-display font-bold text-white text-lg">Límite de Evaluación Alcanzado</h3>
        <p class="text-xs text-slate-400 mt-2 leading-relaxed">Ha agotado sus 3 créditos de prueba. Para procesamiento corporativo ilimitado, exportación ejecutiva en PDF y acceso prioritario a Gemini 2.5 Pro, active una licencia comercial.</p>
      </div>
      
      <div class="w-full bg-black/40 border border-white/10 rounded-xl p-4 text-left flex justify-between items-center">
        <div>
          <span class="text-xs font-semibold text-white block">Licencia Professional Enterprise</span>
          <span class="text-[10px] text-slate-400">Facturación Mensual</span>
        </div>
        <span class="text-base font-bold text-emerald-400 font-mono">$19 <span class="text-xs text-slate-500 font-normal">/mes</span></span>
      </div>
      
      <a href="https://stripe.com" target="_blank" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2.5 px-4 rounded-lg text-xs transition-all text-center flex justify-center items-center gap-2">
        <i data-lucide="credit-card" class="h-3.5 w-3.5"></i> Activar Licencia Comercial
      </a>
      
      <button onclick="closePaywall()" class="text-xs text-slate-500 hover:text-slate-300">Cerrar</button>
    </div>
  </div>

  <!-- Footer -->
  <footer class="w-full border-t border-white/10 py-3.5 px-6 text-center text-xs text-slate-500 font-mono">
    <span>SynthMind AI Enterprise Edition — Generación de Informes de Alta Fidelidad</span>
  </footer>

  <!-- JS Logic -->
  <script>
    let activeFile = null;
    let lastAnalysisResult = null;
    let currentAnalysisType = null;
    let credits = 3;

    document.addEventListener('DOMContentLoaded', () => {
      lucide.createIcons();
      setupFileUploader();
      initCredits();
    });

    function initCredits() {
      let savedCredits = localStorage.getItem('synthmind_credits');
      if (savedCredits === null) {
        localStorage.setItem('synthmind_credits', '3');
        savedCredits = '3';
      }
      credits = parseInt(savedCredits);
      document.getElementById('credits-counter').textContent = credits;
    }

    function decrementCredits() {
      if (credits > 0) {
        credits -= 1;
        localStorage.setItem('synthmind_credits', credits.toString());
        document.getElementById('credits-counter').textContent = credits;
      }
    }

    function showPaywall() {
      const overlay = document.getElementById('paywall-overlay');
      overlay.classList.remove('pointer-events-none', 'opacity-0');
      overlay.classList.add('opacity-100');
    }

    function closePaywall() {
      const overlay = document.getElementById('paywall-overlay');
      overlay.classList.remove('opacity-100');
      overlay.classList.add('pointer-events-none', 'opacity-0');
    }

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
      });

      ['dragleave', 'drop'].forEach(event => {
        dropZone.addEventListener(event, () => {
          dropZone.classList.remove('border-emerald-500');
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
        uploadIconContainer.className = "h-8 w-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex justify-center items-center";
        uploadIconContainer.innerHTML = '<i data-lucide="file-check" class="h-4 w-4"></i>';
        lucide.createIcons();
      }
    }

    document.getElementById('analyze-btn').addEventListener('click', async () => {
      const apiKey = document.getElementById('api-key').value;
      const model = document.getElementById('model-select').value;
      const specialization = document.getElementById('specialization-select').value;
      const analysisType = document.querySelector('input[name="analysis_type"]:checked').value;

      if (credits <= 0) {
        showPaywall();
        return;
      }

      if (!activeFile) {
        alert('Seleccione un documento en formato PDF, TXT o MD antes de ejecutar el análisis.');
        return;
      }

      document.getElementById('placeholder-container').style.display = 'none';
      document.getElementById('data-container').style.display = 'none';
      document.getElementById('export-actions').style.display = 'none';
      const loadingContainer = document.getElementById('loading-container');
      loadingContainer.style.display = 'flex';
      
      updateLoadingUI('Fase 1: Extracción Estructurada', 'Leyendo y limpiando contenido textual fuente...', 'ocr');

      const formData = new FormData();
      formData.append('file', activeFile);
      formData.append('analysis_type', analysisType);
      formData.append('model', model);
      formData.append('specialization', specialization);
      if (apiKey) {
        formData.append('api_key', apiKey);
      }

      try {
        setTimeout(() => {
          updateLoadingUI('Fase 2: Razonamiento Agéntico', 'Ejecutando auditoría de consistencia y cadena de pensamiento...', 'cot');
        }, 1500);

        setTimeout(() => {
          updateLoadingUI('Fase 3: Estructuración & Validación', 'Verificando conformidad con esquema tipado...', 'json');
        }, 4000);

        const response = await fetch('/api/analyze', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || 'Fallo durante el procesamiento en servidor.');
        }

        const data = await response.json();
        lastAnalysisResult = data;
        currentAnalysisType = analysisType;
        
        decrementCredits();
        
        loadingContainer.style.display = 'none';
        document.getElementById('export-actions').style.display = 'flex';
        const dataContainer = document.getElementById('data-container');
        dataContainer.style.display = 'block';
        
        document.getElementById('status-indicator').className = 'h-2 w-2 rounded-full bg-emerald-400';
        document.getElementById('status-text').textContent = 'Análisis Finalizado con Éxito';

        renderResult(analysisType, data);

      } catch (err) {
        loadingContainer.style.display = 'none';
        document.getElementById('placeholder-container').style.display = 'flex';
        document.getElementById('status-indicator').className = 'h-2 w-2 rounded-full bg-red-500';
        document.getElementById('status-text').textContent = 'Error en Ejecución';
        alert('Error procesando el documento: ' + err.message);
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
      const activeEl = document.getElementById(activeObj.id);
      activeEl.className = "flex items-center gap-2 text-xs text-emerald-400 font-semibold";
      activeEl.querySelector('.h-1.5').className = "h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping";
      activeEl.querySelector('i').classList.add('hidden');

      if (activeObj.complete) {
        const completes = Array.isArray(activeObj.complete) ? activeObj.complete : [activeObj.complete];
        completes.forEach(cId => {
          const el = document.getElementById(cId);
          el.className = "flex items-center gap-2 text-xs text-emerald-500";
          el.querySelector('.h-1.5').className = "h-1.5 w-1.5 rounded-full bg-emerald-500 hidden";
          el.querySelector('i').classList.remove('hidden');
        });
      }

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

        let metadataHTML = `
          <div class="p-5 rounded-xl bg-white/[0.02] border border-white/10">
            <span class="text-[10px] text-slate-500 font-mono font-semibold uppercase tracking-wider mb-2 block">Ficha Metadatos Fuente</span>
            <h3 class="font-display font-bold text-white text-base">${metadata.title || 'Documento no titulado'}</h3>
            <div class="flex flex-wrap gap-2 mt-3">
              <span class="text-[11px] bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 py-0.5 px-2.5 rounded font-mono">Dominio: ${metadata.domain}</span>
              <span class="text-[11px] bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 py-0.5 px-2.5 rounded font-mono">Tipo: ${metadata.document_type}</span>
              <span class="text-[11px] bg-slate-500/10 border border-white/10 text-slate-300 py-0.5 px-2.5 rounded font-mono">Idioma: ${metadata.language}</span>
            </div>
            ${metadata.authors && metadata.authors.length > 0 ? `
              <p class="text-xs text-slate-400 mt-3 font-mono">Autores registrados: ${metadata.authors.join(', ')}</p>
            ` : ''}
          </div>
        `;

        let conceptsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs font-mono text-slate-400 uppercase tracking-wider">1. Taxonomía de Conceptos Extraídos</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${concepts.map((concept) => {
                const confPercent = Math.round((concept.confidence_score || 0) * 100);
                return `
                  <div class="p-4 rounded-lg border border-white/10 bg-black/20 flex flex-col gap-2 relative">
                    <span class="absolute top-3 right-3 text-[10px] font-mono py-0.5 px-2 rounded bg-white/5 text-slate-300 border border-white/10">
                      Certeza: ${confPercent}%
                    </span>
                    <span class="text-[10px] text-slate-500 font-mono font-semibold">${concept.concept_id} — ${concept.category}</span>
                    <h5 class="font-semibold text-white text-xs">${concept.name}</h5>
                    <p class="text-xs text-slate-300 leading-relaxed">${concept.definition}</p>
                    
                    <details class="mt-2 text-[11px] border-t border-white/5 pt-2">
                      <summary class="text-emerald-400 hover:text-emerald-300 cursor-pointer outline-none font-medium">Ver cita original</summary>
                      <blockquote class="bg-black/40 p-2.5 rounded border-l-2 border-emerald-500 text-slate-300 italic mt-1.5 font-serif">
                        "${concept.textual_quote}"
                      </blockquote>
                    </details>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;

        let argumentsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs font-mono text-slate-400 uppercase tracking-wider">2. Tesis & Matriz de Evidencias</h4>
            <div class="space-y-4">
              ${argumentsList.map(arg => `
                <div class="p-5 rounded-xl border border-white/10 bg-black/20 flex flex-col gap-3">
                  <div class="flex justify-between items-start gap-4">
                    <div>
                      <span class="text-[10px] text-slate-500 font-mono font-semibold">${arg.argument_id}</span>
                      <h5 class="text-white text-xs font-semibold mt-0.5">${arg.claim_statement}</h5>
                    </div>
                    <span class="text-[10px] border py-0.5 px-2.5 rounded font-mono font-semibold bg-white/5 text-slate-300 border-white/10">
                      Solidez: ${arg.strength_rating}
                    </span>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-1 bg-black/30 p-3 rounded-lg border border-white/5">
                    <div>
                      <h6 class="text-[10px] font-mono uppercase text-slate-500 mb-1">Evidencias de Respaldo</h6>
                      <ul class="list-disc pl-4 space-y-1 text-xs text-slate-300">
                        ${arg.supporting_evidence.map(ev => `<li>${ev}</li>`).join('')}
                      </ul>
                    </div>
                    ${arg.counterarguments_mentioned && arg.counterarguments_mentioned.length > 0 ? `
                      <div>
                        <h6 class="text-[10px] font-mono uppercase text-slate-500 mb-1">Contraargumentos Considerados</h6>
                        <ul class="list-disc pl-4 space-y-1 text-xs text-slate-400">
                          ${arg.counterarguments_mentioned.map(ca => `<li>${ca}</li>`).join('')}
                        </ul>
                      </div>
                    ` : ''}
                  </div>
                  ${arg.source_section ? `
                    <span class="text-[10px] font-mono text-slate-500 self-end">Ubicación: ${arg.source_section}</span>
                  ` : ''}
                </div>
              `).join('')}
            </div>
          </div>
        `;

        let qualityHTML = '';
        if (qualityIssues && qualityIssues.length > 0) {
          qualityHTML = `
            <div class="p-4 rounded-lg border border-amber-500/20 bg-amber-500/5 text-amber-300 text-xs flex gap-3">
              <i data-lucide="alert-circle" class="h-4 w-4 flex-shrink-0 mt-0.5"></i>
              <div>
                <span class="font-semibold block mb-1">Observaciones Técnicas de Calidad:</span>
                <ul class="list-disc pl-4 space-y-0.5">
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

        let auditHTML = `
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="p-5 rounded-xl bg-white/[0.02] border border-white/10 text-center flex flex-col items-center justify-center">
              <span class="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1">Rigor Lógico</span>
              <span class="text-2xl font-mono font-bold text-white">${audit.overall_rigor_score} / 10</span>
            </div>
            <div class="p-5 rounded-xl bg-white/[0.02] border border-white/10 md:col-span-2">
              <span class="text-[10px] font-mono text-slate-400 uppercase tracking-wider block mb-1">Robustez Metodológica</span>
              <p class="text-xs text-slate-300 leading-relaxed">${audit.methodological_robustness}</p>
              ${audit.primary_bias_detected ? `
                <span class="text-xs text-amber-400 font-mono block mt-2">Sesgo Identificado: ${audit.primary_bias_detected}</span>
              ` : ''}
            </div>
          </div>
        `;

        let contradictionsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs font-mono text-slate-400 uppercase tracking-wider">Contradicciones Internas</h4>
            ${contradictions.length === 0 ? `
              <p class="text-xs text-slate-500 italic p-4 bg-black/20 rounded-lg border border-white/5">No se detectaron inconsistencias internas en el texto.</p>
            ` : `
              <div class="space-y-3">
                ${contradictions.map(c => `
                  <div class="p-4 rounded-xl border border-white/10 bg-black/20 flex flex-col gap-2">
                    <div class="flex justify-between items-center">
                      <span class="text-[10px] font-mono text-slate-500 font-semibold">${c.contradiction_id}</span>
                      <span class="text-[10px] font-mono py-0.5 px-2 rounded bg-red-500/10 text-red-400 border border-red-500/20">Impacto: ${c.impact_level}</span>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 bg-black/40 p-3 rounded-lg border border-white/5">
                      <div>
                        <span class="text-[9px] font-mono uppercase text-slate-500 block mb-1">Premisa A</span>
                        <p class="text-xs text-slate-300 italic">"${c.statement_a}"</p>
                      </div>
                      <div>
                        <span class="text-[9px] font-mono uppercase text-slate-500 block mb-1">Premisa B (Opuesta)</span>
                        <p class="text-xs text-slate-300 italic">"${c.statement_b}"</p>
                      </div>
                    </div>
                    <p class="text-xs text-slate-300 mt-1 leading-relaxed"><strong class="text-slate-200">Análisis:</strong> ${c.analysis}</p>
                  </div>
                `).join('')}
              </div>
            `}
          </div>
        `;

        let gapsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs font-mono text-slate-400 uppercase tracking-wider">Vacíos Empíricos Registrados</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${gaps.map(g => `
                <div class="p-4 rounded-xl border border-white/10 bg-black/20 flex flex-col gap-2">
                  <span class="text-[10px] font-mono text-slate-500 font-semibold">${g.gap_id} — ${g.category}</span>
                  <p class="text-xs text-slate-200 font-medium">${g.description}</p>
                  <p class="text-xs text-slate-400 italic bg-black/40 p-2 rounded border-l-2 border-indigo-500">Requerido: ${g.missing_evidence}</p>
                </div>
              `).join('')}
            </div>
          </div>
        `;

        let questionsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs font-mono text-slate-400 uppercase tracking-wider">Líneas de Investigación Abiertas</h4>
            <div class="space-y-3">
              ${questions.map(q => `
                <div class="p-4 rounded-xl border border-white/10 bg-black/20 flex flex-col gap-1">
                  <span class="text-[10px] font-mono text-slate-500">${q.question_id}</span>
                  <p class="text-xs font-semibold text-emerald-400 font-mono">"${q.question}"</p>
                  <p class="text-xs text-slate-400 mt-1">Relevancia: ${q.relevance}</p>
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

        let summaryHTML = `
          <div class="p-5 rounded-xl bg-white/[0.02] border border-white/10 space-y-3">
            <span class="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">Síntesis Ejecutiva TL;DR</span>
            <p class="text-sm font-semibold text-white leading-relaxed italic">"${summary.tldr}"</p>
            <p class="text-xs text-slate-300 leading-relaxed pt-2 border-t border-white/5">${summary.core_narrative}</p>
            <div class="pt-2 border-t border-white/5 flex justify-between items-center text-xs text-slate-400 font-mono">
              <span>Audiencia Objetivo: ${summary.target_audience}</span>
            </div>
          </div>
        `;

        let cardsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs font-mono text-slate-400 uppercase tracking-wider">Fichas de Acción Estratégica</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${cards.map(card => `
                <div class="p-4 rounded-xl border border-white/10 bg-black/20 flex flex-col gap-2">
                  <div class="flex justify-between items-center">
                    <span class="text-[10px] font-mono text-slate-500">${card.card_id} — ${card.topic}</span>
                    <span class="text-[10px] font-mono py-0.5 px-2 rounded bg-white/5 text-slate-300 border border-white/10">Prioridad: ${card.priority_level}</span>
                  </div>
                  <h5 class="text-xs font-semibold text-white mt-1">${card.core_insight}</h5>
                  <p class="text-xs text-slate-300 bg-emerald-500/5 p-2 rounded border-l-2 border-emerald-500/40">${card.actionable_implication}</p>
                </div>
              `).join('')}
            </div>
          </div>
        `;

        let recsHTML = `
          <div class="space-y-3">
            <h4 class="text-xs font-mono text-slate-400 uppercase tracking-wider">Plan Estratégico Sugerido</h4>
            <div class="space-y-3">
              ${recommendations.map(r => `
                <div class="p-4 rounded-xl border border-white/10 bg-black/20 flex items-start gap-3">
                  <span class="h-6 w-6 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono font-bold text-xs flex justify-center items-center flex-shrink-0">${r.step_number}</span>
                  <div>
                    <h5 class="text-xs font-semibold text-white">${r.action_title}</h5>
                    <p class="text-xs text-slate-400 mt-1 leading-relaxed">${r.description}</p>
                  </div>
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
      navigator.clipboard.writeText(JSON.stringify(lastAnalysisResult, null, 2)).then(() => {
        alert('Código JSON copiado al portapapeles.');
      });
    }

    async function downloadReport(format) {
      if (!lastAnalysisResult || !currentAnalysisType) return;
      
      try {
        const response = await fetch(`/api/report/${format}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            data: lastAnalysisResult,
            analysis_type: currentAnalysisType
          })
        });

        if (!response.ok) throw new Error('Error generando archivo');

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `synthmind_report_${currentAnalysisType}.${format === 'markdown' ? 'md' : 'html'}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (err) {
        alert('Error descargando el reporte: ' + err.message);
      }
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return HTMLResponse(content=HTML_CONTENT)


@app.post("/api/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    analysis_type: str = Form(...),
    api_key: Optional[str] = Form(None),
    model: str = Form("gemini-2.5-flash"),
    specialization: str = Form("general")
):
    allowed_extensions = {".pdf", ".txt", ".md"}
    filename = file.filename
    _, ext = os.path.splitext(filename)
    if ext.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato no permitido. Las extensiones admitidas son: {', '.join(allowed_extensions)}"
        )

    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo leer el archivo cargado: {str(e)}")

    try:
        document_text = extract_text_from_file(content, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la extracción textual del documento: {str(e)}")

    if not document_text:
        raise HTTPException(status_code=400, detail="El documento cargado no contiene texto inteligible.")

    try:
        raw_json_response = run_gemini_analysis(
            document_text=document_text,
            analysis_type=analysis_type,
            api_key=api_key,
            model_name=model,
            specialization=specialization
        )
        
        parsed_data = json.loads(raw_json_response)
        return parsed_data
        
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502, 
            detail="Fallo al validar la salida estructurada contra el esquema tipado."
        )
    except Exception as gen_err:
        raise HTTPException(
            status_code=500, 
            detail=f"Fallo del motor agéntico de Gemini: {str(gen_err)}"
        )

@app.post("/api/report/markdown")
async def get_markdown_report(payload: ReportRequest):
    md_content = generate_markdown_report(payload.data, payload.analysis_type)
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=synthmind_report_{payload.analysis_type}.md"}
    )

@app.post("/api/report/html")
async def get_html_report(payload: ReportRequest):
    html_content = generate_html_report(payload.data, payload.analysis_type)
    return Response(
        content=html_content,
        media_type="text/html",
        headers={"Content-Disposition": f"attachment; filename=synthmind_report_{payload.analysis_type}.html"}
    )
