from semantic import (
    build_expression_tree_with_types,
    put_result,
    CustomError,
    St_Scope,
    Mt_Scope,
)


class Parser:
    def __init__(self, tokens) -> None:
        self.allTokens = tokens
        self.token_index = 0
        self.symbol_table = []
        self.definition_table = []
        self.member_table = []
        self.current_class_scope = None
        self.scope = []
        self.am = ""
        self.Id = ""
        self.var_Id = []
        self.dt_type = ""
        self.parent = None
        self.interface = []
        self.constructors = []
        self.turn = 0
        self.param_type = ""
        self.return_type=""
        self.returned=False
        self.expression = []

    def check_next_token_by_class(self, expected_value):
        return self.allTokens[self.token_index]["class"] == expected_value

    def check_next_token(self, expected_value):
        return self.allTokens[self.token_index]["value"] == expected_value

    def accept_token(self):
        self.token_index += 1
        if self.token_index > (len(self.allTokens) - 1):
            self.token_index = -1

    def check_variable_exist(self, id):
        # if self.turn==1:
        exists, symbol = self.scope[-1].check_variable(id)
        if not exists:
            return self.lookup_mt(id)
        return symbol

    def lookup_mt(self, id):
        exists, symbol = self.definition_table[-1].check_variable(id)
        if not exists:
            raise CustomError(f"The name {id} does not exist.")
        if symbol["abstract"]:
            raise CustomError(f"Cannot call abstract method {id}")
        return symbol

    def lookup_mt_for_object(self, classId, id):
        existing_class = list(
            filter(lambda x: (x.Id == classId), self.definition_table)
        )
        if len(existing_class) == 0:
            raise CustomError(f"Variable {id} is not of type class.")
        exists, symbol = existing_class[-1].check_variable(id)
        if not exists:
            raise CustomError(f"The member {id} does not exist.")
        elif symbol["am"] == "private":
            raise CustomError(f"Cannot use private member {id} outside class.")

        return symbol

    def check_class_exist(self, id):
        existing_object = list(filter(lambda x: (x.Id == id), self.definition_table))
        if len(existing_object) == 0:
            raise CustomError(f"The Construct {self.Id} does not exist.")
        else:
            if existing_object[0].is_abstract:
                raise CustomError(f"Cannot create Object for absract class {id}.")
            return id

    def set_class_parent(self):
        existing_object = list(
            filter(
                lambda x: (
                    x.Id == self.allTokens[self.token_index]["value"]
                    and (x.type == "interface" or x.type == "class")
                ),
                self.definition_table,
            )
        )
        if len(existing_object) == 0:
            raise CustomError(
                f"The Class {self.allTokens[self.token_index]['value']} does not exist."
            )
        if existing_object[0].type == "class":
            self.parent = existing_object[0]
        else:
            self.interface.append(existing_object[0])

    def set_class_inteface(self):
        existing_object = list(
            filter(
                lambda x: (
                    x.Id == self.allTokens[self.token_index]["value"]
                    and x.type == "interface"
                ),
                self.definition_table,
            )
        )
        if len(existing_object) == 0:
            raise CustomError(
                f"The Class {self.allTokens[self.token_index]['value']} does not exist."
            )

        self.interface.append(existing_object[0])

    def insert_st(self,dt):
        if self.turn == 0:
            for item in self.var_Id:
                inserted = self.scope[-1].declare_variable(item, dt)
                if not inserted:
                    raise CustomError(f"The variable {item} already Declared.")
            self.var_Id = []

    def insert_dt(self, id, type, am, parent=None, abstract=False, interface=[]):
        if self.turn == 0:
            existing_object = list(filter(lambda x: x.Id == id, self.definition_table))
            if len(existing_object) != 0:
                raise CustomError(f"The Construct {id} already exists.")
            else:
                self.definition_table.append(
                    Mt_Scope(id, type, am, parent, abstract, interface)
                )
                self.am = ""

    def insert_mt(self, id="", type="", am="",abstract=False,isFunc=False):
        if self.turn == 0:
            inserted = self.definition_table[-1].declare_variable(id, type, am,abstract,isFunc)
            self.am = ""

            if not inserted:
                raise CustomError(f"The variable {self.Id} already Declared.")

    def lookup_constructor(self, classId, type):
        existing_class = list(
            filter(lambda x: (x.Id == classId), self.definition_table)
        )
        exists, symbol = existing_class[-1].check_constructor(classId, type)
        if not exists:
            raise CustomError(f"No valid Constructor for class {classId} exist.")

    def object_compatibility(self, typeId, classId):
        if typeId != classId:
            existing_class = list(
                filter(lambda x: (x.Id == classId), self.definition_table)
            )
            if len(existing_class) != 0:
                exists = existing_class[-1].check_parent_compatibility(typeId)
                if not exists:
                    raise CustomError(f"No valid type class {classId} exist.")
            else:
                raise CustomError(f"No class {classId} exist.")

    def compatibility_check(self, typeone, typetwo):
        if typeone == typetwo:
            return True
        else:
            raise CustomError("Type Missmatch!")

    ################################################################################################################
    ################################################################################################################

    def start(self):
        self.importing_modules()
        self.rest()

    def importing_modules(self):
        if self.check_next_token("#"):
            self.accept_token()
            if self.check_next_token("import"):
                self.accept_token()
                self.S_or_M()
            else:
                raise ("Exception")
        else:
            pass

    def S_or_M(self):
        if self.check_next_token_by_class("Id"):
            self.accept_token()
        elif self.check_next_token("{"):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.accept_token()
                self.mutiple_Id()
                if self.check_next_token("}"):
                    self.accept_token()
                else:
                    raise ("Exeption")
            else:
                raise ("Exeption")
        else:
            raise ("Exeption")

    def mutiple_Id(self):
        if self.check_next_token(","):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.accept_token()
                self.mutiple_Id()
            else:
                raise ("Exeption")
        else:
            pass

    def rest(self):
        self.interface_class_struct_dec()
        self.more_classes()

    def more_classes(self):
        if self.token_index != -1:
            self.rest()
        else:
            print("Parsing Complete")

    def interface_class_struct_dec(self):
        if self.check_next_token("interface"):
            self.Interface_dec()
        else:
            self.acces_specifiers()
            abstract = self.isabstract()
            if self.check_next_token("class"):
                self.accept_token()
                if self.check_next_token_by_class("Id"):
                    self.Id = self.allTokens[self.token_index]["value"]
                    temp_id = self.allTokens[self.token_index]["value"]
                    self.accept_token()
                    self.interface = []
                    self.parent = None
                    self.derived()
                    self.insert_dt(
                        temp_id, "class", self.am, self.parent, abstract, self.interface
                    )
                    self.interface = []
                    self.parent = None
                    if self.check_next_token("{"):
                        self.current_class_scope = self.Id
                        self.accept_token()
                        self.cst(abstract)
                        if self.check_next_token("}"):
                            self.definition_table[-1].declare_constructor(
                                self.current_class_scope, self.current_class_scope
                            )
                            self.accept_token()
                        else:
                            raise ("Exeption")
                    else:
                        raise ("Exeption")
                else:
                    raise ("Exeption")
            elif self.check_next_token("struct"):
                self.accept_token()
                self.struct()
            else:
                raise ("Exeption")

    def derived(self):
        if self.check_next_token(":"):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.set_class_parent()
                self.accept_token()
                if self.check_next_token(","):
                    self.derived_list()
            else:
                raise ("Exeption")
        else:
            pass

    def derived_list(self):
        if self.check_next_token(","):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.set_class_inteface()
                self.accept_token()
            else:
                raise Exception("Exception")
        else:
            raise Exception("Exception")

    def constructor(self):
        if self.check_next_token_by_class("Id"):
            if self.current_class_scope == self.allTokens[self.token_index]["value"]:
                self.accept_token()
            else:
                raise (CustomError("Constructor Id should be same as class name!"))
            if self.check_next_token("("):
                self.accept_token()
                self.scope.append(St_Scope())
                self.symbol_table.append(self.scope[-1])
                self.param_type = ""
                self.is_params()
                if self.check_next_token(")"):
                    self.accept_token()
                    self.definition_table[-1].declare_constructor(
                        self.current_class_scope,
                        self.current_class_scope + self.param_type,
                    )
                    self.return_type="constructor"
                    if self.check_next_token("{"):
                        self.accept_token()
                        self.MST()
                        if self.check_next_token("}"):
                            self.scope.pop()
                            self.accept_token()
                        else:
                            raise ("Exception")
                    else:
                        raise ("Exception")
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def is_params(self):
        if self.check_next_token(")"):
            pass
        else:
            self.param_type += "=>"
            self.parameters()

    def parameters(self):
        temp_type=self.dt_or_id()
        if self.check_next_token_by_class("Id"):
            self.var_Id.append(self.allTokens[self.token_index]["value"])
            self.insert_st(temp_type)
            self.accept_token()
            self.more_params()
        else:
            raise ("Exception")

    def dt_or_id(self):
        if self.check_next_token_by_class("DataType"):
            self.param_type += self.allTokens[self.token_index]["value"]
            temp_type = self.allTokens[self.token_index]["value"]
            self.accept_token()
            return temp_type
        elif self.check_next_token_by_class("Id"):
            self.param_type += self.allTokens[self.token_index]["value"]
            temp_type = self.allTokens[self.token_index]["value"]
            self.accept_token()
            return temp_type
        else:
            raise ("Exception")

    def more_params(self):
        if self.check_next_token(","):
            self.param_type += ","
            self.accept_token()
            self.parameters()
        else:
            pass

    def cst(self, is_abstract=False):
        if self.check_next_token("}"):
            pass
        elif self.check_next_token_by_class("Id"):
            self.constructor()
            self.cst(is_abstract)
        else:
            self.acces_specifiers()
            if self.check_next_token("struct"):
                self.accept_token()
                self.struct()
                self.cst(is_abstract)
            else:
                abstract=override=False
                if is_abstract:
                    abstract = self.isabstract()
                    if not abstract:
                        override = self.isoverride()
                else:
                    override = self.isoverride()
                    if self.check_next_token("abstract"):
                        raise CustomError("Only abstract class can have abstract methods")
                if self.check_next_token("void"):
                    self.dt_type=self.allTokens[self.token_index]["value"]
                    self.returned=True
                    self.accept_token()
                else:    
                    self.returned=False
                    self.dt()
                if self.check_next_token_by_class("Id"):
                    self.Id = self.allTokens[self.token_index]["value"]
                    temp_id = self.allTokens[self.token_index]["value"]
                    self.accept_token()
                    self.Dec_Var_func(temp_id, abstract, override)
                    self.cst(is_abstract)
                else:
                    raise ("Exception")

    def sst(self):
        if self.check_next_token("}"):
            # self.accept_token()
            pass
        else:
            self.acces_specifiers()
            self.dt()
            if self.check_next_token_by_class("Id"):
                self.Id = self.allTokens[self.token_index]["value"]
                temp_type = self.allTokens[self.token_index]["value"]
                self.accept_token()
                self.Dec_Var_func(temp_type)
                self.sst()
            else:
                raise ("Exception")

    def isabstract(self):
        if self.check_next_token("abstract"):
            self.accept_token()
            return True
        else:
            return False

    def isoverride(self):
        if self.check_next_token("override"):
            self.accept_token()
            return True
        else:
            return False

    def acces_specifiers(self):
        if self.check_next_token("public"):
            self.am = "public"
            self.accept_token()
        elif self.check_next_token("private"):
            self.am = "private"
            self.accept_token()
        else:
            pass

    def dt(self):
        if self.check_next_token_by_class("DataType"):
            self.dt_type = self.allTokens[self.token_index]["value"]
            self.accept_token()
        elif self.check_next_token_by_class("ArrayDataType"):
            self.dt_type = self.allTokens[self.token_index]["value"]
            self.accept_token()
        elif self.check_next_token_by_class("Id"):
            self.dt_type = self.allTokens[self.token_index]["value"]
            self.accept_token()
        else:
            raise ("Exeption")

    def list(self):
        if self.check_next_token(","):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.var_Id.append(self.allTokens[self.token_index]["value"])
                self.accept_token()
                self.list()
            else:
                raise ("Exception")
        else:
            pass

    def put_value(self):
        if self.check_next_token("="):
            self.accept_token()
            if self.check_next_token("["):
                self.arrConst()
                # if self.check_next_token("]"):
                #     self.accept_token()
                # else:
                #     raise("Exception")
            elif (
                self.check_next_token_by_class("string")
                or self.check_next_token_by_class("char")
                or self.check_next_token_by_class("bool")
                or self.check_next_token_by_class("number")
                or self.check_next_token_by_class("Id")
                or self.check_next_token("(")
            ):
                self.expression = []
                self.exp()
                temp_type = build_expression_tree_with_types(self.expression)
                self.expression = []
                self.compatibility_check(self.dt_type, temp_type)
            else:
                raise ("Exception")
        else:
            pass

    def return_dec(self):
        if self.check_next_token("return"):
            self.accept_token()
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.expression = []
        else:
            pass

    def is_param_value(self):
        if self.check_next_token(")"):
            # self.accept_token()
            pass
        else:
            self.param_type += "=>"
            self.param_values()

    def param_values(self):
        temp_exp = self.expression
        self.expression = []
        self.exp()
        temp_type = build_expression_tree_with_types(self.expression)
        self.expression = temp_exp
        self.expression.append(put_result(temp_type))
        self.more_value_param(temp_type)

    def more_value_param(self, type):
        self.param_type += type
        if self.check_next_token(","):
            self.accept_token()
            self.param_type += ","
            self.param_values()
        else:
            pass

    def Id_value_set(self):
        self.OP()
        if self.check_next_token("="):
            self.accept_token()
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.expression = []
            if self.check_next_token(";"):
                self.accept_token()
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def if_stat(self):
        if self.check_next_token("("):
            self.accept_token()
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check("bool", temp_type)
            self.expression = []
            if self.check_next_token(")"):
                self.accept_token()
                if self.check_next_token("{"):
                    self.scope.append(St_Scope(self.scope[-1]))
                    self.symbol_table.append(self.scope[-1])
                    self.accept_token()
                    self.MST()
                    if self.check_next_token("}"):
                        self.scope.pop()
                        self.accept_token()
                        self.elif_stat()
                    else:
                        raise ("Exception")
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def lop(self):
        if self.check_next_token("and"):
            self.accept_token()
        elif self.check_next_token("or"):
            self.accept_token()
        else:
            raise ("Exception")

    def elif_stat(self):
        if self.check_next_token("elif"):
            self.accept_token()
            if self.check_next_token("("):
                self.accept_token()
                self.expression = []
                self.exp()
                temp_type = build_expression_tree_with_types(self.expression)
                self.compatibility_check("bool", temp_type)
                self.expression = []
                if self.check_next_token(")"):
                    self.accept_token()
                    if self.check_next_token("{"):
                        self.accept_token()
                        self.MST()
                        if self.check_next_token("}"):
                            self.accept_token()
                            self.elif_stat()
                            self.else_stat()
                        else:
                            raise ("Exception")
                    else:
                        raise ("Exception")
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            pass

    def else_stat(self):
        if self.check_next_token("else"):
            self.accept_token()
            if self.check_next_token("{"):
                self.accept_token()
                self.MST()
                if self.check_next_token("}"):
                    self.accept_token()
                else:
                    raise ("Exception")
            else:
                raise ("Exception")

        else:
            pass

    def for_loop(self):
        if self.check_next_token("("):
            self.scope.append(St_Scope(self.scope[-1]))
            self.symbol_table.append(self.scope[-1])
            self.accept_token()
            self.Dec()
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)

            self.expression = []
            if self.check_next_token(";"):
                self.accept_token()
                if self.check_next_token_by_class("Id"):
                    self.check_variable_exist(self.allTokens[self.token_index]["value"])
                    self.accept_token()
                    # self.inc_dec()
                    if self.check_next_token("++") or self.check_next_token("--"):
                        self.accept_token()
                        if self.check_next_token(")"):
                            self.accept_token()
                            if self.check_next_token("{"):
                                self.accept_token()
                                self.MST()
                                if self.check_next_token("}"):
                                    self.scope.pop()
                                    self.accept_token()
                                else:
                                    raise ("Exception")
                            else:
                                raise ("Exception")
                        else:
                            raise ("Exception")
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def while_loop(self):
        if self.check_next_token("while"):
            self.accept_token()
            if self.check_next_token("("):
                self.accept_token()
                self.expression = []
                self.exp()
                temp_type = build_expression_tree_with_types(self.expression)
                self.compatibility_check("bool", temp_type)
                self.expression = []
                if self.check_next_token(")"):
                    self.accept_token()
                    if self.check_next_token("{"):
                        self.scope.append(St_Scope(self.scope[-1]))
                        self.symbol_table.append(self.scope[-1])
                        self.accept_token()
                        self.MST()
                        if self.check_next_token("}"):
                            self.scope.pop()
                            self.accept_token()
                        else:
                            raise ("Exception")
                    else:
                        raise ("Exception")
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
                # else:
                raise ("Exception")

    def for_each_loop(self):
        if self.check_next_token("("):
            self.scope.append(St_Scope(self.scope[-1]))
            self.symbol_table.append(self.scope[-1])
            self.accept_token()
            temp_type=self.dt_or_id()
            if self.check_next_token_by_class("Id"):
                self.var_Id.append(self.allTokens[self.token_index]["value"])
                self.insert_st(temp_type)
                self.accept_token()
                if self.check_next_token("in"):
                    self.accept_token()
                    if self.check_next_token_by_class("Id"):
                        self.check_variable_exist(
                            self.allTokens[self.token_index]["value"]
                        )
                        self.accept_token()
                        if self.check_next_token(")"):
                            self.accept_token()
                            if self.check_next_token("{"):
                                self.accept_token()
                                self.MST()
                                if self.check_next_token("}"):
                                    self.scope.pop()
                                    self.accept_token()
                                else:
                                    raise ("Exception")
                            else:
                                raise ("Exception")
                        else:
                            raise ("Exception")
                    else:
                        raise ("Exception")
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def is_array(self):
        if self.check_next_token("["):
            self.accept_token()
            if self.check_next_token("]"):
                self.accept_token()
            else:
                raise ("Exception")
        else:
            pass

    def value(self):
        if self.check_next_token_by_class("Id"):
            self.VP()
        elif self.check_next_token("("):
            self.expression.append("(")
            self.accept_token()
            self.exp()
            if self.check_next_token(")"):
                self.expression.append(")")
                self.accept_token()
            else:
                raise ("Exception")
        else:
            self.const()

    def bool(self):
        if self.check_next_token("true"):
            self.accept_token()
        elif self.check_next_token("false"):
            self.accept_token()

    def Inc_dec(self):
        if self.check_next_token("++"):
            self.accept_token()
        elif self.check_next_token("--"):
            self.accept_token()

    def CO(self):
        if self.check_next_token(">"):
            self.accept_token()
        elif self.check_next_token("<"):
            self.accept_token()
        elif self.check_next_token("<="):
            self.accept_token()
        elif self.check_next_token(">="):
            self.accept_token()
        elif self.check_next_token("=="):
            self.accept_token()
        elif self.check_next_token("!="):
            self.accept_token()

    def jump_stat(self):
        if self.check_next_token("break"):
            self.accept_token()
            if self.check_next_token(";"):
                self.accept_token()
        elif self.check_next_token("continue"):
            self.accept_token()
            if self.check_next_token(";"):
                self.accept_token()

    def struct(self):
        if self.check_next_token_by_class("Id"):
            self.Id = self.allTokens[self.token_index]["value"]
            temp_id = self.allTokens[self.token_index]["value"]
            self.accept_token()
            if self.check_next_token("{"):
                self.parent = None
                self.insert_dt(temp_id, "struct", self.am)
                self.accept_token()
                self.sst()
                if self.check_next_token("}"):
                    self.accept_token()
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def Dec_Var_func(self, id, is_abstract=False, is_override=False):
        if self.check_next_token("("):
            self.scope.append(St_Scope())
            self.symbol_table.append(self.scope[-1])
            self.accept_token()
            self.param_type = ""
            self.is_params()
            if self.check_next_token(")"):
                self.accept_token()
                if is_override:
                    exists=self.definition_table[-1].check_override_method(id,self.dt_type + self.param_type)
                    if not exists:
                        raise CustomError(f"no method {id} exists in parent for override")
                self.insert_mt(id, self.dt_type + self.param_type, self.am,is_abstract,True)
                if is_abstract:
                    if self.check_next_token(";"):
                        self.accept_token()
                    else:
                        raise CustomError(f"abstract method {id} cannot have a body")
                else:
                    if self.check_next_token("{"):
                        self.accept_token()
                        self.return_type=self.dt_type
                        self.MST()
                        if self.check_next_token("}"):
                            if not self.returned and self.return_type!="void":
                                raise CustomError(f"Method {id} should have a return statement")
                            self.scope.pop()
                            self.accept_token()
                        else:
                            raise ("Exception")
                    else:
                        raise CustomError(f"No body provided for method {id}")
            else:
                raise ("Exception")
        elif self.check_next_token("="):
            if is_abstract:
                raise CustomError("Only methods can be abstract")
            if is_override:
                raise CustomError("Only methods can be override")
            self.put_value()
            if self.check_next_token(";"):
                self.accept_token()
                self.insert_mt(id, self.dt_type, self.am)
            else:
                raise ("Exception")
        elif self.check_next_token(";"):
            if is_abstract:
                raise CustomError("Only methods can be abstract")
            if is_override:
                raise CustomError("Only methods can be override")
            self.insert_mt(id, self.dt_type, self.am)
            self.accept_token()

    def Dec(self):
        self.dt()
        if self.check_next_token_by_class("Id"):
            self.var_Id.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.list()
            self.put_value()
            if self.check_next_token(";"):
                self.insert_st(self.dt_type)
                self.accept_token()
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def MST(self):
        if self.check_next_token_by_class("DataType") or self.check_next_token_by_class(
            "ArrayDataType"
        ):
            self.Dec()
            self.MST()
        elif self.check_next_token("if"):
            self.accept_token()
            self.if_stat()
            self.MST()
        elif self.check_next_token("return"):
            if self.return_type=="void":
                raise CustomError(f"Void function cannot have return type")
            
            if self.return_type=="constructor":
                raise CustomError(f"Constructors cannot have return type")
            
            self.returned=True
            self.accept_token()
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check(temp_type,self.return_type)
            if self.check_next_token(";"):
                self.accept_token()
            else:
                raise Exception("Expected semicolon")    
            self.MST()
        elif self.check_next_token("for"):
            self.accept_token()
            self.for_loop()
            self.MST()
        elif self.check_next_token("forEach"):
            self.accept_token()
            self.for_each_loop()
            self.MST()
        elif self.check_next_token("while"):
            self.while_loop()
            self.MST()
        elif self.check_next_token("break") or self.check_next_token("continue"):
            self.accept_token()
            if self.check_next_token(";"):
                self.accept_token()
                self.MST()
        elif self.check_next_token("struct"):
            self.accept_token()
            self.struct()
            self.MST()
        elif self.check_next_token_by_class("Id"):
            self.Id = self.allTokens[self.token_index]["value"]
            self.accept_token()
            temp_type = ""
            if self.check_next_token_by_class("Id"):
                temp_type = self.check_class_exist(self.Id)
            else:
                temp_type = self.check_variable_exist(self.Id)["type"]
            self.func_call_Id_set_class_init(temp_type)
            if self.check_next_token(";"):
                self.accept_token()
                self.MST()
            else:
                raise ("Exception")
        else:
            pass

    def return_stat(self):
        if self.check_next_token("return"):
            self.accept_token()
        

    def dts(self):
        if self.check_next_token_by_class("number"):
            self.accept_token()
        elif self.check_next_token_by_class("char"):
            self.accept_token()
        elif self.check_next_token_by_class("string"):
            self.accept_token()
        elif self.check_next_token_by_class("bool"):
            self.accept_token()
        else:
            raise ("Exception")

    def const(self):
        if self.check_next_token_by_class("string"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
        elif self.check_next_token_by_class("char"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
        elif self.check_next_token_by_class("bool"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
        elif self.check_next_token_by_class("number"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
        # elif self.check_next_token("["):
        #     self.arrConst()
        else:
            raise ("Exception")

    def arrConst(self):
        if self.check_next_token("["):
            self.accept_token()
            if (
                self.check_next_token_by_class("string")
                or self.check_next_token_by_class("char")
                or self.check_next_token_by_class("bool")
                or self.check_next_token_by_class("number")
                or self.check_next_token_by_class("Id")
            ):
                self.element_list()
                if self.check_next_token("]"):
                    self.accept_token()
                else:
                    raise ("Exception")
            elif self.check_next_token("["):
                self.arr_list()
                if self.check_next_token("]"):
                    self.accept_token()
                else:
                    raise ("Exception")
            else:
                pass
        else:
            raise ("Exception")

    def element_list(self):
        self.expression = []
        self.exp()
        temp_type = build_expression_tree_with_types(self.expression)
        self.expression = []

        self.more_array_value()

    def arr_list(self):
        self.arrConst()
        self.more_array()

    def more_array(self):
        if self.check_next_token(","):
            self.accept_token()
            self.arr_list()
        else:
            pass

    def more_array_value(self):
        if self.check_next_token(","):
            self.accept_token()
            self.element_list()
        else:
            pass

    def index(self):
        if self.check_next_token_by_class("number"):
            self.accept_token()
        else:
            raise ("Exception")

    def OP(self, type=None, check_obj=False):
        if self.check_next_token_by_class("Id"):
            temp_type = ""
            if check_obj:
                temp_type = self.lookup_mt_for_object(
                    type.split("=")[0] if type.__contains__("=>") else type,
                    self.allTokens[self.token_index]["value"],
                )["type"]
            else:
                temp_type = self.check_variable_exist(
                    self.allTokens[self.token_index]["value"]
                )["type"]

            self.accept_token()
            self.OP_ex_Id(temp_type)
        else:
            raise ("Exception")

    def OP_ex_Id(self, type=None):
        if self.check_next_token("["):
            self.accept_token()
            temp_exp = self.expression
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check(type.split("[")[0], temp_type)
            self.expression = temp_exp
            self.dt_type = temp_type
            # self.expression.append(put_result(temp_type))
            if self.check_next_token("]"):
                self.accept_token()
                self.OP_ex_Id(temp_type)
            else:
                raise ("Exception")
        elif self.check_next_token("("):
            self.accept_token()
            temp_exp = self.expression
            self.expression = []
            self.param_type = ""
            self.is_param_value()
            if self.check_next_token(")"):
                self.compatibility_check(
                    type.split("=>")[1] if type.__contains__("=>")else "", self.param_type.split("=>")[1] if self.param_type.__contains__("=>")else self.param_type
                )
                self.expression = temp_exp
                # self.dt_type = temp_type
                # self.expression.append(put_result(type.split("=>")[0]))
                self.param_type = ""
                self.accept_token()
                if self.check_next_token(";"):
                    pass
                else:
                    self.OP_Id_loop(type)
            else:
                raise ("Exception")
        elif self.check_next_token("."):
            self.accept_token()
            self.OP(type, True)
        else:
            self.expression.append(
                put_result(type.split("=")[0] if type.__contains__("=>") else type)
            )
            self.dt_type = type.split("=")[0] if type.__contains__("=>") else type

    def OP_Id_loop(self, type):
        if self.check_next_token("."):
            self.accept_token()
            self.OP(type, True)
        elif self.check_next_token("["):
            self.accept_token()
            temp_exp = self.expression
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check(type.split("[")[0], temp_type)
            self.expression = temp_exp
            self.dt_type = temp_type
            # self.expression.append(put_result(temp_type))
            if self.check_next_token("]"):
                self.accept_token()
                self.OP_ex_Id(temp_type)
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def VP(self, type=None, check_obj=False):
        if self.check_next_token_by_class("Id"):
            temp_type = ""
            if check_obj:
                temp_type = self.lookup_mt_for_object(
                    type.split("=")[0] if type.__contains__("=>") else type,
                    self.allTokens[self.token_index]["value"],
                )["type"]
            else:
                temp_type = self.check_variable_exist(
                    self.allTokens[self.token_index]["value"]
                )["type"]

            self.accept_token()
            self.VP_ex_Id(temp_type)
        else:
            raise ("Exception")

    def VP_ex_Id(self, type):
        if self.check_next_token("["):
            self.accept_token()
            temp_exp = self.expression
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check(type.split("[")[0], temp_type)
            self.expression = temp_exp
            self.dt_type = temp_type
            # self.expression.append(put_result(temp_type))
            if self.check_next_token("]"):
                self.accept_token()
                self.VP_ex_Id(temp_type)
            else:
                raise ("Exception")
        elif self.check_next_token("("):
            self.accept_token()
            temp_exp = self.expression
            self.expression = []
            self.param_type = ""
            self.is_param_value()
            if self.check_next_token(")"):
                self.compatibility_check(
                    type.split("=>")[1] if type.__contains__("=>")else "", self.param_type.split("=>")[1] if self.param_type.__contains__("=>")else self.param_type
                )
                self.expression = temp_exp
                # self.dt_type = temp_type
                # self.expression.append(put_result(type.split("=>")[0]))
                self.param_type = ""
                self.accept_token()
                self.VP_Id_loop(type)
            else:
                raise ("Exception")
        elif self.check_next_token("."):
            self.accept_token()
            self.VP(type, False)
        else:
            self.expression.append(
                put_result(type.split("=")[0] if type.__contains__("=>") else type)
            )
            pass

    def VP_Id_loop(self, type):
        if self.check_next_token("."):
            self.accept_token()
            self.VP(type, False)
        elif self.check_next_token("["):
            self.accept_token()
            temp_exp = self.expression
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.compatibility_check(type.split("[")[0], temp_type)
            self.expression = temp_exp
            self.dt_type = temp_type
            # self.expression.append(put_result(temp_type))
            if self.check_next_token("]"):
                self.accept_token()

                self.VP_ex_Id(temp_type)
            else:
                raise ("Exception")
        else:
            self.expression.append(
                put_result(type.split("=")[0] if type.__contains__("=>") else type)
            )
            pass

    def func_call_Id_set_class_init(self, type=None):
        if (
            self.check_next_token("[")
            or self.check_next_token("(")
            or self.check_next_token(".")
        ):
            self.OP_ex_Id(type)
            self.func_call_Id_set_class_init(self.dt_type)
        elif self.check_next_token("="):
            self.accept_token()
            self.expression = []
            self.exp()
            temp_type = build_expression_tree_with_types(self.expression)
            self.expression = []
            self.compatibility_check(type, temp_type)
        elif self.check_next_token_by_class("Id"):
            self.class_init_or_not(type)
        elif self.check_next_token("++") or self.check_next_token("--"):
            self.accept_token()
        elif self.check_next_token(";"):
            # self.accept_token()
            pass
        else:
            raise ("Exception")

    def class_init_or_not(self, type):
        if self.check_next_token_by_class("Id"):
            id = self.allTokens[self.token_index]["value"]
            self.accept_token()
            if self.check_next_token("="):
                self.accept_token()
                if self.check_next_token("new"):
                    self.accept_token()
                    if self.check_next_token_by_class("Id"):
                        self.object_compatibility(
                            type, self.allTokens[self.token_index]["value"]
                        )
                        temp_Id = self.allTokens[self.token_index]["value"]
                        self.accept_token()
                        if self.check_next_token("("):
                            self.accept_token()
                            self.param_type = ""
                            self.is_param_value()
                            if self.check_next_token(")"):
                                self.lookup_constructor(
                                    temp_Id, temp_Id + self.param_type
                                )
                                self.dt_type = self.Id
                                self.var_Id.append(id)
                                self.insert_st(self.dt_type)
                                self.accept_token()
                            else:
                                raise ("Exception")
                        else:
                            raise ("Exception")
                    else:
                        raise ("Exception")
                else:
                    raise ("Exception")
            else:
                raise ("Exception")

    def exp(self):
        self.AE()
        self.OE()

    def OE(self):
        if self.check_next_token("or"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.AE()
            self.OE()
        else:
            pass

    def AE(self):
        self.RE()
        self.AE1()

    def AE1(self):
        if self.check_next_token("and"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.RE()
            self.AE1()
        else:
            pass

    def RE(self):
        if (
            self.check_next_token_by_class("string")
            or self.check_next_token_by_class("char")
            or self.check_next_token_by_class("bool")
            or self.check_next_token_by_class("number")
            or self.check_next_token_by_class("Id")
            or self.check_next_token("(")
        ):
            self.value()
            self.T1()
            self.E1()
            self.RE1()
        else:
            pass

    def RE1(self):
        if self.check_next_token_by_class("RelationalOperators"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            if (
                self.check_next_token_by_class("string")
                or self.check_next_token_by_class("char")
                or self.check_next_token_by_class("bool")
                or self.check_next_token_by_class("number")
                or self.check_next_token_by_class("Id")
                or self.check_next_token("(")
            ):
                self.value()
                self.T1()
                self.E1()
                self.RE1()
            else:
                raise ("Exception")
        else:
            pass

    def E1(self):
        if self.check_next_token("+"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.value()
            self.T1()
            self.E1()
        elif self.check_next_token("-"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.value()
            self.T1()
            self.E1()
        else:
            pass

    def T1(self):
        if self.check_next_token("*"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.value()
            self.T1()
        elif self.check_next_token("/"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.value()
            self.T1()
        elif self.check_next_token("%"):
            self.expression.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.value()
            self.T1()
        else:
            pass

    def Interface_dec(self):
        if self.check_next_token("interface"):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.Id = self.allTokens[self.token_index]["value"]
                temp_id = self.allTokens[self.token_index]["value"]
                self.accept_token()
                if self.check_next_token("{"):
                    self.accept_token()
                    self.insert_dt(temp_id, "interface", "public")
                    self.IST()
                    if self.check_next_token("}"):
                        self.accept_token()
                    else:
                        raise Exception("Invalid")
                else:
                    raise Exception("Invalid")
            else:
                raise Exception("Invalid")
        else:
            raise Exception("Invalid")

    def IST(self):
        if self.check_next_token("}"):
            # self.accept_token()
            pass
        else:
            # self.acces_specifiers()
            self.dt()
            if self.check_next_token_by_class("Id"):
                self.Id = self.allTokens[self.token_index]["value"]
                temp_id = self.allTokens[self.token_index]["value"]
                self.accept_token()
                self.Inter_Dec_Var_func(temp_id)
                if self.check_next_token(";"):
                    self.accept_token()
                    self.IST()
            else:
                raise Exception("Invalid")

    def Inter_Dec_Var_func(self, id):
        if self.check_next_token("("):
            self.accept_token()
            self.param_type = ""
            self.is_params()
            if self.check_next_token(")"):
                self.accept_token()
                self.insert_mt(id, self.dt_type + self.param_type)
            else:
                raise Exception("Invalid")
        elif self.check_next_token(","):
            self.I_List(id)
        elif self.check_next_token(";"):
            pass
        else:
            raise Exception("Invalid")

    def I_List(self, id):
        self.insert_mt(id, self.dt_type)
        if self.check_next_token(","):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.Id = self.allTokens[self.token_index]["value"]
                temp_id = self.allTokens[self.token_index]["value"]
                self.accept_token()
                self.I_List(temp_id)
            else:
                raise Exception("Invalid")
        else:
            pass


# sqlite3 your_database.db

# .mode csv
# .headers on
# .output output_file.csv

# SELECT * FROM moz_cookies;

# .quit
