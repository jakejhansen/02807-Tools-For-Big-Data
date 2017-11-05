
from mrjob.job import MRJob
import re

#use regular expression to extract words
WORD_RE = re.compile(r"[\w']+")

class MRWordCount(MRJob):
    
    def mapper(self, key, line):
        #take all the words in the streamed lines
        for word in WORD_RE.findall(line):
            yield word.lower(), 1
        
    def reducer(self, key, values):
        #Sum up all the keys and their values
        yield key, sum(values)
        
if __name__ == '__main__':
     MRWordCount.run()