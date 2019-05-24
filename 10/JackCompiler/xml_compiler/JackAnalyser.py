import os
import shutil
import xml.etree.cElementTree as ET
from xml.dom import minidom
from xml_compiler import JackTokenizer
from xml_compiler.XMLcompilationEngine import XMLCompilationEngine

compilation_output = "parser.xml"
file_type = "xml"

def jack_analyzer(file, path):
    return None


def create_output_file(filename):
    root = ET.Element("outputfile")
    return root


def _enable_pretty_printing(filename, path):
     root_xml = ET.parse(path + "/" + filename + ".xml").getroot()
     filename_pretty = path + "/pretty_" + filename + ".xml"
     tree_as_string = ET.tostring(root_xml, short_empty_elements=False)
     xmlstr = minidom.parseString(tree_as_string).toprettyxml(indent="  ")
     with open(filename_pretty, "w") as f:
         f.write(xmlstr)

     return filename_pretty

#NP! returns the location of the parser file
def _move_files_dst(filenames, path):
    for k, v in filenames.items():
        _override_move_file(k, v, path)
    return path + "/" + compilation_output


def _override_move_file(filename, src, dst):
    shutil.move(src, os.path.join(dst, filename))

def patcher(method):
  def patching(self, *args, **kwargs):
    old = self.childNodes
    try:
      if not self.childNodes:
        class Dummy(list):
          def __nonzero__(self):  # Python2
            return True
          def __bool__(self):  # Python3
            return True
        old, self.childNodes = self.childNodes, Dummy([])
      return method(self, *args, **kwargs)
    finally:
      self.childNodes = old
  return patching


def _parse_pretty_printing_xml(filename):
    root_xml = ET.parse(filename).getroot()
    tree_as_string = ET.tostring(root_xml, short_empty_elements=False)
    xmlstr = minidom.parseString(tree_as_string)

    xmlstr.firstChild.__class__.writexml = patcher(xmlstr.firstChild.__class__.writexml)
    test = xmlstr.toprettyxml(indent= "  ")
    with open(filename, "w") as f:
        f.write(test)


