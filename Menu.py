class Menu:
    def __init__(self) -> None:
        self.pass_idx = 0
        self.pass_list = [self.display_pass1]
    
    def display_current_pass(self) -> function:
        return self.pass_list[self.pass_idx]
    
    def display_pass1(self) -> None:
        """display log in, sing up menu"""
        print("1. Log in")
        print("2. Sign up")
        print("3. Quit")
        

        