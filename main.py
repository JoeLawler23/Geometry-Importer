import dxfgrabber

def dxfPrinter(filename):
    """
    This function prints out the given dxf file from the filename given

    Args:
        param1 (string): The file name

    Returns:
        nothing

    """
    file = open(filename+".dxf","r")
    filecontents = file.read()
    print(filecontents)
    file.close

if __name__ == "__main__":
    # dxfPrinter("test")
    dxf = dxfgrabber.readfile("test.dxf")