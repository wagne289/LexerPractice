
from rply import LexerGenerator
from rply import LexingError
from rply import ParserGenerator
import math
import json
import re


def lex_spartytalk(program):
    lexgen = LexerGenerator()

    lexgen.add('SPARTYSAYS', r'spartysays')
    lexgen.add('SEMICOLON', r';')
    lexgen.add('AND', r'and')
    lexgen.add('OR', r'or')
    lexgen.add('IF', r'if')
    lexgen.add('ELSE', r'else')
    lexgen.add('GOGREEN', r'gogreen')
    lexgen.add('GOWHITE', r'gowhite')
    lexgen.add('NVAR', r'nvar')
    lexgen.add('SVAR', r'svar')
    lexgen.add('IDENTIFIER', r'[A-Za-z][A-Za-z0-9]*')
    lexgen.add('NUMBER', r'(\+|\-)[0-9]+[.][0-9]+|[0-9]+[.][0-9]+|[0-9]+|(\+|\-)[0-9]+')
    lexgen.add('STRING', r'"[^"]*"')
    lexgen.add('PLUS', r'\+')
    lexgen.add('MINUS', r'\-')
    lexgen.add('MUL', r'\*')
    lexgen.add('DIV', r'\/')
    lexgen.add('NOTEQ', r'!=')
    lexgen.add('EQ', r'==')
    lexgen.add('LESSEREQ', r'<=')
    lexgen.add('GREATEREQ', r'>=')
    lexgen.add('LESS', r'<')
    lexgen.add('GREATER', r'>')
    lexgen.add('ASSIGNMENT', r'=')
    lexgen.add('OPEN_PARENS', r'\(')
    lexgen.add('CLOSE_PARENS', r'\)')

    lexgen.ignore(r'[ \n\t]+')
    lexer = lexgen.build()

    return lexer

def parse_spartytalk(program):
    class ParserState(object):

        def __init__(self, id):
            self.id = id

    # Implement this function
    lexer = lex_spartytalk(program)
    # build different lexer up here based on pdf
    token_iter = lexer.lex(program)
    possible_tokens = [rule.name for rule in lexer.rules]
    pg = ParserGenerator(possible_tokens,
                         precedence=[('left', ['PLUS', 'MINUS']),
                                     ('left', ['LESS', 'GREATER', 'EQ']),
                                     ('left', ['AND', 'OR', 'NOT']),
                                     ('left', ['MUL', 'DIV'])])

    @pg.production('program : scope')
    def program_procedure(state, p):
        return {"type": "program", "scope": p[0]}

    @pg.production('scope : GOGREEN SEMICOLON statements GOWHITE SEMICOLON')
    def test_function(state, p):

        return {"type": "scope",
                "statements": p[2]
                }

    @pg.production('statements : statement')
    def statement(state, p):
        states = [p[0]]
        return states

    @pg.production('statements : statements statement')
    def statements(state, p):
        p[0].append(p[1])
        return p[0]

    @pg.production('statement : SPARTYSAYS expression SEMICOLON')
    def sparty_Statement(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "spartysays",
            "expression": p[1]
        }

    @pg.production('statement : NVAR IDENTIFIER ASSIGNMENT expression SEMICOLON')
    def nvar_Statement(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "nvar",
            "identifier": p[1].value,
            "expression": p[3]
        }

    @pg.production('statement : SVAR IDENTIFIER ASSIGNMENT expression SEMICOLON')
    def svar_Statement(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "svar",
            "identifier": p[1].value,
            "expression": p[3]
        }

    @pg.production('statement : IDENTIFIER ASSIGNMENT expression SEMICOLON')
    def empty_statement(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "assignment",
            "identifier": p[0].value,
            "expression": p[2]
        }

    @pg.production('statement : IF boolexp scope')
    def statement_if(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "if",
            "boolexp": p[1],
            "scope": p[2]
        }

    @pg.production('statement : IF boolexp scope ELSE scope')
    def statement_if_else(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "ifelse",
            "boolexp": p[1],
            "truescope": p[2],
            "falsescope": p[4]
        }

    @pg.production('boolexp : boolexp AND boolexp')
    @pg.production('boolexp : boolexp OR boolexp')
    def boolexp_boolexp_andor_boolexp(state, p):
        state.id += 1
        if p[1].name == 'AND':
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "and",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == 'OR':
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "or",
                "left": p[0],
                "right": p[2]
            }
        else:
            return None

    @pg.production('boolexp : expression GREATER expression')
    @pg.production('boolexp : expression LESS expression')
    @pg.production('boolexp : expression EQ expression')
    @pg.production('boolexp : expression NOTEQ expression')
    @pg.production('boolexp : expression GREATEREQ expression')
    @pg.production('boolexp : expression LESSEREQ expression')
    def boolexp_exp_op_exp(state, p):
        state.id += 1
        if p[1].name == "GREATER":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "greater",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "LESS":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "less",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "EQ":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "eq",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "NOTEQ":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "noteq",
                "left": p[0],
                "right": p[2]
            }
        if p[1].name == "GREATEREQ":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "greatereq",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].name == "LESSEREQ":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "lessereq",
                "left": p[0],
                "right": p[2]
            }
        else:
            return None


    @pg.production('expression : expression PLUS expression')
    @pg.production('expression : expression MINUS expression')
    @pg.production('expression : expression MUL expression')
    @pg.production('expression : expression DIV expression')
    def div_expression(state, p):
        if p[1].value == '+':
            state.id += 1
            return {
                "id": state.id,
                "type": "expression",
                "expression_type": "plus",
                "left": p[0],
                "right": p[2],
            }
        elif p[1].value == '-':
            state.id += 1
            return {
                "id": state.id,
                "type": "expression",
                "expression_type": "minus",
                "left": p[0],
                "right": p[2],
            }
        elif p[1].value == '*':
            state.id += 1
            return {
                "id": state.id,
                "type": "expression",
                "expression_type": "mul",
                "left": p[0],
                "right": p[2],
            }

        elif p[1].value == '/':
            state.id += 1
            return {
                "id": state.id,
                "type": "expression",
                "expression_type": "div",
                "left": p[0],
                "right": p[2],
            }

    @pg.production('expression : IDENTIFIER')
    def identifyer_expression(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "identifier",
            "identifier": p[0].value
        }

    @pg.production('expression : NUMBER')
    def expression_number(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "number",
            "value": p[0].value
        }

    @pg.production('expression : STRING')
    def string_expression(state, p):
        temp = p[0].value
        result = temp.replace("\"", "")
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "string",
            "value": result
        }

    @pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
    def parenthesis_expression(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "parentheses",
            "expression": p[1]
        }

    @pg.error
    def error_handler(state, token):
        arg = {
            "type": "error",
            "tokentype": token.gettokentype(),
            "line": token.getsourcepos().lineno,
            "column": token.getsourcepos().colno,
            "id": state.id
        }
        raise Exception(arg)

    parser = pg.build()
    ir = parser.parse(token_iter, state=ParserState(0))
    #print (ir)
    return ir

def interpret_spartytalk(program):
    # Implement this function
    ir = parse_spartytalk(program)

    #print(json.dumps(ir, indent=4))

    class RunTimeState:
        def __init__(self):
            self.sso = []
            self.pc = 0
            self.scache = {}
            self.som = {}
            self.symtable = {}

    def evaluate_string_expression(expression, rts):
        if expression["expression_type"] == "string":
            return str(expression["value"])
        elif expression["expression_type"] == "number":
            return str(expression["value"])
        elif expression["expression_type"] == "parentheses":
            result = evaluate_int_expression(expression["expression"], rts)
            if '.' in str(result):
                result = str(math.ceil(result))
            return str(result)
        elif expression["expression_type"] == "identifier":
            if '.' in str(rts.symtable[expression["identifier"]]["value"]):
                result = str(math.ceil(rts.symtable[expression["identifier"]]["value"]))
                return result
            else:
                return rts.symtable[expression["identifier"]]["value"]
        elif expression["expression_type"] == "plus":
            result = evaluate_string_expression(expression["left"], rts) + evaluate_string_expression(
                expression["right"], rts)
            return result
        else:
            print("Expression evaluation error: unknown expression type with: ", expression["expression_type"])

    def evaluate_int_expression(expression, rts):

        if expression["expression_type"] == "number":
            return float(expression["value"])
        elif expression["expression_type"] == "identifier":
            return int(rts.symtable[expression["identifier"]]["value"])
        elif expression['expression_type'] == "parentheses":
            return evaluate_int_expression(expression["expression"], rts)
        elif expression["expression_type"] == "plus":
            return evaluate_int_expression(expression["left"], rts) + evaluate_int_expression(expression["right"], rts)
        elif expression["expression_type"] == "div":
            return evaluate_int_expression(expression["left"], rts) / evaluate_int_expression(expression["right"], rts)
        elif expression["expression_type"] == "mul":
            result = evaluate_int_expression(expression["left"], rts) * evaluate_int_expression(expression["right"],
                                                                                                rts)
            checker = str(math.ceil(result))
            if len(checker) >= 3:
                result = int(result)
            return result
        elif expression["expression_type"] == "minus":
            return evaluate_int_expression(expression["left"], rts) - evaluate_int_expression(expression["right"], rts)
        else:
            print("Expression evaluation error: unknown expression type with: ", expression["expression_type"])

    def evaluate_boolean_expression(boolexp, rts):
        if boolexp["expression_type"] == "and":
            return evaluate_boolean_expression(boolexp["left"], rts) and evaluate_boolean_expression(
                boolexp["right"], rts)
        elif boolexp["expression_type"] == "or":
            return evaluate_boolean_expression(boolexp["left"], rts) or evaluate_boolean_expression(
                boolexp["right"], rts)
        elif boolexp["expression_type"] == "noteq":
            return not (evaluate_int_expression(boolexp["left"], rts) == evaluate_int_expression(
                boolexp["right"], rts))
        elif boolexp["expression_type"] == "eq":
            return evaluate_int_expression(boolexp["left"], rts) == evaluate_int_expression(
                boolexp["right"], rts)
        elif boolexp["expression_type"] == "greater":
            return evaluate_int_expression(boolexp["left"], rts) > evaluate_int_expression(
                boolexp["right"], rts)
        elif boolexp["expression_type"] == "greatereq":
            return evaluate_int_expression(boolexp["left"], rts) >= evaluate_int_expression(
                boolexp["right"], rts)
        elif boolexp["expression_type"] == "less":
            return evaluate_int_expression(boolexp["left"], rts) < evaluate_int_expression(
                boolexp["right"], rts)
        elif boolexp["expression_type"] == "lessereq":
            return evaluate_int_expression(boolexp["left"], rts) <= evaluate_int_expression(
                boolexp["right"], rts)
        else:
            print("Boolean expression evaluat error.")
            return None
    def interpret_scope(ir, rts):
        count = 0
        for statement in ir['statements']:
            # print(statement)
            rts.sso.append(statement["id"])
            rts.som[statement["id"]] = count
            rts.scache[statement["id"]] = statement
            count += 1

        while True:
            # print("EXECUTING STATEMENT:")
            # print(rts.scache[rts.sso[rts.pc]])

            statement = rts.scache[rts.sso[rts.pc]]

            if statement["statement_type"] == "nvar":
                rts.symtable[statement["identifier"]] = {
                    "value": evaluate_int_expression(statement["expression"], rts)
                }

            # check type with identifier
            if statement["statement_type"] == "assignment":
                rts.symtable[statement["identifier"]] = {
                    "value": evaluate_int_expression(statement["expression"], rts)
                }

            if statement["statement_type"] == "svar":
                rts.symtable[statement["identifier"]] = {
                    "value": evaluate_string_expression(statement["expression"], rts)
                }
            if statement["statement_type"] == "if":
                scoperts = RunTimeState()
                scoperts.symtable = rts.symtable
                if evaluate_boolean_expression(statement["boolexp"], rts):
                    interpret_scope(statement["scope"], scoperts)
            if statement["statement_type"] == "ifelse":
                scoperts = RunTimeState()
                scoperts.symtable = rts.symtable
                if evaluate_boolean_expression(statement["boolexp"], rts):
                    interpret_scope(statement["truescope"], scoperts)
                else:
                    interpret_scope(statement["falsescope"], scoperts)
            if statement["statement_type"] == "spartysays":
                if statement["expression"]['expression_type'] == 'Number':
                    print(evaluate_int_expression(statement["expression"], rts))
                elif statement["expression"]['expression_type'] == 'identifier':
                    floatcheck = False
                    if '.' in str(rts.symtable[statement['expression']["identifier"]]['value']):
                        floatcheck = True
                    if floatcheck:
                        print(evaluate_int_expression(statement["expression"], rts))
                    elif str(rts.symtable[statement['expression']["identifier"]]['value']).isdigit():
                        print(evaluate_int_expression(statement["expression"], rts))
                    else:
                        print(evaluate_string_expression(statement["expression"], rts))
                elif statement["expression"]['expression_type'] == 'string':
                    print(evaluate_string_expression(statement["expression"], rts))
                else:
                    print(evaluate_string_expression(statement["expression"], rts))
            if rts.pc == len(rts.sso) - 1:
                break

            rts.pc = rts.som[rts.sso[rts.pc]] + 1

    rts = RunTimeState()
    interpret_scope(ir["scope"], rts)
    return ""
