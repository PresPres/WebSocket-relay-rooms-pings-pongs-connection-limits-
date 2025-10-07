Param(
    [int]$Port = 8000,
    [string]$Host = "127.0.0.1"
)

$env:PYTHONPATH = "$(Resolve-Path ..)" + ";" + $env:PYTHONPATH

uvicorn src.app.main:app --host $Host --port $Port --reload


