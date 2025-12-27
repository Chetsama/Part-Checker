from typing import List, Dict, Any
import requests


# Data models for our application
class ComputerPart:
    def __init__(self, name: str, price: float = 0.0):
        self.name = name
        self.price = price

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "price": self.price}


class PriceRecord:
    def __init__(self, part_name: str, prices: List[float]):
        self.part_name = part_name
        self.prices = prices

    def to_dict(self) -> Dict[str, Any]:
        return {"part_name": self.part_name, "prices": self.prices}


class UserInput:
    def __init__(self, parts_list: List[str]):
        self.parts_list = parts_list

    def to_dict(self) -> Dict[str, Any]:
        return {"parts_list": self.parts_list}
