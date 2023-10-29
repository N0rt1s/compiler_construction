class cfg:
    def __init__(self, tokens) -> None:
        self.allTokens = tokens
        self.token_index = 0
        self.symbol_table = []
        self.definition_table = []
        self.member_table = []
        self.scope = 0
        self.am = ""
        self.Id = ""
        self.dt = ""
        self.cp = ""

    def check_next_token_by_class(self, expected_value):
        return self.allTokens[self.token_index]["class"] == expected_value

    def check_next_token(self, expected_value):
        return self.allTokens[self.token_index]["value"] == expected_value

    def insert_st(self):
        existing_object = list(filter(lambda x: x["id"] == self.Id, self.symbol_table))
        if len(existing_object) == 0 and existing_object[0]["scope"] != self.scope:
            self.symbol_table.append(
                {"id": self.Id, "dataType": self.dt, "scope": self.scope}
            )
        else:
            raise CustomError(f"The variable {self.Id} already exists.")

    def accept_token(self):
        self.token_index += 1
        if self.token_index > (len(self.allTokens) - 1):
            self.token_index = -1

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
            raise ("Exception")

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
        self.class_dec()
        self.more_classes()

    def more_classes(self):
        if self.token_index != -1:
            self.rest()
        else:
            print("Parsing Complete")

    def class_dec(self):
        self.acces_specifiers()
        if self.check_next_token("class"):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.accept_token()
                self.derived()
                if self.check_next_token("{"):
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
        else:
            raise ("Exeption")

    def derived(self):
        if self.check_next_token(":"):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.accept_token()
            else:
                raise ("Exeption")
        else:
            pass

    def constructor(self):
        if self.check_next_token_by_class("Id"):
            self.accept_token()
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
        self.dt_or_id()
        if self.check_next_token_by_class("Id"):
            self.accept_token()
            self.more_params()
        else:
            raise ("Exception")

    def dt_or_id(self):
        if self.check_next_token_by_class("DataType"):
            self.accept_token()
        elif self.check_next_token_by_class("Id"):
            self.accept_token()
        else:
            raise ("Exception")

    def more_params(self):
        if self.check_next_token(","):
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
                self.accept_token()
                self.struct()
                self.cst()
            else:
                self.dt()
                if self.check_next_token_by_class("Id"):
                    self.accept_token()
                    self.Dec_Var_func()
                    self.cst()
                else:
                    raise ("Exception")

    def acces_specifiers(self):
        if self.check_next_token("public"):
            self.accept_token()
        elif self.check_next_token("private"):
            self.accept_token()
        else:
            pass

    def dt(self):
        if self.check_next_token_by_class("DataType"):
            self.accept_token()
        elif self.check_next_token_by_class("ArrayDataType"):
            self.accept_token()
        self.dt = self.allTokens[self.token_index]["value"]

    def list(self):
        if self.check_next_token(","):
            self.accept_token()
            if self.check_next_token_by_class("Id"):
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
                or self.check_next_token_by_class("charConst")
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

    def function(self):
        self.acces_specifiers()
        self.dt()
        if self.check_next_token_by_class("Id"):
            self.accept_token()
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
            self.accept_token()
            self.Dec()
            self.exp()
            if self.check_next_token(";"):
                self.accept_token()
                if self.check_next_token_by_class("Id"):
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

    # def part1(self):
    #     self.dec()

    def while_loop(self):
        if self.check_next_token("while"):
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
            self.accept_token()
            if self.check_next_token_by_class("Id"):
                self.accept_token()
                if self.check_next_token("in"):
                    self.accept_token()
                    if self.check_next_token_by_class("Id"):
                        self.accept_token()
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
            self.accept_token()
            if self.check_next_token("{"):
                self.accept_token()
                self.cst()
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
        elif self.check_next_token(","):
            self.list()
            if self.check_next_token(";"):
                self.accept_token()
        elif self.check_next_token(";"):
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
            self.accept_token()
            # self.Id=s=
            self.list()
            self.put_value()
            if self.check_next_token(";"):
                self.accept_token()
            else:
                raise ("Exception")
        else:
            raise ("Exception")

    def MST(self):
        if self.check_next_token_by_class("DataType"):
            self.Dec()
            self.MST()
        elif self.check_next_token("if"):
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
        elif self.check_next_token_by_class("charConst"):
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
                or self.check_next_token_by_class("charConst")
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

    # def arrConst(self):
    #     if self.check_next_token_by_class("strArrConst"):
    #         self.accept_token()
    #     elif self.check_next_token_by_class("charArrConst"):
    #         self.accept_token()
    #     elif self.check_next_token_by_class("boolArrConst"):
    #         self.accept_token()
    #     elif self.check_next_token_by_class("numArrConst"):
    #         self.accept_token()
    #     elif self.check_next_token_by_class("objArrConst"):
    #         self.arrConst()
    #     else:
    #         raise ("Exception")

    def index(self):
        if self.check_next_token_by_class("numConst"):
            self.accept_token()
        else:
            raise ("Exception")

    def OP(self):
        if self.check_next_token_by_class("Id"):
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
        # if (
        #     self.check_next_token_by_class("strConst")
        #     or self.check_next_token_by_class("charConst")
        #     or self.check_next_token_by_class("boolConst")
        #     or self.check_next_token_by_class("numConst")
        # ):
        #     self.accept_token()
        #     self.T1()
        #     self.E1()
        #     self.RE1()
        # elif self.check_next_token_by_class("Id"):
        #     self.VP()
        #     self.T1()
        #     self.E1()
        #     self.RE1()
        if (
            self.check_next_token_by_class("strConst")
            or self.check_next_token_by_class("charConst")
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
            # if (
            #     self.check_next_token_by_class("strConst")
            #     or self.check_next_token_by_class("charConst")
            #     or self.check_next_token_by_class("boolConst")
            #     or self.check_next_token_by_class("numConst")
            # ):
            #     self.accept_token()
            #     self.T1()
            #     self.E1()
            #     self.RE1()
            # elif self.check_next_token_by_class("Id"):
            #     self.VP()
            #     self.T1()
            #     self.E1()
            #     self.RE1()
            if (
                self.check_next_token_by_class("strConst")
                or self.check_next_token_by_class("charConst")
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


class CustomError(Exception):
    pass
