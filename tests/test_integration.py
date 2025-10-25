"""Integration tests for two-face"""

import pytest
import two_face
from two_face.base.exchange import Exchange


class TestExchangeRegistry:
    """Test exchange registry"""

    def test_exchanges_dict_exists(self):
        """Test that exchanges dict exists"""
        assert hasattr(two_face, 'exchanges')
        assert isinstance(two_face.exchanges, dict)

    def test_polymarket_registered(self):
        """Test Polymarket is registered"""
        assert 'polymarket' in two_face.exchanges
        assert two_face.exchanges['polymarket'] == two_face.Polymarket

    def test_limitless_registered(self):
        """Test Limitless is registered"""
        assert 'limitless' in two_face.exchanges
        assert two_face.exchanges['limitless'] == two_face.Limitless

    def test_exchange_instantiation(self):
        """Test creating exchanges from registry"""
        for exchange_id, exchange_class in two_face.exchanges.items():
            exchange = exchange_class()
            assert isinstance(exchange, Exchange)
            assert exchange.id == exchange_id


class TestUnifiedAPI:
    """Test unified API across exchanges"""

    def test_all_exchanges_have_required_methods(self):
        """Test all exchanges implement required methods"""
        required_methods = [
            'fetch_markets',
            'fetch_market',
            'create_order',
            'cancel_order',
            'fetch_order',
            'fetch_open_orders',
            'fetch_positions',
            'fetch_balance'
        ]

        for exchange_class in two_face.exchanges.values():
            exchange = exchange_class()
            for method in required_methods:
                assert hasattr(exchange, method)
                assert callable(getattr(exchange, method))

    def test_all_exchanges_have_properties(self):
        """Test all exchanges have required properties"""
        for exchange_class in two_face.exchanges.values():
            exchange = exchange_class()
            assert hasattr(exchange, 'id')
            assert hasattr(exchange, 'name')
            assert isinstance(exchange.id, str)
            assert isinstance(exchange.name, str)

    def test_describe_method(self):
        """Test describe method across all exchanges"""
        for exchange_class in two_face.exchanges.values():
            exchange = exchange_class()
            desc = exchange.describe()

            assert 'id' in desc
            assert 'name' in desc
            assert 'has' in desc
            assert isinstance(desc['has'], dict)


class TestModelsExport:
    """Test model exports"""

    def test_market_model_exported(self):
        """Test Market model is exported"""
        assert hasattr(two_face, 'Market')
        from two_face.models.market import Market
        assert two_face.Market == Market

    def test_order_model_exported(self):
        """Test Order model is exported"""
        assert hasattr(two_face, 'Order')
        assert hasattr(two_face, 'OrderSide')
        assert hasattr(two_face, 'OrderStatus')

    def test_position_model_exported(self):
        """Test Position model is exported"""
        assert hasattr(two_face, 'Position')


class TestErrorsExport:
    """Test error exports"""

    def test_base_error_exported(self):
        """Test TwoFaceError is exported"""
        assert hasattr(two_face, 'TwoFaceError')

    def test_all_errors_exported(self):
        """Test all error types are exported"""
        errors = [
            'ExchangeError',
            'NetworkError',
            'RateLimitError',
            'AuthenticationError',
            'InsufficientFunds',
            'InvalidOrder',
            'MarketNotFound'
        ]

        for error_name in errors:
            assert hasattr(two_face, error_name)


class TestPackageVersion:
    """Test package version"""

    def test_version_exists(self):
        """Test __version__ exists"""
        assert hasattr(two_face, '__version__')
        assert isinstance(two_face.__version__, str)

    def test_version_format(self):
        """Test version follows semantic versioning"""
        version = two_face.__version__
        parts = version.split('.')
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)


class TestExchangeInstantiation:
    """Test exchange instantiation"""

    def test_polymarket_instantiation(self):
        """Test creating Polymarket instance"""
        exchange = two_face.Polymarket()
        assert exchange.id == "polymarket"
        assert exchange.name == "Polymarket"
        assert isinstance(exchange, Exchange)

    def test_limitless_instantiation(self):
        """Test creating Limitless instance"""
        exchange = two_face.Limitless()
        assert exchange.id == "limitless"
        assert exchange.name == "Limitless"
        assert isinstance(exchange, Exchange)

    def test_exchange_with_config(self):
        """Test creating exchange with config"""
        config = {'timeout': 60, 'verbose': True}

        poly = two_face.Polymarket(config)
        assert poly.timeout == 60
        assert poly.verbose is True

        limitless = two_face.Limitless(config)
        assert limitless.timeout == 60
        assert limitless.verbose is True


class TestExchangeFactory:
    """Test creating exchanges from factory pattern"""

    def test_create_exchange_from_registry(self):
        """Test creating exchange using registry"""
        exchange = two_face.exchanges['polymarket']()
        assert isinstance(exchange, two_face.Polymarket)
        assert exchange.id == "polymarket"

    def test_iterate_all_exchanges(self):
        """Test iterating through all exchanges"""
        exchanges = []
        for exchange_id in two_face.exchanges:
            exchange = two_face.exchanges[exchange_id]()
            exchanges.append(exchange)

        assert len(exchanges) == 2
        assert all(isinstance(e, Exchange) for e in exchanges)

    def test_exchange_count(self):
        """Test number of registered exchanges"""
        assert len(two_face.exchanges) == 2
