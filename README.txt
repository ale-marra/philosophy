# Philosophy

Starting from a random Wikipedia article (example: http://en.wikipedia.org/wiki/Art) and clicking
on the first non-italicized link not surrounded by parentheses in the main text and then repeating
the process for subsequent articles usually leads to http://en.wikipedia.org/wiki/Philosophy.

* What percentage of pages lead to philosophy?
* Using the random article link (found on any wikipedia article in the left sidebar),
what is the distribution of path lengths for 500 pages, discarding those paths
that never reach the Philosophy page?


## Considerations

In order to minimize the number of requests, this program saves all the pages it visits.


## Compatability

This program has been written with Python 3.6.3


## Install

The only requirements are bs4 and requests, you can install them with
pip3 install -r requirements.txt


## Usage

to run the examples:
python3 run.py

to initialize the class:
wiki = Wiki()

to test a specific page:
wiki.testPage('https://en.wikipedia.org/wiki/Art')
>>>'philosophy'

to visualize the full path, set the parameter display=True:
wiki.testPage('https://en.wikipedia.org/wiki/Art',display=True)
>>>--->>> https://en.wikipedia.org/wiki/Art
>>>--->>> https://en.wikipedia.org/wiki/Human_behavior
>>>--->>> https://en.wikipedia.org/wiki/Motion_(physics)
>>>--->>> https://en.wikipedia.org/wiki/Physics
>>>--->>> https://en.wikipedia.org/wiki/Natural_science
>>>--->>> https://en.wikipedia.org/wiki/Science
>>>--->>> https://en.wikipedia.org/wiki/Knowledge
>>>--->>> https://en.wikipedia.org/wiki/Fact
>>>--->>> https://en.wikipedia.org/wiki/Verificationism
>>>'philosophy'

to test a random page:
wiki.testPage(wiki.randomPage)
>>>'philosophy'

to run a test of 500 samples:
wiki.testRandomPages(500)
>>>
>>>Analytics for 500 random pages:
>>>92.00% pages to philosophy
>>>6.20% pages to cycle
>>>1.80% pages to null
>>>
>>>The average path to the philosophy page is 13.07 links


## Author

**Alessandro Marra** - (https://github.com/Ale-Marra)
