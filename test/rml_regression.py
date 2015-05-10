# coding: utf-8
import sys
from glob import glob
from os import chdir, getcwd
from os.path import abspath, dirname, join, split, splitext
from tempfile import mkdtemp
from shutil import rmtree
from subprocess import Popen, PIPE
from StringIO import StringIO
from PIL import Image, ImageChops

BASE_DIR = dirname(dirname(abspath(__file__)))
PKG_DIR = BASE_DIR
RML_DIR = join(BASE_DIR, 'rmls')


def render_png(pdf_string):
    args = ['gs', '-dNOPAUSE', '-sDEVICE=pngalpha', '-q', '-r96',
            '-sOutputFile=-', '-']
    gs_proc = Popen(args, stdin=PIPE, stdout=PIPE)
    gs_proc.stdin.write(pdf_string)
    gs_proc.stdin.close()
    return Image.open(StringIO(gs_proc.stdout.read()))


class RmlRegessionTester:
    sys.path.insert(0, PKG_DIR)
    trml2pdf = __import__('trml2pdf')

    def __init__(self):
        self.saved_cwd = getcwd()
        chdir(RML_DIR)
        self.work_path = '/tmp' # mkdtemp()

    def __del__(self):
        # rmtree(self.work_path)
        chdir(self.saved_cwd)

    def process_rml_files(self):
        for rml_path in glob('*.rml'):
            self.process_rml_file(rml_path)
        
    def process_rml_file(self, rml_path):
        ref_png = self.render_reference(rml_path)
        gen_png = self.render_generated(rml_path)
        diff = ImageChops.difference(ref_png, gen_png)
        print diff.getbbox()
        ref_png.save(join('/tmp', rml_path+'_ref.png'))
        gen_png.save(join('/tmp', rml_path+'_gen.png'))
        diff.save(join('/tmp', rml_path+'_diff.png'))

    def render_reference(self, rml_path):
        ref_pdf_path = splitext(rml_path)[0]+'.pdf'
        return render_png(open(ref_pdf_path, 'rb').read())

    def render_generated(self, rml_path):
        generated_pdf = self.trml2pdf.parseString(open(rml_path, 'rb').read())
        return render_png(generated_pdf)

        
        
        
RmlRegessionTester().process_rml_files()

# print list(list_rmls())
