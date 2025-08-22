# Deployment Guide - Bitscopic ROI Calculator

## 🚀 Quick Deploy to Streamlit Cloud (Recommended)

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Step 1: Push to GitHub

```bash
# Create new repo on GitHub (github.com/new)
# Then add remote and push:
git remote add origin https://github.com/bitscopic/roi-calculator.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository
4. Set:
   - Branch: `main`
   - Main file path: `main.py`
5. Click "Deploy"

Your app will be live at: `https://bitscopic-roi-calculator.streamlit.app`

## 🌐 Alternative Hosting Options

### Option 1: Heroku (Production-Ready)

Create `Procfile`:
```
web: sh setup.sh && streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]\nheadless = true\nport = $PORT\nenableCORS = false\n" > ~/.streamlit/config.toml
```

Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Option 2: Railway.app (Simple)

1. Connect GitHub repo at [railway.app](https://railway.app)
2. Add environment variable: `PORT=8501`
3. Deploy automatically

### Option 3: Render.com (Free Tier)

Create `render.yaml`:
```yaml
services:
  - type: web
    name: roi-calculator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

### Option 4: Google Cloud Run

```bash
# Create Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

Deploy:
```bash
gcloud run deploy roi-calculator --source . --region us-central1
```

### Option 5: AWS EC2 / DigitalOcean

```bash
# On server:
sudo apt update && sudo apt install python3-pip
git clone https://github.com/bitscopic/roi-calculator.git
cd roi-calculator
pip3 install -r requirements.txt

# Run with systemd service or screen
screen -S roi
streamlit run main.py --server.port=80 --server.address=0.0.0.0
```

## 📦 Repository Structure

```
roi-calculator/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .gitignore             # Git ignore file
├── README.md              # Documentation
├── calculators/           # ROI calculation logic
│   ├── praedigene_calculator.py
│   └── praedialert_calculator.py
├── config/                # Configuration
│   ├── defaults.py
│   └── study_data.py
├── ui/                    # User interface
│   ├── dashboard.py
│   └── styles.py
├── utils/                 # Utilities
│   ├── data_loader.py
│   └── export_handler.py
└── data/                  # Sample data (if needed)
```

## 🔐 Environment Variables

For production, set these in your hosting platform:

```bash
# Optional - for enhanced features
STREAMLIT_THEME_PRIMARY_COLOR="#003F72"
STREAMLIT_THEME_BACKGROUND_COLOR="#FFFFFF"
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50
STREAMLIT_SERVER_ENABLE_CORS=false
```

## 📊 Resource Requirements

- **Memory**: 512MB minimum, 1GB recommended
- **CPU**: 0.5 vCPU minimum
- **Storage**: 1GB
- **Python**: 3.8+

## 🔗 Sharing Your App

Once deployed, share with users:

### Public Access
```
https://your-app-name.streamlit.app
```

### Embed in Website
```html
<iframe
  src="https://your-app-name.streamlit.app?embedded=true"
  height="600"
  width="100%"
  frameborder="0">
</iframe>
```

### Direct Link with Parameters
```
https://your-app-name.streamlit.app/?calculator=praedigene&auto_run=true
```

## 📱 Mobile Optimization

The app automatically adapts to mobile devices. For best experience:
- Use responsive containers
- Test on different screen sizes
- Keep forms simple

## 🚦 Monitoring

### Streamlit Cloud Analytics
- Built-in viewer analytics
- Resource usage monitoring
- Error tracking

### Custom Analytics (Optional)
Add to `main.py`:
```python
import streamlit as st
from datetime import datetime

# Track usage
if 'session_id' not in st.session_state:
    st.session_state.session_id = datetime.now().isoformat()
    # Log to your analytics service
```

## 🆘 Troubleshooting

### Common Issues

1. **"No module named X"**
   - Add missing module to requirements.txt
   - Redeploy

2. **"Port already in use"**
   - Change port in deployment settings
   - Use environment variable PORT

3. **"Memory exceeded"**
   - Optimize data processing
   - Upgrade hosting plan

4. **"Connection timeout"**
   - Add keep-alive settings
   - Check firewall rules

## 📄 License Considerations

Add `LICENSE` file if open-sourcing:
```
MIT License
Copyright (c) 2025 Bitscopic
```

## 🎯 Next Steps

1. **Test locally**: `streamlit run main.py`
2. **Push to GitHub**: `git push origin main`
3. **Deploy to Streamlit Cloud**: Follow steps above
4. **Share URL**: Send to users
5. **Monitor usage**: Check analytics dashboard

---

**Support**: For deployment help, contact vafa@bitscopic.com