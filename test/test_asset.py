import pytest
from app.Asset import Asset

def setup_module(module):
    pass

def test_asset_constructor():
    with pytest.raises(TypeError) as e:
        asset = Asset()