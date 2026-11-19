import os
from PIL import Image, ImageDraw, ImageFont

banner_w, banner_h = 1500, 500
img = Image.new('RGB', (banner_w, banner_h), color='#0B0F19')
draw = ImageDraw.Draw(img)

# Arka plan geometrik ızgara
for i in range(0, banner_w, 40):
    draw.line([(i, 0), (i, banner_h)], fill='#101726', width=1)
for j in range(0, banner_h, 40):
    draw.line([(0, j), (banner_w, j)], fill='#101726', width=1)

# Üst ve alt neon bordürler
draw.line([(0, 495), (banner_w, 495)], fill='#00E5FF', width=5)
draw.line([(0, 490), (banner_w, 490)], fill='#0077B6', width=2)
draw.line([(0, 5), (banner_w, 5)], fill='#00E5FF', width=3)

# Sol tarafta logo/monogram dairesi
poly_center_x, poly_center_y = 220, 250
draw.ellipse([poly_center_x-120, poly_center_y-120, poly_center_x+120, poly_center_y+120], outline='#00E5FF', width=3)
draw.ellipse([poly_center_x-95, poly_center_y-95, poly_center_x+95, poly_center_y+95], outline='#0077B6', width=2)

# Sağ tarafta yükselen yeşil/turkuaz borsa trend çizgisi
points = [(950, 400), (1050, 360), (1150, 380), (1250, 280), (1350, 220), (1450, 140)]
for p in range(len(points)-1):
    draw.line([points[p], points[p+1]], fill='#00E5FF', width=4)
    draw.ellipse([points[p][0]-5, points[p][1]-5, points[p][0]+5, points[p][1]+5], fill='#00FF88')
draw.ellipse([points[-1][0]-8, points[-1][1]-8, points[-1][0]+8, points[-1][1]+8], fill='#00FF88', outline='#FFFFFF', width=2)

# Yazı tipleri
try:
    font_title = ImageFont.truetype('arialbd.ttf', 54)
    font_sub = ImageFont.truetype('arial.ttf', 26)
    font_badge = ImageFont.truetype('arialbd.ttf', 20)
    font_quote = ImageFont.truetype('ariali.ttf', 24)
    font_mono = ImageFont.truetype('arialbd.ttf', 48)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_badge = ImageFont.load_default()
    font_quote = ImageFont.load_default()
    font_mono = ImageFont.load_default()

# Sol rozet içine E YZ yazısı
draw.text((poly_center_x-55, poly_center_y-30), 'E YZ', fill='#00E5FF', font=font_mono)

# Başlık ve Alt Başlık
draw.text((420, 125), 'ERTUGRUL YZ', fill='#FFFFFF', font=font_title)
draw.text((420, 195), 'BORSA & PIYASA ANALIZLERI | DIJITAL TICARET', fill='#00E5FF', font=font_sub)

# 3 Adet kurumsal rozet
badges = ['[+] Seviyesi Tutan Hisseler', '[+] Disiplinli Risk Yonetimi', '[+] Makro Piyasa Pusulasi']
bx = 420
for b in badges:
    draw.rounded_rectangle([bx, 265, bx+290, 315], radius=6, fill='#162035', outline='#0077B6', width=1)
    draw.text((bx+15, 278), b, fill='#E0F2FE', font=font_badge)
    bx += 310

# Slogan
draw.text((420, 360), '\"Disiplin kazandirir, plana sadik kal.\"', fill='#94A3B8', font=font_quote)

out_dir = r'C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-finans-analisti\assets'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'x_banner_ertugrul_yz.png')
img.save(out_path, quality=95)
print('SUCCESS:', out_path)
