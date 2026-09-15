from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 800, 500

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, v))

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def gradient_bg(draw, colors, w=W, h=H, horizontal=False):
    c1, c2 = hex2rgb(colors[0]), hex2rgb(colors[1])
    for i in range(h if not horizontal else w):
        t = i / (h if not horizontal else w)
        r = int(c1[0] + (c2[0]-c1[0])*t)
        g = int(c1[1] + (c2[1]-c1[1])*t)
        b = int(c1[2] + (c2[2]-c1[2])*t)
        if horizontal:
            draw.line([(i,0),(i,h)], fill=(r,g,b))
        else:
            draw.line([(0,i),(w,i)], fill=(r,g,b))

def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def load_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size)
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)
    except:
        return ImageFont.load_default()

def text_center(draw, text, y, font, fill, width=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, y), text, font=font, fill=fill)

def draw_status_bar(draw, title, subtitle, badge_color, badge_text):
    rounded_rect(draw, [20, 20, W-20, 80], 10, fill=(255,255,255,25))
    f_title = load_font(18, bold=True)
    f_sub = load_font(13)
    draw.text((40, 28), title, font=f_title, fill=(255,255,255))
    draw.text((40, 52), subtitle, font=f_sub, fill=(200,200,220))
    # badge
    badge_c = hex2rgb(badge_color)
    rounded_rect(draw, [W-160, 28, W-30, 58], 15, fill=badge_c)
    f_badge = load_font(13, bold=True)
    bbox = draw.textbbox((0,0), badge_text, font=f_badge)
    bw = bbox[2]-bbox[0]
    bx = W-160 + (130-bw)//2
    draw.text((bx, 35), badge_text, font=f_badge, fill=(255,255,255))

def checklist_row(draw, x, y, label, status, w_box=380):
    color = '#10b981' if status == 'OK' else '#ef4444'
    icon = '✓' if status == 'OK' else '✗'
    rounded_rect(draw, [x, y, x+w_box, y+38], 8, fill=(255,255,255,18))
    c = hex2rgb(color)
    rounded_rect(draw, [x+8, y+7, x+30, y+31], 5, fill=c)
    f = load_font(15, bold=True)
    draw.text((x+13, y+10), icon, font=f, fill=(255,255,255))
    f2 = load_font(14)
    draw.text((x+40, y+12), label, font=f2, fill=(230,230,255))
    f3 = load_font(13, bold=True)
    draw.text((x+w_box-55, y+12), status, font=f3, fill=hex2rgb(color))

# ─────────────────────────────────────────
# SMARTRAIL MODULE 2 — already generated, skip
# But let's re-generate all 4 cleanly

def make_smartrail_m1():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#0f0c29','#302b63'])
    draw_status_bar(draw, '🚂 SmartRailShield — Pre-Departure Inspection', 'Train ID: TN-EXP-2024 | Platform 3', '#f59e0b', '⚠ 1 FAULT')
    f_head = load_font(20, bold=True)
    text_center(draw, 'Mechanical Component Health Check', 105, f_head, (200,200,255))
    items = [
        ('Brake Cylinder Pressure',   'OK'),
        ('Coupler & Buffer Assembly',  'OK'),
        ('Bogie Suspension Springs',   'OK'),
        ('Pantograph Condition',       'OK'),
        ('Engine Oil Level',           'OK'),
        ('Brake Shoe Thickness',       'FAULT'),
        ('Wheel Flange Wear',          'OK'),
    ]
    for i, (label, status) in enumerate(items):
        col = 30 if i % 2 == 0 else W//2 + 10
        row = 135 + (i // 2) * 52
        checklist_row(draw, col, row, label, status, w_box=360)
    # alert box
    rounded_rect(draw, [20, H-90, W-20, H-20], 12, fill=(239,68,68,180))
    f_alert = load_font(17, bold=True)
    text_center(draw, '🚨 FAULT DETECTED: Brake Shoe Thickness LOW — Inspect before departure!', H-68, f_alert, (255,255,255))
    img.save('assets/images/smartrail/module1.jpg', quality=92)
    print('✅ smartrail/module1.jpg')

def make_smartrail_m2():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#0d1b2a','#1b4332'])
    draw_status_bar(draw, '🚂 SmartRailShield — Track Obstacle Detection', 'YOLOv8 Live Feed | Track Cam #2', '#ef4444', '🔴 ALERT')
    # simulate camera feed area
    rounded_rect(draw, [20, 95, W-20, H-80], 10, fill=(15,25,20))
    # draw track lines
    draw.line([(W//2-60, 100),(W//2-120, H-90)], fill=(100,100,100), width=6)
    draw.line([(W//2+60, 100),(W//2+120, H-90)], fill=(100,100,100), width=6)
    for i in range(6):
        y = 120 + i*55
        x_l = int(W//2 - 60 - i*10)
        x_r = int(W//2 + 60 + i*10)
        draw.line([(x_l, y),(x_r, y)], fill=(80,80,80), width=4)
    # detection boxes
    # Person box
    rounded_rect(draw, [260, 200, 360, 330], 4, outline=(255,80,80), width=3)
    f_lbl = load_font(13, bold=True)
    rounded_rect(draw, [260, 200, 340, 220], 3, fill=(255,80,80))
    draw.text((265, 202), 'PERSON 94%', font=f_lbl, fill=(255,255,255))
    # Animal box
    rounded_rect(draw, [400, 230, 530, 360], 4, outline=(255,200,0), width=3)
    rounded_rect(draw, [400, 230, 488, 250], 3, fill=(255,200,0))
    draw.text((404, 232), 'ANIMAL 87%', font=f_lbl, fill=(0,0,0))
    # info panel bottom
    rounded_rect(draw, [20, H-75, W-20, H-10], 10, fill=(239,68,68))
    f_warn = load_font(16, bold=True)
    text_center(draw, '⚠ EMERGENCY — Obstacle on Track! Train Stop Signal Sent!', H-60, f_warn, (255,255,255))
    f_s = load_font(13)
    text_center(draw, 'Detected: 1 Person + 1 Animal on Track | Confidence: HIGH', H-40, f_s, (255,220,220))
    img.save('assets/images/smartrail/module2.jpg', quality=92)
    print('✅ smartrail/module2.jpg')

def make_smartrail_m3():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#1a0533','#0d1f3c'])
    draw_status_bar(draw, '🚂 SmartRailShield — Gate Violation ANPR', 'Level Crossing CAM-7 | Gate: CLOSED', '#ef4444', '🚨 VIOLATION')
    # camera feed
    rounded_rect(draw, [20, 95, W-20, H-80], 10, fill=(10,10,20))
    # gate bars
    for i in range(8):
        x = 80 + i*38
        draw.rectangle([x, 95, x+14, 260], fill=(200,30,30) if i%2==0 else (255,255,255))
    # motorcycle silhouette area
    rounded_rect(draw, [200, 260, 500, 380], 6, fill=(20,20,40))
    f_cam = load_font(13)
    draw.text((210, 270), '🏍️  Two-Wheeler Detected', font=f_cam, fill=(200,200,255))
    # ANPR plate box
    rounded_rect(draw, [210, 300, 490, 350], 6, outline=(0,180,255), width=3, fill=(0,30,60))
    f_plate = load_font(28, bold=True)
    text_center(draw, 'TN 05 AB 1234', 308, f_plate, (0,220,255), width=700)
    f_sub = load_font(12)
    text_center(draw, 'ANPR OCR — EasyOCR Detected', 342, f_sub, (150,200,255), width=700)
    # email dispatch panel
    rounded_rect(draw, [20, H-75, W-20, H-10], 10, fill=(16,185,129))
    f_e = load_font(15, bold=True)
    text_center(draw, '✉ E-Fine Dispatched → owner@rto.gov.in | Fine: ₹1,500', H-60, f_e, (255,255,255))
    f_e2 = load_font(12)
    text_center(draw, 'Vehicle Owner: K. Rajan | RTO: Chennai South | Status: SENT', H-40, f_e2, (200,255,230))
    img.save('assets/images/smartrail/module3.jpg', quality=92)
    print('✅ smartrail/module3.jpg')

def make_smartrail_m4():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#0f2027','#203a43'])
    draw_status_bar(draw, '🚂 SmartRailShield — Locopilot Drowsiness Monitor', 'Cab Cam LIVE | EAR Monitoring Active', '#f59e0b', '⚠ DROWSY')
    # face area
    rounded_rect(draw, [W//2-110, 100, W//2+110, 300], 10, fill=(20,30,40))
    # simple face outline
    draw.ellipse([W//2-80, 115, W//2+80, 255], outline=(100,200,100), width=2)
    # eye landmarks (left eye)
    for pt in [(W//2-40,170),(W//2-30,165),(W//2-20,168),(W//2-30,175),(W//2-40,172)]:
        draw.ellipse([pt[0]-3, pt[1]-3, pt[0]+3, pt[1]+3], fill=(0,255,150))
    # eye landmarks (right eye)
    for pt in [(W//2+20,170),(W//2+30,165),(W//2+40,168),(W//2+30,175),(W//2+20,172)]:
        draw.ellipse([pt[0]-3, pt[1]-3, pt[0]+3, pt[1]+3], fill=(0,255,150))
    # EAR value box
    rounded_rect(draw, [W//2-150, 310, W//2+150, 365], 10, fill=(239,68,68))
    f_ear = load_font(22, bold=True)
    text_center(draw, 'EAR: 0.18  ←  DROWSY THRESHOLD: 0.25', 320, f_ear, (255,255,255))
    f_ear2 = load_font(14)
    text_center(draw, 'Eyes closing detected for 2.4 seconds', 347, f_ear2, (255,200,200))
    # stats row
    stats = [('Blink Rate', '42/min'), ('Head Tilt', '18°'), ('Alert Level', 'HIGH'), ('Duration', '2.4s')]
    for i, (k,v) in enumerate(stats):
        x = 25 + i*190
        rounded_rect(draw, [x, 375, x+175, 430], 8, fill=(255,255,255,20))
        f_k = load_font(12)
        f_v = load_font(18, bold=True)
        draw.text((x+10, 380), k, font=f_k, fill=(160,180,220))
        draw.text((x+10, 398), v, font=f_v, fill=(255,100,100) if k=='Alert Level' else (255,255,255))
    # alarm bottom
    rounded_rect(draw, [20, H-70, W-20, H-10], 10, fill=(220,38,38))
    f_alm = load_font(17, bold=True)
    text_center(draw, '🔔 ALARM TRIGGERED — Locopilot Drowsiness Detected! Speed Reducing...', H-55, f_alm, (255,255,255))
    img.save('assets/images/smartrail/module4.jpg', quality=92)
    print('✅ smartrail/module4.jpg')

# ─────────────── SMART BUS ───────────────

def make_bus_m1():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#0f2027','#1a3a4a'])
    draw_status_bar(draw, '🚌 TN Smart Bus — Passenger Live Tracker', 'Route 21C | Chennai | Login: Passenger', '#10b981', '🟢 3 Seats')
    # map area
    rounded_rect(draw, [20, 95, W-20, 340], 10, fill=(18,32,45))
    # grid lines (map)
    for i in range(8):
        draw.line([(20, 110+i*30),(W-20,110+i*30)], fill=(30,50,70), width=1)
    for i in range(12):
        draw.line([(20+i*64, 95),(20+i*64,340)], fill=(30,50,70), width=1)
    # roads
    draw.line([(20,220),(W-20,220)], fill=(50,70,100), width=8)
    draw.line([(300,95),(300,340)], fill=(50,70,100), width=8)
    # bus icon
    rounded_rect(draw, [270, 195, 330, 245], 8, fill=(99,102,241))
    f_bus = load_font(20, bold=True)
    text_center(draw, '🚌', 205, f_bus, (255,255,255), width=600)
    # crowd dot
    draw.ellipse([323, 192, 341, 210], fill=(16,185,129))
    f_dot = load_font(10, bold=True)
    draw.text((326, 196), '●', font=f_dot, fill=(255,255,255))
    # stops
    for sx, sy, name in [(150,220,'Stop A'),(440,220,'Stop B'),(300,150,'Stop C')]:
        draw.ellipse([sx-6,sy-6,sx+6,sy+6], fill=(255,180,0))
        draw.text((sx+8, sy-8), name, font=load_font(11), fill=(200,220,255))
    # bottom status
    rounded_rect(draw, [20, 350, W-20, H-10], 10, fill=(255,255,255,15))
    f_s = load_font(14, bold=True)
    draw.text((35, 360), '🟢 Seats Available', font=f_s, fill=(16,185,129))
    draw.text((220, 360), '🟡 Light Crowd', font=f_s, fill=(245,158,11))
    draw.text((380, 360), '🔴 Overcrowded', font=f_s, fill=(239,68,68))
    draw.text((35, 390), 'Bus 21C ETA: 4 mins | Passengers: 8/50', font=load_font(13), fill=(180,200,230))
    draw.text((35, 412), 'Live GPS Tracking • Last updated: just now', font=load_font(12), fill=(120,160,200))
    img.save('assets/images/smartbus/module1.jpg', quality=92)
    print('✅ smartbus/module1.jpg')

def make_bus_m2():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#1a0533','#0d2040'])
    draw_status_bar(draw, '♿ TN Smart Bus — Disabled Passenger Portal', 'UDID Login Active | Voice Mode: ON', '#8b5cf6', '🎤 VOICE ON')
    # UDID card
    rounded_rect(draw, [W//2-200, 105, W//2+200, 210], 12, fill=(50,20,90))
    rounded_rect(draw, [W//2-195, 110, W//2+195, 205], 10, outline=(139,92,246), width=2)
    f_c = load_font(13, bold=True)
    draw.text((W//2-185, 120), '♿  Government of India — UDID Card', font=f_c, fill=(200,180,255))
    draw.text((W//2-185, 142), 'ID: UDID-TN-2024-00483', font=load_font(16, bold=True), fill=(255,255,255))
    draw.text((W//2-185, 168), 'Name: Selvi R. | DOB: 12/06/1990', font=load_font(12), fill=(180,160,220))
    draw.text((W//2-185, 186), 'Type: Locomotor Disability | Status: ✓ Verified', font=load_font(12), fill=(120,255,160))
    # voice button
    draw.ellipse([W//2-55, 225, W//2+55, 315], fill=(99,60,180))
    draw.ellipse([W//2-45, 235, W//2+45, 305], fill=(139,92,246))
    f_mic = load_font(36, bold=True)
    text_center(draw, '🎤', 248, f_mic, (255,255,255))
    # waveform
    for i in range(20):
        x = W//2 - 100 + i*10
        h2 = 10 + int(20*abs(math.sin(i*0.7)))
        draw.line([(x, 330-h2),(x, 330+h2)], fill=(139,92,246), width=3)
    f_v = load_font(14, bold=True)
    text_center(draw, '"Send request to Bus 21C at Anna Nagar Stop"', 350, f_v, (200,180,255))
    # request button
    rounded_rect(draw, [W//2-150, 375, W//2+150, 420], 12, fill=(16,185,129))
    text_center(draw, '📤  Send Pickup Request', 385, load_font(17, bold=True), (255,255,255))
    f_note = load_font(12)
    text_center(draw, 'Request will be sent to driver • pyttsx3 voice confirmation enabled', 430, f_note, (160,140,200))
    img.save('assets/images/smartbus/module2.jpg', quality=92)
    print('✅ smartbus/module2.jpg')

def make_bus_m3():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#0c1a0e','#0d2040'])
    draw_status_bar(draw, '🚌 TN Smart Bus — Driver Console', 'Bus 21C | Route: Anna Nagar → Adyar', '#3b82f6', '🚦 2 Requests')
    # current location strip
    rounded_rect(draw, [20, 95, W-20, 140], 8, fill=(255,255,255,15))
    draw.text((35, 103), '📍 Current Stop: Koyambedu | Next: Anna Nagar (2.1 km) | Speed: 32 km/h', font=load_font(13), fill=(180,210,255))
    draw.text((35, 122), 'Bus Occupancy: 24/50 passengers  🟡 Light Crowd', font=load_font(13), fill=(245,158,11))
    # request cards
    requests = [
        ('Selvi R.', 'Anna Nagar Bus Stop', 'UDID: TN-00483', 'Locomotor Disability', True),
        ('Muthu K.', 'Vadapalani Stop', 'UDID: TN-00217', 'Visual Impairment', False),
    ]
    for i, (name, stop, udid, dtype, urgent) in enumerate(requests):
        y = 155 + i*135
        rounded_rect(draw, [20, y, W-20, y+120], 10, fill=(255,255,255,12))
        rounded_rect(draw, [20, y, W-20, y+120], 10, outline=(59,130,246) if not urgent else (239,68,68), width=2)
        f_n = load_font(16, bold=True)
        draw.text((38, y+12), f'♿  {name}', font=f_n, fill=(255,255,255))
        draw.text((38, y+34), f'📍 {stop}', font=load_font(13), fill=(160,200,255))
        draw.text((38, y+52), f'{udid} | {dtype}', font=load_font(12), fill=(160,160,200))
        if urgent:
            rounded_rect(draw, [W-120, y+10, W-30, y+36], 8, fill=(239,68,68))
            draw.text((W-113, y+15), 'URGENT', font=load_font(12, bold=True), fill=(255,255,255))
        rounded_rect(draw, [38, y+70, 218, y+108], 8, fill=(16,185,129))
        text_center(draw, '✅ ACCEPT', y+80, load_font(16, bold=True), (255,255,255), width=256)
        rounded_rect(draw, [240, y+70, 420, y+108], 8, fill=(239,68,68))
        text_center(draw, '❌ REJECT', y+80, load_font(16, bold=True), (255,255,255), width=660)
    img.save('assets/images/smartbus/module3.jpg', quality=92)
    print('✅ smartbus/module3.jpg')

def make_bus_m4():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#0c0c1a','#0d1f3c'])
    draw_status_bar(draw, '🛡️ TN Smart Bus — Admin Fleet Console', 'All Buses | Real-Time Fleet Monitoring', '#f59e0b', '🟢 12 Active')
    # fleet stats row
    stats = [('Total Buses','15'),('Active Routes','8'),('Passengers','342'),('Requests','7')]
    colors = ['#3b82f6','#10b981','#8b5cf6','#f59e0b']
    for i,(k,v) in enumerate(stats):
        x = 25 + i*190
        rounded_rect(draw, [x, 100, x+175, 165], 10, fill=hex2rgb(colors[i])+(40,))
        f_v = load_font(28, bold=True)
        draw.text((x+15, 107), v, font=f_v, fill=hex2rgb(colors[i]))
        draw.text((x+15, 143), k, font=load_font(12), fill=(180,180,220))
    # bus fleet table
    rounded_rect(draw, [20, 175, W-20, 200], 0, fill=(255,255,255,20))
    headers = ['Bus No.', 'Route', 'Passengers', 'Crowd Status', 'Requests']
    for i, h in enumerate(headers):
        draw.text((30+i*150, 180), h, font=load_font(13, bold=True), fill=(180,200,255))
    rows = [
        ('21C', 'Koyambedu→Adyar', '24/50', '🟡 Light', '2 Pending'),
        ('14B', 'CMBT→T.Nagar', '48/50', '🔴 Full', '0'),
        ('33A', 'Guindy→Velachery', '8/50',  '🟢 Empty', '1 Pending'),
        ('9G',  'Broadway→Sholinganallur', '36/50','🔴 Crowd','0'),
    ]
    crowd_colors = [(245,158,11),(239,68,68),(16,185,129),(239,68,68)]
    for ri, (row, cc) in enumerate(zip(rows, crowd_colors)):
        y = 205 + ri*42
        rounded_rect(draw, [20, y, W-20, y+38], 5, fill=(255,255,255, 8 if ri%2==0 else 15))
        for ci, cell in enumerate(row):
            color = cc if ci==3 else (210,210,255)
            draw.text((30+ci*150, y+10), cell, font=load_font(13), fill=color)
    f_footer = load_font(13)
    text_center(draw, '📊 Fleet Analytics | 🗺 Live GPS View | 📋 Driver Logs | ⚙ Route Management', H-30, f_footer, (140,160,200))
    img.save('assets/images/smartbus/module4.jpg', quality=92)
    print('✅ smartbus/module4.jpg')

# ─────────────── GOLD ───────────────

def make_gold_m1():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#1a1200','#2d1f00'])
    draw_status_bar(draw, '💰 Gold Rate Prediction — Historical EDA', 'Dataset: 2000–2024 | 8,760 Records', '#f59e0b', '📊 EDA')
    # gold bar graphic
    for i in range(3):
        x = 40 + i*60
        y = 130
        rounded_rect(draw, [x, y, x+50, y+80], 6, fill=(180+i*10, 140+i*5, 20))
        rounded_rect(draw, [x+5, y+5, x+45, y+75], 4, outline=(220,180,60), width=2)
        draw.text((x+8, y+30), '24K', font=load_font(13, bold=True), fill=(255,220,80))
    f_h = load_font(19, bold=True)
    draw.text((260, 140), 'Avg Gold Rate: ₹5,892/gram', font=f_h, fill=(255,210,60))
    draw.text((260, 168), 'Peak: ₹6,450 (Nov 2023)', font=load_font(14), fill=(210,170,40))
    draw.text((260, 192), 'Low:  ₹1,200 (Jan 2003)', font=load_font(14), fill=(180,140,30))
    draw.text((260, 216), 'Trend: ↑ +385% over 20 years', font=load_font(14), fill=(100,220,130))
    # bar chart
    bar_data = [1200,1800,2400,2900,3400,4100,4800,5200,5800,6200,6450,6100]
    bw = 40
    max_v = max(bar_data)
    bx0 = 30
    chart_top = 245
    chart_h = 160
    years = range(2013,2025)
    for i, v in enumerate(bar_data):
        bh = int(v/max_v * chart_h)
        x = bx0 + i*(bw+12)
        gold_c = (200+int(55*i/11), 160+int(20*i/11), 20)
        draw.rectangle([x, chart_top+chart_h-bh, x+bw, chart_top+chart_h], fill=gold_c)
        draw.text((x+5, chart_top+chart_h-bh-18), str(list(years)[i]), font=load_font(10), fill=(200,180,100))
    draw.line([(bx0, chart_top+chart_h),(bx0+len(bar_data)*(bw+12), chart_top+chart_h)], fill=(150,130,60), width=2)
    text_center(draw, 'Annual Average Gold Rate (₹/gram) — 2013 to 2024', chart_top+chart_h+12, load_font(13), (180,160,80))
    img.save('assets/images/gold/module1.jpg', quality=92)
    print('✅ gold/module1.jpg')

def make_gold_m2():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#050d1a','#0f1f3a'])
    draw_status_bar(draw, '💰 Gold Rate Prediction — Polynomial Regression', 'Scikit-learn | Degree-3 Polynomial | R²: 0.978', '#10b981', '✅ Trained')
    # axes
    ox, oy, ew, eh = 60, 400, 680, 300
    draw.line([(ox, oy-eh),(ox, oy)], fill=(100,120,180), width=2)
    draw.line([(ox, oy),(ox+ew, oy)], fill=(100,120,180), width=2)
    # axis labels
    for i in range(6):
        y = oy - int(eh*i/5)
        draw.line([(ox-5, y),(ox+5, y)], fill=(100,120,180), width=1)
        price = 1000 + i*1100
        draw.text((15, y-8), f'₹{price}', font=load_font(10), fill=(140,160,200))
    for i in range(7):
        x = ox + int(ew*i/6)
        draw.line([(x, oy),(x, oy+5)], fill=(100,120,180), width=1)
        yr = 2018+i*1
        draw.text((x-12, oy+8), str(yr), font=load_font(10), fill=(140,160,200))
    # scatter data points
    import random
    random.seed(42)
    data_pts = []
    for i in range(60):
        xi = i/59
        noise = random.uniform(-0.05, 0.05)
        yi = 0.1 + 0.8*xi**2 + 0.15*xi + noise
        yi = max(0.05, min(0.95, yi))
        data_pts.append((xi, yi))
        px = ox + int(xi*ew)
        py = oy - int(yi*eh)
        draw.ellipse([px-4,py-4,px+4,py+4], fill=(99,102,241))
    # polynomial curve
    prev = None
    for i in range(200):
        xi = i/199
        yi = 0.1 + 0.8*xi**2 + 0.15*xi
        px = ox + int(xi*ew)
        py = oy - int(yi*eh)
        if prev:
            draw.line([prev,(px,py)], fill=(245,158,11), width=3)
        prev = (px, py)
    # legend
    rounded_rect(draw, [W-200, 100, W-20, 160], 8, fill=(255,255,255,15))
    draw.ellipse([W-188,114,W-174,128], fill=(99,102,241))
    draw.text((W-168, 112), 'Actual Data', font=load_font(13), fill=(180,200,255))
    draw.line([(W-188,141),(W-174,141)], fill=(245,158,11), width=3)
    draw.text((W-168, 135), 'Fitted Curve', font=load_font(13), fill=(245,158,11))
    text_center(draw, 'Degree-3 Polynomial Regression Fit | R² Score: 0.978 | MSE: 0.0021', H-25, load_font(13), (140,170,220))
    img.save('assets/images/gold/module2.jpg', quality=92)
    print('✅ gold/module2.jpg')

def make_gold_m3():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#1a0e00','#2a1a05'])
    draw_status_bar(draw, '💰 Gold Rate Prediction — Date Picker UI', 'Streamlit Dashboard | Select Target Date', '#f59e0b', '📅 Calendar')
    # calendar widget
    rounded_rect(draw, [W//2-200, 100, W//2+200, 340], 12, fill=(30,20,5))
    rounded_rect(draw, [W//2-200, 100, W//2+200, 340], 12, outline=(245,158,11), width=2)
    # month header
    rounded_rect(draw, [W//2-200, 100, W//2+200, 135], 12, fill=(245,158,11))
    f_mh = load_font(18, bold=True)
    text_center(draw, '◀   August 2025   ▶', 108, f_mh, (0,0,0), width=800)
    # weekday headers
    days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    for i, d in enumerate(days):
        x = W//2 - 190 + i*56
        draw.text((x, 140), d, font=load_font(12, bold=True), fill=(200,160,60))
    # calendar grid
    dates = list(range(1,32))
    for i, d in enumerate(dates):
        col = i % 7
        row = i // 7
        x = W//2 - 190 + col*56
        y = 162 + row*34
        if d == 17:
            rounded_rect(draw, [x-4, y-4, x+32, y+24], 6, fill=(245,158,11))
            draw.text((x+3, y), str(d), font=load_font(15, bold=True), fill=(0,0,0))
        else:
            color = (255,80,80) if col==0 else (180,160,120)
            draw.text((x+3, y), str(d), font=load_font(14), fill=color)
    # prediction result
    rounded_rect(draw, [W//2-220, 355, W//2+220, 440], 12, fill=(50,35,5))
    rounded_rect(draw, [W//2-220, 355, W//2+220, 440], 12, outline=(245,158,11), width=2)
    f_pred = load_font(24, bold=True)
    text_center(draw, 'Selected Date: 17 August 2025', 362, load_font(14), (180,160,100))
    text_center(draw, '💰 Predicted Gold Rate: ₹ 6,287 / gram', 385, f_pred, (255,215,0))
    text_center(draw, 'Model: Polynomial Regression (Degree 3) | Confidence: 94.2%', 420, load_font(12), (160,140,80))
    img.save('assets/images/gold/module3.jpg', quality=92)
    print('✅ gold/module3.jpg')

def make_gold_m4():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#050d1a','#091020'])
    draw_status_bar(draw, '💰 Gold Rate Prediction — Plotly Dashboard', 'Interactive Financial Trend Chart | Zoomable', '#10b981', '📈 Live Chart')
    # axes
    ox, oy, ew, eh = 70, 390, 660, 260
    draw.line([(ox,oy-eh),(ox,oy)], fill=(60,80,120), width=2)
    draw.line([(ox,oy),(ox+ew,oy)], fill=(60,80,120), width=2)
    # grid lines
    for i in range(5):
        y = oy - int(eh*i/4)
        draw.line([(ox,y),(ox+ew,y)], fill=(30,50,80), width=1)
        price = 2000+i*1200
        draw.text((10,y-8), f'₹{price}', font=load_font(10), fill=(100,130,180))
    # historical line
    hist_pts = [(0,0.05),(0.1,0.08),(0.2,0.13),(0.3,0.22),(0.4,0.35),(0.5,0.48),(0.6,0.62),(0.7,0.72),(0.8,0.80),(0.85,0.85)]
    prev = None
    for xi,yi in hist_pts:
        px = ox+int(xi*ew)
        py = oy-int(yi*eh)
        if prev:
            draw.line([prev,(px,py)], fill=(245,158,11), width=3)
        draw.ellipse([px-5,py-5,px+5,py+5], fill=(245,158,11))
        prev = (px,py)
    # forecast dotted line
    prev = (ox+int(0.85*ew), oy-int(0.85*eh))
    forecast_pts = [(0.85,0.85),(0.90,0.88),(0.95,0.92),(1.0,0.96)]
    for xi,yi in forecast_pts:
        px = ox+int(xi*ew)
        py = oy-int(yi*eh)
        for j in range(0,abs(px-prev[0]),8):
            sx = prev[0]+j
            sy = int(prev[1]+(py-prev[1])*j/max(1,abs(px-prev[0])))
            draw.ellipse([sx-2,sy-2,sx+2,sy+2], fill=(16,185,129))
        prev = (px,py)
    # confidence band
    for xi in range(int(0.85*ew), ew, 2):
        yi_m = 0.85 + (xi/ew-0.85)*0.55
        py_top = oy - int((yi_m+0.05)*eh)
        py_bot = oy - int((yi_m-0.05)*eh)
        draw.line([(ox+xi,py_top),(ox+xi,py_bot)], fill=(16,185,129,40))
    # legend
    rounded_rect(draw, [W-210,100,W-20,165], 8, fill=(255,255,255,12))
    draw.line([(W-200,117),(W-178,117)], fill=(245,158,11), width=3)
    draw.text((W-172,111), 'Historical Rate', font=load_font(13), fill=(200,180,100))
    draw.line([(W-200,140),(W-178,140)], fill=(16,185,129), width=2)
    draw.text((W-172,134), 'Forecast (ML)', font=load_font(13), fill=(100,220,150))
    # x labels
    for i,yr in enumerate(['2015','2017','2019','2021','2023','2025']):
        x = ox+int(i*ew/5)
        draw.text((x-10, oy+8), yr, font=load_font(10), fill=(140,160,200))
    text_center(draw, 'Plotly Interactive Chart: Zoom • Pan • Hover for exact values • Export PNG', H-25, load_font(12), (120,150,200))
    img.save('assets/images/gold/module4.jpg', quality=92)
    print('✅ gold/module4.jpg')

# ─────────────── FLOOD ───────────────

def make_flood_m1():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#001020','#001a30'])
    draw_status_bar(draw, '🌊 AI Flood Rescue — Person Detection', 'YOLOv8 Live Feed | Rescue Cam #1', '#ef4444', '🔴 3 Detected')
    # flood scene
    rounded_rect(draw, [20, 95, W-20, H-70], 10, fill=(0,30,60))
    # water effect
    for i in range(6):
        y = 200 + i*20
        draw.line([(20,y),(W-20,y)], fill=(0,50+i*5,100+i*10), width=3)
    # detection boxes
    detections = [
        (100,140,200,280,'PERSON','94%',(255,80,80)),
        (310,160,440,300,'PERSON','89%',(255,80,80)),
        (530,180,640,310,'PERSON','78%',(255,140,0)),
    ]
    for x1,y1,x2,y2,label,conf,col in detections:
        draw.rectangle([x1,y1,x2,y2], outline=col, width=3)
        rounded_rect(draw, [x1,y1,x1+95,y1+22], 3, fill=col)
        draw.text((x1+4,y1+3), f'{label} {conf}', font=load_font(12,bold=True), fill=(255,255,255))
    # counter
    rounded_rect(draw, [W-180,100,W-25,165], 8, fill=(0,0,0,120))
    draw.text((W-170,108), 'Detected:', font=load_font(13,bold=True), fill=(200,200,255))
    draw.text((W-170,128), '3 Persons', font=load_font(18,bold=True), fill=(255,80,80))
    draw.text((W-170,152), 'SEND ALERT', font=load_font(11,bold=True), fill=(255,150,0))
    # bottom alert
    rounded_rect(draw, [20,H-65,W-20,H-10], 10, fill=(239,68,68))
    text_center(draw, '🚨 3 Stranded Persons Detected — GPS Coordinates Logged — Rescue Team Alerted!', H-52, load_font(15,bold=True), (255,255,255))
    img.save('assets/images/flood/module1.jpg', quality=92)
    print('✅ flood/module1.jpg')

def make_flood_m2():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#001528','#001a20'])
    draw_status_bar(draw, '🌊 AI Flood Rescue — Water Segmentation', 'DeepLabV3+ Semantic Segmentation Active', '#3b82f6', '💧 SEG ON')
    # segmentation zones
    rounded_rect(draw, [20, 95, W-20, H-70], 10, fill=(5,20,35))
    # flood zone (blue overlay)
    for y in range(200, 390, 2):
        alpha = int(120 + (y-200)*0.4)
        draw.line([(20,y),(W-20,y)], fill=(0,80+int((y-200)*0.3),180), width=2)
    # safe zone (green overlay)
    for y in range(100, 200, 2):
        draw.line([(20,y),(W//2,y)], fill=(20,100,30), width=2)
    # danger zone (red)
    for y in range(100, 200, 2):
        draw.line([(W//2,y),(W-20,y)], fill=(120,20,20), width=2)
    # labels
    rounded_rect(draw, [30,115,160,145], 6, fill=(20,100,30))
    draw.text((40,121), '🟢 Safe Zone', font=load_font(14,bold=True), fill=(255,255,255))
    rounded_rect(draw, [W//2+10,115,W//2+160,145], 6, fill=(180,30,30))
    draw.text((W//2+20,121), '🔴 Danger Zone', font=load_font(14,bold=True), fill=(255,255,255))
    rounded_rect(draw, [30,215,180,245], 6, fill=(0,70,160))
    draw.text((40,221), '💧 Flood Water', font=load_font(14,bold=True), fill=(255,255,255))
    # stats
    rounded_rect(draw, [20,H-65,W-20,H-10], 10, fill=(59,130,246))
    text_center(draw, 'Flood Coverage: 34% of frame | Boundary Detected | Safe Evacuation Path: NORTH', H-52, load_font(15,bold=True), (255,255,255))
    img.save('assets/images/flood/module2.jpg', quality=92)
    print('✅ flood/module2.jpg')

def make_flood_m3():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#1a0533','#0d1028'])
    draw_status_bar(draw, '🌊 AI Flood Rescue — Face Recognition', 'Missing Person Database Match | 128D Encoding', '#8b5cf6', '🔍 MATCH')
    # two faces side by side
    for i, (label, match, conf) in enumerate([('Live Camera Feed','MATCH FOUND!','92.4%'),('Missing Person DB','Rajan Kumar','Reported: Day 2')]):
        x = 60 + i*380
        rounded_rect(draw, [x, 105, x+300, 300], 10, fill=(30,20,50))
        draw.text((x+10,115), label, font=load_font(13,bold=True), fill=(180,160,220))
        # face placeholder
        draw.ellipse([x+80,130,x+220,270], outline=(139,92,246), width=2, fill=(50,30,80))
        # facial landmarks
        import random; random.seed(i+7)
        for _ in range(20):
            lx = x+100+random.randint(0,100)
            ly = 150+random.randint(0,100)
            draw.ellipse([lx-2,ly-2,lx+2,ly+2], fill=(0,255,150))
        draw.text((x+10,278), match, font=load_font(14,bold=True), fill=(16,185,129) if i==0 else (200,160,255))
        draw.text((x+10,298), conf, font=load_font(12), fill=(160,140,200))
    # match connector
    draw.line([(360,200),(420,200)], fill=(16,185,129), width=3)
    draw.text((363,185),'Match!', font=load_font(12,bold=True), fill=(16,185,129))
    # bottom
    rounded_rect(draw, [20,H-65,W-20,H-10], 10, fill=(139,92,246))
    text_center(draw, '✅ Missing Person IDENTIFIED: Rajan Kumar | Family Notified via Firebase Alert!', H-52, load_font(15,bold=True), (255,255,255))
    img.save('assets/images/flood/module3.jpg', quality=92)
    print('✅ flood/module3.jpg')

def make_flood_m4():
    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img)
    gradient_bg(draw, ['#001020','#0a1a10'])
    draw_status_bar(draw, '🌊 AI Flood Rescue — GPS Rescue Map', 'Folium Live Map | Whisper Distress Call Active', '#10b981', '🗺 MAP ON')
    # map background
    rounded_rect(draw, [20, 95, W-20, H-70], 10, fill=(10,25,20))
    for i in range(10):
        draw.line([(20,100+i*30),(W-20,100+i*30)], fill=(15,40,30), width=1)
    for i in range(14):
        draw.line([(20+i*55,95),(20+i*55,H-70)], fill=(15,40,30), width=1)
    # roads
    draw.line([(20,250),(W-20,250)], fill=(30,60,40), width=8)
    draw.line([(350,95),(350,H-70)], fill=(30,60,40), width=8)
    # victim markers
    victims = [(180,200,'V1'),(420,180,'V2'),(550,300,'V3')]
    for vx,vy,lbl in victims:
        draw.ellipse([vx-14,vy-14,vx+14,vy+14], fill=(239,68,68))
        draw.text((vx-8,vy-8), '🆘', font=load_font(14), fill=(255,255,255))
        draw.text((vx-5,vy+16), lbl, font=load_font(11,bold=True), fill=(255,100,100))
    # rescue team
    draw.ellipse([280,290,310,320], fill=(59,130,246))
    draw.text((284,295), '🚁', font=load_font(14), fill=(255,255,255))
    draw.text((275,322), 'Rescue', font=load_font(11,bold=True), fill=(100,150,255))
    # whisper panel
    rounded_rect(draw, [25,H-130,W//2-10,H-75], 8, fill=(30,20,60))
    draw.text((35,H-125), '🎙️ Whisper AI — Distress Call Transcript:', font=load_font(12,bold=True), fill=(180,160,255))
    draw.text((35,H-105), '"Help! Trapped at North Bridge, water rising!"', font=load_font(12), fill=(200,200,255))
    # GPS coords
    rounded_rect(draw, [W//2+10,H-130,W-25,H-75], 8, fill=(10,40,20))
    draw.text((W//2+20,H-125), '📍 GPS Location Logged:', font=load_font(12,bold=True), fill=(100,220,140))
    draw.text((W//2+20,H-105), '13.0827°N, 80.2707°E → Firebase', font=load_font(12), fill=(150,255,180))
    # bottom
    rounded_rect(draw, [20,H-65,W-20,H-10], 10, fill=(16,185,129))
    text_center(draw, '3 GPS Markers Active | Rescue Helicopter Dispatched | Whisper Alert: SENT', H-52, load_font(15,bold=True), (255,255,255))
    img.save('assets/images/flood/module4.jpg', quality=92)
    print('✅ flood/module4.jpg')

if __name__ == '__main__':
    print('Generating all project module images...\n')
    make_smartrail_m1()
    make_smartrail_m2()
    make_smartrail_m3()
    make_smartrail_m4()
    make_bus_m1()
    make_bus_m2()
    make_bus_m3()
    make_bus_m4()
    make_gold_m1()
    make_gold_m2()
    make_gold_m3()
    make_gold_m4()
    make_flood_m1()
    make_flood_m2()
    make_flood_m3()
    make_flood_m4()
    print('\n🎉 All 16 module images generated successfully!')
