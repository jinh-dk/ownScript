<#
    write the container name in argments, will remove all the container, and its image
#>
Write-Host $PSScriptRoot

foreach ($arg in $args) 
{    
    Push-Location $PSScriptRoot
    $cmd = "$PSScriptRoot\RemoveContainerAndImage.ps1 $arg"
    Invoke-Expression $cmd
    Pop-Location
}