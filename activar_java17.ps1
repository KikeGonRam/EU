# Script para automatizar el uso de Java 17 para Spark en PowerShell
# Guarda este archivo como activar_java17.ps1 y ejecútalo antes de usar Spark

$env:JAVA_HOME = "D:\java"
$env:Path = "$env:JAVA_HOME\bin;" + $env:Path
Write-Host "JAVA_HOME configurado a: $env:JAVA_HOME"
java -version
