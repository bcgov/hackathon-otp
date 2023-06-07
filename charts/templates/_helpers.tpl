{{/*
Expand the name of the chart.
*/}}
{{- define "verify.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "verify.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" $name .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "verify.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "verify.labels" -}}
helm.sh/chart: {{ include "verify.chart" . }}
app: {{ include "verify.fullname" . }}
{{ include "verify.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/component: backend
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: {{ .Release.Name }}
app.openshift.io/runtime: nodejs
{{- end }}

{{/*
Selector labels
*/}}
{{- define "verify.selectorLabels" -}}
app.kubernetes.io/name: {{ include "verify.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "verify.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "verify.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "verify.imagePullSecrets" }}
{{- $artSa := (lookup "artifactory.devops.gov.bc.ca/v1alpha1" "ArtifactoryServiceAccount" .Release.Namespace .Values.artifactoryServiceAccount) }}
{{- if $artSa.spec }}
- name: artifacts-pull-{{ .Values.artifactoryServiceAccount }}-{{ $artSa.spec.current_plate }}
{{- else }}
{{/*
When running helm template, or using --dry-run, lookup returns an empty object
*/}}
- name: image-pull-secret-here
{{- end }}
{{- end }}

{{- define "verify.dbUserSecret" }}
{{- printf "%s-%s" (include "verify.fullname" .) "postgres-pguser-postgres" }}
{{- end }}

{{- define "verify.dbUserPgEnv" }}
- name: SQITCH_TARGET
  value: "db:pg:"
- name: PGUSER
  valueFrom:
    secretKeyRef:
      key: user
      name: {{ template "verify.dbUserSecret" . }}
- name: PGPASSWORD
  valueFrom:
    secretKeyRef:
      key: password
      name: {{ template "verify.dbUserSecret" . }}
- name: PGDATABASE
  valueFrom:
    secretKeyRef:
      key: dbname
      name: {{ template "verify.dbUserSecret" . }}
- name: PGPORT
  valueFrom:
    secretKeyRef:
      key: port
      name: {{ template "verify.dbUserSecret" . }}
- name: PGHOST
  valueFrom:
    secretKeyRef:
{{/*
  dbUsers cannot connect via pgbouncer so we use host instead of pgbouncer-host here
*/}}
      key: host
      name: {{ template "verify.dbUserSecret" . }}
{{- end }}
