import sys

class PrintWrapper:
    fp = None

    def __init__(self, filename):
        if filename == None:
            self.fp = sys.stdout
        else:
            self.fp = open(filename, "w")

    def printf(self, *a):
        print(*a, file=self.fp)

    def close(self):
        if self.fp != sys.stdout:
            self.fp.close()
