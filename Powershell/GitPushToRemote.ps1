#Param(
#    [string] $commitmessage
#)

if ($args.Count -eq 0 )
{
    Write-Host "Commit message is madatory"
    break;
} elseif ($args.Count -ge 2) {
    Write-Host "Too many arguments, only 1 is allowed."
    break;
}


$branch = git branch
if ($branch -contains '* master') {
    Write-Host "you are on master branch, where push is not allowed by this script."
    break;
}

Write-Host " Push the changes..."
$commitmessage = $args[0]
git add .
git commit -m $commitmessage
git push