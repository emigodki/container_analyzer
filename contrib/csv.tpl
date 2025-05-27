"SEVERIDAD","ID VULN","PAQUETE","VERSIÓN INSTALADA","VERSIÓN CORREGIDA","DESCRIPCIÓN"
{{- range . }}
  {{- range .Vulnerabilities }}
"{{ .Severity }}","{{ .VulnerabilityID }}","{{ .PkgName }}","{{ .InstalledVersion }}","{{ .FixedVersion }}","{{ .Description | replace "\"" "'" | replace "\n" " " }}"
  {{- end }}
{{- end }}
