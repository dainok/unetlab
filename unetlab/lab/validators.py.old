import re
import ipaddress
from typing import List, Literal, Union
from pydantic import BaseModel, validator


def is_jinja(value: str) -> bool:
    return "{{" in value and "}}" in value


class InterfaceRule(BaseModel):
    match: str
    address: str
    mask: Union[int, Literal["auto"]]
    features: List[str] = []

    # --- VALIDATORS ---
    @validator("match")
    def validate_match_regex(cls, v):
        if not is_jinja(v):
            try:
                re.compile(v)
            except re.error as e:
                raise ValueError(f"Invalid regex in match: {e}")
        return v

    @validator("address")
    def validate_address(cls, v):
        if is_jinja(v):
            return v
        try:
            ipaddress.ip_network(v, strict=False)
        except ValueError:
            raise ValueError(f"Invalid CIDR address: {v}")
        return v

    @validator("mask")
    def validate_mask(cls, v, values):
        if v == "auto":
            return v
        if "address" in values and not is_jinja(values["address"]):
            try:
                net = ipaddress.ip_network(values["address"], strict=False)
            except ValueError:
                return v
            if v > net.prefixlen:
                raise ValueError(
                    f"Mask {v} is longer than CIDR prefix {net.prefixlen} for address {values['address']}"
                )
        return v

    @validator("features", each_item=True)
    def validate_features(cls, v):
        if is_jinja(v):
            return v
        # formato: feature[:key=value,...]
        parts = v.split(":", 1)
        if not parts[0]:
            raise ValueError(f"Invalid feature format: {v}")
        if len(parts) == 2 and parts[1]:
            for kv in parts[1].split(","):
                if "=" not in kv:
                    raise ValueError(f"Invalid feature argument in {v}: {kv}")
        return v
