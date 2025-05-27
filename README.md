
# 🚢 Container Analyzer

**Container Analyzer** is a fully automated CLI solution for scanning container images (Docker/Podman) for vulnerabilities and generating modern, interactive HTML dashboards. Designed for security teams, DevOps, consultants, educators, and anyone who needs quick, visual, and actionable container risk reports.

---

## 🌟 Features

* **Interactive Image Selection:** Friendly CLI to pick images for analysis
* **Efficient Caching:** Avoids repeated downloads by caching images in a global `tmp/` directory
* **Automated Vulnerability Scanning:** Uses [Trivy](https://github.com/aquasecurity/trivy) for fast, deep scans
* **Comprehensive Reporting:** Generates JSON, CSV, Markdown, and beautiful HTML dashboards
* **Rich Visualization:** Global and per-image dashboards—charts, tables, search, PDF export
* **Project-based Organization:** Each analysis lives in its own folder for easy archiving/sharing

---

## 📁 Project Structure

```
container_analyzer/
├── main.sh                    # Main orchestration script
├── seleccion_imagenes.sh      # Interactive image selection (Bash)
├── vulnerability_analysis.sh  # Trivy-based scanning & reporting
├── json_unified.sh            # Unifies all JSON outputs
├── dashboard_por_imagen.py    # Generates HTML dashboard (Python)
├── index_template.html        # Jinja2 template for the dashboard
├── requirements.txt           # Python dependencies
├── contrib/                   # Extra Trivy templates (e.g., csv.tpl)
├── Proyects/                  # All analysis projects (GIT-IGNORED)
├── tmp/                       # Global image cache (GIT-IGNORED)
├── venv-dashboard/            # Python venv (GIT-IGNORED)
└── README.md
```

---

## 🚀 How To Use

### 1. Clone the Repository

```bash
git clone https://github.com/emigodki/container_analyzer.git
cd container_analyzer
```

### 2. Prepare Your Environment

Make sure you have:

* **Python 3.9+**
* **Podman** (or Docker, but Podman is recommended)
* **Trivy**
* **jq**

#### Example (Linux):

```bash
sudo apt install podman jq python3-venv
wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.50.2_Linux-64bit.deb
sudo dpkg -i trivy_0.50.2_Linux-64bit.deb
```

### 3. Run an Analysis

```bash
bash main.sh
```

* Enter a project name (will create `Proyects/YOUR_PROJECT`)
* Select images to analyze via CLI
* The script will:

  * Download/cache images (`tmp/`)
  * Scan with Trivy
  * Generate all reports and dashboards
  * Open your dashboard automatically in your browser!

### 4. View Your Dashboard

Find your results here:

```
Proyects/YOUR_PROJECT/dashboard_por_imagen/index.html
```

---

## 📊 Dashboard Content

* **Global View:** Pie, bar, radar, and heatmap charts for all images/severities/months
* **Per-Image View:** Charts and interactive, filterable, exportable vulnerability tables
* **PDF Export:** Any section can be exported to PDF

---

## ⚙️ Organization & Paths

* `Proyects/` and `tmp/` at repo root for shared cache between projects
* Single Python venv at root: `venv-dashboard/`
* **Do NOT commit**: `Proyects/`, `tmp/`, or `venv-dashboard/` (they’re ignored)

---

## 📝 Example Workflow

```bash
bash main.sh
# Follow the CLI (project name, select images, etc.)
# When finished, your browser will open the dashboard
```

---

## 📦 Dependencies

* [Trivy](https://github.com/aquasecurity/trivy)
* [Podman](https://podman.io/) (or Docker)
* [jq](https://stedolan.github.io/jq/)
* **Python 3.9+** with:

  * pandas
  * matplotlib
  * seaborn
  * jinja2

Install Python requirements with:

```bash
pip install -r requirements.txt
```

---

## 🙏 Credits & Contribution

Created by [@emigodki](https://github.com/emigodki)

* Pull requests, bug reports, and feature suggestions are welcome!
* Open an issue if you find a bug or have an idea.

---

## 🛑 License

**MIT** — Free for academic and professional use.

