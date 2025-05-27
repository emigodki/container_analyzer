#!/bin/bash
set -euo pipefail

read -rp "Escribe el nombre del proyecto de análisis (no espacios): " NOMBRE_PROYECTO

BASE_DIR="Proyects/$NOMBRE_PROYECTO"
mkdir -p "$BASE_DIR"
cp index_template.html "$BASE_DIR"/

cd "$BASE_DIR"

# Activa env global
if [ ! -d "../../venv-dashboard" ]; then
    python3 -m venv ../../venv-dashboard
fi
source ../../venv-dashboard/bin/activate

pip install --upgrade pip
pip install -r ../../requirements.txt

echo "===== Selección de imágenes a analizar ====="
bash ../../seleccion_imagenes.sh

echo "===== Ejecutando escaneo de vulnerabilidades ====="
bash ../../vulnerability_analysis.sh

echo "===== Unificando reportes JSON ====="
bash ../../json_unified.sh

echo "===== Generando dashboard y visualizaciones ====="
python3 ../../dashboard_por_imagen.py reporte_unificado.json

# Ruta al index final generado
DASHBOARD_HTML="dashboard_por_imagen/index.html"

echo "===== Proceso finalizado ====="
echo "En la carpeta '$BASE_DIR/dashboard_por_imagen' está el index.html con el dashboard listo!"
echo "Abriendo el dashboard..."

# Abrir el dashboard en el navegador según el sistema operativo
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$DASHBOARD_HTML"  # Linux
elif command -v open >/dev/null 2>&1; then
    open "$DASHBOARD_HTML"      # MacOS
elif command -v start >/dev/null 2>&1; then
    start "" "$DASHBOARD_HTML"  # Windows (en bash/cmd)
else
    echo "Por favor, abre manualmente: $DASHBOARD_HTML"
fi
