from typing import Any, Dict

from .crypto import keccak


def collapse_tuple_type(abi):
    """Converts a tuple from a dict to a parenthesized list of its types.

    >>> collapse_tuple_type(
    ...     {
    ...         'components': [
    ...             {'name': 'anAddress', 'type': 'address'},
    ...             {'name': 'anInt', 'type': 'uint256'},
    ...             {'name': 'someBytes', 'type': 'bytes'},
    ...         ],
    ...         'type': 'tuple',
    ...     }
    ... )
    '(address,uint256,bytes)'
    """
    if abi["type"] != "tuple":
        return abi["type"]

    component_types = [
        collapse_tuple_type(component) for component in abi["components"]
    ]

    return "(" + ",".join(component_types) + ")"


def _abi_to_signature(abi: Dict[str, Any]) -> str:
    function_signature = "{fn_name}({fn_input_types})".format(
        fn_name=abi["name"],
        fn_input_types=",".join(
            [collapse_tuple_type(abi_input) for abi_input in abi.get("inputs", [])]
        ),
    )
    return function_signature


def function_signature_to_4byte_selector(event_signature: str) -> bytes:
    return keccak(text=event_signature.replace(" ", ""))[:4]


def function_abi_to_4byte_selector(function_abi: Dict[str, Any]) -> bytes:
    function_signature = _abi_to_signature(function_abi)
    return function_signature_to_4byte_selector(function_signature)


def event_signature_to_log_topic(event_signature: str) -> bytes:
    return keccak(text=event_signature.replace(" ", ""))


def event_abi_to_log_topic(event_abi: Dict[str, Any]) -> bytes:
    event_signature = _abi_to_signature(event_abi)
    return event_signature_to_log_topic(event_signature)
