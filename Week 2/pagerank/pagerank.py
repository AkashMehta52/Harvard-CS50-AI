import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
       sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #create return dictionary
    returnDict = dict.fromkeys(corpus.keys(), 0)
    #first check if page has no outgoing links:
    if(len(corpus[page]) == 0):
        count = len(corpus)
        for pages in corpus:
            returnDict[pages] = ((1-damping_factor)/count)
        #print(returnDict)
        return returnDict
    #now do the math and create the return dict:
    else:
        count = len(corpus)
        #initial probability of links
        for keys in corpus[page]:
            returnDict[keys] = (damping_factor/len(corpus[page]))
        for pages in corpus:
            if pages not in returnDict:
                returnDict[pages] = ((1-damping_factor)/count)
            else:
                initialVal = returnDict[pages]
                returnDict[pages] = initialVal + ((1-damping_factor)/count)
        #print(returnDict)
        return returnDict
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #corpus = dictionary that maps page name to set of all pages linked to by that page
    #n = integer representing number of samples generated to estimate pagerank values
    #create return dictionary:
    returnDict = dict.fromkeys(corpus.keys(), 0)
    #each key maps to a value representing that page's pageRank
    #first sample from choosing from a page at random:
    firstSample = random.choices(list(corpus.keys()), k = 1)[0]
    #increment first sample
    returnDict[firstSample] += 1
    #get transition probabilities:
    transitionProb = transition_model(corpus, firstSample, damping_factor)
    #iterate through the rest of n!
    for i in range(n-1):
        #get the new sample using random and weights from transition probabilities
        sample = random.choices(list(transitionProb.keys()), k = 1, weights = list(transitionProb.values()))[0]
        returnDict[sample] += 1
        transitionProb = transition_model(corpus, sample, damping_factor)
    
    #calculate page rank by iterating over dictionaries and altering keys
    for key in returnDict:
        num = returnDict[key]
        returnDict[key] = num / n
    
    return returnDict
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #create return Dict
    returnDict = dict.fromkeys(corpus.keys(), 1.0/len(corpus))

    #in following formula, there's a constant in each page's rank
    baseRank = (1 - damping_factor) / len(corpus)
    for key in corpus:
        returnDict[key] = baseRank

    #copy corpus and modify so it fits specification:
    corpusCopy = copy.deepcopy(corpus)
    for key in corpusCopy:
        if (len(corpusCopy[key]) == 0):
            corpusCopy[key] = set(corpusCopy.keys())

    #create change transition var:
    threshold = True
    #iterate while threshold holds!
    while threshold:
        #use our prior distribution to ensure changes are above threshold!
        priorDistribution = copy.deepcopy(returnDict)
        for page in corpus:
            #link weight
            linkW = 0
            #summation portion of formula translated
            for pageCheck in corpus:
                if(page in corpus[pageCheck]):
                    linkW += returnDict[pageCheck] / len(corpus[pageCheck])
            #add summation to return:)

            returnDict[page] = (damping_factor * linkW) + baseRank
            #once changes are precise, set threshold to false!
            threshold = (abs(priorDistribution[page] - returnDict[page]) > 0.0001)

    #check to verify code!
    total = 0
    for page in returnDict:
        total += returnDict[page]
    #print("should be 1: ", total)     
    
    return returnDict
    #raise NotImplementedError


if __name__ == "__main__":
    main()
