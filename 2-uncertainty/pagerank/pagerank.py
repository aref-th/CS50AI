import os
import random
import re
import sys

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
    """
    num_pages = len(corpus)
    probabilities = dict()

    if corpus[page]:  # If page has outgoing links
        for p in corpus:
            probabilities[p] = (1 - damping_factor) / num_pages
        for link in corpus[page]:
            probabilities[link] += damping_factor / len(corpus[page])
    else:  # If page has no outgoing links, distribute probability equally
        for p in corpus:
            probabilities[p] = 1 / num_pages

    return probabilities

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    """
    pagerank = {page: 0 for page in corpus}
    page = random.choice(list(corpus.keys()))  # Start with a random page

    for _ in range(n):
        pagerank[page] += 1
        probabilities = transition_model(corpus, page, damping_factor)
        page = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]

    # Normalize probabilities
    total = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] /= total

    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    num_pages = len(corpus)
    pagerank = {page: 1 / num_pages for page in corpus}
    new_pagerank = pagerank.copy()

    while True:
        for page in corpus:
            sum_ranks = 0
            for p in corpus:
                if corpus[p]:
                    if page in corpus[p]:
                        sum_ranks += pagerank[p] / len(corpus[p])
                else:
                    sum_ranks += pagerank[p] / num_pages  # Distribute rank from sink pages
            new_pagerank[page] = (1 - damping_factor) / num_pages + damping_factor * sum_ranks

        # Check for convergence
        if all(abs(new_pagerank[p] - pagerank[p]) < 0.001 for p in pagerank):
            break
        pagerank = new_pagerank.copy()

    return pagerank

if __name__ == "__main__":
    main()
