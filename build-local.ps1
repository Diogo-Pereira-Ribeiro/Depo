#!/usr/bin/env pwsh

<#
.SYNOPSIS
Script local para compilar extensões e gerar índice
.DESCRIPTION
Compila as extensões do repositório e gera o index.min.json localmente para testes
#>

param(
    [switch]$CleanBuild,
    [switch]$Publish
)

$ErrorActionPreference = "Continue"

Write-Host "🚀 Iniciando build de extensões..." -ForegroundColor Cyan

# Limpar build anterior se solicitado
if ($CleanBuild) {
    Write-Host "🗑️  Limpando build anterior..." -ForegroundColor Yellow
    & .\gradlew clean
}

# Compilar todas as extensões
Write-Host "📦 Compilando extensões..." -ForegroundColor Cyan
& .\gradlew :src:pt:hentaistube:assembleRelease -x lint --stacktrace 2>&1 | Tee-Object -Variable buildOutput

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Build completado com avisos (alguns podem ser esperados)" -ForegroundColor Yellow
}

# Criar estrutura do repositório
Write-Host "📁 Criando estrutura do repositório..." -ForegroundColor Cyan
$repoDir = "repo/apk"
$iconDir = "repo/icon"

if (!(Test-Path $repoDir)) {
    New-Item -ItemType Directory -Path $repoDir -Force | Out-Null
}
if (!(Test-Path $iconDir)) {
    New-Item -ItemType Directory -Path $iconDir -Force | Out-Null
}

# Copiar APKs
Write-Host "📋 Copiando APKs compilados..." -ForegroundColor Cyan
$apks = Get-ChildItem -Path "build" -Filter "*.apk" -Recurse
$apkCount = 0

foreach ($apk in $apks) {
    Copy-Item -Path $apk.FullName -Destination "$repoDir\" -Force -ErrorAction SilentlyContinue
    $apkCount++
    Write-Host "  ✓ $($apk.Name)" -ForegroundColor Green
}

Write-Host "  Total: $apkCount APKs copiados" -ForegroundColor Green

# Gerar índice
Write-Host "📝 Gerando índice..." -ForegroundColor Cyan
python3 .github/scripts/generate-index.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Índice gerado com sucesso!" -ForegroundColor Green
    
    # Mostrar ficheiros gerados
    Write-Host "`n📄 Ficheiros de índice:" -ForegroundColor Cyan
    Get-Item -Path "index.json", "index.min.json", "repo.json" -ErrorAction SilentlyContinue | 
        ForEach-Object { Write-Host "  ✓ $($_.Name) ($([math]::Round($_.Length / 1KB, 2)) KB)" -ForegroundColor Green }
    
    Write-Host "`n📁 Estrutura repo/:" -ForegroundColor Cyan
    Get-ChildItem -Path "repo" -Recurse | ForEach-Object {
        $level = ($_.FullName -split '\\').Length - ($repoDir -split '\\').Length
        $indent = "  " * $level
        Write-Host "$indent✓ $($_.Name)" -ForegroundColor Green
    }
    
    # Mostrar conteúdo do índice
    Write-Host "`n📊 Resumo do repositório:" -ForegroundColor Cyan
    $index = Get-Content "index.min.json" | ConvertFrom-Json
    Write-Host "  Nome: $($index.repo.name)" -ForegroundColor Cyan
    Write-Host "  Extensões: $($index.extensions.Count)" -ForegroundColor Cyan
    Write-Host "  Gerado: $($index.generated)" -ForegroundColor Cyan
    
    if ($Publish) {
        Write-Host "`n🚀 Preparando para publicar..." -ForegroundColor Cyan
        Write-Host "  Próximo passo: fazer push para branch 'repo'" -ForegroundColor Yellow
        Write-Host "  Link: https://raw.githubusercontent.com/Diogo-Pereira-Ribeiro/Depo/repo/index.min.json" -ForegroundColor Cyan
    }
}
else {
    Write-Host "❌ Erro ao gerar índice" -ForegroundColor Red
    exit 1
}

Write-Host "`n✨ Build completo!" -ForegroundColor Green
