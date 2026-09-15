import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, FancyBboxPatch
from matplotlib.gridspec import GridSpec
import numpy as np
import io
from PIL import Image

# ─── Dark theme ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0a0f1e',
    'axes.facecolor':   '#0a0f1e',
    'text.color':       'white',
    'font.family':      'DejaVu Sans',
})

fig = plt.figure(figsize=(16, 9), facecolor='#0a0f1e')
gs  = GridSpec(1, 3, figure=fig, wspace=0.03,
               left=0.01, right=0.99, top=0.92, bottom=0.04)

# ══════════════════════════════════════════════════════════════════════════════
# LEFT PANEL — Victim List
# ══════════════════════════════════════════════════════════════════════════════
ax_left = fig.add_subplot(gs[0])
ax_left.set_xlim(0, 1); ax_left.set_ylim(0, 1)
ax_left.axis('off')

# Panel background
left_bg = FancyBboxPatch((0.02, 0.01), 0.96, 0.97,
    boxstyle="round,pad=0.01", linewidth=1.5,
    edgecolor='#1e3a5f', facecolor='#0d1b35', zorder=0)
ax_left.add_patch(left_bg)

# Header
ax_left.text(0.5, 0.95, '[!]  VICTIM DETECTION LOG', ha='center', va='top',
             fontsize=9.5, fontweight='bold', color='#ff4444')
ax_left.axhline(0.91, xmin=0.05, xmax=0.95, color='#ff4444', linewidth=0.8, alpha=0.6)

victims = [
    ('V-001', '11.02°N 79.97°E', 'CRITICAL', '#ff2222'),
    ('V-002', '11.04°N 79.95°E', 'CRITICAL', '#ff2222'),
    ('V-003', '11.06°N 79.98°E', 'WARNING',  '#ffaa00'),
    ('V-004', '11.03°N 80.01°E', 'WARNING',  '#ffaa00'),
    ('V-005', '11.07°N 80.00°E', 'STABLE',   '#22cc66'),
    ('V-006', '11.05°N 79.93°E', 'RESCUED',  '#4488ff'),
    ('V-007', '11.01°N 79.99°E', 'CRITICAL', '#ff2222'),
    ('V-008', '11.08°N 79.96°E', 'RESCUED',  '#4488ff'),
]
for i, (vid, coord, status, col) in enumerate(victims):
    y = 0.87 - i * 0.105
    # card
    card = FancyBboxPatch((0.05, y-0.045), 0.90, 0.09,
        boxstyle="round,pad=0.005", linewidth=0.8,
        edgecolor=col+'55', facecolor='#11223a', zorder=1)
    ax_left.add_patch(card)
    ax_left.text(0.10, y+0.015, vid, fontsize=8.5, fontweight='bold', color='white', va='center')
    ax_left.text(0.10, y-0.018, coord, fontsize=6.5, color='#aabbcc', va='center')
    # status badge
    badge = FancyBboxPatch((0.62, y-0.025), 0.30, 0.05,
        boxstyle="round,pad=0.003", linewidth=0,
        facecolor=col+'33', zorder=2)
    ax_left.add_patch(badge)
    ax_left.text(0.77, y, status, ha='center', va='center',
                 fontsize=6.8, fontweight='bold', color=col)

# Stats at bottom
ax_left.text(0.5, 0.08, 'VICTIMS DETECTED', ha='center', fontsize=7, color='#7799bb')
ax_left.text(0.5, 0.04, '14', ha='center', fontsize=22, fontweight='bold', color='#ff4444')

# ══════════════════════════════════════════════════════════════════════════════
# CENTRE PANEL — GPS Map
# ══════════════════════════════════════════════════════════════════════════════
ax_map = fig.add_subplot(gs[1])
ax_map.set_xlim(79.90, 80.10); ax_map.set_ylim(10.96, 11.14)
ax_map.set_facecolor('#0b1a2f')

# Grid lines (map grid)
for lon in np.arange(79.90, 80.11, 0.04):
    ax_map.axvline(lon, color='#1a3050', linewidth=0.5, alpha=0.7)
for lat in np.arange(10.96, 11.15, 0.04):
    ax_map.axhline(lat, color='#1a3050', linewidth=0.5, alpha=0.7)

# Flood water polygon (blue semi-transparent)
flood_lons = [79.92, 79.95, 80.00, 80.04, 80.06, 80.03, 79.98, 79.93, 79.91]
flood_lats = [10.99, 10.97, 10.98, 10.99, 11.02, 11.06, 11.07, 11.04, 11.01]
ax_map.fill(flood_lons, flood_lats, color='#1a6faa', alpha=0.35, zorder=1)
ax_map.plot(flood_lons + [flood_lons[0]], flood_lats + [flood_lats[0]],
            color='#3399ff', linewidth=1.2, alpha=0.7, zorder=2)

# Road lines
roads = [
    ([79.91, 80.09], [11.05, 11.05]),
    ([79.91, 80.09], [11.00, 11.00]),
    ([79.99, 79.99], [10.97, 11.13]),
    ([79.94, 79.94], [10.97, 11.13]),
]
for lon_r, lat_r in roads:
    ax_map.plot(lon_r, lat_r, color='#2a4060', linewidth=2.5, solid_capstyle='round', zorder=2)

# Victim pins (red)
v_lons = [79.97, 79.95, 79.98, 80.01, 80.00, 79.93, 79.99, 79.96]
v_lats = [11.02, 11.04, 11.06, 11.03, 11.07, 11.05, 11.01, 11.08]
critical_mask = [True, True, False, False, False, False, True, False]
for i, (lon, lat) in enumerate(zip(v_lons, v_lats)):
    col = '#ff2222' if critical_mask[i] else '#ffaa00'
    ax_map.plot(lon, lat, 'v', markersize=12, color=col,
                markeredgecolor='white', markeredgewidth=0.8, zorder=5)
    ax_map.plot(lon, lat, 'o', markersize=18, color=col, alpha=0.2, zorder=4)
    ax_map.text(lon+0.003, lat+0.003, f'V-{i+1:03d}', fontsize=6,
                color='white', fontweight='bold', zorder=6)

# Rescue team path
rescue_path_lon = [79.93, 79.96, 79.97, 79.98, 80.00]
rescue_path_lat = [10.98, 10.99, 11.01, 11.04, 11.06]
ax_map.plot(rescue_path_lon, rescue_path_lat,
            color='#ff8800', linewidth=2.5, linestyle='--',
            alpha=0.9, zorder=5, label='Rescue Route')
# Rescue team marker (blue)
ax_map.plot(79.93, 10.98, 's', markersize=14, color='#2255ff',
            markeredgecolor='white', markeredgewidth=1.2, zorder=7)
ax_map.text(79.927, 10.975, 'RESCUE\nTEAM', fontsize=5.5, color='#88bbff',
            ha='center', fontweight='bold', zorder=7)
# Pulse ring on rescue team
for r, a in [(0.006, 0.4), (0.010, 0.2)]:
    circle = Circle((79.93, 10.98), r, fill=False,
                    edgecolor='#2255ff', linewidth=1.5, alpha=a, zorder=3)
    ax_map.add_patch(circle)

# DAM marker
ax_map.add_patch(Rectangle((79.915, 10.963), 0.015, 0.008,
                 facecolor='#774400', edgecolor='#ffaa44', linewidth=1.5, zorder=4))
ax_map.text(79.923, 10.967, 'DAM', fontsize=7.5, ha='center',
            color='#ffcc66', fontweight='bold', zorder=6)

# Water overflow arrows from dam
for dy in [0.005, 0.010, 0.015]:
    ax_map.annotate('', xy=(79.923, 10.972 + dy), xytext=(79.923, 10.971 + dy - 0.002),
                    arrowprops=dict(arrowstyle='->', color='#3399ff', lw=1.5), zorder=5)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='#ff2222', label='Critical Victim'),
    mpatches.Patch(facecolor='#ffaa00', label='Warning'),
    mpatches.Patch(facecolor='#2255ff', label='Rescue Team'),
    mpatches.Patch(facecolor='#1a6faa', alpha=0.5, label='Flood Zone'),
]
ax_map.legend(handles=legend_elements, loc='lower right', fontsize=6.5,
              facecolor='#0d1b35', edgecolor='#1e3a5f', labelcolor='white',
              framealpha=0.9)

ax_map.set_xlabel('Longitude', fontsize=7, color='#7799bb')
ax_map.set_ylabel('Latitude',  fontsize=7, color='#7799bb')
ax_map.tick_params(colors='#445566', labelsize=6)
for spine in ax_map.spines.values():
    spine.set_edgecolor('#1e3a5f')

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL — Stats & Alerts
# ══════════════════════════════════════════════════════════════════════════════
ax_right = fig.add_subplot(gs[2])
ax_right.set_xlim(0, 1); ax_right.set_ylim(0, 1)
ax_right.axis('off')

right_bg = FancyBboxPatch((0.02, 0.01), 0.96, 0.97,
    boxstyle="round,pad=0.01", linewidth=1.5,
    edgecolor='#1e3a5f', facecolor='#0d1b35', zorder=0)
ax_right.add_patch(right_bg)

ax_right.text(0.5, 0.95, '[*]  RESCUE STATISTICS', ha='center', va='top',
              fontsize=9.5, fontweight='bold', color='#4af')
ax_right.axhline(0.91, xmin=0.05, xmax=0.95, color='#1e4a7f', linewidth=0.8)

# Stat cards
stats = [
    ('Victims Detected', '14', '#ff4444'),
    ('Rescued',          '8',  '#22cc66'),
    ('Critical',         '3',  '#ff8800'),
    ('Search Area (km²)','12', '#4488ff'),
]
for i, (label, val, col) in enumerate(stats):
    y = 0.86 - i * 0.115
    card = FancyBboxPatch((0.06, y-0.05), 0.88, 0.095,
        boxstyle="round,pad=0.008", linewidth=1,
        edgecolor=col+'55', facecolor='#111f38', zorder=1)
    ax_right.add_patch(card)
    ax_right.text(0.55, y+0.010, label, ha='center', va='center',
                  fontsize=7.5, color='#aabbcc')
    ax_right.text(0.55, y-0.022, val, ha='center', va='center',
                  fontsize=20, fontweight='bold', color=col)

# Live Alerts
ax_right.axhline(0.42, xmin=0.05, xmax=0.95, color='#1e4a7f', linewidth=0.8)
ax_right.text(0.5, 0.40, 'LIVE ALERTS', ha='center', fontsize=8.5,
              fontweight='bold', color='#ff4444')

alerts = [
    ('[SOS]', 'V-001 CRITICAL at 11.02N', '#ff2222'),
    ('[SOS]', 'V-002 submerged - SOS active', '#ff2222'),
    ('[!]',   'Dam overflow detected', '#ffaa00'),
    ('[OK]',  'V-006 & V-008 RESCUED', '#22cc66'),
    ('[GPS]', 'GPS signal lost - V-007', '#888888'),
]
for i, (icon, msg, col) in enumerate(alerts):
    y = 0.35 - i * 0.068
    ax_right.text(0.08, y, icon, fontsize=8, va='center', color=col)
    ax_right.text(0.18, y, msg, fontsize=6.8, va='center', color=col)

# AI tag at bottom
ax_right.add_patch(FancyBboxPatch((0.10, 0.03), 0.80, 0.06,
    boxstyle="round,pad=0.006", linewidth=0,
    facecolor='#0d2a4a', zorder=1))
ax_right.text(0.5, 0.06, 'AI FLOOD RESCUE  |  YOLOv8 + Folium + GPS',
              ha='center', va='center', fontsize=6.5,
              color='#4af', fontstyle='italic')

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL TITLE
# ══════════════════════════════════════════════════════════════════════════════
fig.text(0.5, 0.97, 'AI FLOOD RESCUE  --  LIVE GPS MONITORING SYSTEM',
         ha='center', va='top', fontsize=13, fontweight='bold', color='white',
         path_effects=[pe.withStroke(linewidth=3, foreground='#0a0f1e')])

# ── Save ──────────────────────────────────────────────────────────────────────
out = r'assets/images/flood/module4.jpg'
buf = io.BytesIO()
plt.savefig(buf, dpi=150, bbox_inches='tight',
            facecolor='#0a0f1e', edgecolor='none', format='png')
plt.close()
buf.seek(0)
Image.open(buf).convert('RGB').save(out, 'JPEG', quality=95)
print(f"Saved -> {out}")
