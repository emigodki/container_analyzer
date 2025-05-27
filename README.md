🚢 Container Analyzer
Container Analyzer is a fully automated solution for scanning container images for vulnerabilities (Docker/Podman) and generating interactive, professional dashboards in HTML. It’s designed for security teams, consultants, DevOps, teachers, and anyone who needs quick, visual, and actionable risk reports from container scans.

🌟 Main Features
Interactive image selection via CLI (Bash)

Efficient download/caching of images in global directories to avoid repeated downloads

Automated vulnerability scanning using Trivy

Report generation (JSON, CSV, MD, HTML) and beautiful dashboards

Global and per-image views: charts, tables, search, export to PDF

Project-based organization: each analysis has its own folder, easy to replicate or share

📁 Project Structure
graphql
Copiar
Editar
container_analyzer/
├── main.sh                     # Main orchestration script
├── seleccion_imagenes.sh       # Interactive image selection (Bash)
├── vulnerability_analysis.sh   # Scanning & reporting with Trivy
├── json_unified.sh             # JSON unification
├── dashboard_por_imagen.py     # HTML dashboard generator (Python)
├── index_template.html         # Jinja2 HTML dashboard template
├── requirements.txt            # Python requirements
├── contrib/                    # Extra templates for Trivy (e.g., csv.tpl)
├── Proyects/                   # Where all projects are created (IGNORED by git)
├── tmp/                        # Global cache of images (IGNORED by git)
├── venv-dashboard/             # Python virtual environment (IGNORED by git)
└── README.md
🚀 How to Use
1. Clone the repository and enter the folder
bash
Copiar
Editar
git clone https://github.com/emigodki/container_analyzer.git
cd container_analyzer
2. Prepare your environment
Ensure you have:

Python 3.9+

Podman (or Docker, but Podman is used by default)

Trivy

jq

Example for Linux:

bash
Copiar
Editar
sudo apt install podman jq python3-venv
wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.50.2_Linux-64bit.deb
sudo dpkg -i trivy_0.50.2_Linux-64bit.deb
3. Run the analysis
bash
Copiar
Editar
bash main.sh
What does the script do?

Asks for a project name (creates Proyects/YOUR_PROJECT)

Launches an interactive image selection tool

Downloads/saves/caches images (in tmp/)

Runs Trivy to scan and generate all reports

Generates a modern HTML dashboard with graphs and tables

Opens the dashboard automatically in your browser

4. Check your results
Find your dashboard at:
Proyects/YOUR_PROJECT/dashboard_por_imagen/index.html

All generated reports and outputs are stored within your project folder.

📊 Dashboard Content
Global view: Pie, bar, radar, and heatmap charts for severity, month, and image

Per-image view: Charts and interactive vulnerability tables

Filterable/searchable/exportable tables

Export any section to PDF

⚙️ Organization & Paths
Proyects/ and tmp/ are at the root to make caching and sharing images/results between analyses easy.

Global Python env (venv-dashboard/) and requirements.txt are at the root, so dependencies are not duplicated.

Do NOT commit anything inside Proyects/, tmp/, or venv-dashboard/.

📝 Example Workflow
bash
Copiar
Editar
bash main.sh
# Follow the CLI instructions
# (project name, image selection, etc.)
# The dashboard will open when finished
📦 Dependencies
Trivy

Podman (or Docker)

jq

Python 3.9+ with:
pandas matplotlib seaborn jinja2

Install all Python deps with:

nginx
Copiar
Editar
pip install -r requirements.txt
🙏 Credits & Contribution
Created by @emigodki
Pull requests and suggestions are welcome!
Open an issue if you find a bug or have an idea.

🛑 License
MIT — Free for academic and professional use.
