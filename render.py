#!/usr/bin/env python3
"""Render v2 infographic-led front page: THE DAY IN NUMBERS, 22 Nov 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
BG = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 24, 24)
NAVY = (16, 42, 86)
TEAL = (0, 110, 110)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)

def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)

F_SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
F_SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
F_SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
F_SANS = lambda s: font("LiberationSans-Regular.ttf", s)

def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_text(draw, x, y, text, fnt, fill=INK, maxw=976, leading=4, max_lines=None):
    lines = wrap(draw, text, fnt, maxw)
    if max_lines:
        lines = lines[:max_lines]
    lh = fnt.size + leading
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

# --- dot-matrix world map: rows of '.' land / ' ' sea, roughly continental ---
MAP_ROWS = [
    "        oooo  oo                     oooooooo ooo          ",
    "      oooooooo oo        o          oooooooooooooo  ooo    ",
    "     oooooooooo            o       ooo oooooooooooooooo    ",
    "      ooooooo                       oo  ooo  ooooooooo     ",
    "       ooooo     o                   o        ooooo        ",
    "        ooo     ooo                   oo       ooo  oo     ",
    "         oo    ooooo                   o       oo          ",
    "                ooo                    oo      o  o        ",
    "                 o                      ooooooo            ",
    "                                        ooooo              ",
    "                                         ooo        o      ",
    "                                          o                ",
]
# pins: (col,row,number) keyed to story numbers in final numbering
PINS = [(9, 1, 1), (28, 2, 6), (34, 3, 12), (44, 2, 18), (50, 4, 24), (30, 8, 30)]

STATS = [
    ("186", "drones fired at Ukraine overnight; 161 downed"),
    ("98.79%", "record turnout in Hong Kong election polls"),
    ("35%", "electricity share of energy targeted by 2035 in COP31 deal"),
    ("-3.7%", "S&P 500 fall in the AI sell-off, into correction"),
    ("50", "points for Wembanyama as Spurs beat New Orleans"),
    ("24", "dead in the Nigeria boat disaster"),
    ("36", "missing in the Banten factory fire in Indonesia"),
    ("EUR 1.78tn", "proposed EU budget for 2028-2034"),
]

def draw_masthead(draw):
    draw.rectangle([0, 0, W, 6], fill=RED)
    draw.text((W // 2, 14), "THE DAY IN NUMBERS", font=F_SERIF_B(44), fill=INK, anchor="ma")
    draw.text((W // 2, 64), "T H E   W O R L D   I N   O N E   D A Y", font=F_SANS_B(15), fill=RED, anchor="ma")
    # date strip - full date in large type
    draw.rectangle([24, 88, W - 24, 122], fill=INK)
    draw.text((W // 2, 94), "Sunday 22 November 2026", font=F_SANS_B(20), fill=(255, 255, 255), anchor="ma")
    y = 128
    y = draw_text(draw, 24, y, "Sunday 22 November 2026 summed up in one image: a climate deal voted on in Antalya, war across Ukraine and the Gulf, record polls in Hong Kong and a markets rout - told first in numbers, then in 38 numbered stories.", F_SANS(11), fill=GREY, maxw=976, leading=3)
    draw.line([24, y + 2, W - 24, y + 2], fill=INK, width=2)
    return y + 8

def draw_centrepiece(draw, top):
    # panel
    bottom = top + 196
    draw.rectangle([24, top, W - 24, bottom], fill=(235, 240, 248), outline=NAVY, width=3)
    draw.rectangle([24, top, W - 24, top + 34], fill=NAVY)
    draw.text((W // 2, top + 7), "22 NOVEMBER IN NUMBERS", font=F_SANS_B(20), fill=(255, 255, 255), anchor="ma")
    # stat blocks: 4 across x 2 down, left 2/3 of panel
    sx, sy = 36, top + 42
    bw, bh = 150, 70
    for i, (num, label) in enumerate(STATS):
        cx = sx + (i % 4) * (bw + 8)
        cy = sy + (i // 4) * (bh + 8)
        draw.rectangle([cx, cy, cx + bw, cy + bh], fill=(255, 255, 255), outline=(180, 190, 205), width=1)
        # big number auto-fit
        sz = 30
        while sz > 14 and draw.textlength(num, font=F_SANS_B(sz)) > bw - 12:
            sz -= 2
        draw.text((cx + bw // 2, cy + 4), num, font=F_SANS_B(sz), fill=RED, anchor="ma")
        ly = cy + 38
        for ln in wrap(draw, label, F_SANS(9), bw - 12)[:3]:
            draw.text((cx + bw // 2, ly), ln, font=F_SANS(9), fill=INK, anchor="ma")
            ly += 12
    # world map on right side of panel
    mx, my = 676, top + 44
    draw.text((mx, my), "WHERE IT HAPPENED", font=F_SANS_B(10), fill=NAVY)
    dot, gap = 2, 5
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch != " ":
                x0 = mx + c * gap
                y0 = my + 18 + r * gap
                draw.ellipse([x0, y0, x0 + dot, y0 + dot], fill=TEAL)
    for (c, r, n) in PINS:
        x0 = mx + c * gap
        y0 = my + 18 + r * gap
        draw.ellipse([x0 - 6, y0 - 6, x0 + 10, y0 + 10], fill=RED)
        draw.text((x0 + 2, y0 - 5), str(n), font=F_SANS_B(8), fill=(255, 255, 255), anchor="ma")
    draw.text((mx, my + 18 + len(MAP_ROWS) * gap + 6), "Pins key to story numbers below.", font=F_SANS(9), fill=GREY)
    draw.text((mx, my + 18 + len(MAP_ROWS) * gap + 20), "COP31 in Antalya anchors the day.", font=F_SANS(9), fill=GREY)
    return bottom + 8

# (region, colour, [(headline, summary), ...])
SECTIONS = [
    ("COP31 / CLIMATE", RED, [
        ("COP31 puts final deal to a Sunday vote", "After two days of overtime, presidents Turkiye and Australia tabled a ten-page package in Antalya; delegations had until 03:00 GMT to object."),
        ("Final text never mentions fossil fuels", "The draft omits fossil fuels, oil, coal and phase-out entirely - the question that deadlocked the summit for a fortnight."),
        ("Deal admits 1.5C overshoot for the first time", "First COP outcome to acknowledge passing the Paris limit; October 2026 measured 1.8C above pre-industrial levels."),
        ("Electricity to reach 35% of energy by 2035", "Headline goal lifts electricity from about 21% today to 35% by 2035, backed by some 90 countries."),
        ("Quorum fears as delegates leave Antalya", "Organisers worried the summit might not muster the two-thirds of delegates needed to pass the draft at all."),
        ("Adaptation finance tripled by 2035 - no baseline", "Text reaffirms tripling adaptation finance by 2035 but sets no baseline or method for measuring it."),
    ]),
    ("EUROPE", NAVY, [
        ("Russia fires 186 drones at Ukraine overnight", "Ukraine said 161 of 186 drones were shot down or jammed by 08:00 Kyiv time, with strikes at 18 locations."),
        ("'Triple-tap' strike devastates Kryvyi Rih", "Missiles, then drones that hit rescuers, struck Zelensky's home city; a boy of seven and a paramedic were killed, nearly 60 wounded."),
        ("Ukrainian drone sets Russian cargo ship ablaze", "The Sparta II drifted into Finnish waters in the Gulf of Finland; Finland's border guard said the crew was evacuated."),
        ("Finland probes suspected Russian helicopter incursion", "Helsinki investigates a suspected airspace violation of up to 4.1 km near its eastern border."),
        ("Europe wins a seat at Russia-Ukraine talks", "At the Coalition of the Willing in Berlin, allies secured a place in negotiations through the E5, NATO and the EU."),
        ("Costa proposes EUR 1.78 trillion EU budget", "The European Council president tabled a EUR 1.78tn budget for 2028-2034 ahead of the 26-27 November summit."),
    ]),
    ("MIDDLE EAST", (140, 70, 0), [
        ("Iran strikes industrial site in Bahrain", "Bahrain said an Iranian strike set fire to a civilian industrial site late Saturday; no injuries were reported."),
        ("IRGC claims two US Patriot systems disabled", "Iran's Revolutionary Guards said they targeted US bases in Bahrain and disabled two Patriot missile systems."),
        ("Iran shoots down two US drones over Hormuz", "Tehran said its air defences downed two American drones over the strait."),
        ("Coalition intercepts Houthi missiles fired at Riyadh", "Three ballistic missiles were intercepted Saturday, two days after a Houthi strike damaged Riyadh's tallest tower."),
        ("Israeli strikes kill at least four in Gaza City", "Bombardments hit Gaza City while a truce nominally held; a vehicle carrying food was struck, killing three."),
        ("Qatar mediates as Trump seeks nuclear deal with Iran", "Doha continued mediation to end the Iran war while Trump said he wants a permanent deal barring Iranian nuclear weapons."),
    ]),
    ("ASIA-PACIFIC", TEAL, [
        ("Hong Kong votes in election committee polls", "856 candidates contested 723 seats in 31 subsectors to form the 1,500-member committee that elects the next Chief Executive."),
        ("Record 98.79% turnout in Hong Kong polls", "5,640 of 5,709 voters cast ballots before polls closed at 6pm, beating the 89.77% turnout of 2021."),
        ("Trump, Xi and Putin meet in Shenzhen", "The US, Chinese and Russian leaders held a trilateral meeting and agreed to open talks on nuclear risk reduction."),
        ("Indonesia factory fire: 3 dead, 36 missing", "Rescuers searched a confectionery factory in Cikande, Banten, after a blaze killed three workers and injured four."),
        ("Toxic alcohol kills at least 11 in Manipur", "More than 180 people were hospitalised after drinking toxic liquor in the northeastern Indian state."),
        ("North Korea postpones Pyongyang Marathon", "Next year's race moves from April to October, a tour agency said."),
    ]),
    ("NORTH AMERICA", (90, 40, 130), [
        ("US stocks fall into correction in AI sell-off", "A rout in AI and chip shares pushed the S&P 500 down 3.7% into correction; Japan's Nikkei fell 5.06%."),
        ("FBI probes possible breach of crime database", "The bureau investigates a possible intrusion into its national crime data repository."),
        ("US 'willing to accept' a Latin American UN chief", "Ambassador Mike Waltz signalled openness amid gridlock over the next UN secretary-general."),
        ("Florida river breaks a 73-year record", "The St. Johns River flooded towns from Miami to Brevard County; flooding near Cocoa could last into January."),
        ("US presses Ukraine to accept peace deal by January", "Washington is pushing Kyiv toward an agreement with Moscow by the new year."),
    ]),
    ("LATIN AMERICA", (0, 110, 40), [
        ("Mexico captures cartel boss 'El Chapo Isidro'", "Special forces arrested Fausto Isidro Meza Flores in Guasave, Sinaloa, with US support; 11 died in following violence."),
        ("Peru earthquake leaves 170 homes affected", "A preliminary inventory counted 170 homes damaged by the quake."),
    ]),
    ("AFRICA", (160, 100, 0), [
        ("Nigeria boat disaster toll rises to 24", "A crowded boat carrying people to a funeral capsized in southern Nigeria on Friday, agency NEMA said."),
        ("Durban port delays strand truckers", "Congestion at Durban's port left truck drivers stranded for days."),
    ]),
    ("SPORT", (0, 90, 160), [
        ("Verstappen wins Las Vegas Grand Prix", "The Red Bull driver won from pole under floodlights for the third time in four years; Norris and Piastri completed the podium."),
        ("Russell's late crash ends podium hopes", "The Mercedes driver hit the barriers three laps from the end and finished ninth; both Ferraris took 10-second penalties."),
        ("Wembanyama's 50-point night lifts Spurs", "Victor Wembanyama scored 50 points with 19 rebounds as San Antonio rolled past New Orleans 114-91."),
        ("Kansas City wins first NWSL title", "A DiBernardo 'Olympic goal' direct from a corner sealed a 2-1 win over Washington."),
    ]),
    ("SCIENCE & HEALTH", GREY, [
        ("Carbon capture bet under scrutiny", "New reporting questions whether underground CO2 storage can deliver what climate models assume."),
    ]),
]

def all_stories():
    out = []
    for sec, col, items in SECTIONS:
        for h, s in items:
            out.append((sec, col, h, s))
    return out

def draw_story(draw, x, y, num, headline, summary, colw):
    # number badge
    draw.ellipse([x, y, x + 16, y + 16], fill=RED)
    draw.text((x + 8, y + 2), str(num), font=F_SANS_B(9), fill=(255, 255, 255), anchor="ma")
    hy = y
    for ln in wrap(draw, headline, F_SANS_B(11), colw - 22)[:2]:
        draw.text((x + 20, hy), ln, font=F_SANS_B(11), fill=INK)
        hy += 14
    sy = hy + 1
    for ln in wrap(draw, summary, F_SANS(9), colw - 4)[:3]:
        draw.text((x + 2, sy), ln, font=F_SANS(9), fill=(45, 45, 45))
        sy += 11
    return sy + 3

def main():
    stories = all_stories()
    print("story count:", len(stories))
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_centrepiece(draw, y)
    # three columns; distribute sections sequentially, balancing by count
    colw = 312
    xs = [24, 356, 688]
    # split sections into 3 column groups manually for balance
    groups = [
        [SECTIONS[0], SECTIONS[4], SECTIONS[5]],          # COP31, N America, LatAm = 13
        [SECTIONS[1], SECTIONS[3], SECTIONS[8]],          # Europe, Asia, Sci = 13
        [SECTIONS[2], SECTIONS[6], SECTIONS[7]],          # MidEast, Africa, Sport = 12
    ]
    # numbering follows SECTIONS order, so precompute start numbers
    starts, n = {}, 1
    for sec, col, items in SECTIONS:
        starts[sec] = n
        n += len(items)
    for ci, group in enumerate(groups):
        cy = y
        x = xs[ci]
        for sec, col, items in group:
            draw.rectangle([x, cy, x + colw, cy + 17], fill=col)
            draw.text((x + 6, cy + 3), sec, font=F_SANS_B(10), fill=(255, 255, 255))
            cy += 21
            num = starts[sec]
            for h, s in items:
                cy = draw_story(draw, x, cy, num, h, s, colw)
                num += 1
            cy += 4
        print(f"column {ci+1} ends at y={cy}")
    draw.rectangle([0, H - 18, W, H], fill=INK)
    draw.text((W // 2, H - 14), "THE DAY IN NUMBERS  -  Sunday 22 November 2026  -  Sources: Reuters, AP, CNN and official releases", font=F_SANS(9), fill=(255, 255, 255), anchor="ma")
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()

