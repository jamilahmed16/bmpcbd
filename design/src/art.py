import math, random
BN = str.maketrans("0123456789","০১২৩৪৫৬৭৮৯")
def bn(n): return str(n).translate(BN)

RIFLE = "M0 0 L70 0 L70 -2.5 L112 -2.5 L112 1.5 L76 3 L73 8 L59 8 L55 4.5 L24 5 L7 12 L0 10 Z"

def rifle(x, y, ang, s=1, fill="var(--ink)"):
    return f'<path d="{RIFLE}" fill="{fill}" transform="translate({x} {y}) rotate({ang}) scale({s})"/>'

def headband(c="var(--band)"):
    return f'<path d="M37 17 Q50 11 63 17" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round"/><path d="M63 17 L75 25 M64 19 L71 31" fill="none" stroke="{c}" stroke-width="3.5" stroke-linecap="round"/>'

CARVE = 'stroke="var(--carve)" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".55"'

def body_male(stance="apart"):
    legs = {"apart": ((42,140,35,196),(58,140,67,196)),
            "stride": ((43,140,30,194),(57,140,72,190))}[stance]
    l1,l2 = legs
    out = ['<g fill="var(--ink)" stroke="var(--ink)" stroke-linecap="round" stroke-linejoin="round">',
      '<circle cx="50" cy="22" r="12.5" stroke="none"/>',
      '<rect x="45" y="30" width="10" height="12" stroke="none"/>',
      '<path d="M32 46 Q50 37 68 46 L66 72 L62 103 L38 103 L34 72 Z" stroke-width="2"/>',
      '<path d="M37 101 L63 101 L69 143 L31 143 Z" stroke-width="2"/>',
      f'<line x1="{l1[0]}" y1="{l1[1]}" x2="{l1[2]}" y2="{l1[3]}" stroke-width="11"/>',
      f'<line x1="{l2[0]}" y1="{l2[1]}" x2="{l2[2]}" y2="{l2[3]}" stroke-width="11"/>',
      f'<line x1="{l1[2]}" y1="{l1[3]+1}" x2="{l1[2]-11}" y2="{l1[3]+3}" stroke-width="7"/>',
      f'<line x1="{l2[2]}" y1="{l2[3]+1}" x2="{l2[2]+11}" y2="{l2[3]+3}" stroke-width="7"/>',
      '</g>',
      f'<g {CARVE}><path d="M43 56 L46 94"/><path d="M57 54 L55 92"/><path d="M45 110 L42 138"/><path d="M55 110 L59 138"/><path d="M40 150 L37 176"/></g>']
    return "".join(out)

def arms(pts_l, pts_r, w=10):
    pl = " ".join(f"{a},{b}" for a,b in pts_l); pr = " ".join(f"{a},{b}" for a,b in pts_r)
    return (f'<g fill="none" stroke="var(--ink)" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">'
            f'<polyline points="{pl}"/><polyline points="{pr}"/></g>')

def fist(x,y,r=6.5): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--ink)"/>'

def fig_flag(tx, ty, s):
    flag = ('<line x1="80" y1="-96" x2="74" y2="70" stroke="var(--ink)" stroke-width="5" stroke-linecap="round"/>'
            '<path d="M81 -96 Q103 -106 125 -96 T169 -96 L169 -44 Q147 -34 125 -44 T81 -44 Z" fill="var(--green)" stroke="var(--ink)" stroke-width="2.5"/>'
            '<path d="M86 -88 Q104 -96 120 -89" fill="none" stroke="var(--carve)" stroke-width="1.6" opacity=".4"/>'
            '<circle cx="119" cy="-70" r="16" fill="var(--sun)" stroke="var(--ink)" stroke-width="1.5"/>')
    return (f'<g transform="translate({tx} {ty}) scale({s})">{flag}{body_male()}'
            + arms([(36,48),(28,74),(40,90)], [(64,48),(70,22),(76,4)]) + fist(76,4) + headband() + '</g>')

def fig_rifle_up(tx, ty, s):
    return (f'<g transform="translate({tx} {ty}) scale({s})">{body_male("apart")}'
            + arms([(36,48),(26,22),(24,-2)], [(64,48),(72,22),(76,-2)]) + rifle(-8,-8,0,1.0) + fist(24,-3) + fist(76,-3)
            + headband() + '</g>')

def fig_march(tx, ty, s, flip=False):
    tf = f'translate({tx} {ty}) scale({s})' + (' translate(100 0) scale(-1 1)' if flip else '')
    return (f'<g transform="{tf}">{body_male("stride")}'
            + rifle(18,96,-62,0.95)
            + arms([(36,48),(30,72),(34,84)], [(64,48),(62,70),(50,62)]) + fist(50,62,6) + headband() + '</g>')

def fig_woman(tx, ty, s):
    b = ('<g fill="var(--ink)" stroke="var(--ink)" stroke-linecap="round" stroke-linejoin="round">'
         '<circle cx="50" cy="22" r="12" stroke="none"/><circle cx="37" cy="17" r="7" stroke="none"/>'
         '<rect x="45" y="30" width="10" height="12" stroke="none"/>'
         '<path d="M34 46 Q50 38 66 46 L63 98 L37 98 Z" stroke-width="2"/>'
         '<path d="M38 94 L62 94 Q72 150 76 196 L24 196 Q28 150 38 94 Z" stroke-width="2"/></g>'
         '<path d="M64 44 Q52 70 40 98 L48 100 Q58 72 67 50Z" fill="var(--band)"/>'
         '<path d="M25 188 L75 188" stroke="var(--band)" stroke-width="5"/>'
         f'<g {CARVE}><path d="M44 110 Q40 150 36 182"/><path d="M56 110 Q60 150 64 182"/><path d="M50 112 L50 182"/></g>')
    return (f'<g transform="translate({tx} {ty}) scale({s})">{b}'
            + rifle(10,104,-58,0.9)
            + arms([(36,48),(30,72),(34,84)], [(64,48),(60,68),(46,60)], 9) + fist(46,60,5.5) + '</g>')

def crowd(y0, n, x0, x1, color, seed, scale=1.0, arms_p=.5):
    rnd = random.Random(seed); out=[f'<g fill="{color}" stroke="{color}" stroke-linecap="round">']
    step=(x1-x0)/(n-1)
    for i in range(n):
        x = x0+i*step+rnd.uniform(-6,6); y=y0+rnd.uniform(-14,10); s=scale*rnd.uniform(.9,1.1)
        r=9*s
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" stroke="none"/>')
        out.append(f'<path d="M{x-18*s:.1f} {y+44*s:.1f} Q{x-17*s:.1f} {y+13*s:.1f} {x:.1f} {y+13*s:.1f} Q{x+17*s:.1f} {y+13*s:.1f} {x+18*s:.1f} {y+44*s:.1f} L{x+18*s:.1f} 640 L{x-18*s:.1f} 640Z" stroke="none"/>')
        k=rnd.random()
        side = 1 if rnd.random()<.5 else -1
        if k<arms_p:
            ex,ey = x+side*(20*s), y-30*s
            out.append(f'<line x1="{x+side*12*s:.1f}" y1="{y+20*s:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke-width="{7*s:.1f}"/><circle cx="{ex:.1f}" cy="{ey-2*s:.1f}" r="{5.5*s:.1f}" stroke="none"/>')
        elif k<arms_p+.3:
            out.append(f'<line x1="{x-side*14*s:.1f}" y1="{y+40*s:.1f}" x2="{x+side*16*s:.1f}" y2="{y-60*s:.1f}" stroke-width="{3.5*s:.1f}"/>')
    out.append('</g>'); return "".join(out)

def sunburst(cx, cy, n, R, color, op):
    out=[f'<g fill="{color}" opacity="{op}">']
    for i in range(n):
        a0=2*math.pi*i/n; a1=a0+math.pi/n
        out.append(f'<path d="M{cx} {cy} L{cx+R*math.cos(a0):.1f} {cy+R*math.sin(a0):.1f} L{cx+R*math.cos(a1):.1f} {cy+R*math.sin(a1):.1f}Z"/>')
    out.append('</g>'); return "".join(out)

def monument(tx, ty, s, c1="var(--green-deep)", c2="var(--green-mid)"):
    tri=[(118,82),(96,112),(76,142),(58,172),(42,200),(28,226),(15,250)]
    out=[f'<g transform="translate({tx} {ty}) scale({s})">']
    for i,(w,h) in enumerate(tri):
        out.append(f'<path d="M{-w} 0 L0 {-h} L{w} 0Z" fill="{c1 if i%2==0 else c2}"/>')
    out.append('</g>'); return "".join(out)

def birds(items, c="var(--ink)"):
    return f'<g fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round">' + "".join(
        f'<path d="M{x} {y} q{w/4} -{w/4} {w/2} 0 q{w/4} -{w/4} {w/2} 0"/>' for x,y,w in items) + '</g>'

def hero_svg():
    W,H=640,560
    p=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="hero-t"><title id="hero-t">উদীয়মান সূর্যের সামনে জাতীয় স্মৃতিসৌধ; পতাকা হাতে মুক্তিযোদ্ধা, অস্ত্র উঁচিয়ে সহযোদ্ধা ও নারী মুক্তিযোদ্ধা, পেছনে জনতার মিছিল</title>',
       '<defs><clipPath id="hclip"><rect width="640" height="560"/></clipPath><pattern id="paddy" width="16" height="12" patternUnits="userSpaceOnUse"><path d="M3 12 L6 3 M8 12 L8 1 M13 12 L10 4" stroke="var(--green-deep)" stroke-width="1.6" fill="none"/></pattern></defs>',
       '<g clip-path="url(#hclip)">',
       sunburst(360,330,36,700,"var(--red-deep)",.35),
       '<circle class="sunrise" cx="360" cy="300" r="190" fill="var(--sun)"/>',
       '<g fill="var(--red)">' + "".join(f'<rect x="150" y="{y}" width="430" height="{h}"/>' for y,h in [(330,5),(352,8),(378,11),(406,15)]) + '</g>',
       birds([(70,90,30),(118,62,22),(40,140,18),(560,120,22)], "var(--ink)"),
       crowd(392, 15, 10, 630, "var(--red-deep)", 7, 1.0, .55),
       monument(548,486,1.22),
       crowd(428, 8, -10, 420, "var(--crowd-2)", 11, 1.25, .45),
       '<path d="M0 478 C120 466 260 488 380 474 S580 466 640 472 L640 560 L0 560Z" fill="var(--green)"/>',
       '<path d="M0 494 C140 484 280 504 420 494 S580 488 640 492 L640 560 L0 560Z" fill="url(#paddy)"/>',
       '<path d="M0 528 C160 516 340 536 640 522 L640 560 L0 560Z" fill="var(--green-deep)"/>',
       fig_march(0,300,1.0),
       fig_woman(252,302,1.0),
       fig_rifle_up(338,296,1.02),
       fig_flag(108,262,1.22),
       '</g></svg>']
    return "".join(p)

def minar_svg():
    s=['<svg viewBox="0 0 320 180" role="img" aria-label="কেন্দ্রীয় শহীদ মিনার, পেছনে লাল সূর্য">',
       '<circle cx="160" cy="84" r="56" fill="var(--sun)"/>',
       '<g fill="none" stroke="var(--ink)" stroke-width="5" stroke-linejoin="miter">',
       '<path d="M144 150 L144 64 L176 64 L176 150"/><path d="M155 150 L155 64 M165 150 L165 64"/>',
       '<path d="M144 64 L136 34 L172 34 L176 64"/><path d="M148 34 L152 64 M160 34 L163 64"/>',
       '<path d="M104 150 L104 86 L128 86 L128 150 M116 86 L116 150"/>',
       '<path d="M192 150 L192 86 L216 86 L216 150 M204 86 L204 150"/>',
       '<path d="M72 150 L72 104 L90 104 L90 150"/><path d="M230 150 L230 104 L248 104 L248 150"/>',
       '</g><g fill="var(--ink)"><rect x="56" y="150" width="208" height="8"/><rect x="36" y="158" width="248" height="8"/><rect x="18" y="166" width="284" height="8"/></g>',
       '</svg>']
    return "".join(s)

def sunrise_svg():
    rays="".join(f'<line x1="{160+78*math.cos(a):.1f}" y1="{120+78*math.sin(a):.1f}" x2="{160+98*math.cos(a):.1f}" y2="{120+98*math.sin(a):.1f}"/>' for a in [math.pi*(1+k/8) for k in range(1,8)])
    return ('<svg viewBox="0 0 320 180" role="img" aria-label="ধানক্ষেতের উপর উদীয়মান সূর্য">'
            '<circle cx="160" cy="120" r="64" fill="var(--sun)"/>'
            f'<g stroke="var(--sun)" stroke-width="6" stroke-linecap="round">{rays}</g>'
            '<path d="M0 128 C80 120 220 136 320 124 L320 180 L0 180Z" fill="var(--green)"/>'
            '<path d="M0 146 C120 138 220 152 320 142 L320 180 L0 180Z" fill="url(#paddy2)"/>'
            '<path d="M0 162 C120 154 220 168 320 158 L320 180 L0 180Z" fill="var(--green-deep)"/>'
            '<defs><pattern id="paddy2" width="14" height="10" patternUnits="userSpaceOnUse"><path d="M3 10 L5 2 M7 10 L7 1 M11 10 L9 3" stroke="var(--green-deep)" stroke-width="1.4" fill="none"/></pattern></defs>'
            + birds([(232,46,20),(258,30,14)]) + '</svg>')

def flag_svg():
    return ('<svg viewBox="0 0 320 180" role="img" aria-label="বিজয়ের পতাকা হাতে মুক্তিযোদ্ধা">'
            + sunburst(160,190,24,260,"var(--sun)",.18) +
            fig_flag(118,25+48,0.5) +
            '<path d="M0 168 C100 160 220 172 320 164 L320 180 L0 180Z" fill="var(--green)"/>'
            + birds([(230,40,22),(262,62,16)]) + '</svg>')

def torch_svg():
    return ('<svg viewBox="0 0 360 360" role="img" aria-label="মুক্তিযুদ্ধের চেতনার মশাল">'
            + sunburst(180,150,28,260,"var(--red-deep)",.45) +
            '<circle cx="180" cy="150" r="96" fill="var(--sun)"/>'
            '<path d="M180 30 C214 70 236 96 222 136 C214 160 196 170 180 170 C160 170 140 158 136 134 C130 104 150 92 160 64 C166 92 176 96 184 96 C188 76 186 56 180 30Z" fill="var(--paper)" stroke="var(--ink)" stroke-width="4"/>'
            '<path d="M182 84 C198 106 204 122 196 142 C190 154 170 156 164 142 C158 128 170 116 172 100 C176 112 182 112 184 108Z" fill="var(--red)"/>'
            '<path d="M144 168 L216 168 L204 196 L156 196Z" fill="var(--ink)"/>'
            '<path d="M156 196 L204 196 L190 330 L170 330Z" fill="var(--ink)"/>'
            '<g stroke="var(--carve)" stroke-width="2" opacity=".5"><line x1="164" y1="210" x2="174" y2="316"/><line x1="156" y1="182" x2="204" y2="182"/></g>'
            '<path d="M130 236 Q150 220 168 230 L192 226 Q212 226 218 240 Q220 262 200 266 L164 266 Q138 262 130 236Z" fill="var(--ink)"/>'
            '<g stroke="var(--carve)" stroke-width="2" fill="none" opacity=".55"><path d="M176 236 Q196 236 206 246"/><path d="M168 250 Q190 252 210 252"/></g>'
            '</svg>')

def banyan_svg():
    rnd=random.Random(5); circ=[]
    for i in range(40):
        a=rnd.uniform(0,2*math.pi); r=rnd.uniform(0,1)**.6
        x=180+140*r*math.cos(a); y=124+58*r*math.sin(a); rr=rnd.uniform(22,33)
        c = "var(--green-deep)" if (y+rnd.uniform(-20,20))>132 else "var(--green)"
        circ.append((y,f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{c}"/>'))
    circ.sort()
    roots="".join(f'<path d="M{x} {y0} Q{x+rnd.uniform(-6,6):.1f} {(y0+304)/2:.1f} {x+rnd.uniform(-4,4):.1f} 304" stroke="var(--ink)" stroke-width="{rnd.uniform(1.6,3):.1f}" fill="none"/>' for x,y0 in [(70,170),(92,184),(118,196),(240,196),(266,186),(292,170),(310,160)])
    return ('<svg viewBox="0 0 360 330" role="img" aria-label="বটগাছ: শিকড়ে ১৯৭১, শাখায় প্রজন্ম">'
            '<circle cx="282" cy="58" r="46" fill="var(--sun)"/>'
            + roots +
            '<path d="M160 304 Q166 240 156 196 L170 170 L186 170 L198 196 Q190 240 200 304Z" fill="var(--ink)"/>'
            '<path d="M168 190 Q130 170 100 172 M190 190 Q230 168 262 172" stroke="var(--ink)" stroke-width="10" fill="none" stroke-linecap="round"/>'
            + "".join(c for _,c in circ) +
            '<g stroke="var(--carve)" stroke-width="2" fill="none" opacity=".5"><path d="M172 296 Q176 250 170 204"/><path d="M186 296 Q184 250 188 206"/></g>'
            '<path d="M0 300 C100 292 260 306 360 296 L360 330 L0 330Z" fill="var(--green)"/>'
            '<text x="180" y="322" text-anchor="middle" font-family="Anek Bangla, sans-serif" font-weight="700" font-size="15" fill="var(--paper)">শিকড়ে ১৯৭১ · শাখায় প্রজন্ম</text>'
            '</svg>')
