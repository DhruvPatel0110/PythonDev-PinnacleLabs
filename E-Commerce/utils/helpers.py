"""General helper functions."""

import uuid
from pathlib import Path

from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = frozenset({"png", "jpg", "jpeg", "gif", "webp"})
PRODUCT_UPLOAD_SUBDIR = Path("uploads") / "products"


def allowed_image_file(filename):
    if not filename or "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_IMAGE_EXTENSIONS


def get_product_upload_dir(static_folder):
    upload_dir = Path(static_folder) / PRODUCT_UPLOAD_SUBDIR
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def save_product_image(file_storage, static_folder):
    """Save an uploaded image and return the stored filename, or None."""
    if not file_storage or not file_storage.filename:
        return None

    if not allowed_image_file(file_storage.filename):
        return None

    extension = file_storage.filename.rsplit(".", 1)[1].lower()
    base_name = secure_filename(file_storage.filename.rsplit(".", 1)[0]) or "product"
    filename = f"{base_name}_{uuid.uuid4().hex[:12]}.{extension}"

    upload_dir = get_product_upload_dir(static_folder)
    file_storage.save(upload_dir / filename)
    return filename


def delete_product_image(static_folder, image_filename):
    if not image_filename:
        return

    image_path = Path(static_folder) / PRODUCT_UPLOAD_SUBDIR / image_filename
    if image_path.is_file():
        image_path.unlink()
