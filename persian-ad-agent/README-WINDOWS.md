# راهنمای نصب و اجرای Persian Ad Agent در ویندوز

این راهنما برای Windows 10 و Windows 11 است. نسخه فعلی پروژه به API Key، Docker یا سرویس پولی نیاز ندارد.

## ۱) پیش‌نیازها

- Python 3.11 یا جدیدتر
- FFmpeg و ffprobe، در دسترس از طریق PATH
- فونت فارسی مانند Vazirmatn یا Noto Sans Arabic
- Git (فقط برای روش دریافت با git clone؛ برای ZIP لازم نیست)

### نصب Python
1. از [صفحه دانلود Python برای ویندوز](https://www.python.org/downloads/windows/) نسخه 3.11 یا جدیدتر را دانلود و نصب کنید.
2. هنگام نصب گزینه **Add python.exe to PATH** را فعال کنید.
3. یک PowerShell جدید باز کنید و بررسی کنید:

```powershell
py --version
python --version
```

باید نسخه 3.11 یا بالاتر نمایش داده شود. اگر `py` شناخته نشد، نصب Python Launcher را بررسی کنید.

### نصب FFmpeg
1. به [صفحه دانلود FFmpeg ویندوز](https://www.gyan.dev/ffmpeg/builds/) بروید و نسخه **release essentials** را دانلود کنید.
2. فایل را Extract کنید و پوشه را مثلاً به `C:\ffmpeg` منتقل کنید.
3. مطمئن شوید این دو فایل وجود دارند:

```text
C:\ffmpeg\bin\ffmpeg.exe
C:\ffmpeg\bin\ffprobe.exe
```

4. مسیر `C:\ffmpeg\bin` را به PATH اضافه کنید:
   - در Start عبارت **Environment Variables** را جست‌وجو کنید.
   - **Edit the system environment variables** و سپس **Environment Variables** را باز کنید.
   - در بخش User variables، گزینه `Path` را انتخاب و Edit کنید.
   - New را بزنید و `C:\ffmpeg\bin` را اضافه کنید؛ پنجره‌ها را با OK ببندید.
5. PowerShell را ببندید، دوباره باز کنید و تست بگیرید:

```powershell
ffmpeg -version
ffprobe -version
```

اگر نسخه‌ها نمایش داده شدند، FFmpeg آماده است. در غیر این صورت PATH را بررسی کنید.

### نصب فونت فارسی
1. فونت [Vazirmatn](https://github.com/rastikerdar/vazirmatn) را دریافت کنید.
2. فایل TTF را باز کنید و **Install** را بزنید.
3. مسیر فایل فونت را پیدا کنید؛ برای مثال:

```text
C:\Windows\Fonts\Vazirmatn-Regular.ttf
```

نام فایل در سیستم شما ممکن است متفاوت باشد؛ در مراحل بعد مسیر واقعی را وارد کنید.

## ۲) دریافت پروژه

**روش اول ـ با Git:**

```powershell
git clone https://github.com/pouyanaderi/Persian-Ad-Agent.git
cd Persian-Ad-Agent\persian-ad-agent
```

**روش دوم ـ با ZIP:**
1. ZIP پروژه را از GitHub دانلود و Extract کنید.
2. وارد پوشه `persian-ad-agent` شوید؛ همان پوشه‌ای که `requirements.txt` و پوشه `app` در آن هستند.
3. در نوار آدرس File Explorer بنویسید `powershell` و Enter بزنید تا ترمینال در همان مسیر باز شود.

از اینجا به بعد همه دستورها را در ریشه پروژه اجرا کنید. برای اطمینان:

```powershell
Get-ChildItem
```

باید `requirements.txt`، پوشه‌های `app` و `tests` و فایل‌های پروژه را ببینید.

## ۳) ساخت و فعال‌سازی محیط مجازی

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

اگر Python شما نسخه جدیدتری است و دستور اول نسخه را پیدا نکرد، از `py -m venv .venv` استفاده کنید. پس از فعال‌سازی معمولاً `(.venv)` ابتدای خط فرمان دیده می‌شود.

**اگر خطای Execution Policy گرفتید**، فقط برای همین پنجره PowerShell اجرا کنید و دوباره فعال‌سازی را انجام دهید:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## ۴) نصب کتابخانه‌ها

در حالی که محیط مجازی فعال است:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

این دستور FastAPI، Uvicorn، Pillow و سایر وابستگی‌های پروژه را نصب می‌کند.

## ۵) معرفی فونت به برنامه

قبل از اجرای سرور، مسیر فونت فارسی را در همان PowerShell تنظیم کنید (مسیر نمونه را با مسیر واقعی فایل خودتان جایگزین کنید):

```powershell
$env:FONT_PATH = "C:\Windows\Fonts\Vazirmatn-Regular.ttf"
```

برای اطمینان از درست بودن مسیر:

```powershell
Test-Path $env:FONT_PATH
```

خروجی باید `True` باشد.

**نکته درباره فایل .env:** در نسخه فعلی کد، فایل `.env` به‌صورت خودکار بارگذاری نمی‌شود؛ برنامه متغیرها را از محیط سیستم می‌خواند. بنابراین برای تنظیم فونت از دستور PowerShell بالا استفاده کنید. این مقدار تا وقتی همین پنجره باز است معتبر می‌ماند.

## ۶) اجرای برنامه

از ریشه پروژه و با محیط مجازی فعال اجرا کنید:

```powershell
python -m uvicorn app.main:app --reload
```

وقتی پیام مشابه زیر را دیدید، سرور اجرا شده است:

```text
Uvicorn running on http://127.0.0.1:8000
```

مرورگر را باز کنید و وارد آدرس زیر شوید:

**http://127.0.0.1:8000**

برای بررسی سلامت API نیز آدرس **http://127.0.0.1:8000/health** را باز کنید؛ پاسخ باید شامل `"status":"ok"` باشد.

برای متوقف‌کردن سرور در PowerShell کلیدهای `Ctrl + C` را بزنید.

## ۷) ساخت اولین ویدیو

1. عکس محصول با فرمت JPG، PNG یا WEBP و حداکثر حجم ۱۵ مگابایت انتخاب کنید.
2. توضیح محصول و سبک تبلیغ را به فارسی وارد کنید.
3. در صورت نیاز تیتر و متن دعوت به اقدام را تعیین کنید.
4. مدت ویدیو را بین ۴ تا ۲۰ ثانیه انتخاب کنید.
5. نسبت تصویر را انتخاب کنید: `9:16` برای ریلز/استوری و `16:9` برای ویدیوی افقی.
6. روی **ساخت ویدیو** بزنید.
7. پس از پایان پردازش، MP4 را پخش یا دانلود کنید؛ فایل زیرنویس SRT نیز جداگانه قابل دریافت است.

خروجی‌ها به‌صورت پیش‌فرض در مسیر `data\jobs` ذخیره می‌شوند.

## ۸) اجرای تست‌ها (اختیاری)

با فعال بودن محیط مجازی:

```powershell
pytest -q
```

## ۹) رفع خطاهای رایج

**FFmpeg پیدا نمی‌شود:** دستور `ffmpeg -version` را در PowerShell جدید امتحان کنید و PATH را بررسی کنید. اگر FFmpeg در مسیر دیگری نصب شده، پیش از اجرای سرور مسیر کامل را تعیین کنید:

```powershell
$env:FFMPEG_BIN = "C:\ffmpeg\bin\ffmpeg.exe"
```

**فونت پیدا نمی‌شود:** مسیر فایل TTF را اصلاح کنید و `Test-Path $env:FONT_PATH` را اجرا کنید.

**ماژول Python پیدا نمی‌شود:** محیط مجازی را فعال و وابستگی‌ها را مجدداً نصب کنید:

```powershell
python -m pip install -r requirements.txt
```

**پورت ۸۰۰۰ اشغال است:** برنامه را روی پورت دیگری اجرا کنید:

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

سپس `http://127.0.0.1:8001` را باز کنید.

**حروف فارسی جدا یا به‌هم‌ریخته‌اند:** فونت فارسی و مسیر `FONT_PATH` را بررسی کنید. اگر مشکل باقی بود، Pillow را مجدداً نصب/به‌روزرسانی کنید:

```powershell
python -m pip install --upgrade --force-reinstall Pillow
```

اگر با وجود این کارها مشکل باقی ماند، ممکن است نسخه نصب‌شده Pillow پشتیبانی لازم از شکل‌دهی متن راست‌به‌چپ (RAQM) را نداشته باشد.

## ۱۰) محدودیت‌های نسخه فعلی

- این نسخه با FFmpeg از عکس محصول و افکت حرکت آرام (Ken Burns) و متن فارسی ویدیو می‌سازد؛ **ویدیوی جدید را با مدل مولد هوش مصنوعی تولید نمی‌کند**.
- برای اجرای محلی به API Key نیاز ندارد. اینترنت فقط برای دریافت اولیه ابزارها و کتابخانه‌ها لازم است.
- گویندگی خودکار فارسی (TTS) در این نسخه فعال نیست.
- برنامه را بدون احراز هویت و کنترل دسترسی روی اینترنت عمومی منتشر نکنید؛ نسخه فعلی برای اجرای محلی طراحی شده است.
