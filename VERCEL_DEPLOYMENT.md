# Vercel Deployment Guide - Image Storytelling AI

## Prerequisites

- GitHub account with repository: `https://github.com/FasihUllah7/image-storytelling-ai`
- Vercel account (free): https://vercel.com/signup
- OpenAI API key

---

## Step 1: Deploy Backend to Vercel

### 1.1 Import Backend Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository: `FasihUllah7/image-storytelling-ai`
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - **Install Command**: `pip install -r requirements.txt`

### 1.2 Configure Environment Variables

In the Vercel project settings, add:

| Name | Value |
|------|-------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `FLASK_ENV` | `production` |

### 1.3 Deploy

1. Click **"Deploy"**
2. Wait for deployment to complete
3. Copy your backend URL (e.g., `https://image-storytelling-backend.vercel.app`)

---

## Step 2: Update Frontend Configuration

### 2.1 Update API Endpoint

Open `frontend/app.js` and update line 7 with your backend URL:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : 'https://YOUR-BACKEND-URL.vercel.app/api'; // ← Replace with your actual backend URL
```

### 2.2 Commit and Push Changes

```bash
git add frontend/app.js
git commit -m "Update API endpoint for production"
git push origin main
```

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Import Frontend Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import the same GitHub repository
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

### 3.2 Deploy

1. Click **"Deploy"**
2. Wait for deployment to complete
3. Your frontend will be live at `https://image-storytelling-ai.vercel.app`

---

## Step 4: Update Backend CORS (if needed)

If your frontend URL is different from `image-storytelling-ai.vercel.app`, update the CORS settings in `backend/app.py`:

```python
"origins": [
    "http://localhost:*",
    "http://127.0.0.1:*",
    "https://*.vercel.app",
    "https://YOUR-FRONTEND-URL.vercel.app"  # ← Add your actual frontend URL
],
```

Then commit and push:

```bash
git add backend/app.py
git commit -m "Update CORS for production frontend"
git push origin main
```

Vercel will automatically redeploy your backend.

---

## Step 5: Test Your Deployment

1. Visit your frontend URL
2. Upload an image or use camera capture
3. Click "Analyze Image"
4. Verify results display correctly

### Troubleshooting

**If you see CORS errors:**
- Check that backend CORS includes your frontend URL
- Verify environment variables are set in Vercel

**If analysis fails:**
- Check Vercel backend logs for errors
- Verify `OPENAI_API_KEY` is set correctly
- Test backend health endpoint: `https://your-backend-url.vercel.app/api/health`

**If images don't upload:**
- Check browser console for errors
- Verify API endpoint URL in `frontend/app.js`

---

## ✅ Deployment Complete!

Your application is now live:
- **Frontend**: `https://image-storytelling-ai.vercel.app`
- **Backend**: `https://your-backend-name.vercel.app`

### Next Steps

- Share your live URL
- Add custom domain (optional)
- Monitor usage in Vercel dashboard
- Check OpenAI API usage
