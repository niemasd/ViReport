#! /usr/bin/env python3
'''
Implementation of the "ReportFormat" module in Markdown
'''
from ReportFormat import ReportFormat
import ViReport_GlobalContext as GC
from datetime import datetime
from os.path import isfile
GC.report_out_md = None

def md_init():
    if GC.report_out_md is None:
        GC.report_out_md_filename = '%s/Report.md' % GC.OUT_DIR
        GC.report_out_md = open(GC.report_out_md_filename, 'w')
        GC.report_out_md.write("# ViReport v%s &mdash; %s\n" % (GC.VIREPORT_VERSION, datetime.today().strftime('%Y-%m-%d')))

class ReportFormat_Markdown(ReportFormat):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def section(s):
        md_init(); GC.report_out_md.write("\n## %s\n" % s)

    def subsection(s):
        md_init(); GC.report_out_md.write("\n### %s\n" % s)

    def write(s):
        md_init(); GC.report_out_md.write(s)

    def writeln(s):
        md_init(); ReportFormat_Markdown.write(s); ReportFormat_Markdown.write('\n\n')

    def bullets(items, level=0):
        md_init()
        if level == 0:
            GC.report_out_md.write('\n')
        for item in items:
            if isinstance(item, str):
                GC.report_out_md.write('%s* %s\n' % (level*'    ', item))
            elif isinstance(item, list):
                ReportFormat_Markdown.bullets(item, level=level+1)
            else:
                raise ValueError("Invalid bullet item type: %s" % type(item))
        if level == 0:
            GC.report_out_md.write('\n')

    def figure(filename, caption=None, width=None, height=None, keep_aspect_ratio=True):
        if not filename.startswith(GC.OUT_DIR_REPORTFILES):
            raise ValueError("Figures must be in report files directory: %s" % GC.OUT_DIR_REPORTFILES)
        if filename.lower().endswith('.pdf'):
            png_filename = '%s.%s' % ('.'.join(filename.split('.')[:-1]), 'png')
            if not isfile(png_filename):
                GC.pdf_to_png(filename, png_filename)
            filename = png_filename
        GC.report_out_md.write('\n\n<figure>\n<img src="%s"' % filename.replace(GC.OUT_DIR,'.'))
        if width is not None or height is not None:
            GC.report_out_md.write(' width="auto" height="auto" style="')
            if width is not None:
                GC.report_out_md.write('max-width:%d%%;' % int(width*100))
            if height is not None:
                GC.report_out_md.write('max-height:%d%%;' % int(height*100))
            GC.report_out_md.write('"')
        GC.report_out_md.write('>\n')
        if caption is not None:
            GC.report_out_md.write('<figcaption>%s</figcaption>\n' % caption)
        GC.report_out_md.write('</figure>\n\n\n')

    def close():
        md_init()
        GC.report_out_md.close()
        return GC.report_out_md_filename
