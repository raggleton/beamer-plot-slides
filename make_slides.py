#!/usr/bin/env python
"""
This script outputs all the calibration plots in the ROOT file output by
runCalibration.py as one long pdf, cos TBrowser sucks.

It will make the PDF in the same directory as the ROOT file, under a directory
named output_<ROOT file stem>
"""


import glob
import os
import argparse
import subprocess
import beamer_slide_templates as bst
import json


def make_main_tex_file(frontpage_title='', subtitle='', author='',
                       main_tex_file='', slides_tex_file=''):
    """Generate main TeX file for set of slides, usign a template.

    Parameters
    ----------
    frontpage_title : str, optional
        Title for title slide
    subtitle : str, optional
        Subtitle for title slide
    main_tex_file : str, optional
        Filename for main TeX file to be written.
    slides_tex_file : str, optional
        Filename for slides file to be included.
    """
    with open("beamer_template.tex", "r") as template:
        with open(main_tex_file, "w") as f:
            substitute = {"@TITLE": frontpage_title, "@SUBTITLE": subtitle,
                          "@FILE": slides_tex_file, "@AUTHOR": author}
            for line in template:
                for k in substitute:
                    if k in line:
                        line = line.replace(k, substitute[k])
                f.write(line)


def make_slides(config_filename, do_compile_pdf=True):
    """Puts plots into one pdf.

    Parameters
    ----------
    config_filename : str
        Name of JSON config file
    do_compile_pdf : bool, optional
        Compile PDf
    """
    print "Using configuration file", config_filename
    with open(config_filename, "r") as fp:
        config_dict = json.load(fp)

    out_stem = "slides"
    main_file = out_stem + ".tex"
    slides_file = out_stem + "_input.tex"
    print "Writing to", main_file

    # Start beamer file - make main tex file
    # Use template - change title, subtitle, include file
    front_dict = config_dict['frontpage']
    make_main_tex_file(front_dict['title'], front_dict['subtitle'], front_dict['author'],
                       main_file, slides_file)

    # Now make the slides file to be included in main file
    with open(slides_file, "w") as slides:
        slides_dict = config_dict['slides']
        for slide in slides_dict:
            print "Writing slide"
            template = None
            num_plots = len(slide['plots'])
            if num_plots == 1:
                template = bst.one_plot_slide
            elif num_plots == 2:
                template = bst.two_plot_slide
            elif num_plots <= 4:
                template = bst.four_plot_slide
            elif num_plots <= 6:
                template = bst.six_plot_slide
            else:
                raise RuntimeError("Cannot make a slide with %d plots" % num_plots)
            slides.write(
                bst.make_slide(
                    slide_template=template,
                    slide_section=slide['title'],
                    slide_title=slide['title'],
                    plots=slide['plots']
                )
            )

    if do_compile_pdf:
        compile_pdf(main_file, num_compilations=2)  # compile twice to get page numbers correct


def compile_pdf(tex_filename, outdir=None, num_compilations=1, latex_cmd='lualatex', nonstop=False):
    """Compile the pdf. Deletes all non-tex/pdf files afterwards.

    Parameters
    ----------
    tex_filename : str
        Name of TeX file to compile
    outdir : str, optional
        Output directory for PDF file. Default is the same as that of the TeX file.
    num_compilations : int, optional
        Number of times to run tex command. Default is once.
    latex_cmd : str, optional
        Which latex command to run.
    nonstop : bool, optional
        If True, just ignore compilation errors where possible
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

    # Tidy up all the non .tex or .pdf files
    # outdir = outdir or os.path.dirname(os.path.abspath(tex_filename))
    # for f in glob.glob(os.path.join(outdir, tex_filename.replace(".tex", ".*"))):
    #     if os.path.splitext(f)[1] not in [".tex", ".pdf"]:
    #         print 'deleting', f
    #         os.remove(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="JSON configuration file")
    parser.add_argument("--noCompile", help="Don't compile PDF", action='store_true')
    args = parser.parse_args()

    make_slides(config_filename=args.config, do_compile_pdf=not args.noCompile)
