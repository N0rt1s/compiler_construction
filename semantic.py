import re

precedence = {'(': 0, ')': 0, '==': 1, '!=': 1, '<=': 2, '>=': 2, '<': 2, '>': 2, 'or': 3, 'and': 4, '+': 5, '-': 5, '*': 6, '/': 6,'%': 6}
    


class Node:
    def __init__(self, value, node_type=None):
        self.value = value
        self.node_type = node_type
        self.left = None
        self.right = None


def get_result_type(operator, left, right):
    if left == right and operator in ["==", "!=", "<=", ">=", "<", ">"]:
        return "bool"
    elif left == "number" and right == "number":
        return "number"
    elif left == "string" and right == "char" and operator == "+":
        return "string"
    elif left == "string" and right == "string" and operator == "+":
        return "string"
    elif left == "char" and right == "char" and operator == "+":
        return "string"
    else:
        raise Exception("Type Missmatch!")


def get_operand_type(id):
    if re.match(r"true|false$", id):
        return "bool"
    elif re.match(r'^"[^"]*"$', id):
        return "string"

    elif re.match(r"'(?:\\.|[^\\'])'", id):
        return "char"

    elif re.match(r"[0-9]+", id):
        return "number"
    else:
        return "number"

    pass


def get_precedence(operator):
    return precedence.get(operator, -1)


def is_operand(token):
    if token in precedence:
        return False
    return True


def build_expression_tree_with_types(infix_expression):
    stack = []
    output = []

    for token in infix_expression:
        if is_operand(token):
            operand_type = get_operand_type(
                token
            )  # Implement this based on your symbol table
            output.append(Node(token, operand_type))
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(Node(stack.pop()))
            stack.pop()  # Pop the '('
        elif not is_operand(token):
            while stack and get_precedence(token) <= get_precedence(stack[-1]):
                output.append(Node(stack.pop()))
            stack.append(token)

    while stack:
        output.append(Node(stack.pop()))
    return build_tree_from_postfix(output)


def build_tree_from_postfix(postfix_expression):
    stack = []
    for token in postfix_expression:
        if is_operand(token.value):
            stack.append(token)
        elif not is_operand(token.value):
            right_operand = stack.pop()
            left_operand = stack.pop()
            operator_node = Node(token.value)
            operator_node.left = left_operand
            operator_node.right = right_operand
            result_type = get_result_type(
                token.value, left_operand.node_type, right_operand.node_type
            )
            operator_node.node_type = result_type
            stack.append(operator_node)
    result=stack.pop()        
    return result.node_type

def put_result(ty):
    if(ty=="number"):
        return "0"
    if(ty=="char"):
        return "'a'"
    if(ty=="string"):
        return '"a"'
    if(ty=="bool"):
        return "true"


# infix_expression = ['5', '+', '8', '*', '(', '6', '-', "7", ')', '+', 'id']
# expression_tree = build_expression_tree_with_types(infix_expression)
# result_type = expression_tree.node_type
# print(result_type)
# print(is_operand("as"))

