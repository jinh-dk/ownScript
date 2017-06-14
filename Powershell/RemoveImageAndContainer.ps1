<#
    .DESCRIPTION
        Remove a image and all container using this image.
#>

Param (
    [string]$image
)

$names = (Get-Container | Where-Object {$_.Image -eq $image}).Names

foreach ($name in $names) 
{
    Write-Host "Stop and remove container $name"
    Stop-Container $name
    Remove-Container $name
}

Write-Host "Stop and image $name"
Remove-ContainerImage $image

