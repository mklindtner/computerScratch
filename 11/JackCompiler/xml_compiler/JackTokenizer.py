import xml.etree.cElementTree as ET
import re
from enum import Enum
import os

tokens_any_word = "\w+"
tokens_symbol = "{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\="
tokens_keyword = "\method|\constructor|\\function|\class|field|\static|\\var|\int|\char|\\boolean|\\void|\\true|\\false|\\null|\\this|\let|\do|\if|\else|\while|\\return"
tokens_regex = tokens_any_word +"|"+ tokens_symbol +"|"+ tokens_keyword

keywords = ["method", "constructor", "function", "class", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
symbols = ["{","}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "\\", "&", "|", "<", ">", "=", "~"]


# use path to put no_comments_file in proper dir
def create_jack_tokens(filename, path, ext):
    filename_with_path = path + "/" + filename + ".jack"
    filename_with_path_new_ext =  path + "/" + filename + "." + ext #change to .xml

    tokens_output = []
    new_filename = _create_no_comments_file(filename_with_path)
    with open(new_filename) as jf:
        for line in jf:
            tokens = _find_tokens(line)
            tokens_simple = _remove_whitespace(tokens)
            for token in tokens_simple:
                tokens_output.append(token)
    _create_root_xml(tokens_output,filename_with_path_new_ext)
    return filename


def _find_tokens(line):
    if "\"" in line:
        quotes = [index for index, value in enumerate(line) if value == "\""]
        s = []
        cur_index = 0
        while quotes:
            #setup for quotes
            cur_first = quotes.pop(0)
            cur_second = quotes.pop(0)
            cur_quotes = line[cur_first:cur_second+1]

            tmp_s = line[cur_index:cur_first]
            tmp_part1 = re.split('(' + tokens_regex + ')', tmp_s)
            for tmp_val in tmp_part1:
                s.append(tmp_val)
            s.append(cur_quotes)
            #peek next val, if quotes are empty
            if not quotes:
                tmp_s_last = line[cur_second+1:-1]
                tmp_part2 = re.split('(' + tokens_regex + ')', tmp_s_last)
                #flatten s array
                for tmp_val_2 in tmp_part2:
                    s.append(tmp_val_2)
            cur_index = cur_second+1
    else:
        s = re.split('(' + tokens_regex + ')', line)
    return s


def token_type(token):
    if token in symbols:
        return TOKENTYPE.symbol
    elif token in keywords:
        return TOKENTYPE.keyword
    elif "\"" in token:
        return TOKENTYPE.stringConstant
    elif token.isdigit():
        return TOKENTYPE.integerConstant
    return TOKENTYPE.identifier


def key_word(word):
    return KEYWORD_TYPE[word.upper()]


def symbol(word):
    return word


def identifier(word):
    return word


def int_val(word):
    return int(word)


def string_val(word):
    return word[1:-1]


class TOKENTYPE(Enum):
    keyword = 0; symbol = 1; identifier = 2;
    integerConstant = 3; stringConstant = 4;


class KEYWORD_TYPE(Enum):
    CLASS = 0; METHOD = 1; FUNCTION = 2;
    CONSTRUCTOR = 3; INT = 4; BOOLEAN = 5;
    CHAR = 6; VOID = 7; VAR = 8;
    STATIC = 9; FIELD = 10; LET = 11;
    DO = 12; IF = 13; ELSE = 14;
    WHILE = 15; RETURN = 16; TRUE = 17;
    FALSE = 18; NULL = 19; THIS = 20;


#helpers
def _create_root_xml(tokens, filename_with_path):
    tree = ET.Element("tokens")
    for token in tokens:
        t_type = token_type(token)
        if t_type is TOKENTYPE.stringConstant:
            token = string_val(token)
        cur_token = ET.SubElement(tree, t_type.name)
        cur_token.text = token

    tree_as_string = ET.tostring(tree, encoding="unicode")

    openfile = open(filename_with_path, "w+")
    openfile.write(tree_as_string)


def _remove_whitespace(tokens):
    for index, token in enumerate(tokens):
        token = token.strip(" ")
        tokens[index] = token
        if token.isspace():
            tokens.remove(token)
        if token == "":
            tokens.remove(token)
    return tokens


def _create_no_comments_file(jack_file):
    filename, ext = os.path.splitext(jack_file)
    is_comment = False
    new_filename = str(filename) + "_no_comments" + ".jack"
    jack_no_comments = open(new_filename, "w+")
    with open(jack_file) as jf:
        for line in jf:
            cur_line = line
            #comment block starts
            if "/*" in line:
                cur_line = line[0:line.index("/*")]
                is_comment = True
            #line comment
            if "//" in line:
                cur_line = line[0:line.index("//")]

            if not is_comment:
                jack_no_comments.write(cur_line)
            # comment block ends, call after write as to not write "*/"
            if is_comment and "*/" in line:
                is_comment = False
    return new_filename