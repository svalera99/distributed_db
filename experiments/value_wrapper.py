class ValueWrapper:
    def __init__(self, other_val_wrapper = None) -> None:
        if other_val_wrapper is not None:
            self.val = other_val_wrapper.val
        else:
            self.val = 0

    def __eq__(self, __value: object) -> bool:
        if __value == self:
            return True
        if not isinstance(__value, ValueWrapper):
            return False
        return self.val == __value.val
    
    def __str__(self) -> str:
        return str(self.val)