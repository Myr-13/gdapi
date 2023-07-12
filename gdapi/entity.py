from .utils import b64_decrypt, b64_encrypt

data_key_id = 1  # Number
data_key_x = 2  # Number
data_key_y = 3  # Number
data_key_color_channel = 21  # Number
data_key_text = 31  # b64 encoded text
data_key_use_hsv = 41  # Number (1 or 0)
data_key_hsv = 43  # See docs.md (Groups Packing)
data_key_groups = 57  # See docs.md (HSV Packing)


class Entity:
	def __init__(self):
		self.id = 0
		self.x = 0
		self.y = 0

		# Attributes
		self.text = None

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

		data += b";"

		return data
