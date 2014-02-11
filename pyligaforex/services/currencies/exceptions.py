class CurrencyBaseError(RuntimeError):
    pass


class CurrencyNotFoundError(CurrencyBaseError):
    pass
