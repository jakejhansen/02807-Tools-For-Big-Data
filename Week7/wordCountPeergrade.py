from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        # Split the lines into words.
        for word in line.split():
            # yield each word in the line
            yield word, 1

    def reducer(self, key, values):
        # optimization: sum the words we've seen so far
        yield key, sum(values)

if __name__ == '__main__':
    MRWordFrequencyCount.run()