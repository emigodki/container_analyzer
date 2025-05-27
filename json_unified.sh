#!/bin/bash
set -euo pipefail

DIRECTORIO="reportes_json"
JSON_FINAL="reporte_unificado.json"

echo "🧩 Generando JSON final unificado..."

echo "{}" > "$JSON_FINAL"

for archivo in reportes_json/*.json; do
    nombre=$(basename "$archivo" .json)
    jq --arg imagen "$nombre" --slurpfile contenido "$archivo" \
       '.[$imagen] = $contenido[0]' "$JSON_FINAL" > tmp.json && mv tmp.json "$JSON_FINAL"
done


echo "✅ JSON final generado en $JSON_FINAL"
