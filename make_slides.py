#!/usr/bin/env python


"""
Produce a beamer PDF from various PDF images & text.
See example/configuration.json for how to specify a configuration.
Output file will be produced in same dir as the configuration JSON.

Run:

    ./make_slides.py <your_configuration.json>

"""


import glob
import os
import argparse
import subprocess
import beamer_slide_templates as bst
import json
from sys import platform as _platform


def make_main_tex_file(template_filename, frontpage_title='', subtitle='', author='',
                       main_tex_file='', slides_tex_file=''):
    """Generate main TeX file for set of slides, usign a template.

    Parameters
    ----------
    template_filename : str
        Name of beamer texmplate tex file
    frontpage_title : str, optional
        Title for title slide
    subtitle : str, optional
        Subtitle for title slide
    main_tex_file : str, optional
        Filename for main TeX file to be written.
    slides_tex_file : str, optional
        Filename for slides file to be included.
    """
    with open(template_filename, "r") as template:
        with open(main_tex_file, "w") as f:
            substitute = {"@TITLE": frontpage_title, "@SUBTITLE": subtitle,
                          "@FILE": slides_tex_file, "@AUTHOR": author}
            for line in template:
                for k in substitute:
                    if k in line:
                        line = line.replace(k, substitute[k])
                f.write(line)


def make_slides_tex_file(slides_tex_file, slides_dict):
    """Generate TeX file for slides contents

    Parameters
    ----------
    slides_tex_file : str
        Filename for slides TeX file to be written
    slides_dict : dict
        Dict of slides contents
    """
    with open(slides_tex_file, "w") as slides:
        for slide in slides_dict:
            print "Writing slide"
            template = None
            num_plots = len(slide.get('plots', ''))
            if num_plots == 1:
                template = bst.one_plot_slide
            elif num_plots == 2:
                template = bst.two_plot_slide
            elif num_plots == 3:
                template = bst.three_plot_slide
            elif num_plots <= 4:
                template = bst.four_plot_slide
            elif num_plots <= 6:
                template = bst.six_plot_slide
            else:
                raise RuntimeError("Cannot make a slide with %d plots" % num_plots)
            slides.write(
                bst.make_slide(
                    slide_template=template,
                    slide_section=slide.get('title', ''),
                    slide_title=slide.get('title', ''),
                    plots=slide.get('plots', ''),
                    top_text=slide.get('toptext', ''),
                    bottom_text=slide.get('bottomtext', '')
                )
            )


def make_slides(template_filename, config_filename):
    """Puts plots into one pdf.

    Parameters
    ----------
    template_filename : str
        Name of beamer texmplate tex file
    config_filename : str
        Name of JSON config file

    Returns
    -------
    str
        Main TeX filename
    """
    print "Using configuration file", config_filename
    with open(config_filename, "r") as fp:
        config_dict = json.load(fp)

    out_stem = os.path.splitext(config_filename)[0] + "_slides"
    main_file = out_stem + ".tex"
    slides_file = out_stem + "_input.tex"
    print "Writing to", main_file

    # Start beamer file - make main tex file
    # Use template - change title, subtitle, include file
    front_dict = config_dict['frontpage']
    print "Using template file", template_filename
    make_main_tex_file(template_filename,
                       front_dict.get('title', ''),
                       front_dict.get('subtitle', ''),
                       front_dict.get('author', ''),
                       main_file, slides_file)

    # Now make the slides file to be included in main file
    make_slides_tex_file(slides_tex_file=slides_file, slides_dict=config_dict['slides'])
    return main_file


def compile_pdf(tex_filename, outdir=None,
                latex_cmd='lualatex', num_compilations=1,
                nonstop=False, cleanup=True):
    """Compile the pdf. Deletes all non-tex/pdf files afterwards.

    Parameters
    ----------
    tex_filename : str
        Name of TeX file to compile
    outdir : str, optional
        Output directory for PDF file. Default is the same as that of the TeX file.
    latex_cmd : str, optional
        Which latex command to run.
    num_compilations : int, optional
        Number of times to run tex command. Default is once.
    nonstop : bool, optional
        If True, just ignore compilation errors where possible
    cleanup : bool, optional
        If True, remove all the non text/pdf files that latex produced
    """
    args = ["nice", "-n", "19", latex_cmd]
    if nonstop:
        args.extend(["-interaction", "nonstopmode"])
    if outdir is not None:
        args.append("-output-directory=%s" % outdir)
    args.append(tex_filename)
    print 'Compiling PDF with'
    print ' '.join(args)

    for i in range(num_compilations):
        subprocess.call(args)

    if cleanup:
        for ext in ['.toc', '.snm', '.out', '.nav', '.log', '.aux']:
            basename = os.path.splitext(tex_filename)[0]
            this_file = basename + ext
            if os.path.isfile(this_file):
                print "rm", this_file
                os.remove(this_file)


def open_pdf(pdf_filename):
    """Open a PDF file using system's default PDF viewer."""
    if _platform.startswith("linux"):
        # linux
        subprocess.call(["xdg-open", pdf_filename])
    elif _platform == "darwin":
        # OS X
        subprocess.call(["open", pdf_filename])
    elif _platform == "win32":
        # Windows
        subprocess.call(["start", pdf_filename])



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="JSON configuration file")
    parser.add_argument("--template", help="Template beamer tex file", default="beamer_template.tex")
    parser.add_argument("--noCompile", help="Don't compile PDF", action='store_true')
    parser.add_argument("--noCleanup", help="Don't remove auxiliary aux/toc/log etc", action='store_true')
    parser.add_argument("--open", help="Open PDF", action='store_true')
    args = parser.parse_args()

    tex_file = make_slides(template_filename=args.template, config_filename=args.config)

    if not args.noCompile:
        compile_pdf(tex_file,
                    outdir=os.path.dirname(os.path.abspath(tex_file)),
                    num_compilations=2,  # compile twice to get page numbers correct
                    cleanup=not args.noCleanup)

    if args.open:
        open_pdf(tex_file.replace(".tex", ".pdf"))
