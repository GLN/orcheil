
from instrument import Instrument
import const

class Part(object):
    
    def __init__(self, data, index, palette, show_dynamic, show_register):
        self.data = data  # music21 part data
        self.index = index
        self.palette = palette
        self.show_dynamic = show_dynamic
        self.show_register = show_register
    
    def opacity(self, note, range):
        '''Return an opacity multiplier using note location in instrument range.
           A lower note is more opaque, a higher note is more transparent.'''
        # convert to zero-base
        highest = range[1] - range[0]
        pitch = note.pitches[0].midi  # if note is a chord, use lowest note
        pitch = pitch - range[0]
        # calc opacity
        opacity = float(pitch) / float(highest)
        opacity = round(opacity, 3)
        opacity = 1.0 - opacity  # invert
        return opacity
    
    def path(self, color, opacity, width, x1, x2, y):
        '''Return a dictionary containing data for an SVG path.'''        
        d = 'M {} {} h {}'.format(x1, y, x2)  # SVG structure: 'M x1 y h x2'
        path = {}
        path['d'] = d
        path['opacity'] = opacity  # register
        path['stroke'] = color
        path['stroke_width'] = const.STROKE_WIDTH * width  # dynamic
        return path
    
    def paths(self):
        '''Return a list of dictionaries, one SVG path per note.'''
        paths = []
        x1 = 0.0
        x2 = 0.0
        y = self.y_coordinate()
        # create and identify instrument
        instrument = Instrument(self.data, self.palette)
        # determine instrument color
        color = instrument.color()
        # determine instrument range
        range = instrument.range()
        # flatten and filter for note, chord, and rest
        notes = self.data.flat.notesAndRests
        # delimit stream by rest
        notes = notes.findConsecutiveNotes()                
        # create SVG paths -- this loop must be efficient
        for note in notes:
            if note is not None:  # i.e. if note is not a rest
                # dynamic
                if self.show_dynamic is True:
                    width = self.width(note)
                else:
                    width = 1.0
                # register
                if self.show_register is True:
                    opacity = self.opacity(note, range)
                else:
                    opacity = 1.0
                # path start
                x1 = note.offset
                # path finish
                x2 = note.duration.quarterLength
                # create SVG path
                path = self.path(color, opacity, width, x1, x2, y)
                # composite path
                paths.append(path)
        return paths
    
    def visualize(self):
        '''Create and return a part visualization, including metadata.'''
        visualization = {}
        visualization['name'] = self.data.partName
        visualization['paths'] = self.paths()
        return visualization
    
    def width(self, note):
        '''Return a width multiplier using note volume.
           A quieter note is narrower, a louder note is wider.'''
        volume = note.volume.getRealized()
        # round volume to nearest step, e.g. nearest 0.125
        volume = (round(volume * const.DYNAMIC_RESOLUTION) / const.DYNAMIC_RESOLUTION)
        return volume
    
    def y_coordinate(self):
        '''Calculate and return the y coordinate for an SVG path.'''
        return const.Y_INDENT + (const.STROKE_WIDTH * self.index) + (const.GAP * self.index)
