#! /usr/bin/env python3
'''
Implementation of the "ReportFormat" module in HTML
'''
from ReportFormat import ReportFormat
import ViReport_GlobalContext as GC
from datetime import datetime
from os.path import isfile
from pdf2image import convert_from_path
GC.report_out_html = None

def html_init():
    if GC.report_out_html is None:
        GC.report_out_html_filename = '%s/Report.html' % GC.OUT_DIR
        GC.report_out_html = open(GC.report_out_html_filename, 'w')
        GC.report_out_html.write('<!DOCTYPE html>\n<html>\n<body>\n<h1>ViReport v%s &mdash; %s</h1>\n<p>\n' % (GC.VIREPORT_VERSION, datetime.today().strftime('%Y-%m-%d')))

class ReportFormat_HTML(ReportFormat):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def section(s):
        html_init(); GC.report_out_html.write("\n</p>\n<h2>%s</h2>\n<p>\n" % s)

    def subsection(s):
        html_init(); GC.report_out_html.write("\n</p>\n<h3>%s</h3>\n<p>\n" % s)

    def write(s, text_type='normal'):
        html_init(); GC.report_out_html.write(s); GC.report_out_html.write(' ')

    def writeln(s, text_type='normal'):
        html_init(); ReportFormat_HTML.write(s, text_type=text_type); ReportFormat_HTML.write('<br>\n')

    def bullets(items, level=0):
        html_init()
        GC.report_out_html.write('\n%s<ul>\n' % ('  '*level))
        for item in items:
            if isinstance(item, str):
                GC.report_out_html.write('%s  <li>%s</li>\n' % (level*'  ', item))
            elif isinstance(item, list):
                ReportFormat_HTML.bullets(item, level=level+1)
            else:
                raise ValueError("Invalid bullet item type: %s" % type(item))
        GC.report_out_html.write('\n%s</ul>\n' % ('  '*level))

    def figure(filename, caption=None, width=None, height=None):
        if not filename.startswith(GC.OUT_DIR_REPORTFILES):
            raise ValueError("Figures must be in report files directory: %s" % GC.OUT_DIR_REPORTFILES)
        if filename.lower().endswith('.pdf'):
            png_filename = '%s.%s' % ('.'.join(filename.split('.')[:-1]), 'png')
            if not isfile(png_filename):
                convert_from_path(filename, size=2000)[0].save(png_filename, 'PNG')
            filename = png_filename
        GC.report_out_html.write('\n</p>\n\n<figure>\n<img src="%s"' % filename.replace(GC.OUT_DIR,'.'))
        if width is not None or height is not None:
            GC.report_out_html.write(' width="auto" height="auto" style="')
            if width is not None:
                GC.report_out_html.write('max-width:%d%%;' % int(width*100))
            if height is not None:
                GC.report_out_html.write('max-height:%d%%;' % int(height*100))
            GC.report_out_html.write('"')
        GC.report_out_html.write('>\n')
        if caption is not None:
            GC.report_out_html.write('<figcaption>%s</figcaption>\n' % caption)
        GC.report_out_html.write('</figure>\n\n<p>\n')

    def close():
        html_init()
        GC.report_out_html.write('\n</p>\n</body>\n</html>\n')
        GC.report_out_html.close()
        return GC.report_out_html_filename
