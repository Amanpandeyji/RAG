# 🚀 Deployment Guide

## Important: GitHub Push Checklist

Before pushing to GitHub, ensure:

- [ ] `.env` file is NOT committed (check `.gitignore`)
- [ ] All API keys are in `.env` file only
- [ ] `.env.example` is created (template for others)
- [ ] `chroma_db/` is in `.gitignore` (will be regenerated)
- [ ] No hardcoded secrets in code

## 📋 Pre-Deployment Steps

### 1. Check for Exposed Secrets

```bash
# Search for potential exposed keys
grep -r "gsk_" . --exclude-dir={venv,.venv,.venv-1,chroma_db}
grep -r "api_key" . --exclude-dir={venv,.venv,.venv-1,chroma_db}
```

### 2. Verify .gitignore

Ensure these are in `.gitignore`:
```
.env
.env.*
chroma_db/
.streamlit/secrets.toml
*.log
__pycache__/
.venv/
.venv-1/
```

### 3. Create .env from Example

```bash
cp .env.example .env
# Edit .env and add your actual API key
```

## 🔐 GitHub Push Instructions

### First-Time Setup

```bash
# Initialize git (if not already)
cd "C:\Users\asus\Downloads\RAG"
git init

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/dsa-learning-assistant.git

# Create .gitignore (already done)
# Add all files
git add .

# Commit
git commit -m "Initial commit: DSA Learning Assistant with RAG"

# Push to GitHub
git push -u origin main
```

### For Existing Repository

```bash
git add .
git commit -m "Update: Add deployment configurations"
git push
```

## ☁️ Deployment Options

### ⭐ Option 1: Streamlit Cloud (Recommended)

**Note:** Vercel doesn't support Streamlit apps. Use Streamlit Cloud instead!

#### Step-by-Step:

1. **Push to GitHub** (see above)

2. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Sign in with GitHub

3. **Deploy App**
   - Click "New app"
   - Select your repository: `dsa-learning-assistant`
   - Branch: `main`
   - Main file: `app.py`
   - Click "Deploy"

4. **Add Secrets**
   - Go to App settings → Secrets
   - Add your environment variables:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   ```
   - Format: TOML (like the `secrets.toml.example` file)

5. **Done!** Your app will be live at:
   ```
   https://YOUR_USERNAME-dsa-learning-assistant.streamlit.app
   ```

#### Streamlit Cloud Features:
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Auto-deploy on git push
- ✅ Easy secret management
- ✅ Built-in monitoring

### Option 2: Heroku

#### Requirements:
Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

#### Deploy:
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set GROQ_API_KEY=your_api_key_here

# Push to Heroku
git push heroku main

# Open app
heroku open
```

### Option 3: Docker + Any Cloud (AWS, GCP, Azure)

#### Dockerfile (already in project):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run:
```bash
# Build Docker image
docker build -t dsa-assistant .

# Run locally
docker run -p 8501:8501 -e GROQ_API_KEY=your_key dsa-assistant

# Push to Docker Hub
docker tag dsa-assistant YOUR_USERNAME/dsa-assistant
docker push YOUR_USERNAME/dsa-assistant
```

#### Deploy to Cloud:
- **AWS ECS/Fargate**: Use above Docker image
- **Google Cloud Run**: One-click deploy from Docker
- **Azure Container Instances**: Deploy container

### Option 4: Railway.app

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variable: `GROQ_API_KEY`
5. Railway auto-detects Streamlit and deploys

### Option 5: Render.com

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repository
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Add environment variable: `GROQ_API_KEY`
7. Deploy

## 🔒 Security Best Practices

### 1. Never Commit Secrets
```bash
# Check what will be committed
git status
git diff

# If you accidentally committed secrets:
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all
```

### 2. Use Environment Variables
```python
# ❌ BAD - Hardcoded
GROQ_API_KEY = "gsk_1234567890"

# ✅ GOOD - From environment
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

### 3. Rotate Keys if Exposed
If you accidentally expose an API key:
1. Immediately revoke it in Groq Console
2. Generate a new key
3. Update in deployment environment
4. Remove from Git history (see above)

## 📊 Post-Deployment Checks

### 1. Test the Application
```bash
# Visit your deployed URL
# Test queries:
# - "What is an array?"
# - "Explain bubble sort"
# - "What is Big O notation?"
```

### 2. Monitor Performance
- Check Streamlit Cloud Analytics
- Monitor API usage on Groq Console
- Set up rate limiting if needed

### 3. Enable HTTPS
- Streamlit Cloud: Automatic
- Custom domain: Use Cloudflare or Let's Encrypt

## 🔧 Troubleshooting

### Issue: "GROQ_API_KEY not found"
**Solution:**
- Check environment variables in deployment platform
- Restart the app after adding secrets

### Issue: "Module not found"
**Solution:**
- Ensure `requirements.txt` is complete
- Check Python version compatibility (3.8+)

### Issue: "Vector store error"
**Solution:**
- Delete `chroma_db/` folder
- App will regenerate on first run

### Issue: Slow cold starts
**Solution:**
- Use persistent storage for `chroma_db/`
- Consider caching embeddings
- Upgrade to paid tier for faster resources

## 📝 Environment Variables Reference

| Variable | Required | Description | Where to Get |
|----------|----------|-------------|--------------|
| `GROQ_API_KEY` | ✅ Yes | Groq API authentication | https://console.groq.com/keys |
| `HF_TOKEN` | ❌ No | HuggingFace token (optional) | https://huggingface.co/settings/tokens |

## 🔄 CI/CD Setup (Optional)

### GitHub Actions for Auto-Deploy

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest test_assistant.py
```

## 📱 Custom Domain Setup

### Streamlit Cloud:
1. Go to App Settings → General
2. Add custom domain
3. Update DNS records as instructed
4. SSL is automatic

## 📈 Scaling Considerations

### Current Limits:
- Streamlit Cloud Free: 1GB RAM, 1 CPU
- Groq API: Rate limits apply

### If You Need More:
1. **Upgrade Streamlit Cloud** to Team/Enterprise
2. **Use Redis** for caching frequent queries
3. **Implement Queue System** for handling load
4. **Deploy Multiple Instances** behind load balancer

## 🎯 Quick Deploy Commands

```bash
# 1. Prepare for GitHub
git add .
git commit -m "feat: DSA Learning Assistant"
git push

# 2. Deploy to Streamlit Cloud
# Visit https://streamlit.io/cloud
# Click "New app" and follow wizard

# 3. Add secrets in Streamlit Cloud dashboard
# GROQ_API_KEY = "your_key"

# Done! ✨
```

## 📚 Additional Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Repository Best Practices](https://github.com/github/gitignore)
- [Groq API Documentation](https://console.groq.com/docs)
- [Docker Documentation](https://docs.docker.com/)

## 💡 Pro Tips

1. **Use Semantic Versioning**: Tag releases (v1.0.0, v1.1.0, etc.)
2. **Add README Badges**: Build status, version, license
3. **Enable Dependabot**: Auto-update dependencies
4. **Add Analytics**: Track usage with Streamlit or Google Analytics
5. **Monitor Costs**: Set up billing alerts for API usage

## ⚠️ Important Reminders

- ❌ Vercel does NOT support Streamlit (it's for Next.js, React, etc.)
- ✅ Use Streamlit Cloud for easiest deployment
- ✅ Always check `.gitignore` before pushing
- ✅ Never put API keys in code
- ✅ Test locally before deploying
- ✅ Keep dependencies updated

---

**Need Help?** 
- Streamlit Community: https://discuss.streamlit.io/
- GitHub Issues: Open an issue in your repository
- Documentation: Check this guide and official docs
