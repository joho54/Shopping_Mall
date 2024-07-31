class OutputSystem:
    def __init__(self) -> None:
        pass
    
    def str_format(self, string: any, is_line=None):
        string = '-'*18 if is_line else string
        string = str(string)
        col_len = 20
        # product.name의 길이가 col_len보다 길 경우, 이름을 col_len 길이에 맞춰 자릅니다.
        display_name = string if len(string) <= col_len else string[:col_len]
        name_space_half = (col_len - len(display_name)) // 2
        padded_product = '|' + (' ' * name_space_half) + display_name + (' ' * (col_len - len(display_name) - name_space_half)) + '|'
        return padded_product
            