#!/usr/bin/env python3
"""Genera dark.svg y light.svg del README de perfil.

Panel izquierdo: foto real embebida como data URI JPEG, recortada en circulo.
Panel derecho: bloque system.info con relleno de puntos alineado automaticamente.

Editar INFO/CONTACT abajo y correr `python profile_svg.py` para regenerar.
"""
import base64
import io
from html import escape
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
PHOTO = "Linkedln_1.png"
WALL = (208, 206, 202)   # color de la pared del estudio, para aplanar el alfa
PHOTO_PX = 720           # panel ~366 CSS px en GitHub -> 720 cubre pantallas 2x
PHOTO_Q = 82

# ---------------------------------------------------------------- contenido --
PROMPT = "danflea@devos ~ % ./profile.sh --live"
HEADER = "danflea@devos"

INFO = [
    ("Subject", "Danflea"),
    ("Role", "Data & ML Engineer en formación"),
    ("Origin", "Perú"),
    ("Education", "UNALM · Estadística Informática"),
    ("Status", "Building · Learning · Shipping"),
    ("ToolChain", "Claude Code, Git/GitHub CLI, VS Code, Obsidian, Docker"),
    None,
    ("Core.Lang", "R, Python, Bash"),
    ("Core.Data.ML", "caret, caretEnsemble, XGBoost, Random Forest"),
    ("Core.Models", "SVM, GLM, Naive Bayes, KNN, CART, nnet, treebag"),
    ("Core.Infra", "Docker ~30 ctr, Cloudflare Tunnels, n8n, Airflow"),
    ("Core.Database", "PostgreSQL, SQL Server"),
    None,
]
CONTACT = [
    ("Grid.Mail", "danilo.david.eg@gmail.com"),
    ("Grid.Portfolio", "portfolio.danflylab.space"),
    ("Grid.LinkedIn", "linkedin.com/in/danilo-estrella-guerra-9b26a92a5"),
    ("Grid.Github", "DanfleEG"),
    None,
]
FOOTER_NOTE = "Grid de contribuciones en vivo abajo en el README"

# Ancho total de cada linea del panel, en caracteres monospace.
# Courier avanza 0.6em -> 9px a font-size 15. 71*9=639px y el panel deja 643 desde x=520.
LINE_CHARS = 71

# ------------------------------------------------------------------- layout --
X_INFO, Y_INFO0, LINE_STEP = 520, 42, 22
REVEAL_W = 690


def photo_data_uri():
    """Foto -> data URI JPEG. Aplana el alfa circular sobre el gris de la pared."""
    im = Image.open(HERE / PHOTO)
    if im.mode == "RGBA":
        flat = Image.new("RGB", im.size, WALL)
        flat.paste(im, mask=im.getchannel("A"))
        im = flat
    else:
        im = im.convert("RGB")
    side = min(im.size)
    left, top = (im.width - side) // 2, (im.height - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize((PHOTO_PX, PHOTO_PX), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=PHOTO_Q, optimize=True, progressive=True)
    raw = buf.getvalue()
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode("ascii"), len(raw)


def dots(key, value):
    return "." * max(3, LINE_CHARS - 2 - len(key) - 2 - 1 - len(value))


def info_lines():
    out = [("head", HEADER)]
    out += [("kv", kv) if kv else ("blank", None) for kv in INFO]
    out.append(("accent", "- Contact"))
    out += [("kv", kv) if kv else ("blank", None) for kv in CONTACT]
    out.append(("accent", "- Live Stats"))
    out.append(("note", FOOTER_NOTE))
    return out


def build_info(lines, textfill):
    clips, texts = [], []
    rule = " -" + "—" * 44 + "-—-"
    for i, (kind, payload) in enumerate(lines):
        y = Y_INFO0 + i * LINE_STEP
        clips.append(
            f'<clipPath id="lc{i}"><rect x="{X_INFO - 20}" y="{y - 16:.2f}" width="0" height="24">'
            f'<animate attributeName="width" from="0" to="{REVEAL_W}" dur="0.38s" '
            f'begin="{0.75 + i * 0.115:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        if kind in ("head", "accent"):
            body = (f'<tspan x="{X_INFO}" y="{y}" class="{kind}">{escape(payload)}</tspan>'
                    f'<tspan class="cc">{rule}</tspan>')
        elif kind == "blank":
            body = f'<tspan x="{X_INFO}" y="{y}" class="cc">. </tspan>'
        elif kind == "note":
            body = (f'<tspan x="{X_INFO}" y="{y}" class="cc">. </tspan>'
                    f'<tspan class="value">{escape(payload)} ↓</tspan>')
        else:
            key, value = payload
            head, _, tail = key.partition(".")
            keyspans = f'<tspan class="key">{escape(head)}</tspan>'
            for part in (tail.split(".") if tail else []):
                keyspans += f'<tspan class="cc">.</tspan><tspan class="key">{escape(part)}</tspan>'
            body = (f'<tspan x="{X_INFO}" y="{y}" class="cc">. </tspan>{keyspans}'
                    f'<tspan class="cc">: {dots(key, value)} </tspan>'
                    f'<tspan class="value">{escape(value)}</tspan>')
        texts.append(f'<g clip-path="url(#lc{i})"><text x="{X_INFO}" y="0" fill="{textfill}">{body}</text></g>')
    return "\n".join(clips), "\n  ".join(texts)


DARK = dict(
    a1="#22D3EE", a2="#7C3AED", a3="#38BDF8", accent="#10B981",
    bg1="#0B1120", bg2="#050816", panel="#0B1120", panel_op="0.35", bar_op="0.85",
    scan="#22D3EE", scan_mid="#A5F3FC", lines="#7DD3FC", lines_op="0.05",
    key="#22D3EE", value="#E5E7EB", cc="#475569", head="#7C3AED",
    title="#38BDF8", title_op="0.7", label="#64748B", alert="#F87171",
    dot1="#EF4444", dot2="#F59E0B", dot3="#10B981", textfill="#dbeafe",
    photo_op="0.92",
)
LIGHT = dict(
    a1="#4F46E5", a2="#7C3AED", a3="#0EA5E9", accent="#059669",
    bg1="#F8FAFC", bg2="#E2E8F0", panel="#FFFFFF", panel_op="0.55", bar_op="0.9",
    scan="#0EA5E9", scan_mid="#38BDF8", lines="#334155", lines_op="0.035",
    key="#0284C7", value="#1E293B", cc="#94A3B8", head="#7C3AED",
    title="#0284C7", title_op="0.75", label="#64748B", alert="#DC2626",
    dot1="#F87171", dot2="#FBBF24", dot3="#34D399", textfill="#1E293B",
    photo_op="1",
)


def build_svg(t, uri, clips, texts, n_lines):
    panel_h = Y_INFO0 + n_lines * LINE_STEP + 10
    height = 38 + panel_h + 20          # 38 = barra de titulo, 20 = margen inferior
    lp_h = panel_h - 42                  # alto del panel izquierdo
    cx, cy = 258, 26 + lp_h / 2          # centro del retrato
    r = min(488, lp_h) / 2 - 42
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="{height}" viewBox="0 0 1180 {height}">
<defs>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{t['a2']}"/>
    <stop offset="50%" stop-color="{t['a1']}"/>
    <stop offset="100%" stop-color="{t['accent']}"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">
    <stop offset="0%" stop-color="{t['bg1']}"/>
    <stop offset="100%" stop-color="{t['bg2']}"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{t['scan']}" stop-opacity="0"/>
    <stop offset="45%" stop-color="{t['scan']}" stop-opacity="0.05"/>
    <stop offset="50%" stop-color="{t['scan_mid']}" stop-opacity="0.65"/>
    <stop offset="55%" stop-color="{t['scan']}" stop-opacity="0.05"/>
    <stop offset="100%" stop-color="{t['a2']}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{t['lines']}" opacity="{t['lines_op']}"/>
  </pattern>
  <clipPath id="portraitClip"><circle cx="{cx}" cy="{cy:.1f}" r="{r:.1f}"/></clipPath>
  <mask id="revealMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1180" height="{height}">
    <rect x="0" y="0" width="1180" height="0" fill="#fff">
      <animate attributeName="height" from="0" to="{height}" dur="2.6s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
    </rect>
  </mask>
{clips}
  <style>
    .key    {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {t['key']}; font-weight: bold; }}
    .value  {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {t['value']}; }}
    .cc     {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {t['cc']}; }}
    .head   {{ font-family: 'Courier New', Consolas, monospace; font-size: 17px; fill: {t['head']}; font-weight: bold; }}
    .accent {{ font-family: 'Courier New', Consolas, monospace; font-size: 15px; fill: {t['accent']}; font-weight: bold; }}
    text, tspan {{ white-space: pre; }}
    .term-label  {{ font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: {t['label']}; letter-spacing: 0.5px; }}
    .scan-label  {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: {t['alert']}; letter-spacing: 1px; }}
    .panel-title {{ font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: {t['title']}; letter-spacing: 2px; opacity: {t['title_op']}; }}
    .cursor-blink {{ fill: {t['a1']}; }}
  </style>
</defs>

<rect width="1180" height="{height}" rx="18" fill="url(#bgGlow)"/>
<rect width="1180" height="{height}" rx="18" fill="url(#scanlines)"/>

<g id="titlebar">
  <rect x="3" y="3" width="1174" height="34" rx="16" fill="{t['panel']}" fill-opacity="{t['bar_op']}"/>
  <circle cx="24" cy="20" r="5" fill="{t['dot1']}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="42" cy="20" r="5" fill="{t['dot2']}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.3s" repeatCount="indefinite"/></circle>
  <circle cx="60" cy="20" r="5" fill="{t['dot3']}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.6s" repeatCount="indefinite"/></circle>
  <text x="590" y="25" text-anchor="middle" class="term-label">{escape(PROMPT)}</text>
  <circle cx="1095" cy="20" r="4" fill="{t['alert']}">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.1s" repeatCount="indefinite"/>
  </circle>
  <text x="1105" y="24" class="scan-label">SCANNING</text>
</g>

<g transform="translate(0,38)">
  <rect x="14" y="26" width="488" height="{lp_h}" rx="14" fill="{t['panel']}" fill-opacity="{t['panel_op']}" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>
  <rect x="508" y="10" width="655" height="{panel_h - 10}" rx="14" fill="{t['panel']}" fill-opacity="{t['panel_op']}" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>
  <text x="30" y="24" class="panel-title">VISUAL.ID</text>
  <text x="524" y="24" class="panel-title">SYSTEM.INFO</text>

  <g mask="url(#revealMask)">
    <image href="{uri}" x="{cx - r:.1f}" y="{cy - r:.1f}" width="{2 * r:.1f}" height="{2 * r:.1f}"
           clip-path="url(#portraitClip)" opacity="{t['photo_op']}" preserveAspectRatio="xMidYMid slice"/>
    <circle cx="{cx}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.9"/>
    <circle cx="{cx}" cy="{cy:.1f}" r="{r + 12:.1f}" fill="none" stroke="url(#borderGrad)" stroke-width="1"
            stroke-dasharray="6 10" opacity="0.5">
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy:.1f}" to="360 {cx} {cy:.1f}"
                        dur="34s" repeatCount="indefinite"/>
    </circle>
  </g>

  {texts}

  <rect x="522" y="{Y_INFO0 + (n_lines - 1) * LINE_STEP - 15}" width="9" height="16" class="cursor-blink" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1" dur="1.4s" begin="{0.75 + n_lines * 0.115:.2f}s" repeatCount="indefinite"/>
  </rect>
</g>

<rect x="0" y="-70" width="1180" height="70" fill="url(#scanGrad)" opacity="0.7" style="mix-blend-mode:screen">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 {height + 70}" dur="4.2s" repeatCount="indefinite"/>
</rect>

<rect x="3" y="3" width="1174" height="{height - 6}" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.8">
  <animate attributeName="opacity" values="0.5;0.95;0.5" dur="3.2s" repeatCount="indefinite"/>
</rect>
</svg>
'''


def main():
    uri, jpeg_bytes = photo_data_uri()
    lines = info_lines()
    for name, theme in (("dark.svg", DARK), ("light.svg", LIGHT)):
        clips, texts = build_info(lines, theme["textfill"])
        (HERE / name).write_text(build_svg(theme, uri, clips, texts, len(lines)), encoding="utf-8")
        print(f"{name}: {(HERE / name).stat().st_size / 1024:.0f} KB")
    print(f"jpeg embebido: {jpeg_bytes / 1024:.0f} KB ({PHOTO_PX}px q{PHOTO_Q})")

    # check: toda linea key/value ocupa exactamente LINE_CHARS caracteres
    for kv in INFO + CONTACT:
        if kv:
            k, v = kv
            assert 2 + len(k) + 2 + len(dots(k, v)) + 1 + len(v) == LINE_CHARS, f"linea desalineada: {k}"
    # check: la foto entro de verdad y no desbordo un peso razonable
    assert uri.startswith("data:image/jpeg;base64,") and jpeg_bytes > 5000, "foto no embebida"
    assert jpeg_bytes < 200_000, f"jpeg demasiado pesado: {jpeg_bytes}"
    print("checks ok")


if __name__ == "__main__":
    main()
