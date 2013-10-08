
class MissingSignedRequestException(Exception):
    """
    Thrown when a canvas restricted view doesn't have a signed
    request parameter.

    """
    pass


class InvalidSignedRequestException(Exception):
    """
    Thrown when a canvas restricted view has a signed request
    parameter that doesn't parse.

    """
    pass
