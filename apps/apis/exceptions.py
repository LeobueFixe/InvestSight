class PriceAPIError(Exception):
    pass


class ProviderUnavailable(PriceAPIError):
    pass
