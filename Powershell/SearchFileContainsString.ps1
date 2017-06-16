Param (
    [string]$match
)

Get-ChildItem -Recurse | Select-String $match | group path | select name