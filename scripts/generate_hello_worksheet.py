#!/usr/bin/env python3
"""Build the two-page A4 Hello! Meet Me reinforcement worksheet."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "worksheets" / "tema-01-znakomstvo.pdf"
ASSETS = ROOT / "assets" / "topics" / "hello"
W, H = A4
MM = 72 / 25.4
M = 14 * MM
IMAGE_CACHE = {}


def image(path):
    key = str(path)
    if key not in IMAGE_CACHE:
        IMAGE_CACHE[key] = ImageReader(key)
    return IMAGE_CACHE[key]


def register_fonts():
    pdfmetrics.registerFont(TTFont("Lemma", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("LemmaBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


def text(c, x, y, value, size=10, bold=False, color=colors.HexColor("#211A3B")):
    c.setFillColor(color)
    c.setFont("LemmaBold" if bold else "Lemma", size)
    c.drawString(x, y, value)


def para(c, x, y, width, value, size=9, leading=12, align=0):
    style = ParagraphStyle(
        "p", fontName="Lemma", fontSize=size, leading=leading,
        textColor=colors.HexColor("#332B45"), alignment=align,
    )
    p = Paragraph(value, style)
    _, height = p.wrap(width, 200)
    p.drawOn(c, x, y - height)
    return height


def header(c, page):
    text(c, M, H - M, "LEMMA · HELLO! MEET ME", 15, True)
    text(c, W - M - 52, H - M, f"{page} / 2", 9, True, colors.HexColor("#5B45C7"))
    c.setStrokeColor(colors.HexColor("#7661D7"))
    c.setLineWidth(1.2)
    c.line(M, H - M - 8, W - M, H - M - 8)


def image_box(c, path, x, y, w, h, label=None):
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#BDB6C9"))
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    pad = 3
    c.drawImage(image(path), x + pad, y + pad + (10 if label else 0),
                w - 2 * pad, h - 2 * pad - (10 if label else 0), preserveAspectRatio=True,
                anchor="c", mask="auto")
    if label:
        c.setFont("Lemma", 7.5)
        c.setFillColor(colors.HexColor("#4C4559"))
        c.drawCentredString(x + w / 2, y + 4, label)


def phrase_box(c, x, y, w, h, value):
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#8E879B"))
    c.roundRect(x, y, w, h, 7, fill=1, stroke=1)
    c.setFont("LemmaBold", 11)
    c.setFillColor(colors.HexColor("#211A3B"))
    c.drawCentredString(x + w / 2, y + h / 2 - 4, value)


def portrait(c, cx, cy, radius, who, badge=True):
    """Draw the accepted Ben/Mia characters as stable speaker markers."""
    source = ASSETS / "hello-name-v1.webp"
    focus = {
        "Ben": (0.255, 0.795),
        "Mia": (0.745, 0.795),
    }[who]
    draw_w = radius * 4.25
    draw_h = draw_w / 1.5
    c.saveState()
    clip = c.beginPath()
    clip.circle(cx, cy, radius)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(
        image(source),
        cx - focus[0] * draw_w,
        cy - focus[1] * draw_h,
        draw_w,
        draw_h,
        preserveAspectRatio=False,
        mask="auto",
    )
    c.restoreState()
    stroke = colors.HexColor("#7566C8") if who == "Ben" else colors.HexColor("#C77E6E")
    c.setStrokeColor(stroke)
    c.setLineWidth(1.4)
    c.circle(cx, cy, radius, fill=0, stroke=1)
    if badge:
        letter = "A" if who == "Ben" else "B"
        bx, by, br = cx - radius * .72, cy - radius * .72, radius * .34
        c.setFillColor(stroke)
        c.circle(bx, by, br, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("LemmaBold", max(5.5, radius * .47))
        c.drawCentredString(bx, by - radius * .16, letter)


def page_one(c):
    header(c, 1)
    y = H - M - 34
    text(c, M, y, "1. Match · Соедини реплики с ситуациями", 12, True)
    y -= 16
    para(c, M, y, W - 2 * M, "Проведи шесть линий карандашом. Несколько реплик могут подходить к одной картинке.", 8.5)

    scene_w, scene_h, scene_gap = 52 * MM, 25 * MM, 7 * MM
    scene_y = y - 24 - scene_h
    scenes = [
        ("hello-greeting-v1.webp", "Сцена 1"),
        ("hello-morning-arrival-worksheet-v1.webp", "Сцена 2"),
        ("hello-goodbye-v1.webp", "Сцена 3"),
    ]
    for i, (src, label) in enumerate(scenes):
        x = M + i * (scene_w + scene_gap)
        image_box(c, ASSETS / src, x, scene_y, scene_w, scene_h, label)
        c.setFillColor(colors.HexColor("#6D6679"))
        c.circle(x + scene_w / 2, scene_y - 5, 2.2, fill=1, stroke=0)

    phrases = ["Bye!", "Hello!", "Good morning!", "See you!", "Hi!", "Goodbye!"]
    phrase_w, phrase_h, phrase_gap = 52 * MM, 11 * MM, 7 * MM
    phrase_top = scene_y - 12 * MM
    for i, value in enumerate(phrases):
        col, row = i % 3, i // 3
        x = M + col * (phrase_w + phrase_gap)
        py = phrase_top - row * (phrase_h + 4 * MM) - phrase_h
        phrase_box(c, x, py, phrase_w, phrase_h, value)
        c.setFillColor(colors.HexColor("#6D6679"))
        c.circle(x + phrase_w / 2, py + phrase_h + 5, 2.2, fill=1, stroke=0)

    y2 = phrase_top - 2 * (phrase_h + 4 * MM) - 10 * MM
    text(c, M, y2, "2. Find and circle · Найди и обведи", 12, True)
    y2 -= 15
    para(c, M, y2, W - 2 * M, "В каждом ряду обведи одну подходящую картинку. Круг должен полностью поместиться вокруг карточки.", 8.5)
    rows = [
        ("Где герои встретились?", ["hello-goodbye-v1.webp", "hello-greeting-v1.webp", "hello-name-v1.webp"]),
        ("Где герои прощаются?", ["hello-morning-v1.webp", "hello-name-v1.webp", "hello-goodbye-v1.webp"]),
        ("Где сейчас утро?", ["hello-name-v1.webp", "hello-morning-arrival-worksheet-v1.webp", "hello-how-are-you-v1.webp"]),
    ]
    card_w, card_h = 48 * MM, 18 * MM
    for r, (prompt, pics) in enumerate(rows):
        row_top = y2 - 40 - card_h - r * (card_h + 9 * MM)
        text(c, M, row_top + card_h + 5, prompt, 8.5, True)
        for j, pic in enumerate(pics):
            image_box(c, ASSETS / pic, M + j * (card_w + 4 * MM), row_top, card_w, card_h)
    c.showPage()


def page_two(c):
    header(c, 2)
    y = H - M - 34
    text(c, M, y, "3. Dialogue puzzle · Собери знакомство", 12, True)
    y -= 16
    para(c, M, y, W - 2 * M, "Проведи линии от A или B к готовым карточкам. Можно вырезать карточки по пунктиру и наклеить рядом с нужным героем.", 8.5)
    cast_y = y - 58
    for i, (name, role) in enumerate([("Ben", "спрашивает"), ("Mia", "отвечает")]):
        x = M + i * 48 * MM
        portrait(c, x + 10 * MM, cast_y, 9 * MM, name)
        letter = "A" if name == "Ben" else "B"
        text(c, x + 22 * MM, cast_y + 5, f"{letter} · {name}", 9, True)
        text(c, x + 22 * MM, cast_y - 9, role, 7.5, False, colors.HexColor("#6A6276"))
    cards = ["Nice to meet you.", "Hello!", "I'm Mia.", "What's your name?"]
    card_w, card_h = 72 * MM, 14 * MM
    card_x = W - M - card_w
    top = cast_y - 3 * MM
    c.setDash(3, 2)
    for i, phrase in enumerate(cards):
        cy = top - i * (card_h + 4 * MM)
        c.setFillColor(colors.white); c.setStrokeColor(colors.HexColor("#77707F"))
        c.roundRect(card_x, cy, card_w, card_h, 6, fill=1, stroke=1)
        c.setFont("LemmaBold", 10); c.setFillColor(colors.HexColor("#211A3B")); c.drawCentredString(card_x + card_w / 2, cy + card_h / 2 - 4, phrase)
    c.setDash()
    text(c, M, cast_y - 35 * MM, "Линии или вырезание — выбери один способ.", 8, False, colors.HexColor("#6A6276"))

    # Keep task 4 below the full four-card dialogue stack.  The previous
    # offset started the heading beside the last cut-out card on A4.
    y2 = cast_y - 96 * MM
    text(c, M, y2, "4. Put in order · Расставь по порядку", 12, True)
    y2 -= 16
    para(c, M, y2, W - 2 * M, "Карточки перемешаны. Впиши в большие квадраты только цифры 1–4. Английские реплики переписывать не нужно.", 8.5)
    order_cards = [
        ("Mia", "I'm Mia."),
        ("Ben", "Hello!"),
        ("Ben", "Nice to meet you."),
        ("Ben", "What's your name?"),
    ]
    cw, ch = 78 * MM, 35 * MM
    for i, (speaker, phrase) in enumerate(order_cards):
        col, row = i % 2, i // 2
        x, yy = M + col * (cw + 6 * MM), y2 - 22 - row * (ch + 5 * MM) - ch
        c.setStrokeColor(colors.HexColor("#AAA3B5")); c.roundRect(x, yy, cw, ch, 7, fill=0, stroke=1)
        c.rect(x + 4 * MM, yy + ch - 12 * MM, 8 * MM, 8 * MM, fill=0, stroke=1)
        portrait(c, x + 24 * MM, yy + ch / 2 + 2 * MM, 7 * MM, speaker)
        letter = "A" if speaker == "Ben" else "B"
        text(c, x + 18 * MM, yy + 4 * MM, f"{letter} · {speaker}", 7.2, True,
             colors.HexColor("#5C4D9E") if speaker == "Ben" else colors.HexColor("#A85E52"))
        c.setFont("LemmaBold", 9); c.setFillColor(colors.HexColor("#211A3B")); c.drawString(x + 36 * MM, yy + ch / 2 - 3, phrase)

    bottom = 18 * MM
    c.setStrokeColor(colors.HexColor("#827A8F")); c.roundRect(M, bottom, W - 2 * M, 24 * MM, 7, fill=0, stroke=1)
    text(c, M + 5 * MM, bottom + 16 * MM, "Моя карточка имени · необязательно", 9, True)
    text(c, M + 5 * MM, bottom + 8 * MM, "Нарисуй себя или укрась карточку. Взрослый может вписать имя.", 8)
    c.showPage()


def main():
    register_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
    c.setTitle("LEMMA · Hello! Meet Me · Worksheet")
    c.setAuthor("LEMMA")
    page_one(c)
    page_two(c)
    c.save()


if __name__ == "__main__":
    main()
