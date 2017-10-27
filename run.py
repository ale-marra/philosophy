import requests
from bs4 import BeautifulSoup, NavigableString, Tag

class Wiki():

    def __init__(self):
        self.philosophyPage = 'https://en.wikipedia.org/wiki/Philosophy'
        self.randomPage = 'https://en.wikipedia.org/wiki/Special:Random'
        self.pages = {'null':set(), 'cycle':set(), 'philosophy':{self.philosophyPage:0}}
        self.counter = {'philosophy':0,'cycle':0,'null':0}

    def __getNextUrl(self,url,display=False):

        def filterMainParagraphs(tag):
            #main paragraphs are children of the children of an element with id=mw-content-text
            return (tag.name == 'p' or tag.name == 'ul') and tag.parent is not None and tag.parent.parent is not None and tag.parent.parent.get('id') == 'mw-content-text' 

        def filterLinks(tag):
            return tag.name == 'a' and tag.has_attr('href') and tag.has_attr('title') and tag.string != None

        def filterFormattingTags(tag):
            formattingTags = set(['b','span' ,'sup','sub','small','mark','em','ins','del','li'])
            return tag.name in formattingTags

        def removeItalic(tag):
            for part in tag.find_all('i'):
                part.extract()
            return tag

        def cleanRest(tag):
            # removing coordinates on top left of the page (which are nested as a normal paragraph)
            for part in tag.find_all(id='coordinates'):
                part.extract()

            # unwrapping unnecessary tags
            for part in tag.find_all(filterFormattingTags):
                part.unwrap()
            return tag

        def countParentheses(text):
            count = 0
            for char in text:
                if char == '(':
                    count += 1
                elif char == ')':
                    count -= 1
            return count

        def makeRequest(url,display):
            req = requests.get(url)
            if display:
                print('--->>>',req.url)
            return req


        req = makeRequest(url,display)
        output = {'curr':req.url,'next':None}

        if req.status_code != 200:
            return output

        parsedPage = BeautifulSoup(req.text,'html.parser')
        paragraphs = parsedPage.find_all(filterMainParagraphs)

        # analyzing paragraph by paragraph, so that all the cleaning operations have a shorter html input
        for paragraph in paragraphs:
            # removing italic
            paragraphNoIt = removeItalic(paragraph)
            # cleaning the paragraph
            paragraphClean = cleanRest(paragraphNoIt)
            # discarding text inside parenthesis, assuming paragraphs begin with no open parenthesis from previous paragraph
            parentheses = 0
            for element in paragraphClean.contents:
                
                # only considering parentheses in the clean text
                if isinstance(element, NavigableString):
                    parentheses = max(0, parentheses + countParentheses(str(element)))

                elif isinstance(element, Tag) and parentheses == 0 and filterLinks(element):
                    # sometimes the links redirects to https://en.wiktionary.org
                    if element['href'][:8] != 'https://':
                        output['next'] = 'https://en.wikipedia.org' + element['href']
                    else:
                        output['next'] = element['href']
                    return output
                    
        return output


    def testPage(self,currUrl,display=True):

        currVisits = set()
        initialUrls = self.__getNextUrl(currUrl,display)
        pathLength = 0
        path = [initialUrls['curr']]

        while True:
            currVisits.add(currUrl)
            if pathLength == 0:
                currUrl = initialUrls['next']
            else:
                currUrl = self.__getNextUrl(currUrl,display)['next']
            path += [currUrl]
            pathLength += 1

            if currUrl is None or currUrl in self.pages['null']:
                self.pages['null'].update(currVisits)
                return 'null'
            
            if currUrl in self.pages['cycle'] or currUrl in currVisits:
                self.pages['cycle'].update(currVisits)
                return 'cycle'

            if currUrl in self.pages['philosophy']:
                for count, url in enumerate(path):
                    self.pages['philosophy'][url] = pathLength - count
                return 'philosophy'


    def testRandomPages(self,samples=100,display=False):
       
        for sample in range(samples):
            print ('--------')
            resultType = self.testPage(self.randomPage,display)
            self.counter[resultType] += 1
        
        self.displayResults()

    def displayResults(self):

        n = sum(self.counter.values())
        print('\nAnalytics for %i random pages:' %n)
        if n > 0:
            for type, count in self.counter.items():
                print('%.2f%% pages to %s' %(float(count)/n*100,type) )

        m = self.pages['philosophy'].values()
        print('\nThe average path to the philosophy page is %.2f links' %(float(sum(m))/len(m)) )



####### Usage #######
wiki = Wiki()
# wiki.testPage('https://en.wikipedia.org/wiki/Art',display=True)
# wiki.testPage(wiki.randomPage,display=True)
wiki.testRandomPages(20,display=True)



