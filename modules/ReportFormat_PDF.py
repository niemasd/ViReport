#! /usr/bin/env python3
'''
Implementation of the "ReportFormat" module using LaTeX to create a PDF
'''
from ReportFormat import ReportFormat
import ViReport_GlobalContext as GC
from datetime import datetime
from os import chdir,getcwd,makedirs
from shutil import move
from subprocess import call
GC.report_out_tex = None

def tex_init():
    if GC.report_out_tex is None:
        GC.report_tmp_dir = "%s/report_files" % GC.OUT_DIR_TMPFILES
        makedirs(GC.report_tmp_dir, exist_ok=True)
        GC.report_out_tex_filename = "%s/main.tex" % GC.report_tmp_dir
        GC.report_out_tex = open(GC.report_out_tex_filename, 'w')
        GC.report_out_tex.write("\\documentclass{article}")
        GC.report_out_tex.write("\\title{\\vspace{-2.0cm}ViReport}\n")
        GC.report_out_tex.write("\\author{Niema Moshiri}\n")
        GC.report_out_tex.write("\\date{%s}\n" % datetime.today().strftime('%Y-%m-%d'))
        GC.report_out_tex.write("\\begin{document}\n\\maketitle\n")

class ReportFormat_PDF(ReportFormat):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def section(s):
        tex_init(); GC.report_out_tex.write("\\section{%s}\n" % s)

    def subsection(s):
        tex_init(); GC.report_out_tex.write("\\subsection{%s}\n" % s)

    def write(s, text_type='normal'):
        tex_init(); GC.report_out_tex.write(s)

    def writeln(s, text_type='normal'):
        tex_init(); ReportFormat_PDF.write(s, text_type=text_type); ReportFormat_PDF.write('\n')

    def close():
        tex_init()
        GC.report_out_tex.write("\n\\end{document}\n")
        GC.report_out_tex.close()
        orig_dir = getcwd()
        chdir(GC.report_tmp_dir)
        command = ['pdflatex', GC.report_out_tex_filename]
        f = open('%s/command.txt' % GC.report_tmp_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        log = open('%s/log.txt' % GC.report_tmp_dir, 'w')
        call(command, stdout=log)
        log.close()
        chdir(orig_dir)
        pdf_filename = '%s/Report.pdf' % GC.OUT_DIR
        move('%s.pdf' % GC.report_out_tex_filename.rstrip('.tex'), pdf_filename)
        return pdf_filename
