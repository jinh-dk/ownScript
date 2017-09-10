<#
    Create the test document from test script.
#>

param(
    [string]$folder,
    [string]$outputfilename,
    [string]$filetype = "cs"
)

Push-Location $folder
$files = (Get-ChildItem . -Filter "*.$filetype" | Select-Object -ExpandProperty Name)
foreach ($file in $files)
{
    Write-Host $file
    $lines = Get-Content $file
    foreach($line in $lines)
    {
        if( $line -match '.*public\s+.+Test\(.+' ) 
        {
            # Write-Test name
            if ( $line -match "public\s+.+Task")
            {
                $content += $line -replace "public\s+.+Task", ""
            }
            elseif ($line -match "public\s+void")
            {
                $content += $line -replace "public\s+void", ""
            }
            $content += "`r`n"  
        }
        
        if( $line -match '////\s*[Ss]tep\s+:') 
        {
            # Write-Test name
            $content += $line -replace "////", ""
            $content += "`r`n"  
        }
    }
}
Pop-Location
$content | Set-Content $outputfilename


