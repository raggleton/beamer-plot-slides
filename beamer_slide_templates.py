"""
Templates for various beamer slides, like 4 plots, etc

Robin Aggleton 2015
"""


import re

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

one_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=0.7\textwidth]{@PLOT1}
\\
\end{center}
@BOTTOMTEXT
\end{frame}
"""

two_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{0.5\textwidth}
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=\textwidth]{@PLOT1}
\\
\end{center}
\end{column}

\begin{column}{0.5\textwidth}
\begin{center}
@PLOT2TITLE
\\
\includegraphics[width=\textwidth]{@PLOT2}
\end{center}
\end{column}
\end{columns}
@BOTTOMTEXT
\end{frame}
"""

three_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{0.33\textwidth}
\begin{center}
@PLOT1TITLE
\\
\includegraphics[width=\textwidth]{@PLOT1}
\\
\end{center}
\end{column}
\begin{column}{0.33\textwidth}
\begin{center}
@PLOT2TITLE
\\
\includegraphics[width=\textwidth]{@PLOT2}
\\
\end{center}
\end{column}
\begin{column}{0.33\textwidth}
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
"""

four_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{0.3\textwidth}
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

\begin{column}{0.3\textwidth}
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
"""

six_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{0.3\textwidth}
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

\begin{column}{0.3\textwidth}
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

\begin{column}{0.3\textwidth}
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
"""

eight_plot_slide = \
r"""
\section{@SLIDE_SECTION}
\begin{frame}{@SLIDE_TITLE}
@TOPTEXT
\begin{columns}
\begin{column}{0.24\textwidth}
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

\begin{column}{0.24\textwidth}
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

\begin{column}{0.24\textwidth}
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

\begin{column}{0.24\textwidth}
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
"""


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
    for i, (plot_filename, plot_title) in enumerate(plots):
            slide = slide.replace("@PLOT"+str(i+1)+"TITLE", plot_title)
            slide = slide.replace("@PLOT"+str(i+1), plot_filename)

    # cleanup incase we have leftover unused figures
    slide = re.sub(r"@PLOT\dTITLE", "", slide)
    slide = re.sub(r"\\includegraphics\[.*\]{@PLOT\d}", "", slide)  # to avoid "missing .tex file" error
    slide = re.sub(r"\\\\\n\n", "", slide)  # remove useless line breaks
    slide = slide.replace("\n\n\\\\", "\\\\")
    slide = re.sub(r"}\\\\\n", "}\n", slide)
    return slide
