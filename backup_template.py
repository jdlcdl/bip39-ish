import math

UNIT = 10

class Svg:
    fstr = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{width}" height="{height}" overflow="scroll" viewBox="{viewBox}">
  <defs>
    <filter id="blur"><feGaussianBlur in="SourceGraphic" stdDeviation="1" /></filter>
    <rect id="P7" width="70" height="70" stroke-width="0" fill="#000" />
    <rect id="P5" width="50" height="50" stroke-width="0" fill="#fff" />
    <rect id="P3" width="30" height="30" stroke-width="0" fill="#000" />
    <rect id="A5" width="50" height="50" stroke-width="0" fill="#000" />
    <rect id="A3" width="30" height="30" stroke-width="0" fill="#fff" />
    <rect id="A1" width="10" height="10" stroke-width="0" fill="#000" />

    <!-- User has a choice: dots for a punch? or grid for a marker? or both? -->
    <g id="D">
    <rect width="10" height="10" stroke-width="0.4" stroke="#888" fill="#fff" />
    <!--<circle cx="5" cy="5" r="1" fill="#ccc" />-->
    </g>

    <!-- User has a choice: timing as circles? or as blocks? or no timing markers? -->
    <!--<rect id="T" width="10" height="10" stroke-width="0" fill="#000" />-->
    <!--<circle id="T" cx="5" cy="5" r="4" fill="#000" filter="url(#blur)" />-->

  </defs>
{content}
</svg>'''
    def __init__(self, width, height, viewBox, content):
        self.width = width
        self.height = height
        self.viewBox = viewBox
        self.content = content
    def render(self):
        return self.fstr.format(
            width=self.width, 
            height=self.height, 
            viewBox=self.viewBox,
            content=self.content)


class SvgG:
    fstr = """
<g id="{id_}">
{contents}
</g><!-- end of Group id={id_} -->
"""
    def __init__(self, id_, contents=None):
        self.id_ = id_
        if contents: self.contents=contents
        else: self.contents = []
    def append(self, an_item):
        self.contents.append(an_item)
    def extend(self, a_list):
        self.contents.extend(a_list)
    def render(self, xyoff):
        return self.fstr.format(
             id_=self.id_,
             contents='\n'.join([x.render(xyoff) for x in self.contents])
        )


class SvgUse:
    fstr = '<use href="#{}" x="{}" y="{}" />'
    href = None
    def __init__(self, href, x, y):
        self.href = href
        self.x = x
        self.y = y
    def render(self, xyoff):
        return self.fstr.format(
            self.href,
            self.x + xyoff[0], 
            self.y + xyoff[1]
    )


class SvgText:
    fstr = '<text x="{}" y="{}" font-size="{}" fill="{}">{}</text>'
    fill = '#333'
    def __init__(self, text, x, y, font_size, bold=False):
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        if bold:
            self.fill = '#000'
            
    def render(self, xyoff):
        return self.fstr.format(
            round(self.x + xyoff[0]),
            round(self.y + xyoff[1]),
            self.font_size,
            self.fill,
            self.text,
    )


class SvgLine:
    fstr = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke-width="{}" stroke="{}" />'
    stroke_width = 0.9
    stroke = "#333"
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def render(self, xyoff):
        return self.fstr.format(
            round(self.x1 + xyoff[0], 1), 
            round(self.y1 + xyoff[1], 1), 
            round(self.x2 + xyoff[0], 1), 
            round(self.y2 + xyoff[1], 1),
            self.stroke_width,
            self.stroke
    )


class SvgRect:
    fstr = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="{}" stroke-width="{}" rx="{}" />'
    fill = '#fff'
    stroke = '#000'
    stroke_width = .05*UNIT
    def __init__(self, x, y, width, height, rx, bold=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        if bold:
            self.stroke_width = .3*UNIT
    def render(self, xyoff):
        return self.fstr.format(
        round(self.x + xyoff[0]),
        round(self.y + xyoff[1]),
        round(self.width),
        round(self.height),
        self.fill,
        self.stroke,
        self.stroke_width,
        self.rx,
    )


qrcode_defs = {
21: {
    'size': 21,
    'headers': 3,
    'align': None,
    'fontsize': 1.5*UNIT,
    'smallfont': 1*UNIT,
    },
25: {
    'size': 25,
    'headers': 5,
    'align': 16,
    'fontsize': 1.75*UNIT,
    'smallfont': 1.15*UNIT,
    },
29: {
    'size': 29,
    'headers': 6,
    'align': 20,
    'fontsize': 2*UNIT,
    'smallfont': 1.3*UNIT,
    }
}

def quietcells(gridsize):
    xys = []
    for i in range(7):
        xys.append((i, 7))
        xys.append((7, i))
        xys.append((i, gridsize-8))
        xys.append((gridsize-8, i))
        xys.append((gridsize-i-1, 7))
        xys.append((7, gridsize-i-1))
    xys.append((7, 7))
    xys.append((gridsize-8, 7))
    xys.append((7, gridsize-8))
    for tick in range(9, gridsize-9, 2):
        xys.append((tick, 6))
        xys.append((6, tick))
    return xys

def datacells(gridsize, alignment=None):
    xys = []
    for i in range(8, gridsize-8):
        for j in range(6):
            xys.append((i, j))
            xys.append((j, i))
    for x in range(7, gridsize):
        for y in range(7, gridsize):
            if x == 7 and y == 7:
                continue
            if x == 7 and y >= gridsize-8 or \
            y == 7 and x >= gridsize-8:
                continue
            if alignment and \
            alignment <= x < alignment+5 and \
            alignment <= y < alignment+5:
                continue
            xys.append((x, y))
    return xys 

def timingcells(gridsize):
    xys = []
    for tick in range(8, gridsize-8, 2):
        xys.append((tick, 6))
        xys.append((6, tick))
    return xys

def view_size_of_qrcode(gridsize, margin=0):
    left, header, right = margin, 2*UNIT, margin
    grid = qrcode_defs[gridsize]
    span = math.ceil(grid['size'] / grid['headers']) * UNIT
    width = left + header + span*grid['headers'] + right
    height = round(width * (297/210))
    return (width, height)

def mnemonic_template(numwords, size, suffix=None, margin=UNIT):
    assert numwords in (12, 24)
    header, sag = 2*UNIT, UNIT
    grid = qrcode_defs[size]
    width, height = view_size_of_qrcode(grid['size'], margin)
    span = math.ceil(grid['size'] / grid['headers']) * UNIT
    xoff = header + round((width - (header + span*grid['headers'])) / 2)
    yoff = sag + round((height - (header + span*grid['headers'])) / 2)
    font = grid['fontsize']

    if suffix == None:
        suffix = '{:d}w'.format(numwords)
    
    mnemonic = SvgG("Mnemonic" + suffix, [
        SvgRect(0, 0, width, height, UNIT)
    ])

    words = SvgG("Words" + suffix)
    space = font/1.6
    xlmt = grid['headers']*span+xoff
    y = yoff
    ystep = (span*grid['headers'])/13
    for i in range(0, 12):
        if i == 9: space = 0
        x0, x1 = xoff-header+space, (font/1.6)+xoff
        if i and i % 4 == 0: y += ystep
        if numwords == 12:
            words.extend([
                SvgText('{:d}.'.format(i+1), x0, y, font, True),
                SvgLine(x1, y, xlmt, y),
            ])
        elif numwords == 24:
            x2, x3, x4 = .46*width, .54*width, .54*width+header+font/1.6
            words.extend([
                SvgText('{:d}.'.format(i+1), x0, y, font, True),
                SvgLine(x1, y, x2, y),
                SvgText('{:d}.'.format(i+13), x3, y, font, True),
                SvgLine(x4, y, xlmt, y),
            ])
        y += ystep
    mnemonic.append(words)

    mnbody = (xoff-header, yoff-header, *[span*grid['headers']+header]*2) 
    msg = 'Never enter these words into a device\nthat connects to the internet.'
    notes = SvgGNotes(
        'MnNotes' + suffix, width, height, margin, 
        mnbody, font, msg, grid['smallfont']
    )
    mnemonic.append(notes)

    return mnemonic


def SvgGNotes(id_, width, height, margin, avoid_rect, font, msg, msgfont):
    
    x_key = .2*width, .6*width
    y_key = .02*height+margin, 3*UNIT

    #fp = str(b'\xf0\x9f\x90\xbe', 'utf-8')
    #fp = '\N{key}'
    fp = u'\u26bf'
    x_fp = .2*width+.4*font 
    y_fp = .02*height+margin+2*UNIT

    x_ft = margin, width-2*margin
    y_ft = .9*height-margin, .1*height-.1*margin

    star = '\u273d'
    x_star = margin+.4*font
    y_star = .9*height-margin+2*UNIT

    notes = SvgG(id_, [
        SvgRect(x_key[0], y_key[0], x_key[1], y_key[1], 1.5*UNIT, True),
        SvgText(fp, x_fp, y_fp, font),

        SvgRect(x_ft[0], y_ft[0], x_ft[1], y_ft[1], UNIT, True),
        SvgText(star, x_star, y_star, font),
    ])

    x_msg = width*.2
    y_msg = avoid_rect[1] + avoid_rect[3] + 1.2*msgfont

    longest_msg = max([len(m) for m in msg.split('\n')])
    for i, m in enumerate(msg.split('\n')):
        space = ((longest_msg - len(m)) / 2) * msgfont/1.6
        y_msg += 1.1*i*msgfont
        notes.append(SvgText(m, space + x_msg, y_msg, msgfont, True))
    return notes


def qrcode_template(size, suffix=None, margin=UNIT):
    grid = qrcode_defs[size]
    header, sag = 2*UNIT, UNIT
    width, height = view_size_of_qrcode(grid['size'], margin)
    span = math.ceil(grid['size'] / grid['headers']) * UNIT
    xoff = header + round((width - (header + span*grid['headers'])) / 2)
    yoff = sag + round((height - (header + span*grid['headers'])) / 2)

    if suffix == None:
        suffix = '{:d}x{:d}'.format(grid['size'], grid['size'])

    qrcode = SvgG("QRCode" + suffix, [
        SvgRect(0, 0, width, height, UNIT, bold=False)
    ])

    quiet = SvgG("Quiet" + suffix)
    for x, y in quietcells(grid['size']):
        quiet.append(SvgUse("D", x*UNIT+xoff, y*UNIT+yoff))
    qrcode.append(quiet)
    
    timing = SvgG("Timing" + suffix)
    for x, y in timingcells(grid['size']):
        timing.append(SvgUse("T", x*UNIT+xoff, y*UNIT+yoff))
    qrcode.append(timing)

    headers = SvgG("Headers" + suffix)
    font = grid['fontsize']
    for i in range(1, grid['headers']+1):
        headers.extend([
            SvgText(i, i*span -span*.6 +xoff, -UNIT+yoff, font, True),
            SvgText(chr(i + 64), -header+xoff, i*span -span*.4 +yoff, font, True),
        ])
    qrcode.append(headers)

    data = SvgG("Data" + suffix)
    for x, y in datacells(grid['size'], grid['align']):
        data.append(SvgUse("D", x*UNIT+xoff, y*UNIT+yoff))
    qrcode.append(data)

    guides = SvgG("Guides" + suffix)
    for i in range(0, grid['headers']+1):
        guides.extend([
            SvgLine(i*span+xoff, -header+yoff, i*span+xoff, grid['headers']*span+yoff),
            SvgLine(-header+xoff, i*span+yoff, grid['headers']*span+xoff, i*span+yoff),
        ])
    qrcode.append(guides)
    
    if grid['align']:
        alignment = SvgG("Alignment" + suffix)
        for i, j in zip(range(5,0,-2), range(grid['align'], grid['align']+3)):
            alignment.append(SvgUse('A%d' % i, j*UNIT+xoff, j*UNIT+yoff)) 
        qrcode.append(alignment)

    position = SvgG("Position" + suffix)
    for i, j in zip(range(7,2,-2), range(3)):
        position.extend([
            SvgUse("P%d" % i, j*UNIT+xoff, j*UNIT+yoff),
            SvgUse("P%d" % i, (grid['size']-7+j)*UNIT+xoff, j*UNIT+yoff),
            SvgUse("P%d" % i, j*UNIT+xoff, (grid['size']-7+j)*UNIT+yoff),
        ])
    qrcode.append(position)

    msg = 'Never scan this image into a device\nthat connects to the internet.'
    qrbody = (xoff-header, yoff-header, *[span*grid['headers']+header]*2) 
    notes = SvgGNotes(
        'QrNotes' + suffix, width, height, margin, 
        qrbody,font, msg, grid['smallfont']
    )
    qrcode.append(notes)

    return qrcode

def main(form_name):
    templates = {
        'sb12c': (12, 21),
        'sb12s': (12, 25),
        'sb24c': (24, 25),
        'sb24s': (24, 29),
    }
    margin = 0*UNIT 
    cursor_height = 0
    sub_margin = 2*UNIT
    largest = (0, 0)
    content = ''
    for name, (mnsize, qrsize) in templates.items():
        if name != form_name:
            continue

        width, height = view_size_of_qrcode(qrsize, sub_margin)
        content += mnemonic_template(mnsize, qrsize, '_%d'%mnsize, sub_margin).render((margin, margin))
        content += qrcode_template(qrsize, "_%d"%qrsize, sub_margin).render((width+margin, margin))
        cursor_height += height
            
    return Svg("100%", "100%", "0 0 {} {}".format(margin*2+width*2, margin*2+height), content)


if __name__ == '__main__':
    import sys
    page = main(sys.argv[1])
    print(page.render())
