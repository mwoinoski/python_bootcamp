"""
Compress multiple files in parallel using processes
"""
import sys
import time
from multiprocessing import Process
# from threading import Thread
from zipfile import ZipFile, ZIP_DEFLATED


# TODO: make FileCompressor a subclass of Thread
class FileCompressor(Process):
# class FileCompressor(Thread):
    def __init__(self, file):
        # TODO: add a call to the Thread class constructor
        # HINT: use the syntax super().__init__()
        super().__init__()
        self.file = file

    # TODO: change the name of the following method to compress
    def run(self):
        outfile = self.file + '.zip'
        with ZipFile(outfile, 'w', ZIP_DEFLATED) as f:
            f.write(self.file)
        print('Finished compressing', self.file)


if __name__ == '__main__':

    count = len(sys.argv[1:])

    print(f'Compressing {count} files')

    start_time = time.clock()

    # TODO: initialize a variable with an empty list
    compressors = []

    for file in sys.argv[1:]:
        compressor = FileCompressor(file)

        # TODO: replace the call to `compress` with a call to
        #       the inherited `start` method
        compressor.start()

        # TODO: add the compressor object to the list you created earlier
        compressors.append(compressor)

    # TODO: loop over the list of compressors and call
    #       compressor.join() for each one
    for compressor in compressors:
        compressor.join()

    print(f'All files {count} compressed in {time.clock() - start_time} seconds')
