from typing import Callable, Dict, List
from ._exceptions import CommandAlreadyReg
from ._fingerprint import Fingerprint
from ._command_meta import CommandMeta
from inspect import signature, Parameter
import functools

class Callixir:

	def __init__(self):
		self.__commands: Dict[str, CommandMeta] = {}

	def _get_fingerprint(self, func: Callable) -> Fingerprint:
		sig = signature(func)
		param_types = {}
		has_varargs = False

		for param_name, param in sig.parameters.items():
			if param.kind == Parameter.VAR_POSITIONAL:
				has_varargs = True
			param_types[param_name] = param.annotation if param.annotation != param.empty else None

		return Fingerprint(
			signature=sig,
			param_types=param_types,
			has_varargs=has_varargs
		)

	def _register_command(self, name: str, func: Callable):
		if name in self.__commands: raise CommandAlreadyReg(f"Cannot register the same command twice: '{name}'")
		self.__commands[name] = CommandMeta(
			name=name,
			func=func,
			fingerprint=self._get_fingerprint(func)
		)

	def register(self, name: str, func: Callable):
		self._register_command(name=name, func=func)

	# Decorator
	def reg(self, name: str):

		def decorator(func: Callable):
			self._register_command(name=name, func=func)
			return func

		return decorator

	@property
	def commands(self) -> List[CommandMeta]: return [cmd for cmd in self.__commands.values()]