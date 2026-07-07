# 🎬 Video Converter

A simple, fast, and free-to-deploy web application to convert video files between **MP4** and **MKV** formats — powered by FFmpeg, FastAPI, and React.

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![React](https://img.shields.io/badge/React-18-61DAFB) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🔄 **MP4 → MKV** conversion
- 🔄 **MKV → MP4** conversion
- ⚡ Fast FFmpeg-based processing (H.264 / AAC)
- 🌐 Clean, dark-mode web UI
- 📥 One-click download of converted file
- 🧵 Non-blocking async conversion (no UI freeze)
- 🗑️ Auto-cleanup of temporary files after download

---

## 🗂️ Project Structure

```
simple-python file converter/
├── backend/
│   ├── main.py           # FastAPI server with /convert endpoints
│   ├── converter.py      # MKV → MP4 conversion logic
│   ├── converter2.py     # MP4 → MKV conversion logic
│   └── requirements.txt  # Python dependencies
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── App.jsx       # Main React UI component
        ├── main.jsx
        └── index.css
```

---

## 🛠️ Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Backend   | Python, FastAPI, Uvicorn, anyio         |
| Converter | FFmpeg via `imageio-ffmpeg`             |
| Frontend  | React 18, Vite, Tailwind CSS            |
| Styling   | Tailwind CSS v3 (dark mode, cyan theme) |

---

## 🚀 Local Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/QadirKhan9/Real-video-converter.git  
cd "simple-python file converter"
```

---

### 2. Run the Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

> **API Docs**: Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

### 3. Run the Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at: `http://localhost:5173`

---

## 🌐 API Endpoints

| Method | Endpoint              | Description       | Input    | Output   |
|--------|-----------------------|-------------------|----------|----------|
| GET    | `/`                   | Health check      | —        | JSON     |
| POST   | `/convert`            | Convert MP4 → MKV | MP4 file | MKV file |
| POST   | `/convert-mkv-to-mp4` | Convert MKV → MP4 | MKV file | MP4 file |

### Example (curl)

```bash
# Convert MP4 to MKV
curl -X POST "http://127.0.0.1:8000/convert" \
  -F "file=@your-video.mp4" \
  --output converted.mkv

# Convert MKV to MP4
curl -X POST "http://127.0.0.1:8000/convert-mkv-to-mp4" \
  -F "file=@your-video.mkv" \
  --output converted.mp4
```

---

## ☁️ Free Deployment

### Backend → [Render](https://render.com)

1. Push project to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo and set:

   | Setting        | Value                                          |
   |----------------|------------------------------------------------|
   | Root Directory | `backend`                                      |
   | Runtime        | Python                                         |
   | Build Command  | `pip install -r requirements.txt`              |
   | Start Command  | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | Instance Type  | Free                                           |

4. Note the deployed URL (e.g., `https://your-app.onrender.com`)

---

### Frontend → [Vercel](https://vercel.com)

1. Update the API URL in `frontend/src/App.jsx`:

   ```js
   // Replace with your Render backend URL
   const API_URL = 'https://your-app.onrender.com';
   ```

2. Go to [vercel.com](https://vercel.com) → **New Project**
3. Connect your GitHub repo and set:

   | Setting          | Value           |
   |------------------|-----------------|
   | Root Directory   | `frontend`      |
   | Framework Preset | Vite            |
   | Build Command    | `npm run build` |
   | Output Directory | `dist`          |

4. Click **Deploy** ✅

---

### ⚠️ Free Tier Limitations

| Limitation                          | Notes                                            |
|-------------------------------------|--------------------------------------------------|
| Render free spins down after 15 min | Cold start ~30–60 seconds on first request       |
| 512MB RAM on Render free            | Best for small/short video files                 |
| No persistent storage               | Not needed — app uses `/tmp` and cleans up after |

---

## 📦 Python Dependencies

```
fastapi==0.115.0
uvicorn==0.31.0
python-multipart==0.0.17
imageio-ffmpeg==0.6.0
anyio
```

> `imageio-ffmpeg` automatically downloads and bundles the FFmpeg binary — **no separate FFmpeg installation required**.

---

## 🔧 FFmpeg Encoding Settings

| Direction | Video Codec | Audio Codec | CRF | Preset |
|-----------|-------------|-------------|-----|--------|
| MKV → MP4 | H.264       | AAC 192k    | 23  | fast   |
| MP4 → MKV | H.264       | AAC 192k    | 18  | medium |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request
