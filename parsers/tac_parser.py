#!/usr/bin/env python2

from lexer.tag import Tag
from errors import CompilerSyntaxError, EndOfFileError
from tac.node import Leaf, Node

class TACParser (object):
    def __init__(self, lexer):
        self.lex = lexer
        self.move()

    def move(self):
        self.look = self.lex.scan()

    def match(self, tag):
        if self.look.tag == tag:
            self.move()
            return
        else:
            raise CompilerSyntaxError(self.lex.line)

    def P(self):
        self.D()
        self.L()

    def D(self):
        self.B()
        self.N()
        self.match(Tag.END)
        try:
            self.D()
        except CompilerSyntaxError:
            pass

    def B(self):
            self.match(Tag.BASIC)

    def N(self):
        self.match(Tag.ID)
        self.N1()

    def N1(self):
        try:
            self.match(Tag.COMMA)
        except CompilerSyntaxError:
            return

        self.match(Tag.ID)
        self.N1()

    def L(self):
        node = self.S()
        try:
            self.match(Tag.END)
        except EndOfFileError:
            pass

        node.generate()

        try:
            self.L()
        except CompilerSyntaxError:
            pass

    def S(self):
        token = self.look
        try:
            self.match(Tag.ID)
        except CompilerSyntaxError:
            node = self.E()
            return node

        self.match(Tag.ASSIGN)
        e_node = self.E()
        return Node('=', Leaf(token), e_node)

    def E(self):
        t_node = self.T()
        node = self.E1(t_node)
        return node

    def E1(self, inh):
        try:
            self.match(Tag.ADD)
        except CompilerSyntaxError:
            return inh

        t_node = self.T()
        node = self.E1(Node('+', inh, t_node))
        return node

    def T(self):
        f_node = self.F()
        node = self.T1(f_node)
        return node

    def T1(self, inh):
        try:
            self.match(Tag.MUL)
        except CompilerSyntaxError:
            return inh

        f_node = self.F()
        node = self.T1(Node('*', inh, f_node))
        return node

    def F(self):
        try:
            self.match(Tag.OPEN_PARAN)
        except CompilerSyntaxError:
            try:
                token = self.look
                self.match(Tag.NUM)
                node = Leaf(token)
            except CompilerSyntaxError:
                token = self.look
                self.match(Tag.ID)
                node = Leaf(token)
            return node

        node = self.E()
        self.match(Tag.CLOSE_PARAN)
        return node