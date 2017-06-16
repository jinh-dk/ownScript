Param (
    [string]$match
)

Get-ChildItem -Recurse | Get-Content | Select-String -Pattern $match