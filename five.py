#!/usr/bin/env python2

import sys

from lexer.lexer import Lexer
from errors import EndOfFileError, CompilerSyntaxError, CompilerLexError, TypeNarrowError
from parsers.type_checking_parser import TCParser

def process_arguments():
    if len(sys.argv) != 2:
        print "Usage:\n     " , sys.argv[0] , "<input_file>\n"
        sys.exit(1);

    filename = sys.argv[1]

    return filename

def main():
    filename = process_arguments()

    with open(filename) as filebuffer:

        try:
            lex = Lexer(filebuffer)
            parser = TCParser(lex)
            parser.P()

        except EndOfFileError:
            print "Syntax error at line " + str(lex.line)

        except CompilerSyntaxError as e:
            print e
        except CompilerLexError as e:
            print e
        except TypeNarrowError as e:
            print e

if __name__ == '__main__':
    main()