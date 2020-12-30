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
    dxf = dxfgrabber.readfile("test.dxf")
    print("DXF version: {}".format(dxf.dxfversion))
    print("Dict of dxf header vars: {}".format(len(dxf.header)))
    print("Collection of layer definitions: {}".format(len(dxf.layers)))
    print("Collection of block definitions: {}".format(len(dxf.blocks)))
    print("Collection of entities: {}".format(len(dxf.entities)))