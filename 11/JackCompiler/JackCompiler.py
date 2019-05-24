import os
from xml_compiler import JackTokenizer
from xml_compiler.JackAnalyser import _enable_pretty_printing
from vm_compiler import VMCompilationEngine
from xml_compiler.JackAnalyser import _parse_pretty_printing_xml
import sys
from xml_compiler import JackAnalyser
import shutil

class JackCompiler():

    def __init__(self, input):
        self.input = input
        self.tokens = ""
        self.xml_output = ""
        self.tokens_pretty = ""
        self.tokens_file_type = "xml"
        self.filename_with_path = ""
        self._compile_src()

    def _compile_src(self):
        self._handle_multiple_files()

    def _handle_multiple_files(self):
        _, ext = os.path.splitext(self.input) #pong/Ball.jakc
        if ext == '.jack':
            path, filename_with_ext = os.path.split(self.input) #./pong, #Ball.jack
            filename, _ = os.path.splitext(filename_with_ext)
            self.filename = filename
            self.dir = os.path.dirname(os.path.abspath(self.input))
            self.xml_output = self.dir + "/" + filename + ".xml"
            self.filename_with_path = self.dir + "/" + filename + ext
            self._compile_file(filename)
        else:
            list_of_files = os.listdir(self.input)
            self.dir = os.path.dirname(os.path.abspath(self.input)) + "/" + self.input
            for file in list_of_files:
                filename,ext = os.path.splitext(file)
                if ext == '.jack':
                    self.xml_output = self.dir + "/" + filename + ".xml"
                    self.filename_with_path = self.dir + "/" + filename + ext
                    self.filename = filename
                    self._compile_file(filename)


    def _compile_file(self, f_input):
        self.tokens = JackTokenizer.create_jack_tokens(f_input, self.dir, self.tokens_file_type)
        self.tokens_pretty = _enable_pretty_printing(filename=self.tokens, path=self.dir)

        vmc = VMCompilationEngine.VMCE(self.tokens_pretty, self.xml_output)
        vmc.compile()
        _parse_pretty_printing_xml(self.xml_output)

        self._move_files_tmp()


    def _move_files_tmp(self):
        tmp_path = self.dir + "/tmp"
        tokens_path = self.dir + "/" + self.tokens + ".xml"
        tokens_pretty_path = self.tokens_pretty
        xml_path = self.dir + "/" + self.xml_output
        no_comments_path = self.dir + "/" + self.filename + "_no_comments.jack"
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        shutil.move(tokens_path, os.path.join(tmp_path, self.tokens + ".xml"))
        shutil.move(tokens_pretty_path, os.path.join(tmp_path, self.tokens + "_pretty" + ".xml"))
        shutil.move(no_comments_path, os.path.join(tmp_path, "_no_comments.jack"))



compiler = JackCompiler(sys.argv[1])