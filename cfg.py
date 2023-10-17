class cfg:
    def __init__(self, tokens) -> None:
        self.allTokens = tokens
        self.token_index = 0
        self.scope=0
        self.main_symbol_table=[]
        self.class_symbol_table=[]

    def check_next_token_by_class(self, expected_value):
        return self.allTokens[self.token_index]["class"] == expected_value

    def check_next_token(self, expected_value):
        return self.allTokens[self.token_index]["value"] == expected_value

    def accept_token(self, isDeclaration):
        self.token_index += 1
        if len(self.allTokens) > self.token_index:
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
            pass

    def S_or_M(self):
        if self.check_next_token_by_class("Id"):
            self.accept_token()
        elif self.check_next_token("{"):
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
                        self.mst()
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
            self.accept_token()
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
            self.accept_token()
            pass
        else:
            self.acces_specifiers()
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
