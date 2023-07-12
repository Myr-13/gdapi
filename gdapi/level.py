from typing import Dict, List

from .utils import decrypt, encrypt
from .entity import Entity
from .color_channel import ColorChannel


key_author = "k5"
key_data = "k4"
key_desc = "k3"
key_name = "k2"


class Level:
	def __init__(self):
		self.name: str = ""
		self.desc: str = ""
		self.author: str = ""
		self.entities: List[Entity] = []
		self.color_channels: List[ColorChannel] = []

	def __str__(self):
		return f"Level <'{self.name}' by '{self.author}'>"

	def load_data(self, data: bytes):
		data = decrypt(data)

		split_data = data.split(b";")

		cc_data = split_data[0]
		split_data = split_data[1:-1]

		cc_data = cc_data.split(b"|")[:-1]
		for c in cc_data:
			if b"kS38" in c:
				c = c[5:]

			color_channel = ColorChannel()
			color_channel.load(c)

			self.color_channels.append(color_channel)

		for entity_data in split_data:
			ent = Entity()
			ent.load(entity_data)

			self.entities.append(ent)

	def load(self, level_data: Dict[str, str]):
		for k in level_data:
			value = level_data[k]

			if k == key_author:
				self.author = value
			elif k == key_data:
				self.load_data(value.encode())
			elif k == key_desc:
				self.desc = value
			elif k == key_name:
				self.name = value

	def save(self):
		# Encode entities data
		ent_data = b""
		for ent in self.entities:
			ent_data += ent.save()
		groups_data = b"kS38,1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1|1_0_2_102_3_255_11_255_12_255_13_255_4_-1_6_1001_7_1_15_1_18_0_8_1|1_0_2_102_3_255_11_255_12_255_13_255_4_-1_6_1009_7_1_15_1_18_0_8_1|1_255_2_255_3_255_11_255_12_255_13_255_4_-1_6_1002_5_1_7_1_15_1_18_0_8_1|1_255_2_255_3_0_11_255_12_255_13_255_4_-1_6_1005_5_1_7_1_15_1_18_0_8_1|1_255_2_255_3_0_11_255_12_255_13_255_4_-1_6_1006_5_1_7_1_15_1_18_0_8_1|,kA13,0,kA15,0,kA16,0,kA14,,kA6,0,kA7,0,kA17,0,kA18,0,kS39,0,kA2,0,kA3,0,kA8,0,kA4,0,kA9,0,kA10,0,kA11,0;"
		encrypt_data = groups_data + ent_data
		ent_data = encrypt(encrypt_data).decode()

		gzip_header = "H4sIAAAAAAAAC"
		ent_data = gzip_header + ent_data[13:]

		xml_data = f"<d><k>kCEK</k><i>4</i><k>k2</k><s>{self.name}</s><k>k4</k><s>{ent_data}</s><k>k5</k><s>{self.author}</s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>2</i><k>k50</k><i>35</i><k>k47</k><t /><k>kI1</k><r>0</r><k>kI2</k><r>36</r><k>kI3</k><r>1</r><k>kI6</k><d><k>0</k><s>0</s><k>1</k><s>0</s><k>2</k><s>0</s><k>3</k><s>0</s><k>4</k><s>0</s><k>5</k><s>0</s><k>6</k><s>0</s><k>7</k><s>0</s><k>8</k><s>0</s><k>9</k><s>0</s><k>10</k><s>0</s><k>11</k><s>0</s><k>12</k><s>0</s></d></d>"
		data = xml_data.encode()

		return data
