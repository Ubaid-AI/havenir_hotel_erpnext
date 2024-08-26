"""
Whitelist specific methods. Keep it here all-in-one
rather than separating it in different files.


Added on `hooks.py`
# before_request = ["<app_name>.whitelist_endpoint.run"]
"""
import asyncio
import importlib

import frappe

methods = [
    {"scope": "modules.shipping", "fn": "get_rates_for_quotation"},
    {
        "scope": "modules.shipping",
        "fn": "track_shipping",
        "args": {"allow_guest": True},
    },
]


async def add_to_whitelist(method):
    args = method.get("args", {})
    if "methods" not in args:
        args["methods"] = ["GET"]

    scope = importlib.import_module(
        "havenir_hotel_erpnext.{scope}".format(scope=method["scope"])
    )

    fn = getattr(scope, method["fn"])
    whitelisted_method = frappe.whitelist(**args)(fn)

    setattr(scope, method["fn"], whitelisted_method)


async def whitelist():
    tasks: list = []

    for e in methods:
        tasks.append(add_to_whitelist(e))

    _ = await asyncio.gather(*tasks)


def run(**_):
    """
    Whitelist configured methods
    """
    asyncio.run(whitelist())