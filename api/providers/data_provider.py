import os
import threading

from models.warehouses import Warehouses
from models.locations import Locations
from models.transfers import Transfers
from models.transfer_items import TransferItems
from models.items import Items
from models.item_lines import ItemLines
from models.item_groups import ItemGroups
from models.item_types import ItemTypes
from models.inventories import Inventories
from models.suppliers import Suppliers
from models.orders import Orders
from models.order_items import OrderItems
from models.clients import Clients
from models.shipments import Shipments
from models.shipment_items import ShipmentItems

DEBUG = False

_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data")
)

ROOT_PATH = _ROOT + os.sep

""" it now work like a dict in c#. the first api request will create the object in memory and then it will be reused for the next requests"""
_pools = {}
_pools_lock = threading.Lock()

def _get_pool(models_class):
    with _pools_lock:
        if models_class not in _pools:
            _pools[models_class] = models_class(ROOT_PATH, DEBUG)
        return _pools[models_class]

def fetch_warehouse_pool():
    return _get_pool(Warehouses)

def fetch_location_pool():
    return _get_pool(Locations)

def fetch_transfer_pool():
    return _get_pool(Transfers)

def fetch_transfer_item_pool():
    return _get_pool(TransferItems)

def fetch_item_pool():
    return _get_pool(Items)

def fetch_item_line_pool():
    return _get_pool(ItemLines)

def fetch_item_group_pool():
    return _get_pool(ItemGroups)

def fetch_item_type_pool():
    return _get_pool(ItemTypes)

def fetch_inventory_pool():
    return _get_pool(Inventories)

def fetch_supplier_pool():
    return _get_pool(Suppliers)

def fetch_order_pool():
    return _get_pool(Orders)

def fetch_order_item_pool():
    return _get_pool(OrderItems)

def fetch_client_pool():
    return _get_pool(Clients)

def fetch_shipment_pool():
    return _get_pool(Shipments)

def fetch_shipment_item_pool():
    return _get_pool(ShipmentItems)