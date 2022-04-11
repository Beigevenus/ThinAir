
# A basic min/max function
def limit(num: float, minimum: float = 0, maximum: float = 255) -> float:
    # TODO: Write docstring for function
    return max(min(num, maximum), minimum)
