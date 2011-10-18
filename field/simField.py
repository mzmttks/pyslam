import numpy

class Field:
    def __init__(self, filename=None):
        if filename:
            self.data = numpy.array(
                [map(lambda x: int(x) * 255, line.rstrip("\n"))
                 for line in open(filename)
                 if len(line) > 1])

            print self.data

if __name__ == "__main__":
    import visualizer
    fieldObj = Field("test01.fld")
    visualizer.visualize((10, 10), None, None, None, fieldObj)
    

    visualizer.mainloop()
