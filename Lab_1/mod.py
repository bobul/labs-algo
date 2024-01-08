import os
import tempfile
import heapq
import sys


class heapnode:
    def __init__(
            self,
            item,
            fileHandler,
    ):
        self.item = item
        self.fileHandler = fileHandler


class externamMergeSort:

    def __init__(self):
        self.sortedTempFileHandlerList = []
        self.getCurrentDir()

    def getCurrentDir(self):
        self.cwd = os.getcwd()
        temp_dir = os.path.join(self.cwd, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

    def iterateSortedData(self, sortedCompleteData):
        for no in sortedCompleteData:
            print(no)

    def mergeSortedtempFiles(self):
        mergedNo = (map(int, tempFileHandler) for tempFileHandler in
                    self.sortedTempFileHandlerList)
        sortedCompleteData = heapq.merge(
            *mergedNo)
        return sortedCompleteData

    def heapify(
            self,
            arr,
            i,
            n,
    ):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left].item < arr[i].item:
            smallest = left
        else:
            smallest = i

        if right < n and arr[right].item < arr[smallest].item:
            smallest = right

        if i != smallest:
            (arr[i], arr[smallest]) = (arr[smallest], arr[i])
            self.heapify(arr, smallest, n)

    def construct_heap(self, arr):
        l = len(arr) - 1
        mid = l // 2
        while mid >= 0:
            self.heapify(arr, mid, l)
            mid -= 1

    def mergeSortedtempFiles_low_level(self, output_file):
        lst = []
        sorted_output = []

        # Use sys.maxsize instead of sys.maxint
        for tempFileHandler in self.sortedTempFileHandlerList:
            item = int(tempFileHandler.readline().strip())
            lst.append(heapnode(item, tempFileHandler))

        self.construct_heap(lst)

        with open(output_file, 'w') as output_file:
            while True:
                minimum = lst[0]

                if minimum.item == sys.maxsize:
                    break

                sorted_output.append(minimum.item)
                fileHandler = minimum.fileHandler
                item = fileHandler.readline().strip()

                if not item:
                    item = sys.maxsize
                else:
                    item = int(item)

                lst[0] = heapnode(item, fileHandler)
                self.heapify(lst, 0, len(lst))

                # Write to the output file
                output_file.write(f"{minimum.item}\n")

        return sorted_output

    def splitFiles(self, largeFileName, smallFileSize):
        largeFileHandler = open(largeFileName)
        tempBuffer = []
        size = 0
        while True:
            number = largeFileHandler.readline()
            if not number:
                break
            tempBuffer.append(number.encode('utf-8'))
            size += 1
            if size % smallFileSize == 0:
                tempBuffer = sorted(tempBuffer, key=lambda no: int(no.decode('utf-8').strip()))
                tempFile = tempfile.NamedTemporaryFile(dir=self.cwd + '/temp', delete=False)
                tempFile.writelines(tempBuffer)
                tempFile.seek(0)
                self.sortedTempFileHandlerList.append(tempFile)
                tempBuffer = []


if __name__ == '__main__':
    largeFileName = 'largefile'
    smallFileSize = 100000
    outputFileName = 'sorted_output.txt'
    obj = externamMergeSort()
    obj.splitFiles(largeFileName, smallFileSize)

    obj.mergeSortedtempFiles_low_level(outputFileName)
