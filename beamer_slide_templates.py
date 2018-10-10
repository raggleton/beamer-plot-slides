"""
Templates for various beamer slides, like 4 plots, etc

Robin Aggleton 2015
"""


import re

only_title_slide = \
r"""
\begin{frame}
\vfill
\centering
\huge @SLIDE_TITLE
\vfill
\end{frame}
"""


zero_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{center}
@PLOT1TITLE
\end{center}
@BOTTOMTEXT
\end{frame}
"""

one_plot_width = 0.5
one_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=%g\textwidth]{@PLOT1}
\\
\end{center}
@BOTTOMTEXT
\end{frame}
""" % (one_plot_width)

two_plot_width = 0.45
two_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{%g\textwidth}
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=\textwidth]{@PLOT1}
\\
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT2TITLE
\\
\includegraphics[width=\textwidth]{@PLOT2}
\end{center}
\end{column}
\end{columns}
@BOTTOMTEXT
\end{frame}
""" % tuple([two_plot_width]*2)

three_plot_width = 0.33
three_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{%g\textwidth}
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=\textwidth]{@PLOT1}
\\
\end{center}
\end{column}
\begin{column}{%g\textwidth}
\begin{center}
@PLOT2TITLE
\\
\includegraphics[width=\textwidth]{@PLOT2}
\\
\end{center}
\end{column}
\begin{column}{%g\textwidth}
\begin{center}
@PLOT3TITLE
\\
\includegraphics[width=\textwidth]{@PLOT3}
\\
\end{center}
\end{column}
\end{columns}
@BOTTOMTEXT
\end{frame}
""" % tuple([three_plot_width]*3)

four_plot_width = 0.23
four_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{%g\textwidth}
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=\textwidth]{@PLOT1}
\\
@PLOT3TITLE
\\
\includegraphics[width=\textwidth]{@PLOT3}
\\
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT2TITLE
\\
\includegraphics[width=\textwidth]{@PLOT2}
\\
@PLOT4TITLE
\\
\includegraphics[width=\textwidth]{@PLOT4}
\\
\end{center}
\end{column}
\end{columns}
@BOTTOMTEXT
\end{frame}
""" % tuple([four_plot_width]*2)

six_plot_width = 0.22
six_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{%g\textwidth}
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=\textwidth]{@PLOT1}
\\
@PLOT4TITLE
\\
\includegraphics[width=\textwidth]{@PLOT4}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT2TITLE
\\
\includegraphics[width=\textwidth]{@PLOT2}
\\
@PLOT5TITLE
\\
\includegraphics[width=\textwidth]{@PLOT5}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT3TITLE
\\
\includegraphics[width=\textwidth]{@PLOT3}
\\
@PLOT6TITLE
\\
\includegraphics[width=\textwidth]{@PLOT6}
\end{center}
\end{column}
\end{columns}
@BOTTOMTEXT
\end{frame}
""" % tuple([six_plot_width]*3)

eight_plot_width = 0.22
eight_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{%g\textwidth}
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=\textwidth]{@PLOT1}
\\
@PLOT5TITLE
\\
\includegraphics[width=\textwidth]{@PLOT5}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT2TITLE
\\
\includegraphics[width=\textwidth]{@PLOT2}
\\
@PLOT6TITLE
\\
\includegraphics[width=\textwidth]{@PLOT6}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT3TITLE
\\
\includegraphics[width=\textwidth]{@PLOT3}
\\
@PLOT7TITLE
\\
\includegraphics[width=\textwidth]{@PLOT7}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT4TITLE
\\
\includegraphics[width=\textwidth]{@PLOT4}
\\
@PLOT8TITLE
\\
\includegraphics[width=\textwidth]{@PLOT8}
\end{center}
\end{column}
\end{columns}
@BOTTOMTEXT
\end{frame}
""" % tuple([eight_plot_width]*4)

ten_plot_width = 0.18
ten_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=\textwidth]{@PLOT1}
\\
@PLOT6TITLE
\\
\includegraphics[width=\textwidth]{@PLOT6}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT2TITLE
\\
\includegraphics[width=\textwidth]{@PLOT2}
\\
@PLOT7TITLE
\\
\includegraphics[width=\textwidth]{@PLOT7}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT3TITLE
\\
\includegraphics[width=\textwidth]{@PLOT3}
\\
@PLOT8TITLE
\\
\includegraphics[width=\textwidth]{@PLOT8}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT4TITLE
\\
\includegraphics[width=\textwidth]{@PLOT4}
\\
@PLOT9TITLE
\\
\includegraphics[width=\textwidth]{@PLOT9}
\end{center}
\end{column}

\begin{column}{%g\textwidth}
\begin{center}
@PLOT5TITLE
\\
\includegraphics[width=\textwidth]{@PLOT5}
\\
@PLOT10TITLE
\\
\includegraphics[width=\textwidth]{@PLOT10}
\end{center}
\end{column}

\end{columns}
@BOTTOMTEXT
\end{frame}
""" % tuple([ten_plot_width]*5)


def make_slide(slide_template, slide_section, slide_title, plots, top_text=None, bottom_text=None):
    """
    Create slide contents.

    Parameters
    ----------
    slide_template : str
        Slide template
    slide_section : str
        Slide section
    slide_title : str
        Slide title
    plots : list[(str, str)]
        Filename and optional title for each plot
    top_text : str, optional

    bottom_text : str, optional

    Returns
    -------
    str
        Slide contents
    """

    slide = slide_template.replace("@SLIDE_TITLE", slide_title)
    slide = slide.replace("@SLIDE_SECTION", slide_section)
    top_text = top_text or ""
    slide = slide.replace("@TOPTEXT", top_text)
    bottom_text = bottom_text or ""
    slide = slide.replace("@BOTTOMTEXT", bottom_text)
    # Go backwards since we want to replace "PLOT10" before "PLOT1"
    for i in range(len(plots), 0, -1):
        plot_filename, plot_title = plots[i-1]
        slide = slide.replace("@PLOT"+str(i)+"TITLE", plot_title)
        slide = slide.replace("@PLOT"+str(i), plot_filename)

    # cleanup incase we have leftover unused figures
    slide = re.sub(r"@PLOT\dTITLE", "", slide)
    slide = re.sub(r"\\includegraphics\[.*\]{@PLOT\d}", "", slide)  # to avoid "missing .tex file" error
    slide = re.sub(r"\\\\\n\n", "", slide)  # remove useless line breaks
    slide = slide.replace("\n\n\\\\", "\\\\")
    slide = re.sub(r"}\\\\\n", "}\n", slide)
    return slide
