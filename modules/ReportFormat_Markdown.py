#! /usr/bin/env python3
'''
Implementation of the "ReportFormat" module in Markdown
'''
from ReportFormat import ReportFormat
import ViReport_GlobalContext as GC
from datetime import datetime
from os import chdir,getcwd,makedirs
from pdf2image import convert_from_path
from shutil import move
from subprocess import call
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

    def write(s, text_type='normal'):
        md_init(); GC.report_out_md.write(s); GC.report_out_md.write('\n')

    def writeln(s, text_type='normal'):
        md_init(); ReportFormat_Markdown.write(s, text_type=text_type); ReportFormat_Markdown.write('')

    def figure(filename, caption=None, width=None, height=None):
        if not filename.startswith(GC.OUT_DIR_REPORTFILES):
            raise ValueError("Figures must be in report files directory: %s" % GC.OUT_DIR_REPORTFILES)
        if filename.lower().endswith('.pdf'):
            png_filename = '%s.%s' % ('.'.join(filename.split('.')[:-1]), 'png')
            convert_from_path(filename, 500)[0].save(png_filename, 'PNG')
            filename = png_filename
        GC.report_out_md.write('\n\n<img src="%s"' % filename.replace(GC.OUT_DIR,'.'))
        if width is not None or height is not None:
            GC.report_out_md.write(' width="auto" height="auto" style="')
            if width is not None:
                GC.report_out_md.write('max-width:%d%%;' % int(width*100))
            if height is not None:
                GC.report_out_md.write('max-height:%d%%;' % int(height*100))
            GC.report_out_md.write('"')
        GC.report_out_md.write('>\n')
        #if caption is not None:
        #    GC.report_out_md.write("\\caption{%s}\n" % tex_safe(caption))
        GC.report_out_md.write('\n')

    def close():
        md_init()
        GC.report_out_md.close()
        return GC.report_out_md_filename
