class cfg:
    def __init__(self,tokens) -> None:
        self.allTokens=tokens
        self.token_index=0

    def check_next_token_by_class(self,expected_value):
        return self.allTokens[self.token_index]['class'] == expected_value

    def check_next_token(self,expected_value):
        return self.allTokens[self.token_index]['value'] == expected_value

    def accept_token(self,isDeclaration):
        self.token_index+=1

    def excecute_start(self):
        self.exceute_importing_modules()
        self.exceute_rest()

    def exceute_importing_modules(self):
        if self.check_next_token("#"):
            self.accept_token()
            if self.check_next_token("import"):
                self.accept_token()
                self.exceute_S_or_M()
        else:
            pass

    def exceute_S_or_M(self):
        if self.check_next_token_by_class("Id"):
            self.accept_token()
        elif self.check_next_token("{"):
            if self.check_next_token_by_class("Id"):
                self.accept_token()
                self.excecute_mutiple_Id()
            elif self.check_next_token("}"):
                self.accept_token()
                



    def excecute_mutiple_Id(self):
        pass

    def exceute_rest(self):
        pass    









        