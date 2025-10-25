class TwoFaceError(Exception):
    """Base exception for all two-face errors"""
    pass


class ExchangeError(TwoFaceError):
    """Exchange-specific error"""
    pass


class NetworkError(TwoFaceError):
    """Network connectivity error"""
    pass


class RateLimitError(TwoFaceError):
    """Rate limit exceeded"""
    pass


class AuthenticationError(TwoFaceError):
    """Authentication failed"""
    pass


class InsufficientFunds(TwoFaceError):
    """Insufficient funds for operation"""
    pass


class InvalidOrder(TwoFaceError):
    """Invalid order parameters"""
    pass


class MarketNotFound(TwoFaceError):
    """Market does not exist"""
    pass
