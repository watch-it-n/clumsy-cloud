import os
import re

_CAPTION_FILE_EXTENSION = re.compile(
    r"\.(?P<extension>mkv|mp4|avi|mov|webm|m4v|mpg|mpeg|ts|flv|wmv)(?=\s|$)",
    flags=re.IGNORECASE,
)


def replace_last_filename_word(file_name: str) -> str:
    name = str(file_name or "").strip()
    stem, extension = os.path.splitext(name)
    if not extension or extension == "." or not stem.strip():
        return name
    parts = [part for part in re.split(r"[\s._]+", stem.strip()) if part]
    if not parts:
        return name
    parts[-1] = "infinity"
    return f"{'.'.join(parts)}{extension}"


def append_infinity_to_caption_filename(caption: str) -> str:
    """Refine a caption's filename and drop any text after its extension."""
    match = _CAPTION_FILE_EXTENSION.search(caption)
    if not match:
        return caption

    # Only the filename portion through the extension is retained.
    filename = caption[:match.end()].replace("_", ".")
    stem = filename[:match.start()]
    extension = match.group("extension")

    # Replace the last filename component, whether components use spaces or dots.
    component = re.search(r"[^\s.]+$", stem)
    if component:
        stem = f"{stem[:component.start()]}Infinity"
    else:
        stem = "Infinity"
    return f"{stem}.{extension}"


def refine_file_caption(caption: str, fallback_file_name: str = "") -> str:
    """Refine a filename-like caption, falling back to Telegram's filename."""
    caption = str(caption or "").strip()
    refined = append_infinity_to_caption_filename(caption)
    if refined != caption:
        return refined
    fallback = str(fallback_file_name or "").strip()
    return append_infinity_to_caption_filename(fallback) or caption
