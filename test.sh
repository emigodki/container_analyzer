
# Ruta al index final generado
DASHBOARD_HTML="/dashboard_por_imagen/index.html"

echo "===== Proceso finalizado ====="
echo "En la carpeta 'dashboard_por_imagen' está el index.html con el dashboard listo!"
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
