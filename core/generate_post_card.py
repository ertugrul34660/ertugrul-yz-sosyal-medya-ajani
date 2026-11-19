# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Profesyonel X Finans Görseli Üretim Motoru (Dolar İşaretsiz Standart)
Yönetim Kurulu Başkanı Kuralı: Dolar ($) işareti gerekmedikçe kullanılmaz.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
OUTPUT_DIR = os.path.join(ROOT_DIR, "assets", "post_cards")
LOGO_PATH = os.path.join(ASSETS_DIR, "Ertugrul_YZ_Logo.png")

def get_font(size=24, bold=False):
    font_paths = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def create_stock_card(symbol, status_badge, entry_price, target_price, gain_text, summary_text, output_filename, is_pending=False):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    width, height = 1200, 675
    
    img = Image.new("RGB", (width, height), color=(11, 15, 25))
    draw = ImageDraw.Draw(img)

    for y in range(0, height, 45):
        draw.line([(0, y), (width, y)], fill=(18, 25, 42), width=1)
    for x in range(0, width, 60):
        draw.line([(x, 0), (x, height)], fill=(18, 25, 42), width=1)

    margin_x, margin_y = 60, 50
    card_w, card_h = width - 2 * margin_x, height - 2 * margin_y
    draw.rounded_rectangle(
        [(margin_x, margin_y), (margin_x + card_w, margin_y + card_h)],
        radius=20,
        fill=(19, 27, 46),
        outline=(0, 229, 255),
        width=2
    )

    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo = logo.resize((64, 64), Image.Resampling.LANCZOS)
            img.paste(logo, (margin_x + 35, margin_y + 35), mask=logo)
        except Exception:
            pass

    font_brand = get_font(28, bold=True)
    draw.text((margin_x + 115, margin_y + 38), "ERTUĞRUL YZ", fill=(0, 229, 255), font=font_brand)
    
    font_sub = get_font(16, bold=False)
    draw.text((margin_x + 115, margin_y + 74), "Borsa, Finans & Piyasa Analiz Karargahı", fill=(148, 163, 184), font=font_sub)

    font_badge = get_font(17, bold=True)
    badge_bg_color = (245, 158, 11) if is_pending else (16, 185, 129)
    badge_w, badge_h = 240, 44
    badge_x = margin_x + card_w - badge_w - 35
    badge_y = margin_y + 45
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)], radius=10, fill=badge_bg_color, outline=badge_bg_color)
    draw.text((badge_x + 20, badge_y + 10), status_badge, fill=(11, 15, 25), font=font_badge)

    # Hisse Sembolü (Dolar işaretsiz)
    font_symbol = get_font(64, bold=True)
    draw.text((margin_x + 40, margin_y + 140), symbol, fill=(248, 250, 252), font=font_symbol)

    stats_y = margin_y + 240
    col_w = (card_w - 100) // 3
    
    b1_x = margin_x + 40
    draw.rounded_rectangle([(b1_x, stats_y), (b1_x + col_w - 15, stats_y + 110)], radius=12, fill=(26, 36, 59), outline=(30, 41, 59), width=1)
    draw.text((b1_x + 20, stats_y + 18), "Giriş / Seviye", fill=(148, 163, 184), font=get_font(16))
    draw.text((b1_x + 20, stats_y + 50), entry_price, fill=(248, 250, 252), font=get_font(30, bold=True))

    b2_x = b1_x + col_w
    draw.rounded_rectangle([(b2_x, stats_y), (b2_x + col_w - 15, stats_y + 110)], radius=12, fill=(26, 36, 59), outline=(0, 229, 255), width=1)
    draw.text((b2_x + 20, stats_y + 18), "Hedef Direnç", fill=(0, 229, 255), font=get_font(16))
    draw.text((b2_x + 20, stats_y + 50), target_price, fill=(0, 229, 255), font=get_font(30, bold=True))

    b3_x = b2_x + col_w
    highlight_color = (245, 158, 11) if is_pending else (16, 185, 129)
    draw.rounded_rectangle([(b3_x, stats_y), (b3_x + col_w - 15, stats_y + 110)], radius=12, fill=(26, 36, 59), outline=highlight_color, width=2)
    draw.text((b3_x + 20, stats_y + 18), "Net Kazanç / Prim" if not is_pending else "Potansiyel Getiri", fill=highlight_color, font=get_font(16))
    draw.text((b3_x + 20, stats_y + 50), gain_text, fill=highlight_color, font=get_font(30, bold=True))

    font_summary = get_font(20, bold=False)
    draw.text((margin_x + 40, stats_y + 140), "📌 Analiz ve Strateji Özeti:", fill=(0, 229, 255), font=get_font(20, bold=True))
    draw.text((margin_x + 40, stats_y + 175), summary_text, fill=(203, 213, 225), font=font_summary)

    font_footer = get_font(15, bold=False)
    draw.text((margin_x + 40, margin_y + card_h - 35), "⚡ Şeffaf, kayıtlı ve kanıtlı tespitler • Takipte kalın, planla kazanın", fill=(100, 116, 139), font=font_footer)

    out_path = os.path.join(OUTPUT_DIR, output_filename)
    img.save(out_path, quality=95)
    return out_path

def generate_all_cards():
    cards = [
        {
            "symbol": "THYAO (Türk Hava Yolları)",
            "status_badge": "HEDEF VURULDU 🎯",
            "entry_price": "284.50 TL",
            "target_price": "308.00 TL",
            "gain_text": "+%9.03 KÂR",
            "summary_text": "285 TL destek bölgesinden gelen kurumsal hacimle 308 TL direnci aşıldı.",
            "output_filename": "THYAO_Analiz_Karti.png",
            "is_pending": False
        },
        {
            "symbol": "ASELSAN (ASELS)",
            "status_badge": "HEDEF VURULDU 🎯",
            "entry_price": "61.20 TL",
            "target_price": "66.50 TL",
            "gain_text": "+%9.64 KÂR",
            "summary_text": "Düşen kanal kırılımı teyit edildi ve yeni savunma sözleşmeleriyle 67 TL görüldü.",
            "output_filename": "ASELS_Analiz_Karti.png",
            "is_pending": False
        },
        {
            "symbol": "TÜPRAŞ (TUPRS)",
            "status_badge": "HEDEF VURULDU 🎯",
            "entry_price": "142.00 TL",
            "target_price": "153.00 TL",
            "gain_text": "+%8.73 KÂR",
            "summary_text": "142 TL dip seviyesinden gelen güçlü tepkiyle 153 TL direnci eksiksiz tamamlandı.",
            "output_filename": "TUPRS_Analiz_Karti.png",
            "is_pending": False
        },
        {
            "symbol": "EREĞLİ (EREGL)",
            "status_badge": "YENİ TESPİT 🔍",
            "entry_price": "27.80 TL",
            "target_price": "30.50 TL",
            "gain_text": "+%9.71 HEDEF",
            "summary_text": "27.50 TL taban desteği güçlü savunuluyor; dipten dönüş kokusu alıyoruz.",
            "output_filename": "EREGL_Analiz_Karti.png",
            "is_pending": True
        },
        {
            "symbol": "KOÇ HOLDİNG (KCHOL)",
            "status_badge": "HEDEF VURULDU 🎯",
            "entry_price": "178.00 TL",
            "target_price": "200.00 TL",
            "gain_text": "+%12.64 KÂR",
            "summary_text": "İskontolu seviyelerden gelen alımlarla 200 TL psikolojik baraj aşıldı.",
            "output_filename": "KCHOL_Analiz_Karti.png",
            "is_pending": False
        }
    ]

    generated = []
    for c in cards:
        path = create_stock_card(
            symbol=c["symbol"],
            status_badge=c["status_badge"],
            entry_price=c["entry_price"],
            target_price=c["target_price"],
            gain_text=c["gain_text"],
            summary_text=c["summary_text"],
            output_filename=c["output_filename"],
            is_pending=c["is_pending"]
        )
        generated.append(path)
    return generated

if __name__ == "__main__":
    generate_all_cards()
    print("Dolar işaretsiz tüm kartlar başarıyla güncellendi.")
