
class MissingSignedRequestException(Exception):
    """
    Thrown when a canvas restricted view doesnt have a signed request parameter
    """
    pass


class InvalidSignedRequestException(Exception):
    """
    Thrown when a canvas restricted view has a signed request parameter that doesnt parse
    """
    pass