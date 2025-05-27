import os, sys, json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Environment, FileSystemLoader
import csv
import html
import numpy as np

def cargar_datos(json_path):
    with open(json_path) as f:
        data = json.load(f)
    registros = []
    for imagen, info in data.items():
        for result in info.get("Results", []):
            for vuln in result.get("Vulnerabilities", []):
                registros.append({
                    "Imagen": imagen,
                    "Target": result.get("Target", ""),
                    "PkgName": vuln.get("PkgName", ""),
                    "InstalledVersion": vuln.get("InstalledVersion", ""),
                    "FixedVersion": vuln.get("FixedVersion", "N/A"),
                    "Fixed": vuln.get("FixedVersion") is not None,
                    "VulnerabilityID": vuln.get("VulnerabilityID", ""),
                    "Severity": vuln.get("Severity", "UNKNOWN"),
                    "Title": vuln.get("Title", vuln.get("Description", "")),
                    "Published": vuln.get("PublishedDate", vuln.get("Published", None)),
                    "Description": vuln.get("Description", "")
                })
    return pd.DataFrame(registros)

def exportar_tabla_html(tabla, path, max_desc_len=120):
    if "Description" in tabla.columns:
        tabla["Description"] = tabla["Description"].astype(str).apply(
            lambda x: html.escape(x[:max_desc_len] + ("..." if len(x) > max_desc_len else ""))
        )
    tabla_escapada = tabla.applymap(lambda x: html.escape(str(x)) if isinstance(x, str) else x)
    tabla_html = tabla_escapada.to_html(classes="tabla_vuln", index=False, border=0, escape=False)
    tabla_html = tabla_html.replace("{#", "&#123;#").replace("#}", "#&#125;")
    with open(path, "w") as f:
        f.write(tabla_html)

def pie_global(df, output_dir):
    severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']
    plt.figure(figsize=(5,5))
    df["Severity"].value_counts().reindex(severities, fill_value=0).plot.pie(
        autopct="%1.1f%%", startangle=140,
        colors=['#d32f2f', '#f57c00', '#fbc02d', '#4caf50', '#90a4ae']
    )
    plt.title("Vulnerabilidades por severidad")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pie_global.png"))
    plt.close()

def bar_global(df, output_dir):
    df = df.copy()
    df['Month'] = pd.to_datetime(df['Published'], errors='coerce').dt.to_period('M').astype(str)
    df['Month'] = df['Month'].replace('NaT', 'Desconocido')
    data = df.groupby(['Month', 'Severity']).size().unstack(fill_value=0)
    cols = ['CRITICAL','HIGH','MEDIUM','LOW','UNKNOWN']
    data = data[cols] if all(col in data.columns for col in cols) else data
    data.plot(kind="bar", stacked=True, figsize=(12,5),
              color=['#d32f2f', '#f57c00', '#fbc02d', '#4caf50', '#90a4ae'])
    plt.title("Vulnerabilidades por mes")
    plt.xlabel("Mes")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "bar_global.png"))
    plt.close()

def heatmap_vuln_por_imagen_severidad(df, output_dir):
    outpath = os.path.join(output_dir, "heatmap_img_sev.png")
    pivot = pd.pivot_table(
        df, values="VulnerabilityID",
        index="Imagen", columns="Severity",
        aggfunc="count", fill_value=0
    )
    severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']
    for s in severities:
        if s not in pivot.columns:
            pivot[s] = 0
    pivot = pivot[severities]
    plt.figure(figsize=(max(12, len(pivot)*0.8), 6))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues", linewidths=0.5)
    plt.title("Mapa de calor: Vulnerabilidades por Imagen y Severidad")
    plt.ylabel("Imagen")
    plt.xlabel("Severidad")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def radar_global(df, output_dir):
    severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']
    counts = [len(df[df["Severity"] == s]) for s in severities]
    counts += [counts[0]]
    angles = np.linspace(0, 2 * np.pi, len(severities)+1, endpoint=True)
    plt.figure(figsize=(7,7))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, counts, 'o-', linewidth=2, label='Vulnerabilidades')
    ax.fill(angles, counts, alpha=0.15)
    ax.set_thetagrids(np.degrees(angles[:-1]), severities)
    plt.title("Radar global de severidades", y=1.1)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "radar_global_comparativo.png"))
    plt.close()

def generar_graficos_por_imagen(df, output_dir="dashboard_por_imagen", csv_dir="reportes_csv"):
    os.makedirs(output_dir, exist_ok=True)
    imagenes = df["Imagen"].unique()
    resumen = []
    # Graficos globales
    pie_global(df, output_dir)
    bar_global(df, output_dir)
    radar_global(df, output_dir)
    heatmap_vuln_por_imagen_severidad(df, output_dir)

    for imagen in imagenes:
        img_safe = imagen.replace("/", "__").replace(":", "__")
        img_dir = os.path.join(output_dir, img_safe)
        os.makedirs(img_dir, exist_ok=True)
        sub_df = df[df["Imagen"] == imagen]
        # Pie Chart
        plt.figure(figsize=(5,5))
        sub_df["Severity"].value_counts().plot.pie(
            autopct="%1.1f%%", startangle=140,
            colors=['#d32f2f', '#f57c00', '#fbc02d', '#4caf50', '#90a4ae']
        )
        plt.title("Vulnerabilidades por severidad")
        plt.ylabel("")
        plt.savefig(f"{img_dir}/pie.png")
        plt.close()
        # Bar Chart
        top_pkgs = sub_df.groupby(["PkgName", "Severity"]).size().unstack(fill_value=0)
        top = top_pkgs.sum(axis=1).sort_values(ascending=False).head(10)
        top_pkgs = top_pkgs.loc[top.index]
        severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']
        for sev in severities:
            if sev not in top_pkgs.columns:
                top_pkgs[sev] = 0
        top_pkgs = top_pkgs[severities]
        top_pkgs.plot(kind="bar", stacked=True, figsize=(8,5),
                      color=['#d32f2f', '#f57c00', '#fbc02d', '#4caf50', '#90a4ae'])
        plt.title("Top paquetes vulnerables")
        plt.xlabel("PkgName")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(f"{img_dir}/bar.png")
        plt.close()
        # Area Chart
        sub_df = sub_df.copy()
        sub_df['Year'] = pd.to_datetime(sub_df['Published'], errors='coerce').dt.year
        year_severity_counts = sub_df.groupby(['Year', 'Severity']).size().unstack(fill_value=0)
        severities_area = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        for sev in severities_area:
            if sev not in year_severity_counts.columns:
                year_severity_counts[sev] = 0
        year_severity_counts = year_severity_counts[severities_area]
        if not year_severity_counts.empty:
            year_severity_counts.plot(kind='area', stacked=True, figsize=(10,5),
                                      color=['#d32f2f', '#f57c00', '#fbc02d', '#4caf50'])
            plt.title('Vulnerabilidades por Año')
            plt.ylabel('Count')
            plt.xlabel('Year')
            plt.tight_layout()
            plt.savefig(f"{img_dir}/area_year.png")
            plt.close()
        # Tabla HTML
        csv_files = [os.path.join(csv_dir, f) for f in os.listdir(csv_dir) if f.startswith(img_safe)]
        df_csvs = []
        for fcsv in csv_files:
            try:
                dfc = pd.read_csv(fcsv, quoting=csv.QUOTE_ALL, encoding="utf-8", on_bad_lines='skip')
                df_csvs.append(dfc)
            except Exception as e:
                print(f"⚠️ Error leyendo CSV {fcsv}: {e}")
        tabla_path = f"{img_dir}/tabla.html"
        tiene_tabla = False
        if df_csvs:
            tabla = pd.concat(df_csvs, ignore_index=True)
            exportar_tabla_html(tabla, tabla_path, max_desc_len=120)
            tiene_tabla = True
        else:
            empty = pd.DataFrame(columns=["SEVERIDAD", "ID VULN", "PAQUETE", "VERSIÓN INSTALADA", "VERSIÓN CORREGIDA", "DESCRIPCIÓN"])
            exportar_tabla_html(empty, tabla_path, max_desc_len=120)
            tiene_tabla = False
        with open(tabla_path, "r") as f:
            tabla_html = f.read()
        resumen.append({
            "imagen": imagen,
            "tiene_tabla": tiene_tabla,
            "tabla_html": tabla_html
        })
    return resumen

def generar_html_dashboard(imagenes, template_path="index_template.html", output_dir="dashboard_por_imagen"):
    env = Environment(loader=FileSystemLoader([output_dir, "."])) # Busca primero en output_dir
    template = env.get_template(os.path.basename(template_path))
    rendered = template.render(imagenes=imagenes)
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(rendered)

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Uso: python3 dashboard_por_categoria.py <reporte_unificado.json> [output_dir]")
        sys.exit(1)
    json_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) == 3 else "dashboard_por_imagen"
    df = cargar_datos(json_path)
    imagenes = generar_graficos_por_imagen(df, output_dir, csv_dir="reportes_csv")
    # Asume que index_template.html está en la raíz del proyecto (cópialo a cada proyecto si es necesario)
    generar_html_dashboard(imagenes, template_path="index_template.html", output_dir=output_dir)
    print("✅ Dashboard generado en carpeta:", output_dir)
