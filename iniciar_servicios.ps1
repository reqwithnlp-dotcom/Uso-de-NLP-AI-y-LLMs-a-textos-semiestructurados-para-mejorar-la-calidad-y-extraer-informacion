<#
.SYNOPSIS
    Alias en español para start_services.ps1
#>
[CmdletBinding()]
param(
    [switch]$Stop,
    [switch]$Status,
    [switch]$IncludeWebDoc
)

$target = Join-Path $PSScriptRoot "start_services.ps1"
& $target @PSBoundParameters
