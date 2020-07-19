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
from music21 import converter, volume

from part import Part
import const
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
        palette = request.form.get('palette')
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
        parts = []
        for index, data in enumerate(self.data.parts):
            # create part
            part = Part(data, index, self.palette, self.show_dynamic, self.show_register)
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
