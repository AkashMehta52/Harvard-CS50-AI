from typing import KeysView
import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    #Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    #should accept a directory name
    #create empty dictionary
    contents = {}
    #use current directory to access the corpus
    curDir = os.getcwd()
    #join curDir with directory name to access contents
    newDir = os.path.join(curDir, directory)
    #list filenames(x) in directory
    for x in os.listdir(newDir):
        #extract txt file and put into name
        fileDir = os.path.join(newDir, x)
        fileOpen = open(fileDir, "r", encoding="utf8")
        contents[x] = fileOpen.read()

    return contents
    #raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    documentWords = []
    #document is a string, return list of all words in order and lowercase
    docLower = document.lower()
    docTok = nltk.word_tokenize(docLower)
    for word in docTok:
        if (word not in string.punctuation) and (word not in nltk.corpus.stopwords.words("english")):
            documentWords.append(word)
    
    return documentWords
    #raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    #compute idfs returns a dictionary mapping words to their idf values!
    #the return dict should map every word that appears in at least one of the docs
    #idf is the naturallog for the number of docs divided by the #docs in which the word appears
    numDocs = {}
    #first step, find the number of docs each word exists in!
    for doc in documents.values():
        usedInDoc = []
        for word in doc:
            if word not in usedInDoc:
                usedInDoc.append(word)
                if word not in numDocs.keys():
                    numDocs[word] = 1
                else:
                    numDocs[word] += 1
    
    lenDocs = len(documents)

    idfVals = {}
    for wordKey in numDocs.keys():
        idfVals[wordKey] = math.log(lenDocs/numDocs[wordKey])
    
    return idfVals


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #idf values of files to sort by later
    fileIdf = {}
    #first, compute idfs for files
    for docFile in files.keys():
        idfVal = 0 
        for words in query:
            idfVal += files[docFile].count(words) * idfs[words]
        fileIdf[docFile] = idfVal
    
    #now, sort files by idf value(greatest first)
    sortedFiles = sorted(fileIdf.items(), key=lambda idf: idf[1], reverse=True)
    sortedFileNames = [x[0] for x in sortedFiles]
    
    #return top n files
    return sortedFileNames[0:n]        



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    #get a dict of tuples, with sentence as key and matching word measure
    #and query term density as the tuple the key corresponds to!
    
    rankMeasure = {}
    for sentence in sentences.keys():
        wordsInQ = query.intersection(sentences[sentence])
        termDensity = 0
        matchMeasure = 0
        for word in query:
            if word in sentences[sentence]:
                termDensity+=1
        for word in wordsInQ:
            matchMeasure += idfs[word]

        qTermDensity = termDensity/len(sentences[sentence])
        rankMeasure[sentence] = (matchMeasure, qTermDensity)

    sortedRank = sorted(rankMeasure.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
    
    sortedSentences = [key[0] for key in sortedRank]
    return sortedSentences[0:n]


if __name__ == "__main__":
    main()
