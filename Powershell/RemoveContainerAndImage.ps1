<#
    .DESCRIPTION
        Remove the container and its image.
    .DEPENDENCY
        Powershell Docker module.
        https://github.com/Microsoft/Docker-PowerShell
#>

Param (
    [string]$name
)

Write-Host $name

Stop-Container $name
$image = (Get-Container -ContainerIdOrName $name).Image
Remove-Container $name

# Looking for other container which also use this image
$other_container = (Get-Container | Where-Object {$_.Image -eq $image}).Names
Stop-Container $other_containers
Remove-Container $other_container

Remove-ContainerImage $image