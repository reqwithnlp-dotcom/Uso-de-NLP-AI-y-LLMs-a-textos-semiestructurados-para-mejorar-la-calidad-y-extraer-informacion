import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ command }) => ({
  base: command === 'build' ? '/Uso-de-NLP-AI-y-LLMs-a-textos-semiestructurados-para-mejorar-la-calidad-y-extraer-informacion/' : '/',
  plugins: [react()],
}))
