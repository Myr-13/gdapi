from .utils import read_hsv, save_hsv

cc_key_r = 1
cc_key_g = 2
cc_key_b = 3
cc_key_player_color = 4
cc_key_blending = 5
cc_key_id = 6
cc_key_alpha = 7
cc_key_copy_color = 9
cc_key_copy_color_hsv = 10


class ColorChannel:
	def __init__(self):
		self.id = 0
		self.r = 0
		self.g = 0
		self.b = 0
		self.player_color = -1
		self.alpha = 1.0
		self.cc_id = 0
		self.cc_hsv = ()

	def __str__(self):
		return f"ColorChannel <{self.id} {self.r} {self.g} {self.b}>"

	def load(self, data: bytes):
		data = data.split(b"_")
		attrs = {}

		for i in range(0, len(data), 2):
			# Maybe it can be more optimized
			try:
				attrs[int(data[i])] = int(data[i + 1])
			except ValueError as e:
				try:
					attrs[int(data[i])] = float(data[i + 1])
				except ValueError as e:
					attrs[int(data[i])] = data[i + 1].decode()

		for attr in attrs:
			value = attrs[attr]

			if attr == cc_key_r:
				self.r = value
			elif attr == cc_key_g:
				self.g = value
			elif attr == cc_key_b:
				self.b = value
			elif attr == cc_key_id:
				self.id = value
			elif attr == cc_key_player_color:
				self.player_color = value
			elif attr == cc_key_alpha:
				self.alpha = value
			elif attr == cc_key_copy_color:
				self.cc_id = value
			elif attr == cc_key_copy_color_hsv:
				self.cc_hsv = read_hsv(value)

	def save(self):
		data = f"{cc_key_r}_{self.r}_"
		data += f"{cc_key_g}_{self.g}_"
		data += f"{cc_key_b}_{self.b}_"
		data += "11_255_12_255_13_255_"  # IDK what is this
		data += f"{cc_key_player_color}_{self.player_color}_"
		data += f"{cc_key_id}_{self.id}_"
		data += f"{cc_key_alpha}_{int(self.alpha) if (self.alpha == 1.0 or self.alpha == 0.0) else self.alpha}_"
		data += "15_1_18_0_8_1"  # IDK what is this x2
		if self.cc_id != 0:
			data += f"_{cc_key_copy_color}_{self.cc_id}"
		if len(self.cc_hsv) != 0:
			data += f"_{cc_key_copy_color_hsv}_{save_hsv(self.cc_hsv)}"

		return data.encode()
