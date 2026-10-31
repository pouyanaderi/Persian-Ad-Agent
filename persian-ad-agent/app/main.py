from __future__ import annotations
import os, uuid, shutil
from pathlib import Path
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
from .copywriting import make_copy
from .video import render_video

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", "./data/jobs")).resolve()
MAX_UPLOAD = int(os.getenv("MAX_UPLOAD_MB", "15")) * 1024 * 1024
FFMPEG = os.getenv("FFMPEG_BIN", "ffmpeg")
FONT_PATH = os.getenv("FONT_PATH") or None
ALLOWED = {"image/jpeg", "image/png", "image/webp"}

app = FastAPI(title="Persian Ad Agent", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    return (APP_DIR / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status": "ok", "app": "Persian Ad Agent", "mode": "local-ffmpeg"}

@app.post("/api/generate")
async def generate(
    image: UploadFile = File(...),
    description: str = Form(..., min_length=3, max_length=1200),
    headline: str = Form(""),
    cta: str = Form("برای سفارش و اطلاعات بیشتر"),
    duration: int = Form(8, ge=4, le=20),
    aspect: str = Form("9:16"),
):
    if aspect not in {"9:16", "16:9"}:
        raise HTTPException(400, "نسبت تصویر نامعتبر است.")
    if image.content_type not in ALLOWED:
        raise HTTPException(415, "فرمت عکس باید JPG، PNG یا WEBP باشد.")
    raw = await image.read(MAX_UPLOAD + 1)
    if len(raw) > MAX_UPLOAD:
        raise HTTPException(413, f"حداکثر اندازه عکس {MAX_UPLOAD // (1024*1024)} مگابایت است.")
    job_id = uuid.uuid4().hex
    jobdir = DATA_DIR / job_id
    jobdir.mkdir(parents=True, exist_ok=False)
    source = jobdir / "source"
    source.write_bytes(raw)
    try:
        with Image.open(source) as im:
            im.verify()
        # Re-open and normalize extension after verification.
        with Image.open(source) as im:
            fmt = (im.format or "").upper()
        ext = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}.get(fmt)
        if not ext:
            raise HTTPException(415, "فرمت عکس پشتیبانی نمی‌شود.")
        image_path = jobdir / ("product" + ext)
        source.rename(image_path)
        copy = make_copy(description, headline or None, cta)
        output = jobdir / "advertisement.mp4"
        subtitles = jobdir / "subtitles.srt"
        render_video(image_path, output, subtitles, copy["headline"], copy["caption"],
                     duration=duration, aspect=aspect, ffmpeg_bin=FFMPEG, font_path=FONT_PATH)
        return {
            "job_id": job_id,
            "message": "ویدیو آماده شد.",
            "video_url": f"/api/jobs/{job_id}/video",
            "subtitle_url": f"/api/jobs/{job_id}/subtitles",
            "headline": copy["headline"],
            "caption": copy["caption"],
            "mode": "local-ken-burns",
        }
    except HTTPException:
        shutil.rmtree(jobdir, ignore_errors=True)
        raise
    except (UnidentifiedImageError, OSError) as exc:
        shutil.rmtree(jobdir, ignore_errors=True)
        raise HTTPException(400, f"فایل عکس معتبر نیست یا قابل خواندن نیست: {exc}")
    except Exception as exc:
        shutil.rmtree(jobdir, ignore_errors=True)
        raise HTTPException(500, f"ساخت ویدیو ناموفق بود: {exc}")

def _job_file(job_id: str, filename: str) -> Path:
    if not job_id.isalnum() or len(job_id) != 32:
        raise HTTPException(400, "شناسه کار نامعتبر است.")
    path = DATA_DIR / job_id / filename
    if not path.is_file():
        raise HTTPException(404, "فایل پیدا نشد. شاید کار پاک شده باشد.")
    return path

@app.get("/api/jobs/{job_id}/video")
def get_video(job_id: str):
    return FileResponse(_job_file(job_id, "advertisement.mp4"), media_type="video/mp4", filename="persian-ad.mp4")

@app.get("/api/jobs/{job_id}/subtitles")
def get_subtitles(job_id: str):
    return FileResponse(_job_file(job_id, "subtitles.srt"), media_type="application/x-subrip; charset=utf-8", filename="subtitles-fa.srt")
