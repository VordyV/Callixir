from typing import Dict, Type
from inspect import Signature

class Fingerprint:

	def __init__(self, signature: Signature, param_types: Dict, has_varargs: bool, keyword_arg: str, required_args: list):
		self.signature = signature
		self.param_types = param_types
		self.has_varargs = has_varargs
		self.keyword_arg = keyword_arg
		self.required_args = required_args