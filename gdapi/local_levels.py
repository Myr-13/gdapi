from typing import List
from xml.etree import ElementTree as ET

from .utils import *
from .level import Level
from .exceptions import InvalidXMLData


class LocalLevels:
	def __init__(self, debug=False):
		self.debug: bool = debug
		self.levels: List[Level] = []

	def dlog(self, text: str):
		if not self.debug:
			return

		print(f"[DEBUG][LLS]: {text}")

	def load_file(self, file: str):
		file = open(file, "rb")
		data = file.read()

		data = decrypt_level(data)
		self.dlog(data)
		root = ET.fromstring(data)

		levels_root = root.find("dict").find("d")
		for level_data in levels_root.findall("d"):
			key_found = False
			key_name = ""
			values = {}

			for elem in level_data.iter():
				if elem.tag == "k":
					if key_found:
						raise InvalidXMLData("key is found after another key")

					key_name = elem.text
					key_found = True
				elif key_found:
					values[key_name] = elem.text
					key_found = False

			level = Level()
			level.load(values)
			self.levels.append(level)

		file.close()

	def save_file(self, file: str):
		raw_levels_data = []

		for level in self.levels:
			raw_levels_data.append(level.save())

		levels_data = \
			"<?xml version=\"1.0\"?>" \
			"<plist version=\"1.0\" gjver=\"2.0\">" \
			"<dict>" \
			"<k>LLM_01</k>" \
			"<d>" \
			"<k>_isArr</k>" \
			"<t />".encode()
		level_id = 0

		for level_data in raw_levels_data:
			levels_data += f"<k>k_{level_id}</k>".encode()
			levels_data += level_data

			level_id += 1

		levels_data += \
			"</d>" \
			"<k>LLM_02</k>" \
			"<i>35</i>" \
			"</dict>" \
			"</plist>".encode()

		levels_data = encrypt_level(levels_data)

		f = open(file, "wb")
		f.write(levels_data)
