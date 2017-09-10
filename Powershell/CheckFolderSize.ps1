function Get-FolderSize {

param(
    [string]$folder
)
    Write-Host $folder
    $colItems = Get-ChildItem -Recurse "$folder" | Measure-Object -property length -sum
    $sizeInMb =  "{0:N2}" -f ($colItems.sum / 1MB) + " MB"
    return $sizeInMb
}


while($true)
{
    
    $size1 = Get-FolderSize -folder C:\Users\jinxu\Documents\GitHub\kunai\master\docker\BuildServer\volumes\buildserver_01\source
    Write-Host($size1)    
    Start-Sleep -Seconds 60    
    $size2 = Get-FolderSize -folder C:\Users\jinxu\Documents\GitHub\kunai\master\docker\BuildServer\volumes\buildserver_01\source
    Write-Host($size2)    
    if($size1 -eq $size2) {
        Write-Host -BackgroundColor Red "Folder is not increased last minutes"

    }
}