# Pre-Push Security Verification Script
# Run this before pushing to GitHub

Write-Host "🔍 Security Check - Pre-Push Verification" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# Check 1: .env file should not be tracked
Write-Host "[1/8] Checking if .env is tracked by Git..." -ForegroundColor Yellow
$envTracked = git ls-files .env 2>$null
if ($envTracked) {
    Write-Host "❌ ERROR: .env file is being tracked by Git!" -ForegroundColor Red
    Write-Host "   Run: git rm --cached .env" -ForegroundColor Red
    $errors++
} else {
    Write-Host "✅ PASS: .env is not tracked" -ForegroundColor Green
}
Write-Host ""

# Check 2: Search for exposed API keys
Write-Host "[2/8] Searching for exposed API keys in tracked files..." -ForegroundColor Yellow
$exposedKeys = git grep "gsk_" 2>$null | Where-Object { 
    $_ -notmatch "DEPLOYMENT_GUIDE\.md" -and 
    $_ -notmatch "GITHUB_PUSH_CHECKLIST\.md" -and
    $_ -notmatch "grep" -and
    $_ -notmatch "example"
}
if ($exposedKeys) {
    Write-Host "❌ ERROR: Possible API keys found in code!" -ForegroundColor Red
    $exposedKeys | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
    $errors++
} else {
    Write-Host "✅ PASS: No exposed API keys found" -ForegroundColor Green
}
Write-Host ""

# Check 3: Verify .gitignore exists
Write-Host "[3/8] Checking .gitignore..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    if ($gitignoreContent -match "\.env" -and $gitignoreContent -match "chroma_db") {
        Write-Host "✅ PASS: .gitignore is configured correctly" -ForegroundColor Green
    } else {
        Write-Host "⚠️  WARNING: .gitignore might be incomplete" -ForegroundColor Yellow
        $warnings++
    }
} else {
    Write-Host "❌ ERROR: .gitignore not found!" -ForegroundColor Red
    $errors++
}
Write-Host ""

# Check 4: Check if chroma_db is being tracked
Write-Host "[4/8] Checking if chroma_db is tracked..." -ForegroundColor Yellow
$chromaTracked = git ls-files chroma_db/ 2>$null
if ($chromaTracked) {
    Write-Host "⚠️  WARNING: chroma_db files are being tracked" -ForegroundColor Yellow
    Write-Host "   These will be regenerated, consider untracking" -ForegroundColor Yellow
    $warnings++
} else {
    Write-Host "✅ PASS: chroma_db is not tracked" -ForegroundColor Green
}
Write-Host ""

# Check 5: Verify required config files exist
Write-Host "[5/8] Checking required configuration files..." -ForegroundColor Yellow
$requiredFiles = @(
    ".env.example",
    "secrets.toml.example",
    "requirements.txt",
    "Dockerfile",
    "DEPLOYMENT_GUIDE.md"
)
$allPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file - MISSING" -ForegroundColor Red
        $allPresent = $false
        $errors++
    }
}
if ($allPresent) {
    Write-Host "✅ PASS: All configuration files present" -ForegroundColor Green
} else {
    Write-Host "❌ ERROR: Some configuration files are missing" -ForegroundColor Red
}
Write-Host ""

# Check 6: Verify .env.example doesn't have real keys
Write-Host "[6/8] Checking .env.example for real API keys..." -ForegroundColor Yellow
if (Test-Path ".env.example") {
    $envExample = Get-Content ".env.example" -Raw
    if ($envExample -match "gsk_[a-zA-Z0-9]{40}") {
        Write-Host "ERROR: .env.example contains a real API key!" -ForegroundColor Red
        $errors++
    } else {
        Write-Host "PASS: .env.example has placeholder values only" -ForegroundColor Green
    }
} else {
    Write-Host "ERROR: .env.example not found" -ForegroundColor Red
    $errors++
}
Write-Host ""

# Check 7: Verify README doesn't have secrets
Write-Host "[7/8] Checking README for exposed secrets..." -ForegroundColor Yellow
if (Test-Path "README.md") {
    $readme = Get-Content "README.md" -Raw
    if ($readme -match "gsk_[a-zA-Z0-9]{40}") {
        Write-Host "ERROR: README contains an actual API key!" -ForegroundColor Red
        $errors++
    } else {
        Write-Host "PASS: README has no exposed secrets" -ForegroundColor Green
    }
} else {
    Write-Host "WARNING: README.md not found" -ForegroundColor Yellow
    $warnings++
}
Write-Host ""

# Check 8: Verify .env file exists locally
Write-Host "[8/8] Checking if local .env exists..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ PASS: Local .env file exists" -ForegroundColor Green
    Write-Host "   (Make sure it's in .gitignore - already verified above)" -ForegroundColor Gray
} else {
    Write-Host "⚠️  WARNING: No local .env file found" -ForegroundColor Yellow
    Write-Host "   You'll need to create one from .env.example" -ForegroundColor Yellow
    $warnings++
}
Write-Host ""

# Summary
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "🎉 ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your project is secure and ready to push to GitHub." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. git add ." -ForegroundColor White
    Write-Host "  2. git commit -m 'Initial commit: DSA Learning Assistant'" -ForegroundColor White
    Write-Host "  3. git remote add origin https://github.com/YOUR_USERNAME/repo.git" -ForegroundColor White
    Write-Host "  4. git push -u origin main" -ForegroundColor White
    Write-Host ""
} else {
    if ($errors -gt 0) {
        Write-Host "❌ ERRORS FOUND: $errors" -ForegroundColor Red
        Write-Host "   Please fix the errors above before pushing!" -ForegroundColor Red
        Write-Host ""
    }
    if ($warnings -gt 0) {
        Write-Host "⚠️  WARNINGS: $warnings" -ForegroundColor Yellow
        Write-Host "   Review warnings above (may be safe to ignore)" -ForegroundColor Yellow
        Write-Host ""
    }
    
    if ($errors -gt 0) {
        Write-Host "🚫 NOT SAFE TO PUSH YET" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "✅ Safe to push (warnings can be reviewed)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "For detailed deployment instructions, see:" -ForegroundColor Cyan
Write-Host "  DEPLOYMENT_GUIDE.md" -ForegroundColor White
Write-Host "  GITHUB_PUSH_CHECKLIST.md" -ForegroundColor White
Write-Host ""
