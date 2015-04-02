import ConfigParser
import os
import os.path
from flask import Flask, request, url_for, render_template, abort

class DRTCController(object):

    def __init__(self):
        self.config = None

    def readConfig(self):
        if not self.config:
            self.config = ConfigParser.SafeConfigParser()
            self.filepath = os.path.join(os.getcwd(), 'coldbrew.cfg')
            self.config.read(self.filepath)

    def drtc(self):
        return render_template('DRTC/drtc.html')

    def drtc_page(self, filename):
        return render_template('DRTC/' + filename + '.html')

