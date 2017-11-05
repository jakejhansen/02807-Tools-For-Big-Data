from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import numpy as np

class MRStudent(MRJob):
    
    INPUT_PROTOCOL = JSONValueProtocol
    def mapper(self, _, student):
        #yields the gender and the GPA of each student
        yield student["gender"], student["GPA"]
        
    def reducer(self, gender, GPA):
        #yields the gender and the mean grade of the gender
        yield gender, np.mean(list(GPA))
        
if __name__ == '__main__':
     MRStudent.run()