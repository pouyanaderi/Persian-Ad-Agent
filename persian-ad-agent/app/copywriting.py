"""Simple deterministic Persian ad-copy helper; no external API required."""
import re

def make_copy(description: str, headline: str | None = None, cta: str = "همین حالا سفارش دهید") -> dict[str, str]:
    clean = re.sub(r"\s+", " ", description).strip()
    if not clean:
        clean = "محصول شما"
    title = (headline or clean[:48]).strip()
    if len(title) > 64:
        title = title[:61].rstrip() + "…"
    caption = f"{clean}\nکیفیت و زیبایی، در یک انتخاب.\n{cta}"
    return {"headline": title, "caption": caption, "description": clean}
