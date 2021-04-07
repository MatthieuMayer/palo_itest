# -*- coding: utf-8 -*-

# ------------------------------------------ Module Imports & Definitions -------------------------------------------- #

# Standard package(s) import ----------------------------------------------------------------------
import os
import arxiv
from pdfminer.high_level import extract_text
import wordcloud as wcl
from gensim.summarization import keywords


# ------------------------------------------- Keywords Class Definition ---------------------------------------------- #
class Keywords:
    """Download paper given its arxiv id and perform keywords analysis.

    Parameters
    -------------------------------------------------------------------------------------
    paper_id: str
        The arxiv format id of the paper to analyze.
    n: int
        The number of keywords to extract from the paper content.

    Methods
    -------------------------------------------------------------------------------------
    dl_paper():
        Download pdf paper with 'paper_id' in working directory.
    wordcloud():
        Create a wordcloud of the most common words in paper.
    find_keywords():
        Find and return n keywords from the paper content.
    remove_pdf():
        Checks if pdf file exists and deletes it from working directory.
    """

    def __init__(self, paper_id, n=20):
        # arxiv format id of the paper
        self.paper_id = paper_id
        # name of the paper
        self.paper_name = paper_id + '.pdf'
        # extracted title of the paper
        self.paper_title = ''
        # extracted content of the paper
        self.paper_content = ''
        # the number of keywords to extract
        self.nb_keywords = n
        # the display element to return
        self.display = ''

    def dl_paper(self):
        """Download pdf paper with 'paper_id' in working directory."""
        # search paper id in arxiv list
        search = arxiv.Search(id_list=[self.paper_id])
        # get paper object
        paper = next(search.get())
        # extract paper title
        self.paper_title = paper.title
        # download paper as pdf
        paper.download_pdf(filename=self.paper_name)
        # load paper content
        self.paper_content = extract_text(self.paper_name)

    def wordcloud(self):
        """Create a wordcloud of the most common words in paper."""
        # create a WordCloud object
        wordcloud = wcl.WordCloud(background_color="white")
        # generate a word cloud
        wordcloud.generate(self.paper_content)
        # visualize the word cloud
        wordcloud.to_file('wordcloud.png')

    def find_keywords(self):
        """Find and return n keywords from the paper content."""
        # extract keywords from paper content
        values = keywords(text=self.paper_content, split='\n', scores=True)
        # extract n keywords from values
        main_kw = [val[0] for val in values][0:self.nb_keywords]
        # update display element to return for API
        self.display = "{} MAIN KEYWORDS FROM PAPER: \"{}\" <br/>".format(str(self.nb_keywords), self.paper_title)
        for i in range(len(main_kw)):
            self.display = self.display + "  #" + str(i + 1) + ". " + main_kw[i] + "<br/>"

    def remove_pdf(self):
        """Checks if pdf file exists and deletes it from working directory."""
        # current working directory
        cwd_path = os.getcwd()
        # if pdf_file in cwd_path
        if self.paper_name in os.listdir(cwd_path):
            # delete pdf file
            os.remove(self.paper_name)


# ------------------------------------------- Keywords Class main function ------------------------------------------- #
def main():
    # instantiate Keywords src
    paper_kw = Keywords('0704.0003', 20)
    # download paper for paper_kw instance
    paper_kw.dl_paper()
    # create and display wordcloud on paper
    paper_kw.wordcloud()
    # find main keywords from paper
    paper_kw.find_keywords()
    # display main keywords from paper
    print(paper_kw.display)
    # delete downloaded paper
    paper_kw.remove_pdf()


if __name__ == "__main__":
    main()
