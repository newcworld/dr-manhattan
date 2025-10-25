from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..models.market import Market
from ..models.order import Order, OrderSide
from ..models.position import Position


class Exchange(ABC):
    """
    Base class for all prediction market exchanges.
    Follows CCXT-style unified API pattern.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize exchange with optional configuration.

        Args:
            config: Dictionary containing API keys, options, etc.
        """
        self.config = config or {}
        self.api_key = self.config.get('api_key')
        self.api_secret = self.config.get('api_secret')
        self.timeout = self.config.get('timeout', 30)
        self.verbose = self.config.get('verbose', False)

    @property
    @abstractmethod
    def id(self) -> str:
        """Exchange identifier (e.g., 'polymarket', 'kalshi')"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable exchange name"""
        pass

    @abstractmethod
    def fetch_markets(self, params: Optional[Dict[str, Any]] = None) -> list[Market]:
        """
        Fetch all available markets.

        Args:
            params: Optional parameters for filtering/pagination

        Returns:
            List of Market objects
        """
        pass

    @abstractmethod
    def fetch_market(self, market_id: str) -> Market:
        """
        Fetch a specific market by ID.

        Args:
            market_id: Market identifier

        Returns:
            Market object
        """
        pass

    @abstractmethod
    def create_order(
        self,
        market_id: str,
        outcome: str,
        side: OrderSide,
        price: float,
        size: float,
        params: Optional[Dict[str, Any]] = None
    ) -> Order:
        """
        Create a new order.

        Args:
            market_id: Market identifier
            outcome: Outcome to bet on
            side: Buy or sell
            price: Price per share (0-1 or 0-100 depending on exchange)
            size: Number of shares
            params: Additional exchange-specific parameters

        Returns:
            Order object
        """
        pass

    @abstractmethod
    def cancel_order(self, order_id: str, market_id: Optional[str] = None) -> Order:
        """
        Cancel an existing order.

        Args:
            order_id: Order identifier
            market_id: Market identifier (required by some exchanges)

        Returns:
            Updated Order object
        """
        pass

    @abstractmethod
    def fetch_order(self, order_id: str, market_id: Optional[str] = None) -> Order:
        """
        Fetch order details.

        Args:
            order_id: Order identifier
            market_id: Market identifier (required by some exchanges)

        Returns:
            Order object
        """
        pass

    @abstractmethod
    def fetch_open_orders(
        self,
        market_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> list[Order]:
        """
        Fetch all open orders.

        Args:
            market_id: Optional market filter
            params: Additional parameters

        Returns:
            List of Order objects
        """
        pass

    @abstractmethod
    def fetch_positions(
        self,
        market_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> list[Position]:
        """
        Fetch current positions.

        Args:
            market_id: Optional market filter
            params: Additional parameters

        Returns:
            List of Position objects
        """
        pass

    @abstractmethod
    def fetch_balance(self) -> Dict[str, float]:
        """
        Fetch account balance.

        Returns:
            Dictionary with balance info (e.g., {'USDC': 1000.0})
        """
        pass

    def describe(self) -> Dict[str, Any]:
        """
        Return exchange metadata and capabilities.

        Returns:
            Dictionary containing exchange information
        """
        return {
            'id': self.id,
            'name': self.name,
            'has': {
                'fetch_markets': True,
                'fetch_market': True,
                'create_order': True,
                'cancel_order': True,
                'fetch_order': True,
                'fetch_open_orders': True,
                'fetch_positions': True,
                'fetch_balance': True,
            }
        }
