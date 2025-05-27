#!/bin/bash
set -euo pipefail
imagenes_file="imagenes_a_analizar.txt"
> "$imagenes_file"

while true; do
    read -rp "Escribe el nombre de la imagen de contenedor que deseas analizar: " input
    mapfile -t results < <(podman search --format '{{.Name}}' "$input")

    if [ ${#results[@]} -eq 0 ]; then
        echo "No se encontraron imágenes con '$input'."
        continue
    fi

    echo "Resultados encontrados:"
    for i in "${!results[@]}"; do
        echo "$((i+1)). ${results[$i]}"
    done

    read -rp "Elige el número de la imagen (0 para cancelar): " sel
    if [[ "$sel" == "0" ]]; then break; fi

    imagen_elegida="${results[$((sel-1))]}"
    echo "$imagen_elegida" >> "$imagenes_file"
    read -rp "¿Quieres buscar otra imagen? (s/n): " otro
    [[ "$otro" =~ ^[Ss]$ ]] || break
done

if [[ -s "$imagenes_file" ]]; then
    echo "Imágenes seleccionadas guardadas en $imagenes_file"
else
    echo "No se seleccionó ninguna imagen. Saliendo..."
    exit 1
fi

