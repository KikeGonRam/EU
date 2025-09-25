# Script para automatizar entorno Spark y Python correcto en PowerShell
# Guarda este archivo como activar_spark_env.ps1 y ejecútalo antes de usar Spark

$env:JAVA_HOME = "D:\java"
$env:Path = "C:\Users\luis1\.conda\envs\utvt_env;C:\Users\luis1\.conda\envs\utvt_env\Scripts;$env:JAVA_HOME\bin;" + $env:Path
$env:PYSPARK_PYTHON = "C:\Users\luis1\.conda\envs\utvt_env\python.exe"
Write-Host "JAVA_HOME configurado a: $env:JAVA_HOME"
Write-Host "PYSPARK_PYTHON configurado a: $env:PYSPARK_PYTHON"
java -version
python --version
