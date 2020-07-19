
class Color(object):
    
    # source: Google's Material Design
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
    
    DOLAN_PERC = '#211F1F'
    DOLAN_TIMP = '#5E3B1B'
    DOLAN_TPT = '#E62831'
    DOLAN_HN = '#F59333'
    DOLAN_FL = '#BB77A2'
    DOLAN_OB = '#2676B8'
    DOLAN_CL = '#224892'
    DOLAN_BN = '#624189'
    DOLAN_VLN_1 = '#8DC14A'
    DOLAN_VLN_2 = '#7BA647'
    DOLAN_VLA = '#189E4E'
    DOLAN_VC = '#0E7447'
    DOLAN_CB = '#0C683A'


class Palette(object):
    
    @staticmethod
    def choir(identifier):
        '''Return color from choir palette for instrument identifier.'''
        return {
            # CORE INSTRUMENTATION
            'picc': Color.SILVER,
            'fl'  : Color.SILVER,
            'ob'  : Color.SILVER,
            'eh'  : Color.SILVER,
            'cl'  : Color.SILVER,
            'bn'  : Color.SILVER,
            'cbn' : Color.SILVER,
            'hn'  : Color.GOLD,
            'tpt' : Color.GOLD,
            'tbn' : Color.GOLD,
            'tba' : Color.GOLD,
            'timp': Color.LIGHT_BLUE,
            'perc': Color.LIGHT_BLUE,
            'dr'  : Color.LIGHT_BLUE,
            'cym' : Color.LIGHT_BLUE,
            'hp'  : Color.BLACK,
            'pf'  : Color.BLACK,
            'cel' : Color.BLACK,
            'vln1': Color.ORANGE,
            'vln2': Color.ORANGE,
            'vla' : Color.ORANGE,
            'vc'  : Color.ORANGE,
            'cb'  : Color.ORANGE,
            'v'   : Color.PINK,
            # EXTENDED INSTRUMENTATION
            'sax' : Color.SILVER,
            'cast': Color.LIGHT_BLUE,
            'bell': Color.LIGHT_BLUE,
            'mar' : Color.LIGHT_BLUE,
            't-t' : Color.LIGHT_BLUE,
            'tgl' : Color.LIGHT_BLUE,
            'vib' : Color.LIGHT_BLUE,
            'xyl' : Color.LIGHT_BLUE,
            'hpd' : Color.BLACK,
            'org' : Color.BLACK
        }.get(identifier, Color.GRAY)  # default to Color.GRAY

    @staticmethod
    def dolan(identifier):
        '''Return color from dolan palette for instrument identifier.'''
        return {
            'fl'  : Color.DOLAN_FL,
            'ob'  : Color.DOLAN_OB,
            'cl'  : Color.DOLAN_CL,
            'bn'  : Color.DOLAN_BN,
            'hn'  : Color.DOLAN_HN,
            'tpt' : Color.DOLAN_TPT,
            'timp': Color.DOLAN_TIMP,
            'perc': Color.DOLAN_PERC,
            'vln1': Color.DOLAN_VLN_1,
            'vln2': Color.DOLAN_VLN_2,
            'vla' : Color.DOLAN_VLA,
            'vc'  : Color.DOLAN_VC,
            'cb'  : Color.DOLAN_CB,
        }.get(identifier, Color.GRAY)  # default to Color.GRAY
    
    @staticmethod
    def instrument(identifier):
        """Return color from instrument palette for instrument identifier."""
        return {
            # CORE INSTRUMENTATION
            'picc': Color.SILVER,
            'fl'  : Color.SILVER,
            'ob'  : Color.BLACK,
            'eh'  : Color.BLACK,
            'cl'  : Color.BLACK,
            'bn'  : Color.PURPLE,
            'cbn' : Color.PURPLE,
            'hn'  : Color.GOLD,
            'tpt' : Color.GOLD,
            'tbn' : Color.GOLD,
            'tba' : Color.GOLD,
            'timp': Color.BROWN,
            'perc': Color.LIGHT_BLUE,
            'dr'  : Color.BROWN,
            'cym' : Color.GOLD,
            'hp'  : Color.GOLD,
            'pf'  : Color.BLACK,
            'cel' : Color.BROWN,
            'vln1': Color.ORANGE,
            'vln2': Color.ORANGE,
            'vla' : Color.ORANGE,
            'vc'  : Color.ORANGE,
            'cb'  : Color.ORANGE,
            'v'   : Color.PINK,
            # EXTENDED INSTRUMENTATION
            'sax' : Color.GOLD,
            'cast': Color.BROWN,
            'bell': Color.SILVER,
            'mar' : Color.BROWN,
            't-t' : Color.GOLD,
            'tgl' : Color.SILVER,
            'vib' : Color.SILVER,
            'xyl' : Color.BROWN,
            'hpd' : Color.BROWN,
            'org' : Color.SILVER
        }.get(identifier, Color.GRAY)  # default to Color.GRAY
    
    @staticmethod
    def monochrome():
        '''Return single color.'''
        return Color.BLUE
