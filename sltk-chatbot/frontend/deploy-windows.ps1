# SLTK Chatbot - Windows Server Deployment Script
# This script deploys the React frontend to Windows Server

param(
    [Parameter(Mandatory=$true)]
    [string]$IBMiHostname,
    
    [Parameter(Mandatory=$false)]
    [string]$DeployPath = "C:\inetpub\wwwroot\sltk-chatbot",
    
    [Parameter(Mandatory=$false)]
    [string]$Port = "44001"
)

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   SLTK Chatbot - Windows Deployment Script            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$apiUrl = "http://${IBMiHostname}:${Port}"
$frontendPath = $PSScriptRoot

Write-Host "📋 Configuration:" -ForegroundColor Yellow
Write-Host "   IBM i Host: $IBMiHostname" -ForegroundColor White
Write-Host "   API URL: $apiUrl" -ForegroundColor White
Write-Host "   Deploy Path: $DeployPath" -ForegroundColor White
Write-Host ""

# Step 1: Check Node.js
Write-Host "🔍 Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "   ✅ Node.js $nodeVersion found" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Node.js not found! Please install Node.js 18+ first." -ForegroundColor Red
    exit 1
}

# Step 2: Create .env.production file
Write-Host "📝 Creating production environment file..." -ForegroundColor Yellow
$envContent = "VITE_API_URL=$apiUrl"
$envContent | Set-Content "$frontendPath\.env.production"
Write-Host "   ✅ Created .env.production" -ForegroundColor Green

# Step 3: Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
Push-Location $frontendPath
try {
    npm install
    Write-Host "   ✅ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Failed to install dependencies" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Step 4: Build production bundle
Write-Host "🔨 Building production bundle..." -ForegroundColor Yellow
try {
    npm run build
    Write-Host "   ✅ Build completed" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Step 5: Create web.config for IIS
Write-Host "⚙️  Creating IIS configuration..." -ForegroundColor Yellow
$webConfig = @"
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="React Routes" stopProcessing="true">
          <match url=".*" />
          <conditions logicalGrouping="MatchAll">
            <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
            <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
          </conditions>
          <action type="Rewrite" url="/" />
        </rule>
      </rules>
    </rewrite>
    <staticContent>
      <mimeMap fileExtension=".json" mimeType="application/json" />
    </staticContent>
  </system.webServer>
</configuration>
"@
$webConfig | Set-Content "$frontendPath\dist\web.config"
Write-Host "   ✅ web.config created" -ForegroundColor Green

Pop-Location

# Step 6: Display deployment options
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   ✅ Build Complete!                                   ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📂 Built files are in: $frontendPath\dist" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Deployment Options:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Option 1: Deploy to IIS" -ForegroundColor White
Write-Host "   ----------------------" -ForegroundColor Gray
Write-Host "   1. Open IIS Manager" -ForegroundColor White
Write-Host "   2. Create new website:" -ForegroundColor White
Write-Host "      - Site name: SLTK-Chatbot" -ForegroundColor White
Write-Host "      - Physical path: $frontendPath\dist" -ForegroundColor White
Write-Host "      - Binding: http://ae1dcvpap23919:80" -ForegroundColor White
Write-Host "   3. Access: http://ae1dcvpap23919/" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Option 2: Test with Node.js" -ForegroundColor White
Write-Host "   --------------------------" -ForegroundColor Gray
Write-Host "   Run: npm run preview" -ForegroundColor White
Write-Host "   Access: http://localhost:4173/" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Option 3: Serve with PM2" -ForegroundColor White
Write-Host "   -----------------------" -ForegroundColor Gray
Write-Host "   npm install -g serve pm2" -ForegroundColor White
Write-Host "   pm2 serve $frontendPath\dist 80 --name sltk-chatbot --spa" -ForegroundColor White
Write-Host "   Access: http://ae1dcvpap23919/" -ForegroundColor Cyan
Write-Host ""
Write-Host "🧪 Test IBM i Backend:" -ForegroundColor Yellow
Write-Host "   curl $apiUrl/" -ForegroundColor White
Write-Host ""
Write-Host "✅ Deployment preparation complete!" -ForegroundColor Green

