
import re

from music21 import text

from palette import Palette

ID_RANGE_MAP = {
    # CORE INSTRUMENTATION
    'picc': (74, 102),
    'fl'  : (59, 96),
    'ob'  : (58, 91),
    'eh'  : (52, 81),
    'cl'  : (50, 94),
    'bn'  : (34, 75),
    'cbn' : (22, 53),
    'hn'  : (34, 77),
    'tpt' : (55, 82),
    'tbn' : (40, 72),
    'tba' : (28, 58),
    'timp': (40, 55),
    'hp'  : (24, 103),
    'pf'  : (21, 108),
    'cel' : (60, 108),            
    'vln1': (55, 103),
    'vln2': (55, 103),
    'vla' : (48, 91),
    'vc'  : (36, 76),
    'cb'  : (28, 67),
    'v'   : (41, 84),  # composite range, bass to soprano
    # EXTENDED INSTRUMENTATION
    'sax' : (36, 88),  # composite range, baritone to soprano
    'bell': (60, 77),
    'mar' : (45, 96),
    'vib' : (53, 89),
    'xyl' : (65, 108),
    'hpd' : (29, 89),
    'org' : (24, 96)
}

# regex-identifier map (language support: EN, FR, IT, DE)
# source: https://ccrma.stanford.edu/~unjung/ins.html
# source: https://imslp.org/wiki/IMSLP:Abbreviations_for_Instruments
# except: castanets, cymbal, drum, triangle from Boosey & Hawkes standard
# except: tam-tam (t-t) from GLN

REGEX_ID_MAP = [
    # CORE INSTRUMENTATION
    # picc -- EN, DE, IT
    (r'\bpicc|\botta', 'picc'),
    # picc -- FR, DE, IT
    # fl, alto fl -- EN, FR, DE, IT
    (r'\bfl[uûöa]u?t|\baltf', 'fl'),
    # ob -- EN, FR, DE, IT
    (r'\bobo[ei]|\bhaut', 'ob'),
    # cor ang -- EN, FR, DE, IT
    (r'\b[aei]ngl', 'eh'),
    # cl, bass cl -- EN, FR, DE, IT
    (r'\b[ck]lar|\bba(ss|ß)klar', 'cl'),
    # bn -- EN, FR, DE, IT
    (r'\bbasso[on]|\bfag', 'bn'),
    # cbn -- EN, FR, DE, IT
    (r'\bcontr[ae]basso[on]|\b[ck]ontraf', 'cbn'),
    # hn -- EN, FR, DE, IT
    (r'\b[ch]orn?o?', 'hn'),
    # tpt -- EN, FR, DE, IT
    (r'\btr[ou]m[bp][ae]', 'tpt'),
    # tbn, bass tbn -- EN, FR, DE, IT
    (r'\btrombo|\bpos', 'tbn'),
    # tba -- EN, FR, DE, IT
    (r'\btuba', 'tba'),
    # timp -- EN, FR, DE, IT
    (r'\btim[bp]a[ln][ei]s?|\bpauk', 'timp'),
    # perc -- EN, FR, DE, IT
    (r'\bper|\bbat|\bschl', 'perc'),
    # drum & tambourine -- EN, FR, DE, IT
    (r'\bdru|\bcai|\btromm|\bcass|\btamb', 'dr'),
    # cymbal -- EN, FR, DE, IT
    (r'\bcym|\bbeck|\bpiat', 'cym'),
    # hp -- EN, FR, DE, IT
    (r'\bh?ar[fp]a?e?', 'hp'),
    # pf -- EN, FR, DE, IT
    (r'\bpian|\bklavie', 'pf'),
    # cel-- EN, FR, DE, IT
    (r'\bc[eé]le', 'cel'),
    # vln1 -- EN, FR, DE, IT
    (r'\bviol[io]n[eos]?($|\s(i|1))\b|\bgeige($ \
       |\s(i|1))\b', 'vln1'),
    # vln2 -- EN, FR, DE, IT
    (r'\bviol[io]n[eos]?\s?(ii|2)\b|\bgeige\s?(ii|2)\b', 'vln2'),
    # vla -- EN, FR, DE, IT
    (r'\bviol[ae]|\balto|\bbrat', 'vla'),
    # vc -- EN, FR, DE, IT
    (r'cell', 'vc'),    
    # cb -- EN, FR, DE, IT
    (r'\bbass|\bdoub|\bupr|\b[ck]ontr[ae]b[aä](ss|ß)e?o?', 'cb'),
    # EXTENDED INSTRUMENTATION
    # saxophone -- EN, FR, DE, IT
    (r'\bsa(x|ss)o', 'sax'),
    # castanets -- EN, FR, DE, IT
    (r'\b[ck]ast', 'cast'),
    # chimes & glock -- EN, FR, DE, IT
    (r'\b[cg]lo|\bchim|\bjeu|\bcam|\btub[ou]|\bbel|\brohr|\bmeta', 'bell'),
    # marimba
    (r'\bmari', 'mar'),
    # tam-tam
    (r'\btam[-t]', 't-t'),    
    # triangle
    (r'\btri', 'tgl'),
    # vibraphone
    (r'\bvib', 'vib'),    
    # xylophone
    (r'\bx[iy]l', 'xyl'),    
    # harpsichord -- EN, FR, DE, IT
    (r'\bharpsi|\bclav[ei]c|\bcem', 'hpd'),
    # organ -- EN, FR, DE, IT
    (r'\borg[aeu]', 'org')
]

class Instrument(object):
    
    def __init__(self, data, palette):
        self.identifier = self.identifier(data)  # part data
        self.palette = palette
    
    def color(self):
        """Return color of instrument in palette."""
        return {
            'choir': Palette.choir(self.identifier),
            'dolan': Palette.dolan(self.identifier),
            'instrument': Palette.instrument(self.identifier),
            'monochrome': Palette.monochrome()
        }.get(self.palette, Palette.monochrome())  # default to monochrome
    
    def identifier(self, data):
        """Return a unique identifier for an instrument."""
        identifier = None
        if len(text.assembleLyrics(data)) > 0:
            # lyrics present in part, so assume it's a voice part
            identifier = "v"
        else:
            # lyrics not present in part, so derive identifier from instr name
            name = data.getInstrument().bestName()
            for regex, identifier in REGEX_ID_MAP:
                if re.search(regex, name, re.IGNORECASE):
                    # break on first match
                    break
        return identifier
    
    def range(self):
        """Return range of instrument in MIDI note number format."""
        return ID_RANGE_MAP.get(self.identifier, (0, 127))  # default to max
