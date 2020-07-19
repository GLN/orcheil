
# color (from Google's Material Design)
DYNAMIC_RESOLUTION = 8  # ppp, pp, p, mp, mf, f, ff, fff
MEASURE_RESOLUTION = 5  # show every fifth measure number

AMBER = '#FFC107'
BLACK = '#212121'
BLUE = '#2196F3'
BROWN = '#795548'
CYAN = '#00BCD4'
GOLD = '#FFD600'
GRAY = '#9E9E9E'
LIGHT_BLUE = '#03A9F4'
ORANGE = '#FF9800'
PINK = '#E91E63'
PURPLE = '#9C27B0'
SILVER = '#607D8B'

# instrument-color map (language support: EN, FR, IT, DE)

INSTR_COLOR_MAP = [
    
    # CORE INSTRUMENTATION
    
    # picc -- EN, DE, IT
    (r'\bpicc|\botta', SILVER),
    # picc -- FR, DE, IT
    # fl, alto fl -- EN, FR, DE, IT
    (r'\bfl[uûöa]u?t|\baltf', SILVER),
    # ob -- EN, FR, DE, IT
    (r'\bobo[ei]|\bhaut', BLACK),
    # cor ang -- EN, FR, DE, IT
    (r'\b[aei]ngl', BLACK),
    # cl, bass cl -- EN, FR, DE, IT
    (r'\b[ck]lar|\bba(ss|ß)klar', BLACK),
    # bn -- EN, FR, DE, IT
    (r'\bbasso[on]|\bfag', PURPLE),
    # cbn -- EN, FR, DE, IT
    (r'\bcontr[ae]basso[on]|\b[ck]ontraf', PURPLE),
    # hn -- EN, FR, DE, IT
    (r'\b[ch]orn?o?', GOLD),
    # tpt -- EN, FR, DE, IT
    (r'\btr[ou]m[bp][ae]', GOLD),
    # tb, bass tb -- EN, FR, DE, IT
    (r'\btrombo|\bpos', GOLD),
    # tuba -- EN, FR, DE, IT
    (r'\btuba', GOLD),
    # timp -- EN, FR, DE, IT
    (r'\btim[bp]a[ln][ei]s?|\bpauk', BROWN),
    # perc -- EN, FR, DE, IT
    (r'\bper|\bbat|\bschl', LIGHT_BLUE),
    # drum & tambourine -- EN, FR, DE, IT
    (r'\bdru|\bcai|\btromm|\bcass|\btamb', BROWN),
    # cymbal -- EN, FR, DE, IT
    (r'\bcym|\bbeck|\bpiat', GOLD),
    # hp -- EN, FR, DE, IT
    (r'\bh?ar[fp]a?e?', GOLD),
    # pf -- EN, FR, DE, IT
    (r'\bpian|\bklavie', BLACK),
    # cel-- EN, FR, DE, IT
    (r'\bc[eé]le', BROWN),
    # vln, vla, vc -- EN, FR, DE, IT
    (r'\bviol|\bgeig|\balto|\bbrat|\bcell', ORANGE),
    # cb -- EN, FR, DE, IT
    (r'\bbass|\bdoub|\bupr|\b[ck]ontr[ae]b[aä](ss|ß)e?o?', ORANGE),
    
    # EXTENDED INSTRUMENTATION

    # sax -- EN, FR, DE, IT
    (r'\bsa(x|ss)o', GOLD),
    # castanets -- EN, FR, DE, IT
    (r'\b[ck]ast', BROWN),
    # chimes & glock -- EN, FR, DE, IT
    (r'\b[cg]lo|\bchim|\bjeu|\bcam|\btub[ou]|\bbel|\brohr|\bmeta', SILVER),
    # marimba
    (r'\bmari', BROWN),
    # tam-tam
    (r'\btam[-t]', GOLD),    
    # triangle
    (r'\btri', SILVER),
    # vibraphone
    (r'\bvib', SILVER),    
    # xylophone
    (r'\bx[iy]l', BROWN),    
    # harpsichord -- EN, FR, DE, IT
    (r'\bharpsi|\bclav[ei]c|\bcem', BROWN),
    # organ -- EN, FR, DE, IT
    (r'\borg[aeu]', SILVER)
]

# layout

GAP = 4
STROKE_WIDTH = 20
GAP = 2
STROKE_WIDTH = 16
TEXT_HEIGHT = STROKE_WIDTH
Y_INDENT = STROKE_WIDTH / 2

SINGLE_DIGIT = '0.1875em'  # 3/16 em
DOUBLE_DIGIT = '0.3750em'  # 6/16 em
TRIPLE_DIGIT = '0.5625em'  # 9/16 em
