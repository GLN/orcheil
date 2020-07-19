#!/usr/bin/env python3

# file: orcheil.py
# desc: an app for the visualization of orchestration
# auth: Gregory Lee Newsome, greg.newsome@utoronto.ca

# to run on localhost, cd to parent dir of this file, then type in terminal:
# export FLASK_APP=orcheil.py
# export FLASK_DEBUG=1
# flask run
# visit http://localhost:5000/ in a web browser

# import
# --------------------------------------------------------------------------- #

import os, tempfile

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_uploads import configure_uploads, patch_request_class, UploadNotAllowed, UploadSet
from music21 import converter, text

import const as c
import secret  # module not under version control to keep secret.key private

# config
# --------------------------------------------------------------------------- #

# config app
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = secret.key

# config host
application = app  # for islandhosting's passenger_wsgi file

# config upload
app.config['UPLOADED_FILES_DEST'] = 'tmp'
files = UploadSet('files', ('musicxml', 'mxl', 'xml'))
configure_uploads(app, files)
patch_request_class(app)  # set maximum file upload size to default of 16MB

# run
if __name__ == '__main__':
    app.run()

# flask
# --------------------------------------------------------------------------- #

@app.route('/', methods=['GET', 'POST'])
def upload():
    '''Render index page and handle file upload and parsing.'''
    if request.method == 'POST' and 'musicxml' in request.files:
        # save file, if possible
        try:
            # create unique subdir in tmp for each request
            subdir = tempfile.mkdtemp(dir=app.config['UPLOADED_FILES_DEST'])
            # extract subdir from absolute path
            subdir = os.path.basename(os.path.normpath(subdir))
            # save file to subdir (filename = subdir/filename)
            filename = files.save(request.files['musicxml'], folder=subdir)
        except UploadNotAllowed:
            # file-type error, or no file present
            flash('You must choose a .musicxml, .mxl, or .xml file.')
            return redirect(url_for('upload'))
        # file save successful, so continue
        palette_name = request.form.get('palette')
        # parse file, if possible
        try:
            score = Score(filename, palette_name)
        except Exception as e:
            # parse error
            flash('music21 exception: {}'.format(e))
            return redirect(url_for('upload'))
        # file parse successful, so continue
        visualization = score.visualize()
        # clean up
        os.remove(os.path.join(app.config['UPLOADED_FILES_DEST'], filename))
        os.rmdir(os.path.join(app.config['UPLOADED_FILES_DEST'], subdir))
        # render result page
        return render_template('result.html', score=visualization)
    else:
        # render upload page
        return render_template('upload.html')

@app.route('/faq')
def faq():
    '''Render FAQ page.'''
    return render_template('faq.html')

# orcheil
# --------------------------------------------------------------------------- #

class Palette(object):
    
    def complementary(self, index):
        '''Two-color complementary palette, with a variant for each.'''
        index %= 4  # 4 is the color count for this palette
        return {
            0 : c.LIGHT_BLUE,
            1 : c.AMBER,
            2 : c.CYAN,
            3 : c.ORANGE
        }.get(index)
    
    def instrument(self, data):
        '''Derive a color from part data.'''
        if len(text.assembleLyrics(data)) > 0:
            # lyrics are present in part, so assume it's a voice part
            color = c.PINK
        else:
            # lyrics are not present in part, so derive color from instr name
            instr = data.getInstrument().bestName()
            for regex, color in c.INSTR_COLOR_MAP:
                if re.search(regex, instr, re.IGNORECASE):
                    # break on first match
                    break
        return color
    
    def monochrome(self, index):
        '''Two-color monochrome palette.'''
        index %= 2  # 2 is the color count for this palette
        return {
            0 : c.LIGHT_BLUE,
            1 : c.CYAN
        }.get(index)


class Part(object):
    
    def __init__(self, color, data, index):
        self.color = color
        self.data = data  # music21 part data
        self.index = index
    
    def path_with_distance(self, x1, x2):
        '''Return a dictionary containing data for an SVG path.'''
        d = ''  # SVG path structure: 'M x1 y h x2'
        d += 'M '  # move to point
        d += str(x1) + ' '  # left x coordinate
        d += str(self.y_coordinate()) + ' '  # y coordinate
        d += 'h '  # horizontal lineto, relative
        d += str(x2)  # right x coordinate
        path = {}
        path['d'] = d
        path['opacity'] = 1.0
        path['stroke'] = self.color
        path['stroke_width'] = c.STROKE_WIDTH
        return path
    
    def paths(self):
        '''Return a list of dictionaries, each containing data for an SVG path.'''
        draw = False
        paths = []
        x1 = 0.0
        x2 = 0.0
        # flatten and filter for note, chord, and rest
        notes = self.data.flat.notesAndRests
        # delimit stream by rest
        notes = notes.findConsecutiveNotes()
        # append a trailing None to ensure the final path is created
        notes.append(None)
        # create SVG path
        for note in notes:
            if note is not None:
                if draw is False:
                    # path start
                    x1 = note.offset
                    # reset
                    draw = True
                # path accumulate to next rest (None)
                x2 += note.duration.quarterLength
            else:
                # create path
                path = self.path_with_distance(x1, x2)
                # save path
                paths.append(path)
                # reset
                draw = False
                x2 = 0.0
        return paths
    
    def visualize(self):
        '''Create and return a part visualization, including metadata.'''
        visualization = {}
        visualization['name'] = self.data.partName
        visualization['paths'] = self.paths()
        return visualization
    
    def y_coordinate(self):
        '''Calculate and return the y coordinate for an SVG path.'''
        return c.Y_INDENT + (c.STROKE_WIDTH * self.index) + (c.GAP * self.index)


class Score(object):
    
    def __init__(self, filename, palette):
        self.data = None  # music21 score data
        self.filename = filename  # can also be a path
        self.palette = palette
    
    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, filename):
        self._filename = filename
        # parse file and keep the result in "data"
        path = os.path.join(app.config['UPLOADED_FILES_DEST'], filename)
        self.data = converter.parse(path, format='musicxml')
    
    def height(self, part_count):
        '''Calculate and return the height for the SVG element.'''
        return (c.STROKE_WIDTH * part_count) + (c.GAP * (part_count - 1))
        
        return (const.STROKE_WIDTH * part_count) + (const.GAP * (part_count - 1)) + const.TEXT_HEIGHT
    
    def measure(self, number, text_length, x, y):
        '''Return a dictionary containing data for a measure.'''        
        measure = {}
        measure['number'] = number
        measure['text_length'] = text_length
        measure['x'] = x
        measure['y'] = y
        return measure
    
    def measures(self):
        '''Return a list of dictionaries, one per measure.
           This is solely for creating and positioning measure numbers.'''
        measure_map = self.data.measureOffsetMap()
        measures = []
        x = 0.0
        y = self.height(len(self.data.parts))  # height of SVG element
        for key, value in measure_map.items():
            uppermost_measure = value[0]  # value = list of measures with same #
            number = uppermost_measure.number
            x = key  # key is the measure offset
            # draw measure number, include 1 but not 0 (i.e. partial measure)
            if number % const.MEASURE_RESOLUTION is 0 and number is not 0 or number is 1:
                number = str(number)
                text_length = self.text_length(number)
                measure = self.measure(number, text_length, x, y)
                measures.append(measure)
        return measures
    
    def parts(self):
        '''Return a list of part visualizations.'''
        palette = Palette()
        parts = []
        for index, data in enumerate(self.data.parts):
            # create color
            color = None
            if self.palette == 'complementary':
                color = palette.complementary(index)
            if self.palette == 'instrument':
                color = palette.instrument(data)
            if self.palette == 'monochrome':
                color = palette.monochrome(index)
            # if color is None, use default
            color = c.GRAY if color is None else color
            # create part
            part = Part(color, data, index)
            # visualize part and keep the result
            parts.append(part.visualize())
        return parts
    
    def text_length(self, number):
        '''Return an SVG text length for a given number length.
           This is the container size for a measure number, to mitigate scaling.'''
        return {
            1: const.SINGLE_DIGIT,
            2: const.DOUBLE_DIGIT,
            3: const.TRIPLE_DIGIT
        }.get(len(number), '0.75em')  # default to 0.75em, i.e. 12/16 em
    
    def visualize(self):
        '''Create and return a score visualization, including metadata.'''
        visualization = {}
        visualization['filename'] = os.path.split(self.filename)[-1]  # last
        visualization['height'] = self.height(len(self.data.parts))
        visualization['measures'] = self.measures()
        visualization['parts'] = self.parts()
        visualization['release'] = int(self.data.highestTime)
        return visualization
