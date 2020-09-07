import tkinter
from tkinter.filedialog import askopenfilename
from xml.etree import ElementTree as ET

def levels2heights(osm_filename, default_storey_height = None):
    tree = ET.parse(osm_filename)
    root = tree.getroot()
    for child in root:
        if child.tag != 'way':
            continue
        levels = None
        has_height = False
        for element in child:
            if element.tag == 'tag':
                if element.attrib['k'] == 'building:levels':
                    levels = int(element.attrib['v'])
                elif element.attrib['k'] == 'height':
                    has_height = True
                    height = float(element.attrib['v'])
        if levels and not has_height:
            child.append(ET.Element('tag', {'k':'height',
                'v':str(levels*default_storey_height)
                }))
        elif levels and has_height:
            print(f'{levels} levels and {height} m, i.e. storey height = {height/levels:.2f}')
    tree.write(osm_filename[:-4] + '_levels2heights' + osm_filename[-4:])


def main():
    root = tkinter.Tk()
    osm_filename = askopenfilename(filetypes=[('*.osm', 'OSM File')])
    if not osm_filename:
        return
    levels2heights(osm_filename, default_storey_height= 3.5)

if __name__ == '__main__':
    main()