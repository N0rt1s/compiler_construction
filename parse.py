class Parser:
    def __init__(self, tokens) -> None:
        self.allTokens = tokens
        self.token_index = 0
        self.testing = self.allTokens[self.token_index]
        self.symbol_table = []
        self.definition_table = []
        self.member_table = []
        self.class_scope = []
        self.current_class_scope = None
        self.scope = []
        self.scopeNumber = 0
        self.am = ""
        self.Id = ""
        self.var_Id = []
        self.type = ""
        self.dt_type = ""
        self.cp = ""
        self.parent = ""
        self.ref = ""
        self.interface=[]

    def check_next_token_by_class(self, expected_value):
        return self.allTokens[self.token_index]["class"] == expected_value

    def check_next_token(self, expected_value):
        return self.allTokens[self.token_index]["value"] == expected_value

    def check_variable_exist(self, id):
        exists = self.scope[-1].check_variable(id)
        if not exists:
            raise CustomError(f"The variable {id} does not exist.")

    def set_class_parent(self):
        existing_object = list(
            filter(
                lambda x: (x.Id == self.allTokens[self.token_index]["value"] and (x.type=="interface" or x.type=="class")),
                self.definition_table,
            )
        )
        if len(existing_object) == 0:
            raise CustomError(
                f"The Class {self.allTokens[self.token_index]['value']} does not exist."
            )
        if existing_object.type=="class":
            self.parent = existing_object[0]
        else:
            self.interface.append(existing_object[0])    

    def insert_st(self):
        for item in self.var_Id:
            inserted = self.scope[-1].declare_variable(item, self.dt_type)
            if not inserted:
                raise CustomError(f"The variable {item} already Declared.")
        self.var_Id = []

    def insert_dt(self):
        existing_object = list(filter(lambda x: x.Id == self.Id, self.definition_table))
        if len(existing_object) != 0:
            raise CustomError(f"The Construct {self.Id} already exists.")
        else:
            self.definition_table.append(
                Mt_Scope(self.Id, self.type, self.am, self.parent)
            )

    def insert_mt(self):
        inserted = self.definition_table[-1].declare_variable(
            self.Id, self.type, self.am
        )
        if not inserted:
            raise CustomError(f"The variable {self.Id} already Declared.")

    def accept_token(self):
        self.token_index += 1
        if self.token_index > (len(self.allTokens) - 1):
            self.token_index = -1

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
            self.type = "interface"
            self.Interface_dec()
        else:
            self.acces_specifiers()
            if self.check_next_token("class"):
                self.type = "class"
                self.accept_token()
                if self.check_next_token_by_class("Id"):
                    self.Id = self.allTokens[self.token_index]["value"]
                    self.accept_token()
                    self.derived()
                    if self.check_next_token("{"):
                        self.class_scope.append(self.Id)
                        self.current_class_scope = self.class_scope[-1]
                        self.ref = self.Id
                        self.accept_token()
                        self.constructor()
                        self.cst()
                        if self.check_next_token("}"):
                            self.accept_token()
                        else:
                            raise ("Exeption")
                    else:
                        raise ("Exeption")
                else:
                    raise ("Exeption")
            elif self.check_next_token("struct"):
                self.type = "struct"
                self.accept_token()
                self.struct()
            else:
                raise ("Exeption")

    def derived(self):
        if self.check_next_token(":"):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.set_class_parent()
                self.insert_dt()
                self.accept_token()
                if self.check_next_token(","):
                    self.derived_list()
            else:
                raise ("Exeption")
        else:
            self.parent = None
            self.insert_dt()
            pass

    def derived_list(self):
        if self.check_next_token(","):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.set_class_parent()

    def constructor(self):
        if self.check_next_token_by_class("Id"):
            if self.Id == self.allTokens[self.token_index]["value"]:
                self.accept_token()
            else:
                raise (CustomError("Constructor Id should be same as class name!"))
            if self.check_next_token("("):
                self.accept_token()
                self.is_params()
                if self.check_next_token(")"):
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
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def is_params(self):
        if self.check_next_token(")"):
            # self.accept_token()
            pass
        else:
            self.parameters()

    def parameters(self):
        self.type += "=>"
        self.dt_or_id()
        if self.check_next_token_by_class("Id"):
            self.var_Id.append(self.allTokens[self.token_index]["value"])
            self.insert_st()
            self.accept_token()
            self.more_params()
        else:
            raise ("Exception")

    def dt_or_id(self):
        if self.check_next_token_by_class("DataType"):
            self.type += self.allTokens[self.token_index]["value"]
            self.dt_type = self.allTokens[self.token_index]["value"]
            self.accept_token()
        elif self.check_next_token_by_class("Id"):
            self.type += self.allTokens[self.token_index]["value"]
            self.dt_type = self.allTokens[self.token_index]["value"]
            self.accept_token()
        else:
            raise ("Exception")

    def more_params(self):
        if self.check_next_token(","):
            self.type += ","
            self.accept_token()
            self.parameters()
        else:
            pass

    def cst(self):
        if self.check_next_token("}"):
            # self.accept_token()
            pass
        else:
            self.acces_specifiers()
            if self.check_next_token("struct"):
                self.type = "struct"
                self.accept_token()
                self.struct()
                self.cst()
            else:
                self.dt()
                if self.check_next_token_by_class("Id"):
                    self.Id = self.allTokens[self.token_index]["value"]
                    self.accept_token()
                    self.Dec_Var_func()
                    self.cst()
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
                self.accept_token()
                self.Dec_Var_func()
                self.sst()
            else:
                raise ("Exception")

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
            self.type = self.allTokens[self.token_index]["value"]
            self.dt_type = self.allTokens[self.token_index]["value"]
            self.accept_token()
        elif self.check_next_token_by_class("ArrayDataType"):
            self.type = self.allTokens[self.token_index]["value"]
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
                self.check_next_token_by_class("strConst")
                or self.check_next_token_by_class("chrConst")
                or self.check_next_token_by_class("boolConst")
                or self.check_next_token_by_class("numConst")
                or self.check_next_token_by_class("Id")
                or self.check_next_token("(")
            ):
                self.exp()
            else:
                raise ("Exception")
        else:
            pass

    def return_dec(self):
        if self.check_next_token("return"):
            self.accept_token()
            self.exp()
        else:
            pass

    def func_call(self):
        self.OP()
        if self.check_next_token("("):
            self.accept_token()
            self.is_param_value()
            if self.check_next_token(")"):
                self.accept_token()
                if self.check_next_token(";"):
                    self.accept_token()
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def is_param_value(self):
        if self.check_next_token(")"):
            self.accept_token()
            pass
        else:
            self.param_values()

    def param_values(self):
        self.OP()
        self.more_value_param()

    def more_value_param(self):
        if self.check_next_token(","):
            self.accept_token()
            self.param_values()
        else:
            pass

    def Id_value_set(self):
        self.OP()
        if self.check_next_token("="):
            self.accept_token()
            self.exp()
            if self.check_next_token(";"):
                self.accept_token()
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def if_stat(self):
        if self.check_next_token("("):
            self.accept_token()
            self.exp()
            if self.check_next_token(")"):
                self.accept_token()
                if self.check_next_token("{"):
                    self.scopeNumber += 1
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
                self.exp()
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
            self.scopeNumber += 1
            self.scope.append(St_Scope(self.scope[-1]))
            self.symbol_table.append(self.scope[-1])
            self.accept_token()
            self.Dec()
            self.exp()
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
                self.exp()
                if self.check_next_token(")"):
                    self.accept_token()
                    if self.check_next_token("{"):
                        self.scopeNumber += 1
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
            self.scopeNumber += 1
            self.scope.append(St_Scope(self.scope[-1]))
            self.symbol_table.append(self.scope[-1])
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.var_Id.append(self.allTokens[self.token_index]["value"])
                self.insert_st()
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
            self.accept_token()
            self.exp()
            if self.check_next_token(")"):
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

    def class_int(self):
        if self.check_next_token_by_class("Id"):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.accept_token()
                if self.check_next_token("="):
                    self.accept_token()
                    if self.check_next_token("new"):
                        self.accept_token()
                        if self.check_next_token_by_class("Id"):
                            self.accept_token()
                            if self.check_next_token("("):
                                self.accept_token()
                                if self.check_next_token(")"):
                                    self.accept_token()
                                    if self.check_next_token(";"):
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
                # else:
                raise ("Exception")

    def struct(self):
        if self.check_next_token_by_class("Id"):
            self.Id = self.allTokens[self.token_index]["value"]
            self.accept_token()
            if self.check_next_token("{"):
                self.ref = self.Id
                self.parent = None
                self.insert_dt()
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

    def Dec_Var_func(self):
        if self.check_next_token("("):
            self.scopeNumber += 1
            self.scope.append(St_Scope())
            self.symbol_table.append(self.scope[-1])
            self.accept_token()
            self.is_params()
            if self.check_next_token(")"):
                self.accept_token()
                self.insert_mt()
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
        elif self.check_next_token("="):
            self.put_value()
            if self.check_next_token(";"):
                self.accept_token()
                self.insert_mt()
            else:
                raise ("Exception")
        elif self.check_next_token(";"):
            self.insert_mt()
            self.accept_token()

    def func_call_Id_set(self):
        if self.check_next_token("("):
            self.accept_token()
            self.is_params()
            if self.check_next_token(")"):
                self.accept_token()
                if self.check_next_token(";"):
                    self.accept_token()
                else:
                    raise ("Exception")
            else:
                raise ("Exception")
        else:
            if self.check_next_token("="):
                self.accept_token()
                self.exp()
                if self.check_next_token(";"):
                    self.accept_token()
                else:
                    raise ("Exception")
            else:
                raise ("Exception")

    def Dec(self):
        self.dt()
        if self.check_next_token_by_class("Id"):
            self.var_Id.append(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.list()
            self.put_value()
            if self.check_next_token(";"):
                self.insert_st()
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
            self.check_variable_exist(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.func_call_Id_set_class_init()
            if self.check_next_token(";"):
                self.accept_token()
                self.MST()
            else:
                raise ("Exception")
        else:
            pass

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
        if self.check_next_token_by_class("strConst"):
            self.accept_token()
        elif self.check_next_token_by_class("chrConst"):
            self.accept_token()
        elif self.check_next_token_by_class("boolConst"):
            self.accept_token()
        elif self.check_next_token_by_class("numConst"):
            self.accept_token()
        # elif self.check_next_token("["):
        #     self.arrConst()
        else:
            raise ("Exception")

    def arrConst(self):
        if self.check_next_token("["):
            self.accept_token()
            if (
                self.check_next_token_by_class("strConst")
                or self.check_next_token_by_class("chrConst")
                or self.check_next_token_by_class("boolConst")
                or self.check_next_token_by_class("numConst")
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
        self.exp()
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
        if self.check_next_token_by_class("numConst"):
            self.accept_token()
        else:
            raise ("Exception")

    def OP(self):
        if self.check_next_token_by_class("Id"):
            self.check_variable_exist(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.OP_more_Id()
        else:
            raise ("Exception")

    def OP_more_Id(self):
        if self.check_next_token("["):
            self.OP_ex_Id()
        elif self.check_next_token("("):
            self.OP_ex_Id()
        else:
            pass

    def OP_ex_Id(self):
        if self.check_next_token("["):
            self.accept_token()
            self.index()
            if self.check_next_token("]"):
                self.accept_token()
                self.Id_loop()
            else:
                raise ("Exception")
        elif self.check_next_token("("):
            self.accept_token()
            self.is_param_value()
            if self.check_next_token(")"):
                self.accept_token()
                self.Id_loop()
            else:
                raise ("Exception")

    def OP_Id_loop(self):
        if self.check_next_token("."):
            self.accept_token()
            self.OP()
        elif self.check_next_token("("):
            self.accept_token()
            self.is_param_value()
            if self.check_next_token(")"):
                self.accept_token()
                self.Id_loop()
            else:
                raise ("Exception")
        else:
            pass

    def OP_Id_loop1(self):
        if self.check_next_token("."):
            self.accept_token()
            self.OP()

    def VP(self):
        if self.check_next_token_by_class("Id"):
            self.check_variable_exist(self.allTokens[self.token_index]["value"])
            self.accept_token()
            self.VP_more_Id()
        else:
            raise ("Exception")

    def VP_more_Id(self):
        if self.check_next_token("["):
            self.VP_ex_Id()
        else:
            pass

    def VP_ex_Id(self):
        if self.check_next_token("["):
            self.accept_token()
            self.index()
            if self.check_next_token("]"):
                self.accept_token()
                self.Id_loop()
            else:
                raise ("Exception")
        elif self.check_next_token("("):
            self.accept_token()
            self.is_param_value()
            if self.check_next_token(")"):
                self.accept_token()
                self.Id_loop()
            else:
                raise ("Exception")

    def VP_Id_loop(self):
        if self.check_next_token("."):
            self.accept_token()
            self.VP()
        elif self.check_next_token("("):
            self.accept_token()
            self.is_param_value()
            if self.check_next_token(")"):
                self.accept_token()
                self.Id_loop()
            else:
                raise ("Exception")
        else:
            pass

    def VP_Id_loop1(self):
        if self.check_next_token("."):
            self.accept_token()
            self.VP()

    def func_call_Id_set_class_init(self):
        if self.check_next_token("[") or self.check_next_token("("):
            self.OP_ex_Id()
        elif self.check_next_token("="):
            self.accept_token()
            self.exp()
        elif self.check_next_token_by_class("Id"):
            self.class_init_or_not()
        elif self.check_next_token("++") or self.check_next_token("--"):
            self.accept_token()
        else:
            raise ("Exception")

    def class_init_or_not(self):
        if self.check_next_token_by_class("Id"):
            self.accept_token()
        elif self.check_next_token("="):
            self.accept_token()
            if self.check_next_token("new"):
                self.accept_token()
                if self.check_next_token_by_class("Id"):
                    self.accept_token()
                    if self.check_next_token("("):
                        self.accept_token()
                        if self.check_next_token(")"):
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
            self.accept_token()
            self.RE()
            self.AE1()
        else:
            pass

    def RE(self):
        if (
            self.check_next_token_by_class("strConst")
            or self.check_next_token_by_class("chrConst")
            or self.check_next_token_by_class("boolConst")
            or self.check_next_token_by_class("numConst")
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
            self.accept_token()
            if (
                self.check_next_token_by_class("strConst")
                or self.check_next_token_by_class("chrConst")
                or self.check_next_token_by_class("boolConst")
                or self.check_next_token_by_class("numConst")
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
            self.accept_token()
            self.value()
            self.T1()
            self.E1()
        elif self.check_next_token("-"):
            self.accept_token()
            self.value()
            self.T1()
            self.E1()
        else:
            pass

    def T1(self):
        if self.check_next_token("*"):
            self.accept_token()
            self.value()
            self.T1()
        elif self.check_next_token("/"):
            self.accept_token()
            self.value()
            self.T1()
        elif self.check_next_token("%"):
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
                self.accept_token()
                if self.check_next_token("{"):
                    self.accept_token()
                    self.insert_dt()
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
            self.acces_specifiers()
            self.dt()
            if self.check_next_token_by_class("Id"):
                self.Id = self.allTokens[self.token_index]["value"]
                self.accept_token()
                self.Inter_Dec_Var_func()
                if self.check_next_token(";"):
                    self.accept_token()
                    self.IST()
            else:
                raise Exception("Invalid")

    def Inter_Dec_Var_func(self):
        if self.check_next_token("("):
            self.accept_token()
            self.is_params()
            if self.check_next_token(")"):
                self.accept_token()
                self.insert_mt()
            else:
                raise Exception("Invalid")
        elif self.check_next_token(","):
            self.I_List()
        elif self.check_next_token(";"):
            pass
        else:
            raise Exception("Invalid")

    def I_List(self):
        self.insert_mt()
        if self.check_next_token(","):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.Id = self.allTokens[self.token_index]["value"]
                self.accept_token()
                self.I_List()
            else:
                raise Exception("Invalid")
        else:
            pass

#######################################################################################################
#######################################################################################################
class CustomError(Exception):
    pass


class St_Scope:
    def __init__(self, parent=None):
        self.symbols = []
        self.parent = parent

    def declare_variable(self, name, type):
        for symbol in self.symbols:
            if symbol["id"] == name:
                return False
        if self.parent is not None:
            if not self.parent.check_variable(name):
                self.symbols.append({"id": name, "type": type})
            else:
                return False
        self.symbols.append({"id": name, "type": type})
        return True

    def check_variable(self, name):
        for symbol in self.symbols:
            if symbol["id"] == name:
                return True
        if self.parent is not None:
            return self.parent.check_variable(name)
        return False

    def get_variable(self, name):
        for symbol in self.symbols:
            if symbol["id"] == name:
                return symbol
        if self.parent is not None:
            return self.parent.get_variable(name)
        return False


class Mt_Scope:
    def __init__(self, Id, type, am, parent=None):
        self.members = []
        self.Id = Id
        self.am = am
        self.type = type
        self.parent = parent

    def declare_variable(self, name, type, am):
        for symbol in self.members:
            if symbol["id"] == name:
                return False
        self.members.append({"id": name, "type": type, "am": am})
        return True

    def check_variable(self, name):
        for symbol in self.members:
            if symbol["id"] == name:
                return True
        if self.parent is not None:
            return self.parent.check_variable(name)
        return False

    def get_variable(self, name):
        for symbol in self.symbols:
            if symbol["id"] == name:
                return symbol
        if self.parent is not None:
            return self.parent.get_variable(name)
        return False
