#!/usr/bin/env python

"""
This script takes a list of plot names, and list of dirs, and compares each plot amongst all dirs.

Usage:

    ./compare_dirs.py myPlots.pdf --dir "thisDir" --dir "anotherDir" --plotname "met.pdf" --plotname "jet_pt.pdf"
"""


import os
import argparse
import make_slides as ms
import json


def create_json_contents(args):
    """Create the JSON dict to be passed to make_slides.py"""
    json_dict = {
        'frontpage': {
            "title": "Plot comparison",
            "subtitle": "",
            "author": ""
        },
        'slides': []
    }

    for plot in args.plotname:
        this_dict = {"title": plot}
        plot_entries = [[os.path.join(this_dir, plot), ""] for this_dir in args.dir]
        this_dict['plots'] = plot_entries
        json_dict['slides'].append(this_dict)
    
    return json_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="Output PDF filename")
    parser.add_argument("--dir", help="Directory to get plot from. Can be used multiple times", action="append")
    parser.add_argument("--plotname", help="Filename of plot. Can be used multiple times", action="append")
    parser.add_argument("--template", help="Template beamer tex file", default="beamer_template.tex")
    parser.add_argument("--noCompile", help="Don't compile PDF", action='store_true')
    parser.add_argument("--noCleanup", help="Don't remove auxiliary aux/toc/log etc", action='store_true')
    parser.add_argument("--quiet", help="Run in batch mode and remove most of spurioius printout", action='store_true')
    parser.add_argument("--open", help="Open PDF", action='store_true')
    args = parser.parse_args()

    # create a JSON config
    json_dict = create_json_contents(args)

    temp_json = os.path.splitext(args.output)[0] + ".json"
    with open(temp_json, "w") as f:
        f.write(json.dumps(json_dict, indent=4))
    
    # This is horrible FIXME
    new_args = [temp_json]
    new_args.append('--template=' + args.template)
    for name in ['noCompile', 'noCleanup', 'quiet', 'open']:
        if vars(args)[name]:
            new_args.append("--"+name)

    # run the main program as usual
    ms.main(new_args)

    # cleanup JSON
    os.remove(temp_json)
