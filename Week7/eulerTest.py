
from mrjob.job import MRJob
from mrjob.step import MRStep


class MREulerTest(MRJob):
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer_vertex_degree),
            MRStep(reducer=self.reducer_result)
        ]
    
    def mapper(self, key, line):
        #extract and yield the verticies for each line in the file
        yield line.split()[0], 1   #vertex 1
        yield line.split()[1], 1   #vertex 2
        
    def reducer_vertex_degree(self, key, values):
        #Find the degree of all the verticies, and send them all to the same reducer using None as main key
        yield None, (key, sum(values))
        
    def reducer_result(self, _, degrees):
        #determine if the graf has an euler tour or not
        for i, degree in enumerate(degrees):
            #if graph contains a vertex with odd degree, stop
            if degree[1] % 2 == 1:
                print("Graph does not contain an euler tour")
                return
        
        #if no odd degrees detected, print:
        print("Graph contains an euler tour")
        
        
if __name__ == '__main__':
     MREulerTest.run()