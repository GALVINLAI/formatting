"""
Normalize titles at various levels
"""

import re
import pytest
from latex_linter.remove_extra_newlines import remove_extra_newlines

# TODO Xu Tianyi's LaTeX code. Attempt customization of environment adaptation https://raw.githubusercontent.com/tonyxty/fermat/master/CSA.tex

def capitalize_titles(content):
    """
    Capitalize the first letter of titles in a given LaTeX document content (such as \\part, \\chapter, \\section, etc.).
    
    Args:
        content (str): The document content containing LaTeX titles.
    
    Returns:
        str: The processed document content with capitalized titles.
    
    Note:
        - This function uses regular expressions to match and process titles in the document.
        - The content following the title is treated as a single string and stripped of leading and trailing whitespace and trailing punctuation.
        - The first letter of each word in the title (except for specified exception words) is capitalized.
        - Specific acronyms (all uppercase and at least 2 letters long) are left unchanged.
        - The content following the title is wrapped in {} and followed by a newline.
    """
    
    exceptions = {
        "a", "an", "the", "aboard", "about", "abt.", "above", "abreast", "absent", "across", "after", "against", "along",
        "aloft", "alongside", "amid", "amidst", "mid", "midst", "among", "amongst", "anti", "apropos", "around", "round",
        "as", "aslant", "astride", "at", "atop", "ontop", "bar", "barring", "before", "B4", "behind", "below", "beneath",
        "neath", "beside", "besides", "between", "'tween", "beyond", "but", "by", "chez", "circa", "c.", "ca.", "come",
        "concerning", "contra", "counting", "cum", "despite", "spite", "down", "during", "effective", "ere", "except",
        "excepting", "excluding", "failing", "following", "for", "from", "in", "including", "inside", "into", "less",
        "like", "minus", "modulo", "mod", "near", "nearer", "nearest", "next", "notwithstanding", "of", "o'", "off",
        "offshore", "on", "onto", "opposite", "out", "outside", "over", "o'er", "pace", "past", "pending", "per", "plus",
        "post", "pre", "pro", "qua", "re", "regarding", "respecting", "sans", "save", "saving", "short", "since", "sub",
        "than", "through", "thru", "throughout", "thruout", "till", "times", "to", "t'", "touching", "toward", "towards",
        "under", "underneath", "unlike", "until", "unto", "up", "upon", "versus", "vs.", "v.", "via", "vice", "vis-à-vis",
        "wanting", "with", "w/", "w.", "c̄", "within", "w/i", "without", "'thout", "w/o", "abroad", "adrift", "aft",
        "afterward", "afterwards", "ahead", "apart", "ashore", "aside", "away", "back", "backward", "backwards",
        "beforehand", "downhill", "downstage", "downstairs", "downstream", "downward", "downwards", "downwind", "east",
        "eastward", "eastwards", "forth", "forward", "forwards", "heavenward", "heavenwards", "hence", "henceforth",
        "here", "hereby", "herein", "hereof", "hereto", "herewith", "home", "homeward", "homewards", "indoors", "inward",
        "inwards", "leftward", "leftwards", "north", "northeast", "northward", "northwards", "northwest", "now", "onward",
        "onwards", "outdoors", "outward", "outwards", "overboard", "overhead", "overland", "overseas", "rightward",
        "rightwards", "seaward", "seawards", "skywards", "skyward", "south", "southeast", "southwards", "southward",
        "southwest", "then", "thence", "thenceforth", "there", "thereby", "therein", "thereof", "thereto", "therewith",
        "together", "underfoot", "underground", "uphill", "upstage", "upstairs", "upstream", "upward", "upwards", "upwind",
        "west", "westward", "westwards", "when", "whence", "where", "whereby", "wherein", "whereto", "wherewith", "although",
        "because", "considering", "given", "granted", "if", "lest", "once", "provided", "providing", "seeing", "so", "supposing",
        "though", "unless", "whenever", "whereas", "wherever", "while", "whilst", "ago", "according to", "as regards", "counter to",
        "instead of", "owing to", "pertaining to", "at the behest of", "at the expense of", "at the hands of", "at risk of",
        "at the risk of", "at variance with", "by dint of", "by means of", "by virtue of", "by way of", "for the sake of", "for sake of",
        "for lack of", "for want of", "from want of", "in accordance with", "in addition to", "in case of", "in charge of", "in compliance with",
        "in conformity with", "in contact with", "in exchange for", "in favor of", "in front of", "in lieu of", "in light of", "in the light of",
        "in line with", "in place of", "in point of", "in quest of", "in relation to", "in regard to", "with regard to", "in respect to",
        "with respect to", "in return for", "in search of", "in step with", "in touch with", "in terms of", "in the name of", "in view of",
        "on account of", "on behalf of", "on grounds of", "on the grounds of", "on the part of", "on top of", "with a view to", "with the exception of",
        "à la", "a la", "as soon as", "as well as", "close to", "due to", "far from", "in case", "other than", "prior to", "pursuant to",
        "regardless of", "subsequent to", "as long as", "as much as", "as far as", "by the time", "in as much as", "inasmuch", "in order to",
        "in order that", "even", "provide that", "if only", "whether", "whose", "whoever", "why", "how", "or not", "whatever", "what", "both",
        "and", "or", "not only", "but also", "either", "neither", "nor", "just", "rather", "no sooner", "such", "that", "yet", "is", "it"
    }
    
    def capitalize(match):
        """
        Format the matched text, including stripping leading and trailing whitespace, converting multiple whitespace characters to a single space, and capitalizing the first letter of each word (excluding specific words).
        
        Args:
            match: A match object containing the matched text from the original string.
        
        Returns:
            str: The formatted string, including the text before the match, the processed text, and a newline.
        
        """
        text = match.group(2).strip()  # Strip leading and trailing whitespace
        text = text.rstrip(" .,;:!。，；：！")  # Strip trailing punctuation
        text = re.sub(r'\s+', ' ', text)  # Convert internal multiple whitespace characters to a single space

        # Capitalize the first letter of each word in the content
        words = text.split()
        capitalized_words = [
            # Process the first word, if it is already all uppercase, leave it unchanged; otherwise, capitalize its first letter. The key point is not to exclude exceptions.
            words[0] if words[0].isupper() else words[0].capitalize()
        ] + [
            # Process subsequent words. If the word is in the exceptions list, or is all uppercase, or is an all-uppercase acronym (matched by the regular expression ^[A-Z]{2,}$), leave it unchanged; otherwise, capitalize its first letter.
            word if word.lower() in exceptions or word.isupper() or re.match(r'^[A-Z]{2,}$', word) else word.capitalize() for word in words[1:]
        ]
        capitalized_text = ' '.join(capitalized_words)

        begin = re.sub(r'\s*', '', match.group(1).strip())

        return '\n\n' + begin + '{' + capitalized_text + '}\n\n'

    # Note that this line uses greedy mode. The valid premise is that, for example, \section{title} is followed by a new line.
    content = re.sub(r'(\s*(?:\\part|\\chapter|\\section|\\subsection|\\subsubsection|\\paragraph|\\subparagraph)\s*\*?\s*)\{(.*)\}\s*', capitalize, content)
    content = remove_extra_newlines(content)

    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("\section{introduction}", "\n\section{Introduction}\n\n"),
        ("  \subsection {related work}  ", "\n\subsection{Related Work}\n\n"),
        ("  \subsubsection *  {the importance of AI}", "\n\subsubsection*{The Importance of AI}\n\n"),
        ("\section*{abstract}", "\n\section*{Abstract}\n\n"),
        ("\chapter{summary and conclusions}", "\n\chapter{Summary and Conclusions}\n\n"),
        ("\paragraph{this is a test}", "\n\paragraph{This is a Test}\n\n"),
        ("\section{A simple test}", "\n\section{A Simple Test}\n\n"),
        ("\section{NASA and the future}", "\n\section{NASA and the Future}\n\n"),
#        (r"\subsection{use of iPhones in research}", r"\subsection{Use of iPhones in Research}\n\n"),
    ]
)
def test_capitalize_titles(input_text, expected_output):
    assert capitalize_titles(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])