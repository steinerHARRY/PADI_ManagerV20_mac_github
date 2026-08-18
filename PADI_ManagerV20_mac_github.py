# created by H. Steiner, steinerh@telus.net
# all copyright reserved
# 14-08-2026

import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageTk, ImageOps
#from pdf2image import convert_from_path
import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    DictionaryObject, NameObject, NumberObject, FloatObject,
    ArrayObject, DecodedStreamObject, TextStringObject, BooleanObject
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from reportlab.lib.utils import ImageReader
import re
import hashlib
import base64
from datetime import date

# Import tkcalendar for the date picker widget
from tkcalendar import DateEntry

# ---------------- EMBEDDED APPLICATION LOGO ----------------
# Logo is stored directly in this source as Base64 PNG data.
EMBEDDED_LOGO_PNG = (
    "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"
)


editing_active = False
current_inline_entry = None

reopened_exported_pdf = False
loaded_pdf_values = {}
pdf_field_mapping = {}
pdf_field_rects = {}
tooltip_window = None
# ---------------- APPLICATION / RESOURCE PATHS ----------------

import sys
import os

# Platform flags used by Tk event bindings and diagnostics.
IS_MACOS = (sys.platform == "darwin")
import copy
import tempfile
import traceback
import shutil

APP_NAME = "PADI Manager"

def _get_resource_dir():
    """Return the directory containing read-only bundled application resources."""
    if not getattr(sys, "frozen", False):
        return Path(__file__).resolve().parent

    candidates = []

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass))

    executable = Path(sys.executable).resolve()
    candidates.append(executable.parent)

    if sys.platform == "darwin":
        # Typical .app layout:
        # App.app/Contents/MacOS/App
        candidates.append(executable.parent.parent / "Resources")
        candidates.append(executable.parent.parent)

    # Prefer a candidate containing the bundled logo or other known resource.
    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0] if candidates else Path.cwd()


def _get_user_data_dir():
    """Return a writable per-user data directory.

    The application bundle/install directory is never used for mutable data.
    This is important on macOS, where an installed .app is commonly read-only.
    """
    if sys.platform == "darwin":
        data_dir = Path.home() / "Library" / "Application Support" / APP_NAME
    elif os.name == "nt":
        root = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        data_dir = Path(root) / APP_NAME if root else Path.home() / APP_NAME
    else:
        data_dir = Path.home() / ".padi_manager"

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


RESOURCE_DIR = _get_resource_dir()
DATA_DIR = _get_user_data_dir()

# BASE_DIR is retained as the resource directory for existing resource paths.
BASE_DIR = RESOURCE_DIR

# Mutable application data belongs in the user's writable data directory.
DB_FILE = DATA_DIR / "instructors.json"
SIGNATURE_DIR = DATA_DIR / "signatures"
STATE_FILE = DATA_DIR / "state_padi.json"
COMMENTS_FILE = DATA_DIR / "comments.json"
SIGNATURE_DIR.mkdir(parents=True, exist_ok=True)

# Clean source PDFs are cached here. Exported PDFs contain a flattened/static
# appearance layer, so re-exporting an exported PDF directly would stack the
# old appearance under the new one. Keeping a clean source prevents that.
TEMPLATE_CACHE_DIR = DATA_DIR / "template_cache"
TEMPLATE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

current_base_pdf_path = None
current_base_id = None

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _cache_clean_template(path):
    """Cache a pristine PDF and return (base_id, cached_path)."""
    path = Path(path).expanduser().resolve()
    base_id = _sha256_file(path)
    cached = TEMPLATE_CACHE_DIR / f"{base_id}.pdf"
    if not cached.exists():
        shutil.copy2(path, cached)
        print("CACHED CLEAN TEMPLATE =", cached)
    return base_id, cached

def _base_id_from_pdf(path):
    """Read PADI Manager's clean-template ID from an exported PDF."""
    try:
        reader = PdfReader(str(path))
        metadata = reader.metadata or {}
        value = metadata.get("/PADIManagerBaseID")
        return str(value) if value else None
    except Exception as e:
        print("BASE ID READ WARNING:", e)
        return None

def _cached_base_for_id(base_id):
    if not base_id:
        return None
    candidate = TEMPLATE_CACHE_DIR / f"{base_id}.pdf"
    return candidate if candidate.exists() else None

def _single_cached_template():
    """Compatibility fallback for legacy exports made before base IDs existed."""
    candidates = sorted(TEMPLATE_CACHE_DIR.glob("*.pdf"))
    return candidates[0] if len(candidates) == 1 else None


def resolve_signature_path(value):
    """Resolve a saved signature path across Windows/macOS/Linux."""
    if not value:
        return None

    text = str(value)
    candidate = Path(text).expanduser()

    if candidate.exists():
        return candidate

    # A state file created on Windows can contain backslashes. On macOS/Linux
    # those are not path separators, so normalize them before taking basename.
    portable_name = Path(text.replace("\\", "/")).name
    if portable_name:
        candidate = SIGNATURE_DIR / portable_name
        if candidate.exists():
            return candidate

    return Path(text)


def _migrate_legacy_user_data():
    """Migrate old writable files from the application directory once.

    The master mask is deliberately excluded. Existing user databases and
    signatures are moved/copied into the platform-appropriate user-data
    directory so an installed macOS .app never needs write access to itself.
    """
    legacy_files = ("instructors.json", "state_padi.json", "comments.json")

    for filename in legacy_files:
        source = RESOURCE_DIR / filename
        target = DATA_DIR / filename
        if source.exists() and not target.exists():
            try:
                shutil.copy2(source, target)
                print("MIGRATED:", source, "->", target)
            except Exception as e:
                print("LEGACY DATA MIGRATION WARNING:", source, e)

    legacy_signatures = RESOURCE_DIR / "signatures"
    if legacy_signatures.exists() and legacy_signatures.is_dir():
        try:
            for source in legacy_signatures.iterdir():
                target = SIGNATURE_DIR / source.name
                if source.is_file() and not target.exists():
                    shutil.copy2(source, target)
                    print("MIGRATED SIGNATURE:", source, "->", target)
        except Exception as e:
            print("SIGNATURE MIGRATION WARNING:", e)


_migrate_legacy_user_data()


def _atomic_json_write(path, data):
    """Write JSON atomically in the writable user-data directory."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.stem}_",
        suffix=".tmp",
        dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        Path(temp_name).replace(path)
        return True
    except Exception:
        try:
            Path(temp_name).unlink(missing_ok=True)
        except Exception:
            pass
        raise


print("RESOURCE_DIR =", RESOURCE_DIR)
print("DATA_DIR =", DATA_DIR)
print("COMMENTS_FILE =", COMMENTS_FILE)
# ---------------- ZOOM SETTINGS ----------------

zoom_level_def = 0.50
ZOOM_STEP =0.1
MIN_ZOOM = 0.3
MAX_ZOOM = 3.0
zoom_level = zoom_level_def

# ---------------- Instructor Database ----------------

def load_instructors():
    if not DB_FILE.exists():
        return {"instructors": []}
    try:
        with DB_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return {"instructors": []}
    if "instructors" not in data:
        data["instructors"] = []
    return data

def save_instructors(data):
    try:
        _atomic_json_write(DB_FILE, data)
        return True
    except Exception as e:
        messagebox.showerror("Instructor Error", f"Failed to save instructor data:\n{e}")
        return False

db = load_instructors()
instructor_list = db["instructors"]

# ---------------- PDF Comments ----------------
# Comments live in a separate comments.json file and NEVER modify the field mask.
comments_db = {}

def load_comments_db():
    if not COMMENTS_FILE.exists():
        return {}
    try:
        with COMMENTS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        print("COMMENT LOAD ERROR:", e)
        return {}

def save_comments_db(data):
    try:
        _atomic_json_write(COMMENTS_FILE, data)
        return True
    except Exception as e:
        messagebox.showerror("Comment Error", f"Failed to save comments:\n{e}")
        return False

def _comment_identity(pdf_file):
    """Return stable identifiers for a PDF without touching the mask JSON."""
    path = str(Path(pdf_file).resolve()) if pdf_file else ""
    filename = Path(pdf_file).name if pdf_file else ""
    path_key = hashlib.sha256(path.encode("utf-8")).hexdigest() if path else ""
    student = str(state.get("Student Name", "")).strip() if "state" in globals() else ""
    return path_key, filename, student

def get_saved_comment(pdf_file):
    if not pdf_file:
        return ""
    path_key, filename, student = _comment_identity(pdf_file)
    record = comments_db.get(path_key)
    if isinstance(record, dict):
        return str(record.get("comment", ""))

    # Fallback: if the PDF was moved/renamed, try filename + student name.
    for item in comments_db.values():
        if not isinstance(item, dict):
            continue
        if item.get("filename") == filename and student and item.get("student_name") == student:
            return str(item.get("comment", ""))
    return ""

def save_comment_for_pdf(pdf_file, comment):
    if not pdf_file:
        messagebox.showerror("Comment", "Load a PDF before saving a comment.")
        return False

    path_key, filename, student = _comment_identity(pdf_file)
    comments_db[path_key] = {
        "filename": filename,
        "student_name": student,
        "pdf_path": str(Path(pdf_file).resolve()),
        "comment": comment,
    }
    return save_comments_db(comments_db)

def display_comment(pdf_file):
    """Load the saved comment for a PDF into the main-menu textbox."""
    if "comment_text" not in globals():
        return

    comment_text.delete("1.0", "end")
    update_comment_box_color()

    if pdf_file:
        saved = get_saved_comment(pdf_file)
        if saved:
            comment_text.insert("1.0", saved)
            update_comment_box_color()

    comment_text.see("1.0")


def save_current_comment(pdf_file=None):
    """Save the text currently in the main-menu comment box."""
    target = pdf_file or globals().get("pdf_path")
    if not target or "comment_text" not in globals():
        return False

    comment = comment_text.get("1.0", "end-1c").strip()
    return save_comment_for_pdf(target, comment)


# PDF converter  
def convert_from_path(pdf_path, dpi=200):
    """Render a PDF with PDFium while releasing native objects promptly.

    Explicit cleanup is important in a long-running frozen macOS app because
    PDFium bitmaps can otherwise retain substantial native memory.
    """
    pdf = pdfium.PdfDocument(str(pdf_path))
    rendered_pages = []
    scale = dpi / 72.0

    try:
        for page_index in range(len(pdf)):
            page = None
            bitmap = None
            try:
                page = pdf[page_index]
                bitmap = page.render(scale=scale)
                image = bitmap.to_pil().convert("RGB")
                # Detach PIL image data from the PDFium bitmap before closing it.
                image.load()
                rendered_pages.append(image.copy())
                image.close()
            finally:
                if bitmap is not None:
                    try:
                        bitmap.close()
                    except Exception:
                        pass
                if page is not None:
                    try:
                        page.close()
                    except Exception:
                        pass
    finally:
        try:
            pdf.close()
        except Exception:
            pass

    return rendered_pages
# ---------------- Field Map + State ----------------

# ---------------- EMBEDDED MASTER MASK ----------------
# The master 10056 OW Records mask is embedded directly in this source.
# No external mask JSON file is required or consulted at runtime.
HARDCODED_MASK = {
    "fields": [
        {
            "name": "Student Name",
            "type": "text",
            "page": 0,
            "x1": 204,
            "y1": 177,
            "x2": 625,
            "y2": 206
        },
        {
            "name": "Birth Date",
            "type": "text",
            "page": 0,
            "x1": 160,
            "y1": 223,
            "x2": 222,
            "y2": 252
        },
        {
            "name": "undefined",
            "type": "text",
            "page": 0,
            "x1": 242,
            "y1": 223,
            "x2": 304,
            "y2": 252
        },
        {
            "name": "undefined_2",
            "type": "text",
            "page": 0,
            "x1": 324,
            "y1": 223,
            "x2": 386,
            "y2": 252
        },
        {
            "name": "Mailing address 1",
            "type": "text",
            "page": 0,
            "x1": 215,
            "y1": 284,
            "x2": 625,
            "y2": 314
        },
        {
            "name": "Mailing address 2",
            "type": "text",
            "page": 0,
            "x1": 75,
            "y1": 340,
            "x2": 315,
            "y2": 369
        },
        {
            "name": "Mailing address 3",
            "type": "text",
            "page": 0,
            "x1": 325,
            "y1": 340,
            "x2": 427,
            "y2": 369
        },
        {
            "name": "Mailing address 4",
            "type": "text",
            "page": 0,
            "x1": 436,
            "y1": 340,
            "x2": 502,
            "y2": 369
        },
        {
            "name": "Mailing address 5",
            "type": "text",
            "page": 0,
            "x1": 512,
            "y1": 340,
            "x2": 625,
            "y2": 369
        },
        {
            "name": "undefined_3",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 419,
            "x2": 337,
            "y2": 448
        },
        {
            "name": "undefined_4",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 419,
            "x2": 625,
            "y2": 448
        },
        {
            "name": "undefined_5",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 459,
            "x2": 337,
            "y2": 489
        },
        {
            "name": "undefined_6",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 459,
            "x2": 625,
            "y2": 489
        },
        {
            "name": "undefined_7",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 500,
            "x2": 337,
            "y2": 529
        },
        {
            "name": "undefined_8",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 500,
            "x2": 625,
            "y2": 529
        },
        {
            "name": "Email",
            "type": "text",
            "page": 0,
            "x1": 125,
            "y1": 540,
            "x2": 625,
            "y2": 569
        },
        {
            "name": "init_padi_instructor_1",
            "type": "text",
            "page": 0,
            "x1": 204,
            "y1": 691,
            "x2": 625,
            "y2": 720
        },
        {
            "name": "Init_Instructor_Signature_1",
            "type": "signature",
            "page": 0,
            "x1": 165,
            "y1": 731,
            "x2": 625,
            "y2": 760
        },
        {
            "name": "Init_PADI_no_1",
            "type": "text",
            "page": 0,
            "x1": 155,
            "y1": 772,
            "x2": 275,
            "y2": 801
        },
        {
            "name": "Init_Dive_Resort_No_1",
            "type": "text",
            "page": 0,
            "x1": 494,
            "y1": 772,
            "x2": 625,
            "y2": 801
        },
        {
            "name": "Init_day_1",
            "type": "text",
            "page": 0,
            "x1": 114,
            "y1": 817,
            "x2": 177,
            "y2": 846
        },
        {
            "name": "Init_month_1",
            "type": "text",
            "page": 0,
            "x1": 197,
            "y1": 817,
            "x2": 259,
            "y2": 846
        },
        {
            "name": "Init_year_1",
            "type": "text",
            "page": 0,
            "x1": 279,
            "y1": 817,
            "x2": 341,
            "y2": 846
        },
        {
            "name": "undefined_11",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 889,
            "x2": 337,
            "y2": 919
        },
        {
            "name": "Init_Phone_1",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 889,
            "x2": 625,
            "y2": 919
        },
        {
            "name": "undefined_13",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 930,
            "x2": 337,
            "y2": 959
        },
        {
            "name": "undefined_14",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 930,
            "x2": 625,
            "y2": 959
        },
        {
            "name": "Init_Email_1",
            "type": "text",
            "page": 0,
            "x1": 125,
            "y1": 970,
            "x2": 625,
            "y2": 1000
        },
        {
            "name": "Init_padi_instructor_2",
            "type": "text",
            "page": 0,
            "x1": 204,
            "y1": 1035,
            "x2": 625,
            "y2": 1065
        },
        {
            "name": "Init_Instructor_Signature_2",
            "type": "signature",
            "page": 0,
            "x1": 165,
            "y1": 1076,
            "x2": 625,
            "y2": 1105
        },
        {
            "name": "Init_PADI_no_2",
            "type": "text",
            "page": 0,
            "x1": 155,
            "y1": 1116,
            "x2": 275,
            "y2": 1145
        },
        {
            "name": "Init_Dive_Resort_No_2",
            "type": "text",
            "page": 0,
            "x1": 494,
            "y1": 1116,
            "x2": 625,
            "y2": 1145
        },
        {
            "name": "Init_day_2",
            "type": "text",
            "page": 0,
            "x1": 114,
            "y1": 1162,
            "x2": 177,
            "y2": 1191
        },
        {
            "name": "Init_month_2",
            "type": "text",
            "page": 0,
            "x1": 197,
            "y1": 1162,
            "x2": 259,
            "y2": 1191
        },
        {
            "name": "Init_year_2",
            "type": "text",
            "page": 0,
            "x1": 279,
            "y1": 1162,
            "x2": 341,
            "y2": 1191
        },
        {
            "name": "undefined_17",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 1229,
            "x2": 337,
            "y2": 1258
        },
        {
            "name": "Init_Phone_2",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 1229,
            "x2": 625,
            "y2": 1258
        },
        {
            "name": "undefined_19",
            "type": "text",
            "page": 0,
            "x1": 277,
            "y1": 1269,
            "x2": 337,
            "y2": 1298
        },
        {
            "name": "undefined_20",
            "type": "text",
            "page": 0,
            "x1": 345,
            "y1": 1269,
            "x2": 625,
            "y2": 1298
        },
        {
            "name": "Init_Email_2",
            "type": "text",
            "page": 0,
            "x1": 125,
            "y1": 1309,
            "x2": 625,
            "y2": 1338
        },
        {
            "name": "CW2_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 244,
            "x2": 803,
            "y2": 273
        },
        {
            "name": "CW2_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 244,
            "x2": 893,
            "y2": 273
        },
        {
            "name": "CW2_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 244,
            "x2": 985,
            "y2": 273
        },
        {
            "name": "CW3_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 277,
            "x2": 803,
            "y2": 306
        },
        {
            "name": "CW3_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 277,
            "x2": 893,
            "y2": 306
        },
        {
            "name": "CW3_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 277,
            "x2": 985,
            "y2": 306
        },
        {
            "name": "CW4_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 310,
            "x2": 803,
            "y2": 339
        },
        {
            "name": "CW4_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 310,
            "x2": 893,
            "y2": 339
        },
        {
            "name": "CW4_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 310,
            "x2": 985,
            "y2": 339
        },
        {
            "name": "CW1_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 210,
            "x2": 1086,
            "y2": 239
        },
        {
            "name": "CW2_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 244,
            "x2": 1086,
            "y2": 273
        },
        {
            "name": "CW3_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 277,
            "x2": 1086,
            "y2": 306
        },
        {
            "name": "CW4_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 310,
            "x2": 1086,
            "y2": 339
        },
        {
            "name": "CW1_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 210,
            "x2": 803,
            "y2": 239
        },
        {
            "name": "CW1_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 210,
            "x2": 893,
            "y2": 239
        },
        {
            "name": "CW1_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 210,
            "x2": 985,
            "y2": 239
        },
        {
            "name": "CW1_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 210,
            "x2": 1192,
            "y2": 239
        },
        {
            "name": "CW15_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 211,
            "x2": 1407,
            "y2": 239
        },
        {
            "name": "CW15_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 211,
            "x2": 1498,
            "y2": 239
        },
        {
            "name": "CW15_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 211,
            "x2": 1588,
            "y2": 239
        },
        {
            "name": "undefined_32",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 211,
            "x2": 1761,
            "y2": 239
        },
        {
            "name": "CW15_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 211,
            "x2": 1983,
            "y2": 239
        },
        {
            "name": "CW15_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 211,
            "x2": 2117,
            "y2": 239
        },
        {
            "name": "CW2_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 244,
            "x2": 1192,
            "y2": 273
        },
        {
            "name": "CW16_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 240,
            "x2": 1407,
            "y2": 270
        },
        {
            "name": "CW16_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 240,
            "x2": 1498,
            "y2": 270
        },
        {
            "name": "CW16_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 240,
            "x2": 1588,
            "y2": 270
        },
        {
            "name": "undefined_38",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 240,
            "x2": 1761,
            "y2": 270
        },
        {
            "name": "CW16_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 240,
            "x2": 1983,
            "y2": 270
        },
        {
            "name": "CW16_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 240,
            "x2": 2117,
            "y2": 270
        },
        {
            "name": "CW3_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 277,
            "x2": 1192,
            "y2": 306
        },
        {
            "name": "CW17_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 271,
            "x2": 1407,
            "y2": 300
        },
        {
            "name": "CW17_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 271,
            "x2": 1498,
            "y2": 300
        },
        {
            "name": "CW17_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 271,
            "x2": 1588,
            "y2": 300
        },
        {
            "name": "undefined_44",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 271,
            "x2": 1761,
            "y2": 300
        },
        {
            "name": "CW17_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 271,
            "x2": 1983,
            "y2": 300
        },
        {
            "name": "CW17_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 271,
            "x2": 2117,
            "y2": 300
        },
        {
            "name": "CW4_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 310,
            "x2": 1192,
            "y2": 339
        },
        {
            "name": "CW18_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 302,
            "x2": 1407,
            "y2": 331
        },
        {
            "name": "CW18_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 302,
            "x2": 1498,
            "y2": 331
        },
        {
            "name": "CW18_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 302,
            "x2": 1588,
            "y2": 331
        },
        {
            "name": "undefined_50",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 302,
            "x2": 1761,
            "y2": 331
        },
        {
            "name": "CW18_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 302,
            "x2": 1983,
            "y2": 331
        },
        {
            "name": "CW18_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 302,
            "x2": 2117,
            "y2": 331
        },
        {
            "name": "CW5_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 343,
            "x2": 803,
            "y2": 373
        },
        {
            "name": "CW5_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 343,
            "x2": 893,
            "y2": 373
        },
        {
            "name": "CW5_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 343,
            "x2": 985,
            "y2": 373
        },
        {
            "name": "CW5_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 343,
            "x2": 1086,
            "y2": 373
        },
        {
            "name": "CW5_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 343,
            "x2": 1192,
            "y2": 373
        },
        {
            "name": "CW19_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 332,
            "x2": 1407,
            "y2": 361
        },
        {
            "name": "CW19_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 332,
            "x2": 1498,
            "y2": 361
        },
        {
            "name": "CW19_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 332,
            "x2": 1588,
            "y2": 361
        },
        {
            "name": "undefined_58",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 332,
            "x2": 1761,
            "y2": 361
        },
        {
            "name": "CW19_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 332,
            "x2": 1983,
            "y2": 361
        },
        {
            "name": "CW19_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 332,
            "x2": 2117,
            "y2": 361
        },
        {
            "name": "CW20_day",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 375,
            "x2": 1407,
            "y2": 404
        },
        {
            "name": "CW20_month",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 375,
            "x2": 1498,
            "y2": 404
        },
        {
            "name": "CW20_year",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 375,
            "x2": 1588,
            "y2": 404
        },
        {
            "name": "CW20_quizz",
            "type": "text",
            "page": 0,
            "x1": 1681,
            "y1": 375,
            "x2": 1761,
            "y2": 404
        },
        {
            "name": "CW20_initials",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 375,
            "x2": 1983,
            "y2": 404
        },
        {
            "name": "CW20_padi",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 375,
            "x2": 2117,
            "y2": 404
        },
        {
            "name": "CW6_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 486,
            "x2": 1086,
            "y2": 516
        },
        {
            "name": "CW6_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 486,
            "x2": 803,
            "y2": 516
        },
        {
            "name": "CW6_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 486,
            "x2": 893,
            "y2": 516
        },
        {
            "name": "CW6_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 486,
            "x2": 985,
            "y2": 516
        },
        {
            "name": "CW6_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 486,
            "x2": 1192,
            "y2": 516
        },
        {
            "name": "Instructor_signature_4",
            "type": "signature",
            "page": 0,
            "x1": 1379,
            "y1": 480,
            "x2": 1690,
            "y2": 509
        },
        {
            "name": "PADI_no_4",
            "type": "text",
            "page": 0,
            "x1": 1717,
            "y1": 480,
            "x2": 1832,
            "y2": 509
        },
        {
            "name": "day_4",
            "type": "text",
            "page": 0,
            "x1": 1888,
            "y1": 480,
            "x2": 1970,
            "y2": 509
        },
        {
            "name": "month_4",
            "type": "text",
            "page": 0,
            "x1": 1990,
            "y1": 480,
            "x2": 2043,
            "y2": 509
        },
        {
            "name": "year_4",
            "type": "text",
            "page": 0,
            "x1": 2063,
            "y1": 480,
            "x2": 2117,
            "y2": 509
        },
        {
            "name": "CW7_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 559,
            "x2": 985,
            "y2": 589
        },
        {
            "name": "CW7_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 559,
            "x2": 1086,
            "y2": 589
        },
        {
            "name": "CW7_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 559,
            "x2": 1192,
            "y2": 589
        },
        {
            "name": "CW7_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 559,
            "x2": 803,
            "y2": 589
        },
        {
            "name": "CW7_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 559,
            "x2": 893,
            "y2": 589
        },
        {
            "name": "CW8_initials",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 676,
            "x2": 1086,
            "y2": 705
        },
        {
            "name": "CW8_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 676,
            "x2": 1192,
            "y2": 705
        },
        {
            "name": "CW22_day",
            "type": "text",
            "page": 0,
            "x1": 1275,
            "y1": 641,
            "x2": 1328,
            "y2": 671
        },
        {
            "name": "CW22_month",
            "type": "text",
            "page": 0,
            "x1": 1348,
            "y1": 641,
            "x2": 1402,
            "y2": 671
        },
        {
            "name": "CW22_year",
            "type": "text",
            "page": 0,
            "x1": 1421,
            "y1": 641,
            "x2": 1475,
            "y2": 671
        },
        {
            "name": "CW21_initials",
            "type": "text",
            "page": 0,
            "x1": 1494,
            "y1": 612,
            "x2": 1547,
            "y2": 637
        },
        {
            "name": "CW22_initials",
            "type": "text",
            "page": 0,
            "x1": 1494,
            "y1": 641,
            "x2": 1547,
            "y2": 671
        },
        {
            "name": "CW22_padi",
            "type": "text",
            "page": 0,
            "x1": 1583,
            "y1": 641,
            "x2": 1654,
            "y2": 671
        },
        {
            "name": "CW24_day",
            "type": "text",
            "page": 0,
            "x1": 1728,
            "y1": 641,
            "x2": 1781,
            "y2": 671
        },
        {
            "name": "CW24_month",
            "type": "text",
            "page": 0,
            "x1": 1801,
            "y1": 641,
            "x2": 1854,
            "y2": 671
        },
        {
            "name": "CW24_year",
            "type": "text",
            "page": 0,
            "x1": 1874,
            "y1": 641,
            "x2": 1928,
            "y2": 671
        },
        {
            "name": "CW23_initials",
            "type": "text",
            "page": 0,
            "x1": 1956,
            "y1": 612,
            "x2": 2010,
            "y2": 637
        },
        {
            "name": "CW24_initials",
            "type": "text",
            "page": 0,
            "x1": 1956,
            "y1": 641,
            "x2": 2010,
            "y2": 671
        },
        {
            "name": "CW21_day",
            "type": "text",
            "page": 0,
            "x1": 1275,
            "y1": 612,
            "x2": 1328,
            "y2": 637
        },
        {
            "name": "CW21_month",
            "type": "text",
            "page": 0,
            "x1": 1348,
            "y1": 612,
            "x2": 1401,
            "y2": 637
        },
        {
            "name": "CW21_year",
            "type": "text",
            "page": 0,
            "x1": 1421,
            "y1": 612,
            "x2": 1475,
            "y2": 637
        },
        {
            "name": "CW21_padi",
            "type": "text",
            "page": 0,
            "x1": 1583,
            "y1": 612,
            "x2": 1654,
            "y2": 637
        },
        {
            "name": "CW23_day",
            "type": "text",
            "page": 0,
            "x1": 1728,
            "y1": 612,
            "x2": 1781,
            "y2": 637
        },
        {
            "name": "CW23_month",
            "type": "text",
            "page": 0,
            "x1": 1801,
            "y1": 612,
            "x2": 1854,
            "y2": 637
        },
        {
            "name": "CW23_year",
            "type": "text",
            "page": 0,
            "x1": 1874,
            "y1": 612,
            "x2": 1928,
            "y2": 637
        },
        {
            "name": "CW23_padi",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 612,
            "x2": 2117,
            "y2": 637
        },
        {
            "name": "CW24_padi",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 641,
            "x2": 2117,
            "y2": 671
        },
        {
            "name": "CW8_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 676,
            "x2": 803,
            "y2": 705
        },
        {
            "name": "CW8_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 676,
            "x2": 893,
            "y2": 705
        },
        {
            "name": "CW8_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 676,
            "x2": 985,
            "y2": 705
        },
        {
            "name": "CW9_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 756,
            "x2": 1086,
            "y2": 785
        },
        {
            "name": "CW9_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 756,
            "x2": 1192,
            "y2": 785
        },
        {
            "name": "CW9_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 756,
            "x2": 803,
            "y2": 785
        },
        {
            "name": "CW9_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 756,
            "x2": 893,
            "y2": 785
        },
        {
            "name": "CW9_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 756,
            "x2": 985,
            "y2": 785
        },
        {
            "name": "Dive_2",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 773,
            "x2": 1779,
            "y2": 803
        },
        {
            "name": "CW10_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 835,
            "x2": 803,
            "y2": 864
        },
        {
            "name": "CW10_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 835,
            "x2": 985,
            "y2": 864
        },
        {
            "name": "CW10_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 835,
            "x2": 1086,
            "y2": 864
        },
        {
            "name": "CW10_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 835,
            "x2": 1192,
            "y2": 864
        },
        {
            "name": "Dive_3",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 804,
            "x2": 1779,
            "y2": 833
        },
        {
            "name": "CW10_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 835,
            "x2": 893,
            "y2": 864
        },
        {
            "name": "Dive_4",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 835,
            "x2": 1779,
            "y2": 864
        },
        {
            "name": "CW11_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 915,
            "x2": 1192,
            "y2": 944
        },
        {
            "name": "Dive_5",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 865,
            "x2": 1779,
            "y2": 894
        },
        {
            "name": "CW11_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 915,
            "x2": 803,
            "y2": 944
        },
        {
            "name": "Dive_6",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 896,
            "x2": 1779,
            "y2": 925
        },
        {
            "name": "CW11_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 915,
            "x2": 893,
            "y2": 944
        },
        {
            "name": "CW11_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 915,
            "x2": 985,
            "y2": 944
        },
        {
            "name": "CW11_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 915,
            "x2": 1086,
            "y2": 944
        },
        {
            "name": "Dive_7",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 926,
            "x2": 1779,
            "y2": 956
        },
        {
            "name": "CW12_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 994,
            "x2": 1086,
            "y2": 1024
        },
        {
            "name": "CW12_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 994,
            "x2": 1192,
            "y2": 1024
        },
        {
            "name": "Dive_8",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 957,
            "x2": 1779,
            "y2": 986
        },
        {
            "name": "CW12_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 994,
            "x2": 803,
            "y2": 1024
        },
        {
            "name": "CW12_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 994,
            "x2": 893,
            "y2": 1024
        },
        {
            "name": "CW12_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 994,
            "x2": 985,
            "y2": 1024
        },
        {
            "name": "Dive_9",
            "type": "text",
            "page": 0,
            "x1": 1698,
            "y1": 988,
            "x2": 1778,
            "y2": 1017
        },
        {
            "name": "Dive_initials_1",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 744,
            "x2": 1912,
            "y2": 772
        },
        {
            "name": "Dive_initials_2",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 773,
            "x2": 1912,
            "y2": 803
        },
        {
            "name": "Dive_initials_3",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 804,
            "x2": 1912,
            "y2": 833
        },
        {
            "name": "Dive_initials_4",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 835,
            "x2": 1912,
            "y2": 864
        },
        {
            "name": "Dive_initials_5",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 865,
            "x2": 1912,
            "y2": 894
        },
        {
            "name": "Dive_initials_6",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 896,
            "x2": 1912,
            "y2": 925
        },
        {
            "name": "Dive_initials_7",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 926,
            "x2": 1912,
            "y2": 956
        },
        {
            "name": "Dive_initials_8",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 957,
            "x2": 1912,
            "y2": 986
        },
        {
            "name": "Dive_1",
            "type": "text",
            "page": 0,
            "x1": 1699,
            "y1": 744,
            "x2": 1779,
            "y2": 772
        },
        {
            "name": "Dive_padi_1",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 744,
            "x2": 2081,
            "y2": 772
        },
        {
            "name": "Dive_padi_2",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 773,
            "x2": 2081,
            "y2": 803
        },
        {
            "name": "Dive_padi_3",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 804,
            "x2": 2081,
            "y2": 833
        },
        {
            "name": "Dive_padi_4",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 835,
            "x2": 2081,
            "y2": 864
        },
        {
            "name": "Dive_padi_5",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 865,
            "x2": 2081,
            "y2": 894
        },
        {
            "name": "Dive_padi_6",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 896,
            "x2": 2081,
            "y2": 925
        },
        {
            "name": "Dive_padi_7",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 926,
            "x2": 2081,
            "y2": 956
        },
        {
            "name": "Dive_padi_8",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 957,
            "x2": 2081,
            "y2": 986
        },
        {
            "name": "Dive_padi_9",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 988,
            "x2": 2081,
            "y2": 1017
        },
        {
            "name": "CW13_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 1083,
            "x2": 985,
            "y2": 1113
        },
        {
            "name": "CW13_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 1083,
            "x2": 1086,
            "y2": 1113
        },
        {
            "name": "CW13_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 1083,
            "x2": 1192,
            "y2": 1113
        },
        {
            "name": "Dive_10",
            "type": "text",
            "page": 0,
            "x1": 1698,
            "y1": 1018,
            "x2": 1778,
            "y2": 1047
        },
        {
            "name": "Dive_padi_10",
            "type": "text",
            "page": 0,
            "x1": 1992,
            "y1": 1018,
            "x2": 2081,
            "y2": 1047
        },
        {
            "name": "CW13_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 1083,
            "x2": 803,
            "y2": 1113
        },
        {
            "name": "CW13_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 1083,
            "x2": 893,
            "y2": 1113
        },
        {
            "name": "CW14_year",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 1172,
            "x2": 985,
            "y2": 1202
        },
        {
            "name": "CW14_initials",
            "type": "text",
            "page": 0,
            "x1": 1023,
            "y1": 1172,
            "x2": 1086,
            "y2": 1202
        },
        {
            "name": "CW14_padi",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 1172,
            "x2": 1192,
            "y2": 1202
        },
        {
            "name": "Instructor_signature_5",
            "type": "signature",
            "page": 0,
            "x1": 1379,
            "y1": 1128,
            "x2": 1690,
            "y2": 1158
        },
        {
            "name": "PADI_no_5",
            "type": "text",
            "page": 0,
            "x1": 1708,
            "y1": 1128,
            "x2": 1814,
            "y2": 1158
        },
        {
            "name": "day_5",
            "type": "text",
            "page": 0,
            "x1": 1863,
            "y1": 1128,
            "x2": 1935,
            "y2": 1158
        },
        {
            "name": "month_5",
            "type": "text",
            "page": 0,
            "x1": 1954,
            "y1": 1128,
            "x2": 2026,
            "y2": 1158
        },
        {
            "name": "year_5",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 1128,
            "x2": 2117,
            "y2": 1158
        },
        {
            "name": "CW14_day",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 1172,
            "x2": 803,
            "y2": 1202
        },
        {
            "name": "CW14_month",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 1172,
            "x2": 893,
            "y2": 1202
        },
        {
            "name": "student_signature",
            "type": "signature",
            "page": 0,
            "x1": 1370,
            "y1": 1316,
            "x2": 1814,
            "y2": 1345
        },
        {
            "name": "Stu_day",
            "type": "text",
            "page": 0,
            "x1": 1869,
            "y1": 1316,
            "x2": 1940,
            "y2": 1345
        },
        {
            "name": "Stu_month",
            "type": "text",
            "page": 0,
            "x1": 1960,
            "y1": 1316,
            "x2": 2030,
            "y2": 1345
        },
        {
            "name": "Stu_year",
            "type": "text",
            "page": 0,
            "x1": 2051,
            "y1": 1316,
            "x2": 2122,
            "y2": 1345
        },
        {
            "name": "Instructor_signature_3",
            "type": "signature",
            "page": 0,
            "x1": 819,
            "y1": 1353,
            "x2": 1192,
            "y2": 1383
        },
        {
            "name": "PADI_no_3",
            "type": "text",
            "page": 0,
            "x1": 721,
            "y1": 1409,
            "x2": 890,
            "y2": 1438
        },
        {
            "name": "day_3",
            "type": "text",
            "page": 0,
            "x1": 940,
            "y1": 1409,
            "x2": 1011,
            "y2": 1438
        },
        {
            "name": "month_3",
            "type": "text",
            "page": 0,
            "x1": 1031,
            "y1": 1409,
            "x2": 1102,
            "y2": 1438
        },
        {
            "name": "year_3",
            "type": "text",
            "page": 0,
            "x1": 1122,
            "y1": 1409,
            "x2": 1193,
            "y2": 1438
        },
        {
            "name": "Instructor_signature_6",
            "type": "signature",
            "page": 0,
            "x1": 1387,
            "y1": 1459,
            "x2": 1690,
            "y2": 1488
        },
        {
            "name": "PADI_no_6",
            "type": "text",
            "page": 0,
            "x1": 1708,
            "y1": 1459,
            "x2": 1814,
            "y2": 1488
        },
        {
            "name": "day_6",
            "type": "text",
            "page": 0,
            "x1": 1863,
            "y1": 1459,
            "x2": 1935,
            "y2": 1488
        },
        {
            "name": "month_6",
            "type": "text",
            "page": 0,
            "x1": 1954,
            "y1": 1459,
            "x2": 2026,
            "y2": 1488
        },
        {
            "name": "year_6",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 1459,
            "x2": 2117,
            "y2": 1488
        },
        {
            "name": "Instructor_signature_7",
            "type": "signature",
            "page": 0,
            "x1": 1379,
            "y1": 1555,
            "x2": 1690,
            "y2": 1584
        },
        {
            "name": "PADI_no_7",
            "type": "text",
            "page": 0,
            "x1": 1708,
            "y1": 1555,
            "x2": 1814,
            "y2": 1584
        },
        {
            "name": "day_7",
            "type": "text",
            "page": 0,
            "x1": 1863,
            "y1": 1555,
            "x2": 1935,
            "y2": 1584
        },
        {
            "name": "month_7",
            "type": "text",
            "page": 0,
            "x1": 1954,
            "y1": 1555,
            "x2": 2026,
            "y2": 1584
        },
        {
            "name": "year_7",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 1555,
            "x2": 2117,
            "y2": 1584
        },
        {
            "name": "Dive_initials_9",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 988,
            "x2": 1912,
            "y2": 1017
        },
        {
            "name": "Dive_initials_10",
            "type": "text",
            "page": 0,
            "x1": 1850,
            "y1": 1018,
            "x2": 1912,
            "y2": 1046
        },
        {
            "name": "Check Box20",
            "type": "checkbox",
            "page": 0,
            "x1": 542,
            "y1": 232,
            "x2": 556,
            "y2": 250
        },
        {
            "name": "Check Box21",
            "type": "checkbox",
            "page": 0,
            "x1": 594,
            "y1": 232,
            "x2": 608,
            "y2": 250
        },
        {
            "name": "Check Box22",
            "type": "checkbox",
            "page": 0,
            "x1": 1942,
            "y1": 135,
            "x2": 1957,
            "y2": 151
        },
        {
            "name": "Check Box23",
            "type": "checkbox",
            "page": 0,
            "x1": 1850,
            "y1": 135,
            "x2": 1864,
            "y2": 151
        },
        {
            "name": "Check Box24",
            "type": "checkbox",
            "page": 0,
            "x1": 1742,
            "y1": 135,
            "x2": 1756,
            "y2": 151
        },
        {
            "name": "Check Box25",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 221,
            "x2": 1637,
            "y2": 237
        },
        {
            "name": "Check Box26",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 221,
            "x2": 1840,
            "y2": 237
        },
        {
            "name": "Check Box27",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 251,
            "x2": 1637,
            "y2": 267
        },
        {
            "name": "Check Box28",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 251,
            "x2": 1840,
            "y2": 267
        },
        {
            "name": "Check Box29",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 282,
            "x2": 1637,
            "y2": 298
        },
        {
            "name": "Check Box30",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 282,
            "x2": 1840,
            "y2": 298
        },
        {
            "name": "Check Box31",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 312,
            "x2": 1637,
            "y2": 329
        },
        {
            "name": "Check Box32",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 312,
            "x2": 1840,
            "y2": 329
        },
        {
            "name": "Check Box33",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 343,
            "x2": 1637,
            "y2": 359
        },
        {
            "name": "Check Box34",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 343,
            "x2": 1840,
            "y2": 359
        },
        {
            "name": "Check Box35",
            "type": "checkbox",
            "page": 0,
            "x1": 1623,
            "y1": 385,
            "x2": 1637,
            "y2": 401
        },
        {
            "name": "Check Box36",
            "type": "checkbox",
            "page": 0,
            "x1": 1826,
            "y1": 385,
            "x2": 1840,
            "y2": 401
        },
        {
            "name": "CW 2",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 244,
            "x2": 803,
            "y2": 273
        },
        {
            "name": "undefined_21",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 244,
            "x2": 893,
            "y2": 273
        },
        {
            "name": "undefined_22",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 244,
            "x2": 985,
            "y2": 273
        },
        {
            "name": "CW 3",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 277,
            "x2": 803,
            "y2": 306
        },
        {
            "name": "undefined_23",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 277,
            "x2": 893,
            "y2": 306
        },
        {
            "name": "undefined_24",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 277,
            "x2": 985,
            "y2": 306
        },
        {
            "name": "CW 4",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 310,
            "x2": 803,
            "y2": 339
        },
        {
            "name": "undefined_25",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 310,
            "x2": 893,
            "y2": 339
        },
        {
            "name": "undefined_26",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 310,
            "x2": 985,
            "y2": 339
        },
        {
            "name": "Initials 1",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 210,
            "x2": 1085,
            "y2": 240
        },
        {
            "name": "Initials 2",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 244,
            "x2": 1085,
            "y2": 273
        },
        {
            "name": "Initials 3",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 277,
            "x2": 1085,
            "y2": 306
        },
        {
            "name": "Initials 4",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 310,
            "x2": 1085,
            "y2": 339
        },
        {
            "name": "CW 1",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 210,
            "x2": 803,
            "y2": 240
        },
        {
            "name": "undefined_27",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 210,
            "x2": 893,
            "y2": 240
        },
        {
            "name": "undefined_28",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 210,
            "x2": 985,
            "y2": 240
        },
        {
            "name": "undefined_29",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 210,
            "x2": 1192,
            "y2": 240
        },
        {
            "name": "Section 1",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 211,
            "x2": 1407,
            "y2": 239
        },
        {
            "name": "undefined_30",
            "type": "text",
            "page": 0,
            "x1": 1426,
            "y1": 211,
            "x2": 1498,
            "y2": 239
        },
        {
            "name": "undefined_31",
            "type": "text",
            "page": 0,
            "x1": 1517,
            "y1": 211,
            "x2": 1588,
            "y2": 239
        },
        {
            "name": "undefined_33",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 211,
            "x2": 1983,
            "y2": 239
        },
        {
            "name": "undefined_34",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 211,
            "x2": 2117,
            "y2": 239
        },
        {
            "name": "undefined_35",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 244,
            "x2": 1192,
            "y2": 273
        },
        {
            "name": "Section 2",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 240,
            "x2": 1407,
            "y2": 270
        },
        {
            "name": "undefined_41",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 277,
            "x2": 1192,
            "y2": 306
        },
        {
            "name": "undefined_47",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 310,
            "x2": 1192,
            "y2": 339
        },
        {
            "name": "CW 5",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 343,
            "x2": 803,
            "y2": 373
        },
        {
            "name": "undefined_53",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 343,
            "x2": 893,
            "y2": 373
        },
        {
            "name": "undefined_54",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 343,
            "x2": 985,
            "y2": 373
        },
        {
            "name": "DSD with all CW Dive 1 skills  Open Water Diver CW Dive 1",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 343,
            "x2": 1085,
            "y2": 373
        },
        {
            "name": "undefined_55",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 343,
            "x2": 1192,
            "y2": 373
        },
        {
            "name": "200 metreyard Swim OR 300 metreyard MaskSnorkelFin Swim",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 487,
            "x2": 1085,
            "y2": 516
        },
        {
            "name": "10 Minute Survival Float",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 487,
            "x2": 803,
            "y2": 516
        },
        {
            "name": "undefined_66",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 487,
            "x2": 893,
            "y2": 516
        },
        {
            "name": "undefined_67",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 487,
            "x2": 985,
            "y2": 516
        },
        {
            "name": "undefined_68",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 487,
            "x2": 1192,
            "y2": 516
        },
        {
            "name": "undefined_72",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 559,
            "x2": 985,
            "y2": 589
        },
        {
            "name": "undefined_73",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 559,
            "x2": 1085,
            "y2": 589
        },
        {
            "name": "undefined_74",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 559,
            "x2": 1192,
            "y2": 589
        },
        {
            "name": "undefined_75",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 559,
            "x2": 803,
            "y2": 589
        },
        {
            "name": "undefined_76",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 559,
            "x2": 893,
            "y2": 589
        },
        {
            "name": "undefined_77",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 676,
            "x2": 1085,
            "y2": 705
        },
        {
            "name": "undefined_78",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 676,
            "x2": 1192,
            "y2": 705
        },
        {
            "name": "Equipment Preparation and Care",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 676,
            "x2": 803,
            "y2": 705
        },
        {
            "name": "undefined_91",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 676,
            "x2": 893,
            "y2": 705
        },
        {
            "name": "undefined_92",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 676,
            "x2": 985,
            "y2": 705
        },
        {
            "name": "undefined_93",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 756,
            "x2": 1085,
            "y2": 785
        },
        {
            "name": "undefined_94",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 756,
            "x2": 1192,
            "y2": 785
        },
        {
            "name": "Disconnect Low Pressure Inflator Hose",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 756,
            "x2": 803,
            "y2": 785
        },
        {
            "name": "undefined_95",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 756,
            "x2": 893,
            "y2": 785
        },
        {
            "name": "undefined_96",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 756,
            "x2": 985,
            "y2": 785
        },
        {
            "name": "Loose Cylinder Band",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 835,
            "x2": 803,
            "y2": 864
        },
        {
            "name": "undefined_97",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 835,
            "x2": 985,
            "y2": 864
        },
        {
            "name": "undefined_98",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 835,
            "x2": 1085,
            "y2": 864
        },
        {
            "name": "undefined_99",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 835,
            "x2": 1192,
            "y2": 864
        },
        {
            "name": "undefined_100",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 835,
            "x2": 893,
            "y2": 864
        },
        {
            "name": "undefined_101",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 915,
            "x2": 1192,
            "y2": 944
        },
        {
            "name": "Weight System Removal and Replacement surface",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 915,
            "x2": 803,
            "y2": 944
        },
        {
            "name": "undefined_102",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 915,
            "x2": 893,
            "y2": 944
        },
        {
            "name": "undefined_103",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 915,
            "x2": 985,
            "y2": 944
        },
        {
            "name": "undefined_104",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 915,
            "x2": 1085,
            "y2": 944
        },
        {
            "name": "undefined_105",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 994,
            "x2": 1085,
            "y2": 1024
        },
        {
            "name": "undefined_106",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 994,
            "x2": 1192,
            "y2": 1024
        },
        {
            "name": "Emergency Weight Drop or in OW",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 994,
            "x2": 803,
            "y2": 1024
        },
        {
            "name": "undefined_107",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 994,
            "x2": 893,
            "y2": 1024
        },
        {
            "name": "undefined_108",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 994,
            "x2": 985,
            "y2": 1024
        },
        {
            "name": "undefined_118",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 1083,
            "x2": 985,
            "y2": 1112
        },
        {
            "name": "undefined_119",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 1083,
            "x2": 1085,
            "y2": 1112
        },
        {
            "name": "undefined_120",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 1083,
            "x2": 1192,
            "y2": 1112
        },
        {
            "name": "Skin Diving Skills",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 1083,
            "x2": 803,
            "y2": 1112
        },
        {
            "name": "undefined_122",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 1083,
            "x2": 893,
            "y2": 1112
        },
        {
            "name": "undefined_123",
            "type": "text",
            "page": 0,
            "x1": 914,
            "y1": 1172,
            "x2": 985,
            "y2": 1202
        },
        {
            "name": "undefined_124",
            "type": "text",
            "page": 0,
            "x1": 1024,
            "y1": 1172,
            "x2": 1085,
            "y2": 1202
        },
        {
            "name": "undefined_125",
            "type": "text",
            "page": 0,
            "x1": 1121,
            "y1": 1172,
            "x2": 1192,
            "y2": 1202
        },
        {
            "name": "Note If all Confined Water Dives Confined Water Dive Flexible Skills and Wa",
            "type": "text",
            "page": 0,
            "x1": 731,
            "y1": 1172,
            "x2": 803,
            "y2": 1202
        },
        {
            "name": "undefined_129",
            "type": "text",
            "page": 0,
            "x1": 822,
            "y1": 1172,
            "x2": 893,
            "y2": 1202
        },
        {
            "name": "undefined_36",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 240,
            "x2": 1498,
            "y2": 270
        },
        {
            "name": "undefined_37",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 240,
            "x2": 1588,
            "y2": 270
        },
        {
            "name": "undefined_39",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 240,
            "x2": 1983,
            "y2": 270
        },
        {
            "name": "undefined_40",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 240,
            "x2": 2117,
            "y2": 270
        },
        {
            "name": "Section 3",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 271,
            "x2": 1407,
            "y2": 300
        },
        {
            "name": "undefined_42",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 271,
            "x2": 1498,
            "y2": 300
        },
        {
            "name": "undefined_43",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 271,
            "x2": 1588,
            "y2": 300
        },
        {
            "name": "undefined_45",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 271,
            "x2": 1983,
            "y2": 300
        },
        {
            "name": "undefined_46",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 271,
            "x2": 2117,
            "y2": 300
        },
        {
            "name": "Section 4",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 302,
            "x2": 1407,
            "y2": 331
        },
        {
            "name": "undefined_48",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 302,
            "x2": 1498,
            "y2": 331
        },
        {
            "name": "undefined_49",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 302,
            "x2": 1588,
            "y2": 331
        },
        {
            "name": "undefined_51",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 302,
            "x2": 1983,
            "y2": 331
        },
        {
            "name": "undefined_52",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 302,
            "x2": 2117,
            "y2": 331
        },
        {
            "name": "Section 5",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 332,
            "x2": 1407,
            "y2": 361
        },
        {
            "name": "undefined_56",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 332,
            "x2": 1498,
            "y2": 361
        },
        {
            "name": "undefined_57",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 332,
            "x2": 1588,
            "y2": 361
        },
        {
            "name": "undefined_59",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 332,
            "x2": 1983,
            "y2": 361
        },
        {
            "name": "undefined_60",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 332,
            "x2": 2117,
            "y2": 361
        },
        {
            "name": "Quick Review",
            "type": "text",
            "page": 0,
            "x1": 1336,
            "y1": 375,
            "x2": 1407,
            "y2": 404
        },
        {
            "name": "undefined_61",
            "type": "text",
            "page": 0,
            "x1": 1427,
            "y1": 375,
            "x2": 1498,
            "y2": 404
        },
        {
            "name": "undefined_62",
            "type": "text",
            "page": 0,
            "x1": 1518,
            "y1": 375,
            "x2": 1588,
            "y2": 404
        },
        {
            "name": "undefined_64",
            "type": "text",
            "page": 0,
            "x1": 1903,
            "y1": 375,
            "x2": 1983,
            "y2": 404
        },
        {
            "name": "undefined_65",
            "type": "text",
            "page": 0,
            "x1": 2028,
            "y1": 375,
            "x2": 2117,
            "y2": 404
        },
        {
            "name": "Dive 2",
            "type": "text",
            "page": 0,
            "x1": 1275,
            "y1": 641,
            "x2": 1328,
            "y2": 671
        },
        {
            "name": "undefined_79",
            "type": "text",
            "page": 0,
            "x1": 1348,
            "y1": 641,
            "x2": 1402,
            "y2": 671
        },
        {
            "name": "undefined_80",
            "type": "text",
            "page": 0,
            "x1": 1421,
            "y1": 641,
            "x2": 1475,
            "y2": 671
        },
        {
            "name": "Initials 1_2",
            "type": "text",
            "page": 0,
            "x1": 1494,
            "y1": 612,
            "x2": 1547,
            "y2": 637
        },
        {
            "name": "Initials 2_2",
            "type": "text",
            "page": 0,
            "x1": 1494,
            "y1": 641,
            "x2": 1547,
            "y2": 671
        },
        {
            "name": "undefined_81",
            "type": "text",
            "page": 0,
            "x1": 1583,
            "y1": 641,
            "x2": 1654,
            "y2": 671
        },
        {
            "name": "Dive 4",
            "type": "text",
            "page": 0,
            "x1": 1728,
            "y1": 641,
            "x2": 1781,
            "y2": 671
        },
        {
            "name": "undefined_82",
            "type": "text",
            "page": 0,
            "x1": 1801,
            "y1": 641,
            "x2": 1854,
            "y2": 671
        },
        {
            "name": "undefined_83",
            "type": "text",
            "page": 0,
            "x1": 1874,
            "y1": 641,
            "x2": 1928,
            "y2": 671
        },
        {
            "name": "Initials 1_3",
            "type": "text",
            "page": 0,
            "x1": 1956,
            "y1": 612,
            "x2": 2010,
            "y2": 637
        },
        {
            "name": "Initials 2_3",
            "type": "text",
            "page": 0,
            "x1": 1956,
            "y1": 641,
            "x2": 2010,
            "y2": 671
        },
        {
            "name": "Dive 1",
            "type": "text",
            "page": 0,
            "x1": 1275,
            "y1": 612,
            "x2": 1328,
            "y2": 637
        },
        {
            "name": "undefined_84",
            "type": "text",
            "page": 0,
            "x1": 1348,
            "y1": 612,
            "x2": 1401,
            "y2": 637
        },
        {
            "name": "undefined_85",
            "type": "text",
            "page": 0,
            "x1": 1421,
            "y1": 612,
            "x2": 1475,
            "y2": 637
        },
        {
            "name": "undefined_86",
            "type": "text",
            "page": 0,
            "x1": 1583,
            "y1": 612,
            "x2": 1654,
            "y2": 637
        },
        {
            "name": "Dive 3",
            "type": "text",
            "page": 0,
            "x1": 1728,
            "y1": 612,
            "x2": 1781,
            "y2": 637
        },
        {
            "name": "undefined_87",
            "type": "text",
            "page": 0,
            "x1": 1801,
            "y1": 612,
            "x2": 1854,
            "y2": 637
        },
        {
            "name": "undefined_88",
            "type": "text",
            "page": 0,
            "x1": 1874,
            "y1": 612,
            "x2": 1928,
            "y2": 637
        },
        {
            "name": "undefined_89",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 612,
            "x2": 2117,
            "y2": 637
        },
        {
            "name": "undefined_90",
            "type": "text",
            "page": 0,
            "x1": 2045,
            "y1": 641,
            "x2": 2117,
            "y2": 671
        },
        {
            "name": "undefined_126",
            "type": "text",
            "page": 0,
            "x1": 1708,
            "y1": 1128,
            "x2": 1814,
            "y2": 1158
        }
    ]
}


def load_fields():
    """Return a fresh copy of the embedded master field mask.

    The external 10056_OW_Records_mask.json file is intentionally NOT read,
    created, checked, or required. The embedded Python definition is the
    single source of truth for the master mask.
    """
    return copy.deepcopy(HARDCODED_MASK.get("fields", []))


def save_fields(fields):
    """Compatibility hook for older field-edit code.

    Field edits remain in memory for the current session. The master mask is
    embedded in the application and is therefore never overwritten by the GUI.
    """
    return True

def load_state():
    if not STATE_FILE.exists():
        return {}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return {}

        # Current location-aware state format stores each value as
        # {"value": ..., "page": ..., "x1": ..., ...}.
        # Convert that back to the flat runtime state used by the GUI.
        normalized = {}
        wrapped = False

        for name, value in data.items():
            if isinstance(value, dict) and "value" in value:
                normalized[name] = value.get("value")
                wrapped = True
            else:
                normalized[name] = value

        return normalized if wrapped else data

    except Exception as e:
        print("STATE LOAD ERROR:", e)
        return {}

def save_state_with_locations():
    try:
        return _atomic_json_write(STATE_FILE, state)
    except Exception as e:
        messagebox.showerror("State Error", f"Failed to save application state:\n{e}")
        return False

fields = []
state = load_state()
comments_db = load_comments_db()

def show_program_fields():

    fields_used = """
PROGRAM FIELD LOGIC (OW 10056 document)

Student:(Left block)
-----------
Student Name
student_signature (Right block at the end)
Stu_day
Stu_month
Stu_year

Init Instructor Blocks: (Left  block)
(Instructors involved)
-----------------------
init_padi_instructor_1
init_padi_instructor_2

Init_Instructor_Signature_1 (All PADI Instructors #1 who initial this document ... )
Init_Instructor_Signature_2 (All PADI Instructors #1 who initial this document ... )

Init_PADI_no_1
Init_PADI_no_2

Init_Dive_Resort_No_1
Init_Dive_Resort_No_2

Init_day_1
Init_month_1
Init_year_1

Init_day_2
Init_month_2
Init_year_2

Init_Phone_1
Init_Phone_2

Init_Email_1
Init_Email_2

Instructor Signoffs:
--------------------
Instructor_signature_3  (All Confined have been completed)
Instructor_signature_4  (All Knowledge Development sessions listed above have been completed, Quizzes/Exams passed)
Instructor_signature_5  (All Open Water Dive Flexible Skills listed above have been completed.)
Instructor_signature_6  (All requirements for certification as a PADI Scuba Diver have been met)
Instructor_signature_7  (All requirements for certification as a PADI Open Water Diver have been met.)

PADI_no_3 to PADI_no_7
day_3 to day_7
month_3 to month_7
year_3 to year_7

CW Auto-Populate Pattern:
-------------------------
CW1_day ... CW24_day  (Starts at CW 1*)
CW1_month ... CW24_month
CW1_year ... CW24_year
CW1_initials ... CW24_initials
CW1_padi ... CW24_padi (ends at the year for the final signoff)

Dive Logic:
-----------
Dive_1 ... Dive_10
Dive_initials_1 ... Dive_initials_10
Dive_padi_1 ... Dive_padi_10

Special Logic:
--------------
CW12 auto-fills Dive_4
"""

    win = tk.Toplevel(root)
    win.title("Program Field Logic")
    win.geometry("700x700")

    txt = tk.Text(win, wrap="word")
    txt.pack(fill="both", expand=True)

    txt.insert("1.0", fields_used)
    txt.config(state="disabled")

# ---------------- Signature Drawing Window ----------------

def draw_student_signature_window(field_name):

    win = tk.Toplevel(root)
    win.title("Student Signature")
    win.geometry("620x320")

    width, height = 600, 120

    canvas_sig = tk.Canvas(
        win,
        bg="#E6E6E6",
        width=width,
        height=height
    )
    canvas_sig.pack(pady=10)

    img = Image.new("RGB", (width, height), "white")
    draw_obj = ImageDraw.Draw(img)

    last = {"x": None, "y": None}

    def start_draw(event):
        last["x"], last["y"] = event.x, event.y

    def draw_line(event):
        if last["x"] is not None:
            canvas_sig.create_line(
                last["x"], last["y"], event.x, event.y,
                fill="black", width=3
            )
            draw_obj.line(
                (last["x"], last["y"], event.x, event.y),
                fill="black", width=3
            )
        last["x"], last["y"] = event.x, event.y

    canvas_sig.bind("<Button-1>", start_draw)
    canvas_sig.bind("<B1-Motion>", draw_line)

    def clear_canvas():
        canvas_sig.delete("all")
        draw_obj.rectangle((0, 0, width, height), fill="white")

    def save_signature():

        filename = SIGNATURE_DIR / f"{field_name}_student.png"
        img.save(filename)

        state[field_name] = str(filename)

        d = date_picker.get_date()

        state["Stu_day"] = str(d.day)
        state["Stu_month"] = [
            "Jan","Feb","Mar","Apr","May","Jun",
            "Jul","Aug","Sep","Oct","Nov","Dec"
        ][d.month - 1]
        state["Stu_year"] = str(d.year)

        save_state_with_locations()

        redraw_all_text_fields()
        redraw_all_signatures()

        win.destroy()

    def delete_signature():
        if field_name in state:
            del state[field_name]
            save_state_with_locations()
            redraw_all_signatures()
        win.destroy()

    # Buttons
    tk.Button(
        win,
        text="Clear",
        command=clear_canvas
    ).pack(side="left", padx=20)

    tk.Button(
        win,
        text="Save Signature",
        command=save_signature
    ).pack(side="right", padx=20)

    tk.Button(
        win,
        text="Delete Signature",
        command=delete_signature
    ).pack(side="left", padx=20)

def draw_signature_window(name, padi_number, signature_var):

    win = tk.Toplevel(root)
    win.title(f"Draw Signature for {name}")
    win.geometry("620x320")

    width, height = 600, 120

    canvas_sig = tk.Canvas(
        win,
        bg="#E6E6E6",
        width=width,
        height=height
    )
    canvas_sig.pack(pady=10)

    img = Image.new("RGB", (width, height), "white")
    draw_obj = ImageDraw.Draw(img)

    last = {"x": None, "y": None}

    def start_draw(event):
        last["x"], last["y"] = event.x, event.y

    def draw_line(event):

        if last["x"] is not None:

            canvas_sig.create_line(
                last["x"],
                last["y"],
                event.x,
                event.y,
                fill="black",
                width=3
            )

            draw_obj.line(
                (last["x"], last["y"], event.x, event.y),
                fill="black",
                width=3
            )

        last["x"], last["y"] = event.x, event.y

    canvas_sig.bind("<Button-1>", start_draw)
    canvas_sig.bind("<B1-Motion>", draw_line)

    def clear_canvas():
        canvas_sig.delete("all")
        draw_obj.rectangle(
            (0, 0, width, height),
            fill="white"
        )

    def save_signature():

        safe_padi = re.sub(
            r"[^A-Za-z0-9_-]",
            "_",
            str(padi_number)
        )

        filename = SIGNATURE_DIR / f"{safe_padi}.png"

        img.save(filename)

        signature_var.set(str(filename))

        messagebox.showinfo(
            "Saved",
            f"Signature saved as:\n{filename}"
        )

        win.destroy()

        try:
            instructor_window.lift()
            instructor_window.focus_force()
        except:
            pass

    tk.Button(
        win,
        text="Clear",
        command=clear_canvas
    ).pack(side="left", padx=20, pady=5)

    tk.Button(
        win,
        text="Save Signature",
        command=save_signature
    ).pack(side="right", padx=20, pady=5)

# ---------------- PDF Viewer ----------------

pdf_path = None
pages = []
current_page = 0

def render_page():

    global zoom_level

    if not pages:
        print("RENDER PAGE ABORTED: pages list is empty")
        return

    if current_page < 0 or current_page >= len(pages):
        print("RENDER PAGE ABORTED: invalid page index", current_page)
        return

    try:
        print("RENDER_PAGE START: page", current_page + 1, "of", len(pages))

        # Clear canvas drawing objects only. Do not destroy Tk child widgets and
        # do not call root.update() from inside a drawing callback; both can
        # cause event-loop re-entry problems on macOS.
        canvas_pdf.delete("all")
        canvas_pdf.image = None

        if hasattr(canvas_pdf, "signature_images"):
            canvas_pdf.signature_images.clear()

        page = pages[current_page]
        w, h = page.size
        new_w = max(1, int(w * zoom_level))
        new_h = max(1, int(h * zoom_level))

        print("SOURCE PAGE SIZE =", (w, h), "DISPLAY SIZE =", (new_w, new_h))

        if new_w == w and new_h == h:
            display_image = page
        else:
            display_image = page.resize((new_w, new_h), Image.LANCZOS)

        print("CREATING TK PDF IMAGE")
        tk_img = ImageTk.PhotoImage(display_image, master=root)
        canvas_pdf.image = tk_img  # keep a strong reference

        image_id = canvas_pdf.create_image(
            0,
            0,
            anchor="nw",
            image=tk_img,
            tags=("pdf_backdrop",)
        )
        canvas_pdf.tag_lower("pdf_backdrop")
        canvas_pdf.config(scrollregion=(0, 0, new_w, new_h))

        print("PDF BACKDROP IMAGE ID =", image_id)

        print("DRAWING FIELD BOXES")
        draw_all_field_boxes()
        print("DRAWING TEXT FIELDS")
        redraw_all_text_fields()
        print("DRAWING SIGNATURES")
        redraw_all_signatures()
        print("DRAWING CHECKBOXES")
        redraw_all_checkboxes()

        canvas_pdf.tag_raise("text_drawn")
        canvas_pdf.tag_raise("signature_drawn")
        canvas_pdf.tag_raise("checkbox_drawn")
        canvas_pdf.tag_raise("field_box")

        print("RENDER_PAGE COMPLETE")

    except Exception as e:
        print("RENDER_PAGE ERROR:", repr(e))
        traceback.print_exc()
        messagebox.showerror(
            "PDF Display Error",
            f"The PDF page could not be displayed:\n\n{e}"
        )


# ---------------- Advanced Field Detection ----------------

def detect_acroform_fields(pdf_path, pages):
    reader = PdfReader(pdf_path)
    root = reader.trailer.get("/Root", {})
    if "/AcroForm" not in root:
        return []

    form = root["/AcroForm"]
    fields_raw = form.get("/Fields", [])

    detected = []

    for field_ref in fields_raw:
        field = field_ref.get_object()

        ftype = field.get("/FT")
        rect = field.get("/Rect")
        page_ref = field.get("/P")

        if not rect or not page_ref:
            continue

        try:
            page_obj = page_ref.get_object()
        except:
            page_obj = page_ref

        page_index = None
        for i, p in enumerate(reader.pages):
            if p.indirect_reference.idnum == page_obj.indirect_reference.idnum:
                page_index = i
                break

        if page_index is None:
            print("WARNING: Could not resolve page for field:", field)
            continue

        x1_pdf, y1_pdf, x2_pdf, y2_pdf = rect

        pdf_page = reader.pages[page_index]
        pdf_w = float(pdf_page.mediabox.width)
        pdf_h = float(pdf_page.mediabox.height)

        img_w, img_h = pages[page_index].size

        scale_x = img_w / pdf_w
        scale_y = img_h / pdf_h

        x1_img = int(x1_pdf * scale_x)
        x2_img = int(x2_pdf * scale_x)
        y1_img = int((pdf_h - y2_pdf) * scale_y)
        y2_img = int((pdf_h - y1_pdf) * scale_y)

        if ftype == "/Sig":
            my_type = "signature"
        elif ftype == "/Tx":
            my_type = "text"
        elif ftype == "/Btn":
            my_type = "checkbox"
        else:
            my_type = "unknown"

        detected.append({
            "name": field.get("/T", f"{my_type}_field_{len(detected)+1}"),
            "type": my_type,
            "page": page_index,
            "x1": x1_img,
            "y1": y1_img,
            "x2": x2_img,
            "y2": y2_img
        })

    return detected
def build_pdf_field_mapping():
    """
    Map application/mask fields to the real AcroForm widgets.

    The mask coordinates are 200-DPI image coordinates, while the PDF stores
    widget rectangles in PDF points.  The PADI PDF also uses many generic
    field names (for example "CW 2", "PADI No", "undefined_9") while the
    application uses semantic names such as "CW2_day".

    Therefore mapping is based primarily on page + rectangle position.
    Exact names are preferred only when they occur at the same location.
    Each real PDF widget is claimed once so duplicate OCR/mask entries do
    not overwrite one another.
    """
    global pdf_field_mapping, pdf_field_rects

    pdf_field_mapping = {}
    pdf_field_rects = {}

    if not pdf_path:
        return

    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print("Error reading PDF fields:", e)
        return

    render_sizes = {
        page_index: page_image.size
        for page_index, page_image in enumerate(pages)
    }

    actual_widgets = []

    for page_index, page in enumerate(reader.pages):
        pdf_w = float(page.mediabox.width)
        pdf_h = float(page.mediabox.height)

        if page_index in render_sizes:
            img_w, img_h = render_sizes[page_index]
            scale_x = img_w / pdf_w
            scale_y = img_h / pdf_h
        else:
            scale_x = 200.0 / 72.0
            scale_y = 200.0 / 72.0

        annots_ref = page.get("/Annots")
        if not annots_ref:
            continue

        try:
            annots = annots_ref.get_object()
        except Exception:
            annots = annots_ref

        for annot_ref in annots:
            try:
                annot = annot_ref.get_object()
            except Exception:
                annot = annot_ref

            if annot.get("/Subtype") != "/Widget":
                continue

            name_obj = annot.get("/T")
            rect = annot.get("/Rect")
            ftype = annot.get("/FT")

            if not name_obj or not rect:
                continue

            if not ftype and annot.get("/Parent"):
                try:
                    parent = annot["/Parent"].get_object()
                    ftype = parent.get("/FT")
                except Exception:
                    pass

            name = str(name_obj)

            x1_pdf, y1_pdf, x2_pdf, y2_pdf = [float(v) for v in rect]

            x1_img = x1_pdf * scale_x
            x2_img = x2_pdf * scale_x
            y1_img = (pdf_h - y2_pdf) * scale_y
            y2_img = (pdf_h - y1_pdf) * scale_y

            if ftype == "/Sig":
                widget_type = "signature"
            elif ftype == "/Tx":
                widget_type = "text"
            elif ftype == "/Btn":
                widget_type = "checkbox"
            else:
                widget_type = "unknown"

            actual_widgets.append({
                "name": name,
                "type": widget_type,
                "page": page_index,
                "x1": x1_img,
                "y1": y1_img,
                "x2": x2_img,
                "y2": y2_img,
            })

    claimed = set()

    def box_score(mask_field, widget):
        return (
            abs(float(mask_field["x1"]) - widget["x1"]) +
            abs(float(mask_field["y1"]) - widget["y1"]) +
            abs(float(mask_field["x2"]) - widget["x2"]) +
            abs(float(mask_field["y2"]) - widget["y2"])
        )

    for mask_field in fields:
        mask_name = mask_field["name"]
        page_index = mask_field["page"]

        candidates = [
            w for w in actual_widgets
            if w["page"] == page_index and w["name"] not in claimed
        ]

        if not candidates:
            pdf_field_mapping[mask_name] = None
            continue

        best = min(candidates, key=lambda w: box_score(mask_field, w))
        best_score = box_score(mask_field, best)

        if best_score > 10:
            pdf_field_mapping[mask_name] = None
            continue

        exact_candidates = [
            w for w in candidates
            if w["name"] == mask_name and box_score(mask_field, w) <= 10
        ]
        if exact_candidates:
            best = min(exact_candidates, key=lambda w: box_score(mask_field, w))

        claimed.add(best["name"])
        pdf_field_mapping[mask_name] = best["name"]

        pdf_field_rects[best["name"]] = (
            best["page"],
            best["x1"],
            best["y1"],
            best["x2"],
            best["y2"],
        )

    print("PDF FIELD MAPPING (coordinate based):")
    mapped_count = 0
    for app_name, pdf_name in pdf_field_mapping.items():
        if pdf_name:
            mapped_count += 1
            print(f"{app_name} -> {pdf_name}")

    print(
        f"Mapped {mapped_count} of {len(fields)} mask fields "
        f"to {len(claimed)} real PDF widgets."
    )

def heuristic_signature_boxes(page_image, page_index):
    w, h = page_image.size
    gray = ImageOps.grayscale(page_image)
    pixels = gray.load()

    candidates = []
    min_length = int(w * 0.2)
    threshold = 60

    for y in range(int(h * 0.2), int(h * 0.9)):
        dark_run = 0
        start_x = None
        for x in range(int(w * 0.05), int(w * 0.95)):
            if pixels[x, y] < threshold:
                if dark_run == 0:
                    start_x = x
                dark_run += 1
            else:
                if dark_run >= min_length:
                    candidates.append({
                        "name": f"signature_heuristic_{len(candidates)+1}",
                        "type": "signature",
                        "page": page_index,
                        "x1": start_x,
                        "y1": y - 10,
                        "x2": x,
                        "y2": y + 10
                    })
                dark_run = 0
                start_x = None

    return candidates

def save_state_with_locations():
    save_data = {}

    for f in fields:
        name = f["name"]

        if name not in state:
            continue

        save_data[name] = {
            "value": state[name],
            "page": f["page"],
            "x1": f["x1"],
            "y1": f["y1"],
            "x2": f["x2"],
            "y2": f["y2"],
            "type": f["type"]
        }

    try:
        return _atomic_json_write(STATE_FILE, save_data)
    except Exception as e:
        messagebox.showerror(
            "State Error",
            f"Failed to save application state:\n{e}"
        )
        return False

def clear_signature(field_name):
    if field_name in state:
        del state[field_name]
    save_state_with_locations()
    redraw_all_signatures()


def load_state_by_location():

    if not STATE_FILE.exists():
        return {}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            old_data = json.load(f)

    except Exception:
        return {}

    new_state = {}

    for current_field in fields:

        best_match = None
        best_score = 999999

        for old_name, old_info in old_data.items():

            if not isinstance(old_info, dict):
                continue

            #
            # FIRST TRY EXACT FIELD NAME MATCH
            #
            if old_name == current_field["name"]:

                print(
                    "NAME MATCH:",
                    current_field["name"],
                    "<--",
                    old_info.get("value")
                )

                new_state[current_field["name"]] = (
                    old_info.get("value")
                )

                best_match = None
                break

            #
            # OTHERWISE FALL BACK TO LOCATION MATCHING
            #
            if current_field["page"] != old_info.get("page"):
                continue

            score = (
                abs(current_field["x1"] - old_info["x1"]) +
                abs(current_field["y1"] - old_info["y1"]) +
                abs(current_field["x2"] - old_info["x2"]) +
                abs(current_field["y2"] - old_info["y2"])
            )

            if score < best_score:
                best_score = score
                best_match = old_info

        #
        # ONLY USE LOCATION MATCH IF
        # NAME MATCH DID NOT ALREADY HAPPEN
        #
        if (
            current_field["name"] not in new_state
            and best_match
            and best_score < 10
        ):

            print(
                "LOCATION MATCH:",
                current_field["name"],
                "<--",
                best_match.get("value"),
                "score=",
                best_score
            )

            new_state[current_field["name"]] = (
                best_match.get("value")
            )

    print("new_state =", new_state)
    print("LOADED STATE COUNT =", len(new_state))

    return new_state


def load_pdf_field_values(pdf_file):

    values = {}

    try:

        reader = PdfReader(pdf_file)

        pdf_fields = reader.get_fields()

        print("\n========================")
        print("ACTUAL PDF FIELD NAMES")
        print("========================")

        for name in sorted(pdf_fields.keys()):
            print(repr(name))

        print("========================\n")

        for name, info in pdf_fields.items():

            if info.get("/FT") == "/Btn":

                print("\nCHECKBOX FIELD:", name)

                for k, v in info.items():
                    print("   ", k, "=", v)

        print("================================")
        print("PDF FIELDS FROM EXPORTED FILE")
        print("================================")
        print(pdf_fields)

        if not pdf_fields:
            print("NO FIELDS FOUND")
            return values

        for field_name, info in pdf_fields.items():

            print("\n================================")
            print("FIELD:", field_name)
            print("================================")

            for k, v in info.items():
                print(k, "=", v)

            value = info.get("/V")

            print("VALUE =", value)
            print("FT    =", info.get("/FT"))

            if value is not None:
                values[field_name] = str(value)

        print("LOADED VALUES =", values)

    except Exception as e:

        print("FIELD LOAD ERROR:", e)

    return values


def pdf_values_to_state(pdf_values):
    """
    Convert raw PDF AcroForm values into the application's state dictionary.
    Signature fields in PDFs contain only metadata and must be ignored.
    """

    loaded_state = {}

    for app_name, pdf_name in pdf_field_mapping.items():

        # Skip if PDF field not present
        if pdf_name not in pdf_values:
            continue

        value = pdf_values[pdf_name]

        # Find field info from mask
        field_info = next((f for f in fields if f["name"] == app_name), None)
        if not field_info:
            continue

        # ⭐ SIGNATURE FIX ⭐
        # Ignore ALL signature fields from PDF
        if field_info["type"] == "signature":
            continue

        # Checkbox handling
        if field_info["type"] == "checkbox":
            loaded_state[app_name] = (
                str(value).lower() not in ("/off", "off", "", "false")
            )
            continue

        # Normal text fields
        loaded_state[app_name] = value

    return loaded_state


def load_pdf():

    global pdf_path
    global pages
    global current_page
    global zoom_level
    global state
    global reopened_exported_pdf
    global loaded_pdf_values
    global current_base_pdf_path
    global current_base_id

    pdf_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")],
        title="Select a PADI PDF"
    )

    if not pdf_path:
        pdf_label.config(text="No PDF loaded")
        return

    #
    # INSPECT PDF
    #
    try:

        reader = PdfReader(pdf_path)

        pdf_fields = reader.get_fields()

        print("")
        print("================================")
        print("PDF FIELD TEST")
        print("================================")

        if pdf_fields:

            for name, info in pdf_fields.items():

                value = info.get("/V")

                print(
                    "FIELD:",
                    name,
                    "VALUE:",
                    value
                )

        else:

            print("NO ACROFORM FIELDS FOUND")

        print("================================")
        print("")

    except Exception as e:

        print("FIELD TEST ERROR:", e)

    pdf_label.config(
        text=f"Loaded: {Path(pdf_path).name}"
    )

    # Load the saved comment into the main-menu textbox.
    display_comment(pdf_path)

    #
    # DETECT WHETHER THIS IS A PREVIOUS PADI MANAGER EXPORT
    #
    # New exports carry /PADIManagerBaseID.  Older exports are detected from
    # meaningful AcroForm values.  /Off and false checkbox defaults do not count.
    current_base_id = _base_id_from_pdf(pdf_path)
    reopened_exported_pdf = bool(current_base_id)

    if not reopened_exported_pdf:
        try:
            reader = PdfReader(pdf_path)
            pdf_fields = reader.get_fields() or {}
            for field_name, info in pdf_fields.items():
                value = info.get("/V")
                if value not in (None, "", "/Off", "Off", False, 0):
                    reopened_exported_pdf = True
                    break
        except Exception as e:
            print("PDF DETECTION ERROR:", e)

    print("REOPENED EXPORTED PDF =", reopened_exported_pdf)
    print("PADI MANAGER BASE ID =", current_base_id)

    # Always start from the embedded master mask.
    fields.clear()
    fields.extend(load_fields())
    print("FIELDS FROM EMBEDDED MASTER MASK =", len(fields))

    # Resolve the pristine source PDF used as the viewer backdrop and export base.
    # This is the key fix for duplicate/stacked edits.
    current_base_pdf_path = None

    if current_base_id:
        current_base_pdf_path = _cached_base_for_id(current_base_id)
        if current_base_pdf_path:
            print("FOUND CACHED CLEAN BASE =", current_base_pdf_path)

    if current_base_pdf_path is None and not reopened_exported_pdf:
        # A blank/original form becomes the clean source for future updates.
        try:
            current_base_id, current_base_pdf_path = _cache_clean_template(pdf_path)
        except Exception as e:
            print("TEMPLATE CACHE WARNING:", e)
            current_base_pdf_path = Path(pdf_path)

    if current_base_pdf_path is None and reopened_exported_pdf:
        # Compatibility for exports created by an older PADI Manager version.
        fallback = _single_cached_template()
        if fallback is not None:
            current_base_pdf_path = fallback
            current_base_id = fallback.stem
            print("USING SINGLE CACHED TEMPLATE FOR LEGACY EXPORT =", fallback)
        else:
            # We can read/edit the file, but its previous static overlay cannot be
            # erased safely because merge_page permanently added it to page content.
            current_base_pdf_path = Path(pdf_path)
            print("WARNING: NO CLEAN BASE AVAILABLE FOR THIS LEGACY EXPORT")

    # Render the CLEAN BASE as the GUI backdrop.  Values are still read from
    # pdf_path below, so reopened edits remain editable without displaying the
    # old flattened/static text underneath the new Tk overlays.
    try:
        render_source = str(current_base_pdf_path or pdf_path)
        print("RENDERING CLEAN PDF BACKDROP =", render_source)
        pages = convert_from_path(render_source, dpi=200)
        print("PDF PAGES RENDERED =", len(pages))
        if not pages:
            raise RuntimeError("PDFium returned no rendered pages.")
        for page_no, page_image in enumerate(pages, start=1):
            print("PAGE", page_no, "SIZE =", page_image.size)
    except Exception as e:
        pages = []
        print("PDF RENDER ERROR:", repr(e))
        traceback.print_exc()
        messagebox.showerror(
            "PDF Render Error",
            f"The PDF could not be rendered for display:\n\n{e}"
        )
        return

    #
    # Build field mapping only after rendered page dimensions are available.
    try:
        build_pdf_field_mapping()

        print("\n========= DUPLICATE TEST =========")
        seen = {}
        for app_field, pdf_field in pdf_field_mapping.items():
            print(app_field, "->", pdf_field)
            seen.setdefault(pdf_field, []).append(app_field)

        for pdf_field, apps in seen.items():
            if len(apps) > 1:
                print("DUPLICATE PDF FIELD:", pdf_field)
                print("USED BY:", apps)

        print("==================================")

        if reopened_exported_pdf:
            print("READING VALUES FROM EXPORTED PDF")
            pdf_values = load_pdf_field_values(pdf_path)
            print("PDF_VALUES =", pdf_values)
            state = pdf_values_to_state(pdf_values)

            # Restore signature image paths from the writable user state.
            saved_state = load_state_by_location()
            for field in fields:
                if field["type"] != "signature":
                    continue

                name = field["name"]
                pdf_val = state.get(name)
                saved_sig_path = saved_state.get(name)

                if pdf_val in (None, "", "/Sig") and saved_sig_path:
                    state[name] = saved_sig_path

            print("Student Name in PDF =", pdf_values.get("Student Name"))
            print("Student Name mapping =", pdf_field_mapping.get("Student Name"))
            print("STATE LOADED FROM PDF =", state)
        else:
            print("BLANK TEMPLATE PDF")
            state = {}

        loaded_pdf_values = dict(state)
        print("STATE AFTER LOAD =", state)
        print("STUDENT NAME AFTER LOAD =", state.get("Student Name"))

    except Exception as e:
        print("PDF FIELD/MASK LOAD ERROR:", repr(e))
        traceback.print_exc()
        messagebox.showerror(
            "PDF Load Error",
            f"Failed to prepare the PDF:\n{e}"
        )
        state = {}
        loaded_pdf_values = {}

    current_page = 0
    zoom_level = zoom_level_def

    root.update_idletasks()
    render_page()



def close_pdf():

    global pdf_path
    global pages
    global current_page
    global state
    global fields
    global loaded_pdf_values
    global pdf_field_mapping
    global reopened_exported_pdf
    global current_base_pdf_path
    global current_base_id

    pdf_path = None
    pages = []
    current_page = 0

    state = {}
    fields.clear()

    loaded_pdf_values = {}
    pdf_field_mapping = {}
    reopened_exported_pdf = False
    current_base_pdf_path = None
    current_base_id = None

    canvas_pdf.delete("all")

    canvas_pdf.config(
        scrollregion=(0, 0, 0, 0)
    )

    if hasattr(canvas_pdf, "signature_images"):
        canvas_pdf.signature_images.clear()

    pdf_label.config(
        text="No PDF loaded"
    )

    if "comment_text" in globals():
        comment_text.delete("1.0", "end")
        update_comment_box_color()

    status_label.config(
        text="PDF and Mask Closed"
    )


def next_page():
    global current_page
    if not pages:
        return
    if current_page < len(pages) - 1:
        current_page += 1
        render_page()

def prev_page():
    global current_page
    if not pages:
        return
    if current_page > 0:
        current_page -= 1
        render_page()

# ---------------- Zoom Controls ----------------

def zoom_in():
    global zoom_level
    if zoom_level < MAX_ZOOM:
        zoom_level += ZOOM_STEP
        render_page()

def zoom_out():
    global zoom_level
    if zoom_level > MIN_ZOOM:
        zoom_level -= ZOOM_STEP
        render_page()

def zoom_fit():
    global zoom_level
    if not pages:
        return

    page = pages[current_page]
    w, h = page.size

    canvas_w = canvas_pdf.winfo_width()
    canvas_h = canvas_pdf.winfo_height()

    zoom_w = canvas_w / w
    zoom_h = canvas_h / h

    zoom_level = min(zoom_w, zoom_h)
    render_page()

# ---------------- Field Detection ----------------

def find_field(x, y, page_index):
    for f in fields:
        if f.get("page", 0) != page_index:
            continue
        if f["x1"] <= x <= f["x2"] and f["y1"] <= y <= f["y2"]:
            return f
    return None


def action_field_info(field):
    """Return a short description for fields whose click triggers multiple updates."""
    if not field:
        return None

    name = str(field.get("name", "")).strip().lower()

    if re.fullmatch(r"cw\d+_day", name):
        prefix = name.rsplit("_", 1)[0].upper()
        return (
            f"{prefix} auto-fill\n"
            "Click to fill date, instructor initials and PADI number."
        )

    if re.fullmatch(r"init_padi_instructor_\d+", name):
        return (
            "Instructor auto-fill\n"
            "Click to fill instructor, PADI number, store, contact, signature and date."
        )

    if re.fullmatch(r"instructor_signature_\d+", name):
        return (
            "Instructor sign-off\n"
            "Click to add/remove the selected instructor signature, PADI number and date."
        )

    if re.fullmatch(r"dive_\d+", name):
        return (
            "Dive counter / auto-fill\n"
            "Click to cycle the dive count and update instructor initials/PADI number."
        )

    if name == "student_signature":
        return (
            "Student signature\n"
            "Click to add/replace the student signature and student signing date."
        )

    return None


def is_action_field(field):
    return action_field_info(field) is not None


def populate_cw_row(prefix):
    """Populate day, month, year, initials, and PADI# for a CW row."""

    # Date fields
    d = date_picker.get_date()

    state[f"{prefix}_day"] = str(d.day)
    state[f"{prefix}_month"] = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ][d.month - 1]

    state[f"{prefix}_year"] = str(d.year)

    # Instructor fields
    selected_name = instructor_var.get()

    instructor = next(
        (
            i for i in instructor_list
            if i["name"] == selected_name
        ),
        None
    )

    if instructor:

        state[f"{prefix}_initials"] = instructor.get(
            "initials",
            ""
        )

        state[f"{prefix}_padi"] = instructor.get(
            "padi_number",
            ""
        )

        # Auto-credit Confined Dive 4 when CW12 is completed
        if prefix == "CW12":

            state["Dive_4"] = "CONF"

            state["Dive_initials_4"] = instructor.get(
                "initials",
                ""
            )

            state["Dive_padi_4"] = instructor.get(
                "padi_number",
                ""
            )

    redraw_all_text_fields()
    redraw_all_signatures()

def redraw_all_text_fields():

    print(
        "ALL ITEMS BEFORE DELETE =",
        canvas_pdf.find_all()
    )

    print(
        "TEXT ITEMS BEFORE DELETE =",
        canvas_pdf.find_withtag("text_drawn")
    )

    canvas_pdf.delete("text_drawn")

    print(
        "TEXT ITEMS AFTER DELETE =",
        canvas_pdf.find_withtag("text_drawn")
    )

    canvas_pdf.delete("text_drawn") 

    if state is None:
        print("ERROR: state is None")
        return

    for f in fields:

        if f.get("page", 0) != current_page:
            continue

        if f["type"] not in ("day", "month", "year", "text"):
            continue

        if f["name"] == "Student Name":
            print(
                "DRAW STUDENT NAME:",
                repr(state.get(f["name"])),
                f["x1"],
                f["y1"]
            )

        value = state.get(f["name"])

        print(
            "DRAW:",
            repr(f["name"]),
            "=",
            repr(value)
        )

        if not value:
            continue

        x = int(f["x1"] * zoom_level)
        y = int(f["y1"] * zoom_level)

        print(
            "COORD:",
            f["name"],
            f["x1"],
            f["y1"]
        )
        item = canvas_pdf.create_text(
            x,
            y,
            anchor="nw",
            text=str(value),
            fill="black",
            font=("Helvetica", 10),
            tags="text_drawn"
        )


    # force text above image
    canvas_pdf.tag_raise("text_drawn")

    # keep boxes above text
    canvas_pdf.tag_raise("field_box")


def start_inline_edit(field):

    print("********************************")
    print("START_INLINE_EDIT CALLED")
    print("FIELD =", field["name"])
    print("STATE VALUE =", state.get(field["name"]))
    print("********************************")

    global editing_active
    global current_inline_entry

    if editing_active:
        return

    # Destroy any previous editor
    if current_inline_entry:
        try:
            current_inline_entry.destroy()
        except:
            pass

        current_inline_entry = None

    editing_active = True

    canvas_pdf.unbind("<Button-1>")

    current_value = state.get(field["name"], "")

    print("CURRENT VALUE =", repr(current_value))

    entry_var = tk.StringVar(value=current_value)

    entry = tk.Entry(
        canvas_pdf,
        textvariable=entry_var,
        width=20
    )

    current_inline_entry = entry

    x = int(field["x1"] * zoom_level)
    y = int(field["y1"] * zoom_level)

    # hide existing drawn text while editing
    #canvas_pdf.delete("text_drawn")

    entry_window = canvas_pdf.create_window(
        x,
        y,
        anchor="nw",
        window=entry
    )

    def save_inline(event=None):

        global editing_active
        global current_inline_entry

        new_value = entry_var.get()

        print("ENTRY VALUE =", repr(new_value))

        state[field["name"]] = new_value

        print(
            "SAVED:",
            field["name"],
            "=",
            state[field["name"]]
        )

        canvas_pdf.delete(entry_window)

        if entry.winfo_exists():
            entry.destroy()

        current_inline_entry = None
        editing_active = False

        canvas_pdf.bind("<Button-1>", on_pdf_click)

        #redraw_all_text_fields()
        #save_state_with_locations()
        render_page()
        save_state_with_locations()

    def cancel_inline(event=None):

        global editing_active
        global current_inline_entry

        canvas_pdf.delete(entry_window)

        if entry.winfo_exists():
            entry.destroy()

        current_inline_entry = None
        editing_active = False

        canvas_pdf.bind("<Button-1>", on_pdf_click)

        #redraw_all_text_fields()
        render_page()

    entry.bind("<Return>", save_inline)
    entry.bind("<Escape>", cancel_inline)

    entry.focus_set()
    entry.select_range(0, tk.END)



def redraw_all_checkboxes():

    canvas_pdf.delete("checkbox_drawn")

    for f in fields:

        if f.get("page", 0) != current_page:
            continue

        if f["type"] != "checkbox":
            continue

        checked = bool(state.get(f["name"], False))

        if not checked:
            continue

        x1 = int(f["x1"] * zoom_level)
        y1 = int(f["y1"] * zoom_level)
        x2 = int(f["x2"] * zoom_level)
        y2 = int(f["y2"] * zoom_level)

        canvas_pdf.create_text(
            (x1 + x2) // 2,
            (y1 + y2) // 2,
            text="✓",
            fill="black",
            font=("Arial", 14, "bold"),
            tags="checkbox_drawn"
        )
   

def on_pdf_click(event):
    global editing_active

    if editing_active:
        return

    if not pages:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    field = find_field(scaled_x, scaled_y, current_page)

    if not field:
        return

    global identify_mode, rename_mode

    print(
        "CLICKED:",
        field["name"],
        "rename_mode=",
        rename_mode
    )

    # ---------------------------
    # IDENTIFY MODE
    # ---------------------------

    if identify_mode:

        info = (
            f"Field Name: {field['name']}\n"
            f"Type: {field['type']}\n"
            f"Page: {field['page']}\n"
            f"Coordinates:\n"
            f"  x1={field['x1']}, y1={field['y1']}\n"
            f"  x2={field['x2']}, y2={field['y2']}"
        )

        messagebox.showinfo(
            "Field Info",
            info
        )

        print("FIELD JSON ENTRY:", field)

        return

    # ---------------------------
    # RENAME MODE
    # ---------------------------

    if rename_mode:

        new_name = simpledialog.askstring(
            "Rename Field",
            f"Enter new name for field '{field['name']}':",
            initialvalue=field["name"]
        )

        if new_name:

            field["name"] = new_name

            save_fields(fields)

            draw_all_field_boxes()
            redraw_all_text_fields()
            redraw_all_signatures()

            messagebox.showinfo(
                "Renamed",
                f"Field renamed to '{new_name}'"
            )

        return

    # ---------------------------
    # DIVE COUNTER
    # ---------------------------

    m = re.fullmatch(
        r"dive_(\d+)",
        field["name"].lower()
    )

    if m:

        dive_num = m.group(1)

        instructor = next(
            (
                i for i in instructor_list
                if i["name"] == instructor_var.get()
            ),
            None
        )

        current_value = state.get(
            field["name"],
            ""
        )

        if current_value == "":
            current_value = "1"
        elif current_value == "1":
            current_value = "2"
        elif current_value == "2":
            current_value = "3"
        elif current_value == "3":
            current_value = "4"
        else:
            current_value = ""

        state[field["name"]] = current_value

        if current_value == "":

            state[f"Dive_initials_{dive_num}"] = ""
            state[f"Dive_padi_{dive_num}"] = ""

        elif instructor:

            state[f"Dive_initials_{dive_num}"] = (
                instructor.get("initials", "")
            )

            state[f"Dive_padi_{dive_num}"] = (
                instructor.get("padi_number", "")
            )

        redraw_all_text_fields()
        save_state_with_locations()

        return

    # ---------------------------
    # CHECKBOX
    # ---------------------------

    if field["type"] == "checkbox":

        current_value = bool(
            state.get(field["name"], False)
        )

        state[field["name"]] = (
            not current_value
        )

        redraw_all_checkboxes()
        save_state_with_locations()

        return

    # ---------------------------
    # CW AUTO POPULATE
    # ---------------------------

    if field["name"].lower().endswith("_day"):

        name = field["name"].lower()

        m = re.search(
            r"(cw\d+)",
            name
        )

        if m:

            prefix = m.group(1).upper()

            populate_cw_row(prefix)

            return

    # ---------------------------
    # STUDENT SIGNATURE
    # ---------------------------

    if (
        field["name"]
        .strip()
        .lower()
        == "student_signature"
    ):

        existing_sig = state.get(
            field["name"]
        )

        if (
            existing_sig
            and resolve_signature_path(existing_sig).exists()
        ):

            answer = messagebox.askyesno(
                "Warning",
                "This student signature already exists.\n\n"
                "Replacing a signature may invalidate a previously "
                "signed training record.\n\n"
                "Do you want to continue?"
            )

            if not answer:
                return

        draw_student_signature_window(
            field["name"]
        )

        return

    # ---------------------------
    # INIT PADI INSTRUCTOR
    # ---------------------------

    m = re.fullmatch(
    r"init_padi_instructor_(\d+)",
    field["name"].strip().lower()
)

    if m:

        instructor_num = m.group(1)

        selected_name = instructor_var.get()

        if not selected_name:
            messagebox.showerror(
                "Error",
                "Select an instructor first."
            )
            return

        instructor = next(
            (i for i in instructor_list
            if i["name"] == selected_name),
            None
        )

        # Toggle OFF
        if state.get(field["name"]):

            state.pop(field["name"], None)

            state.pop(f"Init_PADI_no_{instructor_num}", None)
            state.pop(f"Init_Dive_Resort_No_{instructor_num}", None)
            state.pop(f"Init_Email_{instructor_num}", None)
            state.pop(f"Init_Phone_{instructor_num}", None)

            state.pop(
                f"Init_Instructor_Signature_{instructor_num}",
                None
            )

            state.pop(f"Init_day_{instructor_num}", None)
            state.pop(f"Init_month_{instructor_num}", None)
            state.pop(f"Init_year_{instructor_num}", None)

        # Toggle ON
        else:

            state[field["name"]] = selected_name

            if instructor:

                state[f"Init_PADI_no_{instructor_num}"] = \
                    instructor.get("padi_number", "")

                state[f"Init_Dive_Resort_No_{instructor_num}"] = \
                    instructor.get("store_number", "")

                state[f"Init_Email_{instructor_num}"] = \
                    instructor.get("email", "")

                state[f"Init_Phone_{instructor_num}"] = \
                    instructor.get("phone", "")

                sig_path = instructor.get("signature")

                if sig_path and resolve_signature_path(sig_path).exists():
                    state[
                        f"Init_Instructor_Signature_{instructor_num}"
                    ] = str(resolve_signature_path(sig_path))

            d = date_picker.get_date()

            state[f"Init_day_{instructor_num}"] = str(d.day)

            state[f"Init_month_{instructor_num}"] = [
                "Jan","Feb","Mar","Apr",
                "May","Jun","Jul","Aug",
                "Sep","Oct","Nov","Dec"
            ][d.month - 1]

            state[f"Init_year_{instructor_num}"] = str(d.year)

        redraw_all_text_fields()
        redraw_all_signatures()
        save_state_with_locations()

        return 

    # ---------------------------
    # INSTRUCTOR SIGNATURE
    # ---------------------------

    # ---------------------------
# INSTRUCTOR SIGNATURE
# ---------------------------

    m = re.fullmatch(
        r"instructor_signature_(\d+)",
        field["name"].strip().lower()
    )

    if m:

        selected_name = instructor_var.get()

        if not selected_name:
            messagebox.showerror(
                "Error",
                "Select an instructor first."
            )
            return

        instructor = next(
            (
                i for i in instructor_list
                if i["name"] == selected_name
            ),
            None
        )

        if not instructor:
            return

        signoff_num = m.group(1)

        # Toggle OFF
        if state.get(field["name"]):

            state.pop(field["name"], None)

            state.pop(f"PADI_no_{signoff_num}", None)
            state.pop(f"day_{signoff_num}", None)
            state.pop(f"month_{signoff_num}", None)
            state.pop(f"year_{signoff_num}", None)

        # Toggle ON
        else:

            sig_path = instructor.get("signature")

            if sig_path and resolve_signature_path(sig_path).exists():

                state[field["name"]] = sig_path

                state[f"PADI_no_{signoff_num}"] = (
                    instructor.get("padi_number", "")
                )

                d = date_picker.get_date()

                state[f"day_{signoff_num}"] = str(d.day)

                state[f"month_{signoff_num}"] = [
                    "Jan","Feb","Mar","Apr",
                    "May","Jun","Jul","Aug",
                    "Sep","Oct","Nov","Dec"
                ][d.month - 1]

                state[f"year_{signoff_num}"] = str(d.year)

        redraw_all_text_fields()
        redraw_all_signatures()
        save_state_with_locations()

        return

    # ---------------------------
    # NORMAL TEXT EDIT
    # ---------------------------

    start_inline_edit(field)


def on_pdf_right_click_normal(event):
    global editing_active
    if editing_active:
        return

    if not pages:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    field = find_field(scaled_x, scaled_y, current_page)
    if not field:
        return

    if field["type"] in ("text", "day", "month", "year"):

        for child in canvas_pdf.place_slaves():
            child.destroy()

        entry_var = tk.StringVar(value=state.get(field["name"], ""))

        entry = tk.Entry(canvas_pdf, textvariable=entry_var, width=20)

        x = int(field["x1"] * zoom_level)
        y = int(field["y1"] * zoom_level)
        
        entry_window = canvas_pdf.create_window(
            x,
            y,
            anchor="nw",
            window=entry
        )

        
        
        def save_entry(event=None):
            state[field["name"]] = entry_var.get()
            save_state_with_locations()

            print("ENTRY EXISTS BEFORE =", entry.winfo_exists())
            entry.destroy()
            print("ENTRY EXISTS AFTER =", entry.winfo_exists())

            redraw_all_text_fields()
            
        entry.bind("<Return>", save_entry)
        entry.focus_set()




# ---------------- Hover Highlight ----------------

hover_field = None

def on_pdf_motion(event):
    global editing_active, zoom_level
    if editing_active:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    global hover_field
    new_field = find_field(scaled_x, scaled_y, current_page)

    #
    # SHOW TOOLTIP FOR ACTION / AUTO-FILL FIELDS
    #
    global tooltip_window

    action_tip = action_field_info(new_field)

    if action_tip:

        if tooltip_window is None:
            tooltip_window = tk.Toplevel(root)
            tooltip_window.overrideredirect(True)
            tooltip_window._label = tk.Label(
                tooltip_window,
                text=action_tip,
                bg="lightyellow",
                relief="solid",
                borderwidth=1,
                justify="left",
                padx=5,
                pady=3
            )
            tooltip_window._label.pack()
        else:
            try:
                tooltip_window._label.config(text=action_tip)
            except Exception:
                pass

        tooltip_window.geometry(
            f"+{event.x_root + 15}+{event.y_root + 15}"
        )

    else:

        if tooltip_window:
            tooltip_window.destroy()
            tooltip_window = None

    if new_field is hover_field:
        return

    hover_field = new_field

    draw_all_field_boxes()

    #if new_field:
   #  print("HOVER:", repr(new_field["name"]))

def on_pdf_leave(event):

    global tooltip_window

    if tooltip_window:
        tooltip_window.destroy()
        tooltip_window = None


def draw_all_field_boxes():

    global editing_active
    global zoom_level

    if editing_active:
        return

    canvas_pdf.delete("field_box")

    for f in fields:

        if f.get("page", 0) != current_page:
            continue

        x1 = int(f["x1"] * zoom_level)
        y1 = int(f["y1"] * zoom_level)
        x2 = int(f["x2"] * zoom_level)
        y2 = int(f["y2"] * zoom_level)

        outline_color = "blue"
        width = 1
        dash = None

        # Orange dashed boxes identify fields that perform an action and
        # populate/update several related fields when clicked.
        if is_action_field(f):
            outline_color = "darkorange"
            width = 2
            dash = (5, 3)

        if hover_field is f:
            outline_color = "red"
            width = 3
            dash = None

        canvas_pdf.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline=outline_color,
            width=width,
            dash=dash,
            tags="field_box"
        )

# ---------------- Mask Editor ----------------

mask_edit_mode = False
drag_start = None
identify_mode = False
rename_mode = False


def bind_mask_edit_events():
    canvas_pdf.bind("<ButtonPress-3>", on_pdf_button_press)
    canvas_pdf.bind("<ButtonRelease-3>", on_pdf_button_release)

def unbind_mask_edit_events():
    canvas_pdf.unbind("<ButtonPress-3>")
    canvas_pdf.unbind("<ButtonRelease-3>")
    canvas_pdf.unbind("<Button-3>")




def toggle_mask_edit():
    global mask_edit_mode, identify_mode, rename_mode

    mask_edit_mode = not mask_edit_mode

    if mask_edit_mode:
        identify_mode = False
        rename_mode = False

        bind_mask_edit_events()

        status_label.config(
            text="Mask Edit Mode: ON (left drag=create field, right click=delete field)"
        )

    else:
        unbind_mask_edit_events()

        # Restore normal handlers
        canvas_pdf.bind("<Button-1>", on_pdf_click)
        canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal)
        if IS_MACOS:
            canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal)

        status_label.config(text="Mask Edit Mode: OFF")
    update_button_colors()


def toggle_rename_mode():
    global rename_mode, identify_mode, mask_edit_mode

    rename_mode = not rename_mode
    print("RENAME MODE =", rename_mode)
    
    if rename_mode:
        # Disable other modes
        identify_mode = False
        mask_edit_mode = False
        unbind_mask_edit_events()

        # Restore left-click handler for rename mode
        canvas_pdf.bind("<Button-1>", on_pdf_click)

        # Remove right-click text entry
        canvas_pdf.unbind("<Button-3>")

        status_label.config(text="Rename Mode: Click a field to rename it")

    else:
        # Restore normal right-click behavior
        canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal, add="+")
        if IS_MACOS:
            canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal, add="+")
        status_label.config(text="Rename Mode: OFF")

    update_button_colors()



def on_pdf_button_press(event):
    global drag_start

    global editing_active
    if editing_active:
        return

    if not mask_edit_mode or not pages:
        return


    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    drag_start = (canvas_x, canvas_y)

def on_pdf_button_release(event):
    global editing_active
    if editing_active:
        return

    if not mask_edit_mode or not pages or drag_start is None:
        return


    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    x1_canvas, y1_canvas = drag_start
    x2_canvas, y2_canvas = canvas_x, canvas_y

    if abs(x2_canvas - x1_canvas) < 5 or abs(y2_canvas - y1_canvas) < 5:
        drag_start = None
        return

    x1 = int(min(x1_canvas, x2_canvas) / zoom_level)
    y1 = int(min(y1_canvas, y2_canvas) / zoom_level)
    x2 = int(max(x1_canvas, x2_canvas) / zoom_level)
    y2 = int(max(y1_canvas, y2_canvas) / zoom_level)

    new_field = {
        "name": f"field_{len(fields)+1}",
        "type": "signature",
        "page": current_page,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2
    }

    fields.append(new_field)
    messagebox.showinfo("Field Created", "Field added to the current session.")

    #save_fields(fields)  
    draw_all_field_boxes()

    messagebox.showinfo(
        "Field Created",
        f"New signature field created:\n{new_field['name']}\nPage {current_page}"
    )

    drag_start = None

def redraw_all_signatures():
    canvas_pdf.delete("signature_drawn")
    canvas_pdf.signature_images = []   # ⭐ REQUIRED FIX

    for f in fields:
        if f.get("page", 0) != current_page:
            continue
        if f["type"] != "signature":
            continue

        sig_path = state.get(f["name"])
        if not isinstance(sig_path, str):
            continue

        if not resolve_signature_path(sig_path).exists():
            continue


        img = Image.open(resolve_signature_path(sig_path))
        w = int((f["x2"] - f["x1"]) * zoom_level)
        h = int((f["y2"] - f["y1"]) * zoom_level)
        img = img.resize((w, h), Image.LANCZOS)

        tk_img = ImageTk.PhotoImage(img)
        canvas_pdf.signature_images.append(tk_img)

        x = int(f["x1"] * zoom_level)
        y = int(f["y1"] * zoom_level)

        canvas_pdf.create_image(x, y, anchor="nw", image=tk_img, tags="signature_drawn")


# ---------------- Date Control Handler ----------------

def on_date_changed(event):
    """Fires automatically when a date context gets updated inside the dropdown calendar."""
    current_date = date_picker.get_date()
    state["global_selected_date"] = current_date.strftime("%Y-%m-%d")


def on_date_changed(event):
    current_date = date_picker.get_date()

    print("DATE PICKER =", current_date)

    state["global_selected_date"] = current_date.strftime("%Y-%m-%d")

# ---------------- Dynamic Widgets ----------------

def show_field_widget(field):
    for child in widget_frame.winfo_children():
        child.destroy()

    ftype = field["type"]
    name = field["name"]

    selected_name = instructor_var.get()
    instructor = next((i for i in instructor_list if i["name"] == selected_name), None)

    # Automatically sync granular date items using the top menu selection fallback context
    if ftype == "day":
        default_day = str(date_picker.get_date().day)
        values = [str(i) for i in range(1, 32)]
        var = tk.StringVar(value=state.get(name, default_day))
        cb = ttk.Combobox(widget_frame, values=values, textvariable=var, width=4)
        cb.pack(side="left")
        set_field_value(name, var.get())
        cb.bind("<<ComboboxSelected>>", lambda e: set_field_value(name, var.get()))

    elif ftype == "month":
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        default_month = months[date_picker.get_date().month - 1]
        var = tk.StringVar(value=state.get(name, default_month))
        cb = ttk.Combobox(widget_frame, values=months, textvariable=var, width=6)
        cb.pack(side="left")
        set_field_value(name, var.get())
        cb.bind("<<ComboboxSelected>>", lambda e: set_field_value(name, var.get()))

    elif ftype == "year":
        default_year = str(date_picker.get_date().year)
        values = [str(y) for y in range(2020, 2035)]
        var = tk.StringVar(value=state.get(name, default_year))
        cb = ttk.Combobox(widget_frame, values=values, textvariable=var, width=6)
        cb.pack(side="left")
        set_field_value(name, var.get())
        cb.bind("<<ComboboxSelected>>", lambda e: set_field_value(name, var.get()))

    elif ftype == "text":
        var = tk.StringVar(value=state.get(name, ""))
        entry = tk.Entry(widget_frame, textvariable=var, width=40)
        entry.pack(side="left")
        entry.bind("<Return>", lambda e: set_field_value(name, var.get()))

    elif ftype == "checkbox":
        var = tk.BooleanVar(value=bool(state.get(name, False)))
        cb = tk.Checkbutton(widget_frame, text=name, variable=var,
                            command=lambda: set_field_value(name, var.get()))
        cb.pack(side="left")

    elif ftype == "signature":
        if not instructor:
            messagebox.showerror("Error", "Select an instructor first.")
            return

        sig_path = instructor.get("signature")
        if not sig_path or not resolve_signature_path(sig_path).exists():
            messagebox.showerror("Error", "Instructor has no saved signature or file missing.")
            return

        set_field_value(name, sig_path)
        place_signature_on_canvas(field, sig_path)

def set_field_value(name, value):
    state[name] = value

# ---------------- PDF Export ----------------
from pypdf.generic import NameObject, BooleanObject, NumberObject

def _fit_font_size(text, box_width, box_height, start_size=9.0, min_size=4.5):
    if not text:
        return start_size

    size = start_size
    estimated_width = max(1.0, len(text) * 0.52)

    if estimated_width * size > box_width:
        size = box_width / estimated_width

    return max(min_size, min(start_size, size))


def _draw_static_form_values(page_canvas, page_index, pdf_values):
    """
    Draw form values directly into the PDF page.

    This is necessary because some PDF viewers/renderers do not display
    AcroForm appearance streams generated by pypdf.  The AcroForm values are
    still retained for later retrieval by the application.
    """
    for pdf_name, value in pdf_values.items():
        rect_info = pdf_field_rects.get(pdf_name)
        if not rect_info:
            continue

        field_page, x1_img, y1_img, x2_img, y2_img = rect_info
        if field_page != page_index:
            continue

        field_type = "text"

        for app_name, mapped_name in pdf_field_mapping.items():
            if mapped_name == pdf_name:
                info = next(
                    (f for f in fields if f["name"] == app_name),
                    None
                )
                if info:
                    field_type = info.get("type", "text")
                break

        scale = 200.0 / 72.0
        page_w, page_h = page_canvas._pagesize

        x1 = float(x1_img) / scale
        x2 = float(x2_img) / scale
        y_bottom = page_h - (float(y2_img) / scale)
        y_top = page_h - (float(y1_img) / scale)

        width = max(1.0, x2 - x1)
        height = max(1.0, y_top - y_bottom)

        if field_type == "signature":
            continue

        if field_type == "checkbox":
            if str(value) in ("/Yes", "Yes", "True", "true", "1"):
                page_canvas.setLineWidth(
                    max(0.8, min(1.5, height * 0.12))
                )
                page_canvas.line(
                    x1 + width * 0.18,
                    y_bottom + height * 0.48,
                    x1 + width * 0.42,
                    y_bottom + height * 0.20
                )
                page_canvas.line(
                    x1 + width * 0.42,
                    y_bottom + height * 0.20,
                    x1 + width * 0.82,
                    y_bottom + height * 0.80
                )
            continue

        text = str(value)
        if not text:
            continue

        font_size = _fit_font_size(
            text,
            width - 2,
            height - 1,
            start_size=min(9.0, max(6.0, height * 0.70))
        )

        page_canvas.setFont("Helvetica", font_size)
        page_canvas.setFillColorRGB(0, 0, 0)

        baseline = y_bottom + max(
            1.0,
            (height - font_size) / 2.0
        )

        page_canvas.drawString(
            x1 + 1,
            baseline,
            text
        )


def _add_signature_stamp_annotation(writer, page_num, image_path, x, y, width, height, field_name="Signature"):
    """Add a visible, removable PDF Stamp annotation containing a signature PNG.

    Unlike merge_page(), this does not burn the signature into page content.
    Standard annotation-aware PDF editors can select/delete the signature.
    """
    if width <= 0 or height <= 0:
        return

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.drawImage(
        ImageReader(image_path),
        0,
        0,
        width=width,
        height=height,
        mask="auto"
    )
    c.save()
    packet.seek(0)

    appearance_reader = PdfReader(packet)
    appearance_page = appearance_reader.pages[0]
    contents = appearance_page.get_contents()
    appearance_data = contents.get_data() if contents is not None else b""

    appearance = DecodedStreamObject()
    appearance.set_data(appearance_data)
    appearance[NameObject("/Type")] = NameObject("/XObject")
    appearance[NameObject("/Subtype")] = NameObject("/Form")
    appearance[NameObject("/FormType")] = NumberObject(1)
    appearance[NameObject("/BBox")] = ArrayObject([
        FloatObject(0), FloatObject(0), FloatObject(width), FloatObject(height)
    ])

    resources = appearance_page.get("/Resources")
    if resources is not None:
        resources = resources.get_object() if hasattr(resources, "get_object") else resources
        appearance[NameObject("/Resources")] = resources.clone(writer)

    appearance_ref = writer._add_object(appearance)

    annotation = DictionaryObject()
    annotation[NameObject("/Type")] = NameObject("/Annot")
    annotation[NameObject("/Subtype")] = NameObject("/Stamp")
    annotation[NameObject("/Rect")] = ArrayObject([
        FloatObject(x), FloatObject(y),
        FloatObject(x + width), FloatObject(y + height)
    ])
    annotation[NameObject("/Contents")] = TextStringObject(str(field_name))
    annotation[NameObject("/Name")] = NameObject("/Approved")
    # Print the annotation, but do not lock it. It remains removable/editable.
    annotation[NameObject("/F")] = NumberObject(4)
    annotation[NameObject("/AP")] = DictionaryObject({
        NameObject("/N"): appearance_ref
    })

    writer.add_annotation(page_number=page_num, annotation=annotation)


def overlay_pdf_with_state(
    input_pdf,
    output_pdf,
    fields,
    state,
    burn_signatures=False
):
    for f in fields:

        if f["type"] == "signature":

            print(
                "SIGNATURE FIELD:",
                f["name"],
                "=",
                state.get(f["name"])
            )

    reader = PdfReader(input_pdf)

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    # Mark the export with the pristine source ID.  When this PDF is reopened,
    # the app renders/exports from the cached clean source instead of stacking
    # another flattened appearance on top of this file.
    if current_base_id:
        try:
            metadata = {}
            if reader.metadata:
                for k, v in reader.metadata.items():
                    if isinstance(k, str) and isinstance(v, str):
                        metadata[k] = v
            metadata["/PADIManagerExport"] = "1"
            metadata["/PADIManagerBaseID"] = str(current_base_id)
            writer.add_metadata(metadata)
        except Exception as e:
            print("PDF METADATA WARNING:", e)

    # Keep the AcroForm interactive. Standard PDF editors need the widget
    # annotations to remain visible/editable and may regenerate their visual
    # appearances after a field value changes.
    if "/AcroForm" in writer._root_object:
        acro = writer._root_object["/AcroForm"]
        acro.update({
            NameObject("/NeedAppearances"):
            BooleanObject(True)
        })

    print("\n==============================")
    print("SIGNATURES BEFORE EXPORT")
    print("==============================")

    for f in fields:

        if f["type"] == "signature":

            print(
                f["name"],
                "=",
                repr(state.get(f["name"]))
            )

    print("==============================\n")
    
    pdf_values = {}

    for f in fields:

        value = state.get(f["name"])

        if value in (None, ""):
            continue

        #
        # Signature PNGs are handled later
        #
        if f["type"] == "signature":
            continue

        pdf_name = pdf_field_mapping.get(f["name"])

        if pdf_name:
            if f["type"] == "checkbox":

                if value:
                    pdf_values[pdf_name] = "/Yes"
                else:
                    pdf_values[pdf_name] = "/Off"

            else:

                pdf_values[pdf_name] = str(value)

    print("PDF VALUES =", pdf_values)
    print("\n===== EXPORT VALUES =====")

    for k, v in pdf_values.items():
        print(k, "=", repr(v))

    print("=========================\n")
    # Write the values into the real AcroForm fields and regenerate their
    # appearances.  The fields stay editable in Acrobat, Foxit, Preview,
    # PDF-XChange and other standard form-aware PDF editors.
    for page in writer.pages:
        writer.update_page_form_field_values(
            page,
            pdf_values,
            auto_regenerate=True
        )

    #
    # OPTIONAL SIGNATURE BURN-IN
    #
    # By default signatures are NOT merged into the saved PDF. This keeps the
    # exported form free of permanently burned signature artwork. The GUI
    # option "Burn signatures into PDF" enables the old behaviour when a
    # finalized/static copy is required.
    if burn_signatures:
        print("SIGNATURE BURN-IN = ON")

        for page_num, page in enumerate(writer.pages):

            packet = io.BytesIO()

            pdf_page = reader.pages[page_num]

            page_w = float(pdf_page.mediabox.width)
            page_h = float(pdf_page.mediabox.height)

            c = canvas.Canvas(
                packet,
                pagesize=(page_w, page_h)
            )

            # Do NOT draw ordinary text/check-box values into the page content.
            # They remain true AcroForm fields so external PDF editors can
            # change them. Only signature PNGs are optionally stamped here.

            signatures_drawn = 0

            for f in fields:

                if f.get("page", 0) != page_num:
                    continue

                if f["type"] != "signature":
                    continue

                sig_path = state.get(f["name"])

                if not sig_path:
                    continue

                resolved_sig = resolve_signature_path(sig_path)
                if not resolved_sig or not resolved_sig.exists():
                    continue

                print(
                    "STAMPING:",
                    f["name"],
                    "=",
                    resolved_sig
                )

                img_w, img_h = pages[page_num].size

                scale_x = page_w / img_w
                scale_y = page_h / img_h

                x = f["x1"] * scale_x

                y = page_h - (
                    f["y2"] * scale_y
                )

                width = (
                    f["x2"] - f["x1"]
                ) * scale_x

                height = (
                    f["y2"] - f["y1"]
                ) * scale_y

                c.drawImage(
                    ImageReader(resolved_sig),
                    x,
                    y,
                    width=width,
                    height=height,
                    mask="auto"
                )
                signatures_drawn += 1

            c.save()

            # Only merge an overlay if this page actually had a signature.
            if signatures_drawn:
                packet.seek(0)
                overlay_reader = PdfReader(packet)
                page.merge_page(overlay_reader.pages[0])

        # Leave all widget annotations visible and interactive. Hiding them
        # (annotation flag /F = 2) makes the saved PDF look flattened and
        # prevents normal click-to-edit behaviour in standard PDF editors.
    else:
        print("SIGNATURE BURN-IN = OFF (default): adding removable signature stamp annotations")

        # Keep signatures visible in ordinary PDF viewers without flattening
        # them into the page. Each signature is a /Stamp annotation with a
        # custom image appearance. Annotation-aware editors can select/delete
        # it, while the original page content remains untouched.
        for page_num, page in enumerate(writer.pages):
            pdf_page = reader.pages[page_num]
            page_w = float(pdf_page.mediabox.width)
            page_h = float(pdf_page.mediabox.height)

            for f in fields:
                if f.get("page", 0) != page_num or f["type"] != "signature":
                    continue

                sig_path = state.get(f["name"])
                if not sig_path:
                    continue

                resolved_sig = resolve_signature_path(sig_path)
                if not resolved_sig or not resolved_sig.exists():
                    print("SIGNATURE FILE NOT FOUND:", f["name"], "=", resolved_sig)
                    continue

                img_w, img_h = pages[page_num].size
                scale_x = page_w / img_w
                scale_y = page_h / img_h

                x = f["x1"] * scale_x
                y = page_h - (f["y2"] * scale_y)
                width = (f["x2"] - f["x1"]) * scale_x
                height = (f["y2"] - f["y1"]) * scale_y

                print("ADDING REMOVABLE SIGNATURE STAMP:", f["name"], "=", resolved_sig)
                _add_signature_stamp_annotation(
                    writer,
                    page_num,
                    resolved_sig,
                    x,
                    y,
                    width,
                    height,
                    f["name"]
                )

    output_pdf = Path(output_pdf).expanduser().resolve()
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Write to a temporary file in the destination directory first. This
    # prevents a partially written PDF from replacing a good existing file.
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{output_pdf.stem}_",
        suffix=".pdf.tmp",
        dir=str(output_pdf.parent)
    )
    try:
        with os.fdopen(fd, "wb") as fp:
            writer.write(fp)
            fp.flush()
            os.fsync(fp.fileno())
        Path(temp_name).replace(output_pdf)
    except Exception:
        try:
            Path(temp_name).unlink(missing_ok=True)
        except Exception:
            pass
        raise

    print("INPUT PDF =", input_pdf)
    print("OUTPUT PDF =", output_pdf)


#def save_progress():
 #   save_state_with_locations()
  #  messagebox.showinfo("Saved", "Progress saved.")

def export_pdf():
    """Export an editable AcroForm PDF; signature burn-in is optional."""

    if not pdf_path:
        messagebox.showerror("Error", "No PDF loaded.")
        return

    student_name = state.get("Student Name", "").strip()

    if student_name:
        safe_name = student_name.replace("/", "_").replace("\\", "_")
        default_filename = f"{safe_name}_PADI_Record.pdf"
    else:
        default_filename = "PADI_Record.pdf"

    output = filedialog.asksaveasfilename(
        title="Export PDF",
        initialfile=default_filename,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not output:
        return

    try:
        # Rebuild against the PDF currently being exported so mappings cannot
        # become stale after opening more than one PDF in a session.
        build_pdf_field_mapping()

        export_base = str(current_base_pdf_path or pdf_path)
        print("EXPORT BASE PDF =", export_base)
        overlay_pdf_with_state(
            export_base,
            output,
            fields,
            state,
            burn_signatures=bool(burn_signature_var.get())
        )

        # Save the comment independently of the PDF export. A comment database
        # problem must never make a successfully written PDF look like a failed
        # export.
        try:
            save_current_comment(output)
        except Exception as comment_error:
            print("COMMENT SAVE WARNING:", comment_error)

        messagebox.showinfo(
            "Exported",
            f"PDF exported:\n{Path(output).resolve()}"
        )

    except Exception as e:
        print("PDF EXPORT ERROR:", repr(e))
        traceback.print_exc()
        messagebox.showerror(
            "PDF Export Error",
            str(e)
        )


# ---------------- Add New Instructor ----------------

def add_instructor_window():
    global instructor_window
    instructor_window = tk.Toplevel(root)
    win = instructor_window
    win.title("Instructor Manager")
    win.geometry("400x650")

    # Force window to front
    win.lift()
    win.focus_force()

    # ---------------- Existing Instructor ----------------

    tk.Label(win, text="Existing Instructor").pack(pady=5)

    existing_var = tk.StringVar()

    existing_combo = ttk.Combobox(
        win,
        textvariable=existing_var,
        values=[i["name"] for i in instructor_list],
        width=30
    )
    existing_combo.pack(pady=5)

    # ---------------- Instructor Details ----------------

    tk.Label(win, text="Name:").pack(pady=5)
    name_var = tk.StringVar()
    tk.Entry(win, textvariable=name_var).pack()

    tk.Label(win, text="Email:").pack(pady=5)
    email_var = tk.StringVar()
    tk.Entry(win, textvariable=email_var).pack()

    tk.Label(win, text="Phone Number:").pack(pady=5)
    phone_var = tk.StringVar()
    tk.Entry(win, textvariable=phone_var).pack()

    tk.Label(win, text="PADI Number:").pack(pady=5)
    padi_var = tk.StringVar()
    tk.Entry(win, textvariable=padi_var).pack()

    tk.Label(win, text="PADI Store Number:").pack(pady=5)
    store_var = tk.StringVar(value="4491")
    tk.Entry(win, textvariable=store_var).pack()

    tk.Label(win, text="Initials:").pack(pady=5)
    initials_var = tk.StringVar()
    tk.Entry(win, textvariable=initials_var).pack()

    tk.Label(win, text="Signature (draw inside app):").pack(pady=5)
    signature_var = tk.StringVar()

    
    

    def open_signature_draw():

        name = name_var.get()
        padi = padi_var.get()

        if not name:
            messagebox.showerror(
                "Error",
                "Enter name first."
            )
            return

        if not padi:
            messagebox.showerror(
                "Error",
                "Enter PADI number first."
            )
            return

        draw_signature_window(
            name,
            padi,
            signature_var
        )

    tk.Button(win, text="Draw Signature", command=open_signature_draw).pack(pady=10)

    def delete_instructor():
        name = name_var.get()

        if not name:
            messagebox.showerror("Error", "Enter or select an instructor name.")
            return

        instructor = next(
            (i for i in instructor_list if i["name"] == name),
            None
        )

        if not instructor:
            messagebox.showerror("Error", f"Instructor '{name}' not found.")
            return

        if not messagebox.askyesno(
            "Delete Instructor",
            f"Delete instructor '{name}'?"
        ):
            return

        instructor_list.remove(instructor)
        save_instructors({"instructors": instructor_list})

        instructor_dropdown["values"] = [
            i["name"] for i in instructor_list
        ]

        instructor_var.set("")

        messagebox.showinfo(
            "Deleted",
            f"Instructor '{name}' removed."
        )

        win.destroy()

    def load_selected(event=None):
        
        name = existing_var.get()

        instructor = next(
            (i for i in instructor_list if i["name"] == name),
            None
        )

        if not instructor:
            return

        name_var.set(instructor.get("name", ""))
        email_var.set(instructor.get("email", ""))
        phone_var.set(instructor.get("phone", ""))
        padi_var.set(instructor.get("padi_number", ""))
        store_var.set(instructor.get("store_number", "4491"))
        initials_var.set(instructor.get("initials", ""))
        signature_var.set(instructor.get("signature", ""))
        
    existing_combo.bind("<<ComboboxSelected>>", load_selected)

    def save_new():
        name = name_var.get()
        email = email_var.get()
        phone = phone_var.get()
        padi = padi_var.get()
        store = store_var.get()
        initials = initials_var.get()
        signature = signature_var.get()
        print("DEBUG signature_var =", signature)

        if not signature or not resolve_signature_path(signature).exists():
            messagebox.showerror("Error", "Signature must be drawn and saved.")
            return

        if not name or not email or not phone or not padi or not store or not initials:
            messagebox.showerror("Error", "All fields are required.")
            return

        new_inst = {
            "name": name,
            "email": email,
            "phone": phone,
            "padi_number": padi,
            "store_number": store,
            "initials": initials,
            "signature": signature
        }

        instructor_list.append(new_inst)
        save_instructors({"instructors": instructor_list})

        instructor_dropdown["values"] = [i["name"] for i in instructor_list]
        instructor_var.set(name)
        update_instructor_info()


        messagebox.showinfo("Saved", "Instructor added successfully.")
        
        win.destroy()

    btn_frame = tk.Frame(win)
    
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)


    tk.Button(
        btn_frame,
        text="Save Instructor",
        command=save_new
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text="Delete Instructor",
        command=delete_instructor,
        bg="tomato"
    ).pack(side="left", padx=10)


# ---------------- Instructor Info Display ----------------

def update_instructor_info(*args):
    name = instructor_var.get()
    instructor = next((i for i in instructor_list if i["name"] == name), None)

    if not instructor:
        instructor_info.config(text="No instructor selected")
        return

    sig_path = instructor.get("signature")
    if sig_path and resolve_signature_path(sig_path).exists():
        sig_status = "✔ Signature saved"
    elif sig_path:
        sig_status = "✘ Signature path set but file missing"
    else:
        sig_status = "✘ No signature path set"

    info_text = (
        f"Name: {instructor['name']}   "
        f"Email: {instructor['email']}   "
        f"Phone: {instructor['phone']}\n"
        f"PADI#: {instructor['padi_number']}   "
        f"Store#: {instructor.get('store_number', '4491')}   "
        f"Initials: {instructor.get('initials', 'N/A')}   "
        f"{sig_status}"
    )


    instructor_info.config(text=info_text)

def toggle_identify_mode():
    global identify_mode, mask_edit_mode
    identify_mode = not identify_mode
    canvas_pdf.unbind("<Button-3>")


    if identify_mode:
        mask_edit_mode = False

        # Unbind ALL right-click handlers from mask edit mode
        canvas_pdf.unbind("<ButtonPress-3>")
        canvas_pdf.unbind("<ButtonRelease-3>")
        canvas_pdf.unbind("<Button-3>")   # ← REQUIRED

        # Bind identify-mode delete handler


        status_label.config(text="Identify Mode: Left-click to inspect, Right-click to delete")
        update_button_colors()

    else:
        canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal, add="+")
        if IS_MACOS:
            canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal, add="+")

        status_label.config(text="Identify Mode: OFF")
        update_button_colors()




def auto_detect_fields():
    global fields

    if not pdf_path or not pages:
        messagebox.showerror("Error", "Load a PDF first.")
        return

    # Run AcroForm detection
    auto_fields = detect_acroform_fields(pdf_path, pages)

    # Run heuristic detection
    heuristic_fields = []
    for idx, img in enumerate(pages):
        heuristic_fields.extend(heuristic_signature_boxes(img, idx))

    # Merge results
    new_fields = auto_fields + heuristic_fields

    if not new_fields:
        messagebox.showinfo("Auto-Detect Fields", "No fields detected.")
        return

    # Filter out duplicates by name
    existing_names = {f["name"] for f in fields}
    unique_new_fields = [f for f in new_fields if f["name"] not in existing_names]

    if not unique_new_fields:
        messagebox.showinfo("Auto-Detect Fields", "All detected fields already exist.")
        return

    # Append only unique fields
    fields.extend(unique_new_fields)

    draw_all_field_boxes()
    redraw_all_signatures()

    messagebox.showinfo(
        "Auto-Detect Fields",
        f"Added {len(unique_new_fields)} new fields.\n\n"
        "Changes are in memory only and will reset when a new PDF is loaded."
    )

def on_pdf_right_click(event):
    if not pages:
        return

    global identify_mode
    if not identify_mode:
        return  # only delete in identify mode

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    field = find_field(scaled_x, scaled_y, current_page)
    if not field:
        return

    print("CLICKED FIELD =", repr(field["name"]))

    if messagebox.askyesno("Delete Field", f"Delete field '{field['name']}'?"):
        fields.remove(field)
        #save_fields(fields)

        # ⭐ REQUIRED FIX — clear hover state
        global hover_field
        hover_field = None

        draw_all_field_boxes()
        redraw_all_signatures()

        messagebox.showinfo("Field Deleted", f"Field '{field['name']}' removed from the current session.")

 
def update_button_colors():

    if mask_edit_mode:
        btn_mask_edit.config(bg="orange")
    else:
        btn_mask_edit.config(bg=root.cget("bg"))

    if identify_mode:
        btn_identify.config(bg="lightgreen")
    else:
        btn_identify.config(bg=root.cget("bg"))

    if rename_mode:
        btn_rename.config(bg="lightgreen")
    else:
        btn_rename.config(bg=root.cget("bg"))


# ---------------- GUI SETUP ----------------

def _on_application_close():
    """Close secondary windows and terminate Tk cleanly."""
    try:
        save_current_comment(pdf_path)
    except Exception as e:
        print("COMMENT SAVE ON EXIT WARNING:", e)

    try:
        root.destroy()
    except Exception:
        pass


def _write_crash_log(exc_type, exc_value, exc_tb):
    """Persist unexpected GUI errors where a macOS .app user can retrieve them."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        log_path = DATA_DIR / "crash.log"
        with log_path.open("a", encoding="utf-8") as f:
            f.write("\n" + "=" * 72 + "\n")
            f.write(f"Platform: {sys.platform}\nPython: {sys.version}\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
    except Exception:
        pass
    traceback.print_exception(exc_type, exc_value, exc_tb)


def _tk_exception_handler(exc_type, exc_value, exc_tb):
    _write_crash_log(exc_type, exc_value, exc_tb)
    try:
        messagebox.showerror(
            "PADI Manager Error",
            f"An unexpected error occurred:\n\n{exc_value}\n\n"
            f"A diagnostic log was written to:\n{DATA_DIR / 'crash.log'}"
        )
    except Exception:
        pass


sys.excepthook = _write_crash_log

root = tk.Tk()
root.report_callback_exception = _tk_exception_handler
root.title("PADI Manager V20")
root.geometry("1200x800")
root.protocol("WM_DELETE_WINDOW", _on_application_close)

hover_info_label = tk.Label(
    root,
    text="",
    bg="lightyellow",
    relief="solid",
    borderwidth=1,
    justify="left"
)

top_frame = ttk.Frame(root)
top_frame.pack(fill="x", pady=5)
try:
    # Decode the embedded logo; no external logo.png is required.
    logo_bytes = base64.b64decode(EMBEDDED_LOGO_PNG)
    logo_img = Image.open(io.BytesIO(logo_bytes)).convert("RGBA")
    logo_img = logo_img.resize((64, 64), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(top_frame, image=logo_photo)
    logo_label.image = logo_photo   # keep reference alive for Tkinter
    logo_label.pack(side="left", padx=5)

except Exception as e:
    print("Embedded logo load failed:", e)

tk.Label(top_frame, text="Instructor:").pack(side="left", padx=5)
instructor_var = tk.StringVar()
instructor_dropdown = ttk.Combobox(
    top_frame,
    textvariable=instructor_var,
    values=[i["name"] for i in instructor_list],
    width=25
)
instructor_dropdown.pack(side="left")

tk.Button(top_frame, text="Add/Manage Instructor", command=add_instructor_window).pack(side="left", padx=10)



# --- Integrated Date Picker Widget ---
tk.Label(top_frame, text="Select Date:").pack(side="left", padx=(15, 2))


date_picker = DateEntry(
    top_frame,
    width=12,
    background='darkblue',
    foreground='white',
    borderwidth=2,
    date_pattern='yyyy-mm-dd'
)

date_picker.configure(state="readonly")
date_picker.set_date(date.today())

date_picker.pack(side="left", padx=5)
date_picker.bind("<<DateEntrySelected>>", on_date_changed)

instructor_info = tk.Label(top_frame, text="No instructor selected", anchor="w", justify="left")
instructor_info.pack(side="left", padx=20)

instructor_var.trace_add("write", update_instructor_info)


mid_frame = ttk.Frame(root)
mid_frame.pack(fill="x", pady=5)

tk.Button(mid_frame, text="Load PDF", command=load_pdf).pack(side="left", padx=5)
pdf_label = tk.Label(mid_frame, text="No PDF loaded")
pdf_label.pack(side="left", padx=10)

tk.Button(mid_frame, text="Prev Page", command=prev_page).pack(side="left", padx=5)
tk.Button(mid_frame, text="Next Page", command=next_page).pack(side="left", padx=5)

tk.Button(mid_frame, text="Zoom +", command=zoom_in).pack(side="left", padx=5)
tk.Button(mid_frame, text="Zoom -", command=zoom_out).pack(side="left", padx=5)
tk.Button(mid_frame, text="Fit Page", command=zoom_fit).pack(side="left", padx=5)


tk.Button(
    mid_frame,
    text="Save/Update PDF",
    command=export_pdf
).pack(side="left", padx=5)

# Signature export mode. Default is OFF so signatures stay in the app state
# and are not permanently merged into the PDF page artwork.
burn_signature_var = tk.BooleanVar(value=False)
burn_signature_check = tk.Checkbutton(
    mid_frame,
    text="Burn signatures into PDF",
    variable=burn_signature_var,
    onvalue=True,
    offvalue=False
)
burn_signature_check.pack(side="left", padx=(6, 4))

# ------------------------------------------------------------
# Main-menu comment box
# ------------------------------------------------------------
# No separate Comment button/window.  The textbox is always visible
# beside Save/Update PDF and reads/writes comments.json.
comment_frame = tk.Frame(mid_frame)
comment_frame.pack(
    side="left",
    padx=(6, 10),
    pady=0,
    fill="y"
)

comment_text = tk.Text(
    comment_frame,
    width=34,
    height=2,
    wrap="word",
    undo=True,
    font=("Arial", 9)
)

comment_scrollbar = tk.Scrollbar(
    comment_frame,
    orient="vertical",
    command=comment_text.yview
)

comment_text.configure(
    yscrollcommand=comment_scrollbar.set
)

comment_text.pack(
    side="left",
    fill="both",
    expand=True
)

comment_scrollbar.pack(
    side="right",
    fill="y"
)

def update_comment_box_color(event=None):
    content = comment_text.get("1.0", "end-1c").strip()

    if content:
        comment_text.configure(bg="orange")
    else:
        comment_text.configure(bg="white")

comment_text.bind("<KeyRelease>", update_comment_box_color)

# Set initial color
update_comment_box_color()





status_label = tk.Label(root, text="Mask Edit Mode: OFF")
status_label.pack(pady=5)

#
# Main area = PDF viewer + right tools panel
#
main_view_frame = tk.Frame(root)
main_view_frame.pack(fill="both", expand=True)

#
# PDF Viewer Area
#
pdf_frame = tk.Frame(main_view_frame)
pdf_frame.pack(side="left", fill="both", expand=True)

#
# Right Tools Panel
#
tools_frame = tk.Frame(
    main_view_frame,
    width=110,
    relief="groove",
    bd=2
)

tools_frame.pack(
    side="right",
    fill="y",
    padx=5,
    pady=5
)
weite=10
tools_frame.pack_propagate(False)

# Legend for clickable fields that trigger multiple automatic updates.
action_legend = tk.Label(
    tools_frame,
    text="Orange dashed =\nauto-fill/action",
    fg="darkorange",
    justify="center",
    wraplength=100
)
action_legend.pack(fill="x", pady=(2, 6))

btn_mask_edit = tk.Button(
    tools_frame,
    text="Toggle Mask Edit",
    command=toggle_mask_edit,
    width=weite
)

btn_identify = tk.Button(
    tools_frame,
    text="Identify Field",
    command=toggle_identify_mode,
    width=weite
)

btn_rename = tk.Button(
    tools_frame,
    text="Rename Field",
    command=toggle_rename_mode,
    width=weite
)

btn_close_pdf = tk.Button(
    tools_frame,
    text="Close PDF",
    command=close_pdf,
    width=weite
)

#
# Right-side tool buttons
#
btn_mask_edit.pack(
    fill="x",
    pady=2
)

btn_identify.pack(
    fill="x",
    pady=2
)

btn_rename.pack(
    fill="x",
    pady=2
)

tk.Button(
    tools_frame,
    text="Auto-Detect Fields",
    command=auto_detect_fields
).pack(
    fill="x",
    pady=2
)





btn_close_pdf.pack(
    fill="x",
    pady=2
)

tk.Button(
    tools_frame,
    text="Field Logic 10056",
    command=show_program_fields
).pack(
    fill="x",
    pady=2
)

update_button_colors()
update_button_colors()

v_scroll = tk.Scrollbar(pdf_frame, orient="vertical")
h_scroll = tk.Scrollbar(pdf_frame, orient="horizontal")

canvas_pdf = tk.Canvas(
    pdf_frame,
    bg="grey",
    width=900,
    height=600,
    scrollregion=(0, 0, 2000, 2000),
    yscrollcommand=v_scroll.set,
    xscrollcommand=h_scroll.set
)
canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal, add="+")
if IS_MACOS:
    canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal, add="+")

canvas_pdf.focus_set()

v_scroll.config(command=canvas_pdf.yview)
h_scroll.config(command=canvas_pdf.xview)

v_scroll.pack(side="right", fill="y")
h_scroll.pack(side="bottom", fill="x")
canvas_pdf.pack(side="left", fill="both", expand=True)

def _on_mousewheel(event):
    """Cross-platform wheel/trackpad scrolling."""
    delta = getattr(event, "delta", 0)
    if not delta:
        return
    if IS_MACOS:
        # macOS Tk reports small, high-resolution trackpad deltas.
        units = -1 if delta > 0 else 1
    else:
        units = int(-delta / 120)
        if units == 0:
            units = -1 if delta > 0 else 1
    canvas_pdf.yview_scroll(units, "units")

canvas_pdf.bind("<Button-1>", on_pdf_click)
canvas_pdf.bind("<Motion>", on_pdf_motion)
canvas_pdf.bind("<Leave>", on_pdf_leave)
canvas_pdf.bind("<MouseWheel>", _on_mousewheel)
# Linux/X11 fallback; harmless for source runs outside macOS/Windows.
canvas_pdf.bind("<Button-4>", lambda e: canvas_pdf.yview_scroll(-1, "units"))
canvas_pdf.bind("<Button-5>", lambda e: canvas_pdf.yview_scroll(1, "units"))



def bind_mask_edit_events():
    # LEFT CLICK = create field
    canvas_pdf.bind("<ButtonPress-1>", on_mask_left_press)
    canvas_pdf.bind("<ButtonRelease-1>", on_mask_left_release)

    # RIGHT CLICK = delete field
    canvas_pdf.bind("<Button-3>", on_mask_right_click)
    if IS_MACOS:
        canvas_pdf.bind("<Control-Button-1>", on_mask_right_click)


def unbind_mask_edit_events():
    canvas_pdf.unbind("<ButtonPress-1>")
    canvas_pdf.unbind("<ButtonRelease-1>")
    canvas_pdf.unbind("<Button-3>")

    canvas_pdf.bind("<Button-1>", on_pdf_click)
    canvas_pdf.bind("<Button-3>", on_pdf_right_click_normal)
    if IS_MACOS:
        canvas_pdf.bind("<Control-Button-1>", on_pdf_right_click_normal)

# ---------------- Mask Edit: LEFT CLICK = Create Field ----------------

def on_mask_left_press(event):
    global drag_start
    if not mask_edit_mode or not pages:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)
    drag_start = (canvas_x, canvas_y)


def on_mask_left_release(event):
    global drag_start
    if not mask_edit_mode or not pages or drag_start is None:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    x1_canvas, y1_canvas = drag_start
    x2_canvas, y2_canvas = canvas_x, canvas_y

    # Ignore tiny drags
    if abs(x2_canvas - x1_canvas) < 5 or abs(y2_canvas - y1_canvas) < 5:
        drag_start = None
        return

    x1 = int(min(x1_canvas, x2_canvas) / zoom_level)
    y1 = int(min(y1_canvas, y2_canvas) / zoom_level)
    x2 = int(max(x1_canvas, x2_canvas) / zoom_level)
    y2 = int(max(y1_canvas, y2_canvas) / zoom_level)

    new_field = {
        "name": f"field_{len(fields)+1}",
        "type": "text",
        "page": current_page,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2
    }

    fields.append(new_field)
    draw_all_field_boxes()
    messagebox.showinfo("Field Created", f"New field created:\n{new_field['name']}")

    drag_start = None


# ---------------- Mask Edit: RIGHT CLICK = Delete Field ----------------

def on_mask_right_click(event):
    if not mask_edit_mode or not pages:
        return

    canvas_x = canvas_pdf.canvasx(event.x)
    canvas_y = canvas_pdf.canvasy(event.y)

    scaled_x = int(canvas_x / zoom_level)
    scaled_y = int(canvas_y / zoom_level)

    field = find_field(scaled_x, scaled_y, current_page)
    if not field:
        return

    if messagebox.askyesno("Delete Field", f"Delete field '{field['name']}'?"):
        fields.remove(field)
        draw_all_field_boxes()
        redraw_all_signatures()



canvas_pdf.bind("<ButtonPress-2>", on_pdf_button_press)
canvas_pdf.bind("<ButtonRelease-2>", on_pdf_button_release)

canvas_pdf.bind("<B3-Motion>", lambda e: None)
canvas_pdf.bind("<B2-Motion>", lambda e: None)

widget_frame = ttk.Frame(root)
widget_frame.pack(fill="x", pady=5)

if __name__ == "__main__":
    # Delay first render so canvas dimensions are correct
    # Only render after Tk finishes drawing the window
    root.after(200, lambda: render_page() if pages else None)
    root.mainloop()

