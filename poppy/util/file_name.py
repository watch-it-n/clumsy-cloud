import os
import re

_CAPTION_FILE_EXTENSION = re.compile(
    r"\.(?P<extension>mkv|mp4|avi|mov|webm|m4v|mpg|mpeg|ts|flv|wmv)(?=\s|$)",
    flags=re.IGNORECASE,
)
# Strip join links in both ordinary and escaped-caption forms (for example,
# ``Join ~ [link]`` and ``Join \~ [link]\``).
_JOIN_MARKER = re.compile(r"Join\s*\\?~?\s*\[[^\]]*\]\\?", flags=re.IGNORECASE)
_VIDEO_FILE_EXTENSION = re.compile(
    r"\.(?P<extension>mkv|mp4|avi|mov|webm|m4v|mpg|mpeg|ts|flv|wmv)$",
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
    caption = _JOIN_MARKER.sub("", str(caption or ""))
    caption = re.sub(r"[ \t]+", " ", caption).strip()
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
    """Refine a caption filename, using the Telegram filename's extension if needed."""
    caption = _JOIN_MARKER.sub("", str(caption or ""))
    caption = re.sub(r"[ \t]+", " ", caption).strip()
    refined = append_infinity_to_caption_filename(caption)
    if _CAPTION_FILE_EXTENSION.search(caption):
        return refined

    # Captions without a video extension often contain metadata below the filename.
    # Keep only the first line (or tab-delimited field) as the filename candidate.
    filename = re.split(r"[\r\n\t]", caption, maxsplit=1)[0].strip()
    if not filename:
        filename = str(fallback_file_name or "").strip()
    fallback = str(fallback_file_name or "").strip()
    extension_match = _VIDEO_FILE_EXTENSION.search(fallback)
    extension = extension_match.group("extension") if extension_match else "mkv"
    filename_match = _VIDEO_FILE_EXTENSION.search(filename)
    if filename_match:
        extension = filename_match.group("extension")
        filename = filename[:filename_match.start()]

    filename = filename.rstrip(" .")
    if not filename:
        filename = os.path.splitext(fallback)[0].strip() or "Infinity"
    return append_infinity_to_caption_filename(f"{filename}.{extension}")
