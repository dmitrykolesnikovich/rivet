# Copyright (C) 2022 The Rivet Team. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.

from . import type

class SourceFile:
    def __init__(self, file, decls):
        self.file = file
        self.decls = decls

# ---- Declarations ----
class EmptyDecl:
    pass

class Attr:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

class Attrs:
    def __init__(self):
        self.attrs = []

    def add(self, attr):
        self.attrs.append(attr)

    def lookup(self, name):
        for attr in self.attrs:
            if attr.name == name:
                return attr
        return None

class ExternPkg:
    def __init__(self, pkg_name, pos):
        self.pkg_name = pkg_name
        self.pos = pos

class ModDecl:
    def __init__(self, name, is_pub, decls, pos):
        self.name = name
        self.is_pub = is_pub
        self.decls = decls
        self.pos = pos

# ------ Expressions -------
class EmptyExpr:
    def __init__(self, pos):
        self.pos = pos

    def __repr__(self):
        return f"<EmptyExpr pos={self.pos}>"

    def __str__(self):
        return self.__repr__()

class GuardExpr: # if (let x = optional_or_result_fn()) { ... }
    def __init__(self, ident, is_mut, expr, pos):
        self.ident = ident
        self.is_mut = is_mut
        self.expr = expr
        self.pos = pos

    def __repr__(self):
        kmut = "mut" if self.is_mut else ""
        return f"let {kmut} {self.ident} = {self.expr}"

    def __str__(self):
        return self.__repr__()

class TypeNode:
    def __init__(self, ty, pos):
        self.ty = ty
        self.pos = pos

    def __repr__(self):
        return "{self.ty}"

    def __str__(self):
        return self.__repr__()

class CastExpr:
    def __init__(self, expr, ty, pos):
        self.expr = expr
        self.ty = ty
        self.pos = pos

    def __repr__(self):
        return f"cast({self.expr}, {self.ty})"

    def __str__(self):
        return self.__repr__()

class UnsafeExpr:
    def __init__(self, expr, pos, typ=None):
        self.expr = expr
        self.typ = typ
        self.pos = pos

    def __repr__(self):
        return f"unsafe {self.expr}"

    def __str__(self):
        return self.__repr__()

class NoneCheckExpr:
    def __init__(self, expr, pos, typ=None):
        self.expr = expr
        self.typ = typ
        self.pos = pos

    def __repr__(self):
        return f"{self.expr}.?"

    def __str__(self):
        return self.__repr__()

class IndirectExpr:
    def __init__(self, expr, pos, typ=None):
        self.expr = expr
        self.typ = typ
        self.pos = pos

    def __repr__(self):
        return f"{self.expr}.*"

    def __str__(self):
        return self.__repr__()

class Ident:
    def __init__(self, name, pos, scope):
        self.name = name
        self.pos = pos
        self.ty = None
        self.scope = scope

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

class NoneLiteral:
    def __init__(self, pos):
        self.pos = pos
        self.typ = None

    def __repr__(self):
        return "none"

    def __str__(self):
        return self.__repr__()

class BoolLiteral:
    def __init__(self, lit, pos):
        self.lit = lit
        self.pos = pos
        self.typ = None

    def __repr__(self):
        return "true" if self.lit else "false"

    def __str__(self):
        return self.__repr__()

class CharLiteral:
    def __init__(self, lit, pos, is_byte=False):
        self.lit = lit
        self.pos = pos
        self.is_byte = is_byte
        self.typ = None

    def __repr__(self):
        p = "b" if self.is_byte else ""
        return f"{p}'{self.lit}'"

    def __str__(self):
        return self.__repr__()

class IntegerLiteral:
    def __init__(self, lit, pos):
        self.lit = lit
        self.pos = pos

    def __repr__(self):
        return self.lit

    def __str__(self):
        return self.__repr__()

class FloatLiteral:
    def __init__(self, lit, pos):
        self.lit = lit
        self.pos = pos

    def __repr__(self):
        return self.lit

    def __str__(self):
        return self.__repr__()

class StringLiteral:
    def __init__(self, lit, is_raw, is_bytestr, pos):
        self.lit = lit
        self.is_raw = is_raw
        self.is_bytestr = is_bytestr
        self.pos = pos
        self.typ = None

    def __repr__(self):
        p = "b" if self.is_bytestr else "r" if self.is_raw else ""
        return f'{p}"{self.lit}"'

    def __str__(self):
        return self.__repr__()

class TupleLiteral:
    def __init__(self, exprs, pos):
        self.exprs = exprs
        self.typ = type.unit_t
        self.pos = pos

    def __repr__(self):
        res = "("
        for i, e in enumerate(self.exprs):
            res += e.__str__()
            if i < len(self.exprs) - 1:
                res += ", "
        return f"{res})"

    def __str__(self):
        return self.__repr__()

class StructLiteral:
    def __init__(self, sym, fields, pos):
        self.sym = sym
        self.fields = fields
        self.typ = type.unit_t
        self.field_types = {}
        self.pos = pos

class ArrayLiteral:
    def __init__(self, elem_ty, elems, size, pos):
        self.elem_ty = elem_ty
        self.elems = elems
        self.size = size
        self.typ = type.unit_t
        self.pos = pos

    def __repr__(self):
        return f"[{self.elem_ty}; {self.size}]{{ {', '.join([e.__str__() for e in self.elems])} }}"

    def __str__(self):
        return self.__repr__()

class SelfExpr:
    def __init__(self, typ, scope, pos):
        self.typ = typ
        self.scope = scope
        self.pos = pos

    def __repr__(self):
        return "self"

    def __str__(self):
        return self.__repr__()

class UnaryExpr:
    def __init__(self, right, op, pos=None):
        self.right = right
        self.op = op
        self.pos = pos
        self.typ = type.unit_t

    def __repr__(self):
        return f"{self.op}{self.right}"

    def __str__(self):
        return self.__repr__()

class BinaryExpr:
    def __init__(self, left, op, right, pos=None):
        self.left = left
        self.op = op
        self.right = right
        self.pos = pos
        self.typ = type.unit_t

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

    def __str__(self):
        return self.__repr__()

class PostfixExpr:
    def __init__(self, left, op, pos=None):
        self.left = left
        self.op = op
        self.pos = pos
        self.typ = type.unit_t

    def __repr__(self):
        return f"{self.left}{self.op}"

    def __str__(self):
        return self.__repr__()

class ParExpr:
    def __init__(self, expr, pos):
        self.expr = expr
        self.typ = expr.typ
        self.pos = pos

    def __repr__(self):
        return f"({self.expr})"

class IndexExpr:
    def __init__(self, left, index, pos):
        self.left = left
        self.index = index
        self.left_typ = type.unit_t
        self.typ = type.unit_t
        self.pos = pos

    def __repr__(self):
        return f"{self.left}[{self.index}]"

    def __str__(self):
        return self.__repr__()

class CallExpr:
    def __init__(self, left, args, pos):
        self.left = left
        self.args = args
        self.pos = pos
        self.typ = type.unit_t
        self.info = None

    def get_named_arg(self, name):
        for arg in self.args:
            if arg.is_named and arg.name == name:
                return arg
        return None

    def args_len(self):
        l = 0
        for arg in self.args:
            if not arg.is_named:
                l += 1
        return l

    def __repr__(self):
        return f"{self.left}({', '.join([a.__str__() for a in self.args])})"

    def __str__(self):
        return self.__repr__()

class CallArg:
    def __init__(self, expr, pos, name=""):
        self.expr = expr
        self.pos = pos
        self.name = name
        self.is_named = name != ""

    def __repr__(self):
        return (f"{self.name}: " if self.is_named else "") + f"{self.expr}"

    def __str__(self):
        return self.__repr__()

class RangeExpr:
    def __init__(
        self, start, end, is_inclusive, pos, has_start=True, has_end=True
    ):
        self.start = start
        self.end = end
        self.is_inclusive = is_inclusive
        self.has_start = has_start
        self.has_end = has_end
        self.pos = pos
        self.typ = None

    def __repr__(self):
        sep = "=" if self.is_inclusive else ""
        return f"{self.start}..{sep}{self.end}"

    def __str__(self):
        return self.__repr__()

class BuiltinCallExpr:
    def __init__(self, left, args, pos):
        self.left = left
        self.args = args
        self.typ = type.unit_t
        self.pos = pos

    def __repr__(self):
        return f"{self.left}!({', '.join([a.__str__() for a in self.args])})"

    def __str__(self):
        return self.__repr__()

class SelectorExpr:
    def __init__(self, left, field_name, pos):
        self.left = left
        self.field_name = field_name
        self.field_info = None
        self.left_typ = type.unit_t
        self.typ = type.unit_t
        self.pos = pos

    def __repr__(self):
        return f"{self.left}.{self.field_name}"

    def __str__(self):
        return self.__repr__()

class PathExpr:
    def __init__(self, left, field_name, pos):
        self.left = left
        self.field_name = field_name
        self.field_info = None
        self.left_typ = type.unit_t
        self.typ = type.unit_t
        self.is_last = False
        self.pos = pos

    def __repr__(self):
        return f"{self.left}::{self.field_name}"

    def __str__(self):
        return self.__repr__()

class TryExpr:
    def __init__(self, expr, pos):
        self.expr = expr
        self.pos = pos

    def __repr__(self):
        return f"try {self.expr}"

    def __str__(self):
        return self.__repr__()
