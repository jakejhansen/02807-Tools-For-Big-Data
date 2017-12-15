import glob
import numpy as np
import cv2
from sklearn.preprocessing import normalize
import time
import multiprocessing
from PIL import Image
import av


# import the necessary packages
from threading import Thread
import sys
from queue import Queue


class FileVideoStream():
    def __init__(self, path, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.frames = 0

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
    

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                self.frames += 1
                
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return

                # add the frame to the queue
                self.Q.put(frame)
                
                
    def read(self):
        # return next frame in the queue
        return self.Q.get()

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0
    
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        
        
        

def worker(vid, i):
    # Opens a video-file and process it frame by frame
    

    tot_frames = []
    
    fvs = FileVideoStream(vid).start()
    time.sleep(0.01)
    
    while fvs.more() == False:
        time.sleep(0.01)
    
    # loop over frames from the video file stream
    processed_frames = 0
    while fvs.more():
        frame = fvs.read()
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #hist = cv2.calcHist([gray], [0], None, [64], [0, 256])
        #hist = normalize(hist, norm='l1', axis=0)
        #hist_frame.append(hist)
        if processed_frames == 0:
            tot_frames = np.zeros((frame.shape[0], frame.shape[1], 3))
        tot_frames += frame

        processed_frames += 1
        
        if processed_frames > 2:
            break
        
        while not fvs.more() and not fvs.stopped:
            time.sleep(0.0001)
        
    fvs.stop()

    img = tot_frames / processed_frames
    return(img)
    #return(np.mean(hist_frame, axis = 0))
    #return(np.sum(hist_frame))




def frame_iter(video):
    for packet in video.demux():
        for frame in packet.decode():
            yield frame
            

def fast(path):
    pool = multiprocessing.Pool(4)
    results = []
    
    fileNames = glob.glob(path)
    for i, vid in enumerate(fileNames[:2]):
        res = pool.apply_async(worker,[vid, i])
        results.append([vid,res])

    #wait for jobs to complete
    pool.close()
    pool.join()

    return(results)

if __name__ == '__main__':
    start = time.time()

    res_cv = fast('easy/*')
    print("Time:", time.time()-start)