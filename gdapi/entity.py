from .utils import b64_decrypt, b64_encrypt

# Every entity
data_key_id = 1  # Number
data_key_x = 2  # Number
data_key_y = 3  # Number
data_key_groups = 57  # See docs.md (HSV Packing)

# Normal tile
data_key_color_channel = 21  # Number
data_key_use_hsv = 41  # Number (1 or 0)
data_key_hsv = 43  # See docs.md (Groups Packing)

# Triggers
data_key_trigger_time = 10  # Number
data_key_trigger_group = 51  # Number
data_key_trigger_spawn_t = 62  # Number (1 or 0)
data_key_trigger_spawn_mt = 87  # Number (1 or 0)

# Color trigger
data_key_ct_r = 7  # Number
data_key_ct_g = 8  # Number
data_key_ct_b = 9  # Number
data_key_ct_color_channel = 23  # Number

# Move trigger
data_key_mt_x = 28  # Number
data_key_mt_y = 29  # Number
data_key_mt_easing_time = 85  # Float

# Spawn trigger
data_key_st_delay = 63  # Float

# Text object
data_key_text = 31  # b64 encoded text


class Entity:
	def __init__(self):
		self.id = 0
		self.x = 0
		self.y = 0

		# Attributes
		self.text = None
		self.color_channel = 0

	def __str__(self):
		return f"Entity <{self.id} {self.x} {self.y}>"

	def load(self, data: bytes):
		data = data.decode().split(",")

		attrs = {}
		for i in range(0, len(data), 2):
			attrs[data[i]] = data[i + 1]

		print(attrs)

		for attr in attrs:
			value = attrs[attr]
			attr = int(attr)

			if value.isdigit():
				value = int(value)

			if attr == data_key_id:
				self.id = value
			elif attr == data_key_x:
				self.x = value
			elif attr == data_key_y:
				self.y = value
			elif attr == data_key_text:
				self.text = b64_decrypt(value.encode())
			elif attr == data_key_color_channel:
				self.color_channel = value

	def save(self):
		data = b""

		data += f"{data_key_id},{self.id},".encode()
		data += f"{data_key_x},{self.x},".encode()
		data += f"{data_key_y},{self.y}".encode()

		if self.text:
			text_data = self.text
			if isinstance(text_data, str):
				text_data = text_data.encode()

			data += f",{data_key_text},{b64_encrypt(text_data).decode()}".encode()
		if self.color_channel:
			data += f",{data_key_color_channel},{self.color_channel}".encode()

		data += b";"

		return data
