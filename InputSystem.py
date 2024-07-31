import string

class InputSystem:
    def __init__(self) -> None:
        pass
    
    def get_input_range(self, prompt, options):
        """Gets prompt string and possible options. Returns the value if is it correct else False.
        **Warning: it changes type of user input to int before range check.

        Args:
            prompt (str): prompt to show
            options (list): possible option for input

        Returns:
            user_input: user input.
        """
        while True:
            user_input = input(prompt)
            if user_input in options:
                return user_input
            else:
                print("Invalid input, please try again.")
    
    def get_input(self, prompt: str, type=None):
        while True:
            user_input = input(prompt)
            if not user_input:
                print("Value is empty.")
                continue
            if type == int and user_input.isdigit():
                return user_input
            elif type == str and not user_input.isdigit():
                return user_input
            elif type is None:
                return user_input
            print("Invalid input. Please try again")


if __name__ == "__main__":
    inputs = InputSystem()
    a = inputs.get_input_of_type("enter str: ", string)
    print(a)