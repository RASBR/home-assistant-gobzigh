# Gobzigh Integration Installation Script for Home Assistant (Windows)
# This script helps install the Gobzigh integration into your Home Assistant instance

param(
    [Parameter(Mandatory=$true)]
    [string]$ConfigPath
)

Write-Host "🏠 Gobzigh Home Assistant Integration Installer" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

$CustomComponentsDir = Join-Path $ConfigPath "custom_components"
$GobzighDir = Join-Path $CustomComponentsDir "gobzigh"

Write-Host "📁 Installing to: $ConfigPath" -ForegroundColor Blue
Write-Host ""

# Create custom_components directory if it doesn't exist
if (!(Test-Path $CustomComponentsDir)) {
    Write-Host "📂 Creating custom_components directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $CustomComponentsDir -Force | Out-Null
}

# Check if gobzigh integration already exists
if (Test-Path $GobzighDir) {
    Write-Host "⚠️  Gobzigh integration already exists at $GobzighDir" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/N)"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "❌ Installation cancelled." -ForegroundColor Red
        exit 1
    }
    Write-Host "🗑️  Removing existing installation..." -ForegroundColor Yellow
    Remove-Item -Path $GobzighDir -Recurse -Force
}

# Copy the integration
Write-Host "📋 Copying Gobzigh integration files..." -ForegroundColor Blue
$SourceDir = Join-Path $PSScriptRoot "custom_components\gobzigh"
Copy-Item -Path $SourceDir -Destination $CustomComponentsDir -Recurse

Write-Host ""
Write-Host "✅ Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart Home Assistant" -ForegroundColor White
Write-Host "2. Go to Configuration → Integrations" -ForegroundColor White
Write-Host "3. Click '+ ADD INTEGRATION'" -ForegroundColor White
Write-Host "4. Search for 'Gobzigh' and select it" -ForegroundColor White
Write-Host "5. Enter your 24-character User ID (e.g., 507f1f77bcf86cd799439011)" -ForegroundColor White
Write-Host "6. Add discovered devices as needed" -ForegroundColor White
Write-Host ""
Write-Host "📖 For more information, see:" -ForegroundColor Cyan
Write-Host "   - README.md for detailed documentation" -ForegroundColor White
Write-Host "   - CONFIGURATION.md for setup guide" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Enjoy your new Gobzigh integration!" -ForegroundColor Green

# Example usage information
Write-Host ""
Write-Host "Example usage:" -ForegroundColor DarkGray
Write-Host "  .\install.ps1 -ConfigPath 'C:\path\to\homeassistant\config'" -ForegroundColor DarkGray
Write-Host "  .\install.ps1 -ConfigPath '\\server\config'" -ForegroundColor DarkGray
