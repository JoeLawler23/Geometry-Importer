import ezdxf

if __name__ == "__main__":
    dxf = ezdxf.readfile("3D Examples.dxf")
    msp = dxf.modelspace()
    print("DXF Version: {}".format(dxf.dxfversion))
    print("Collection of models: {}".format(len(msp)))
    for e in msp:
        print(e.dxftype())