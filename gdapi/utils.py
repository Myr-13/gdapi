import base64
import gzip


# GD uses key 11 for encrypting levels
def xor(data: bytes) -> bytes:
	res = b""
	for i in data:
		res += (i ^ 11).to_bytes(1, "little")
	return res


def b64_decrypt(data: bytes):
	while len(data) % 4 != 0:
		data += b"="
	return base64.b64decode(data)


def b64_encrypt(data: bytes):
	data = base64.b64encode(data)
	return data


def decrypt(data: bytes):
	final = data.replace(b"-", b"+").replace(b"_", b"/")
	final = b64_decrypt(final)
	final = gzip.decompress(final)

	return final


def decrypt_level(data: bytes):
	final = xor(data)
	final = decrypt(final)

	return final


def encrypt(data: bytes):
	final = gzip.compress(data)
	final = b64_encrypt(final)
	final = final.replace(b"+", b"-").replace(b"/", b"_")

	return final


def encrypt_level(data: bytes):
	final = encrypt(data)
	final = xor(final)

	return final


def read_hsv(data: str):
	s = data.split("a")
	final = []

	for s2 in s:
		final.append(float(s2))

	return tuple(final)


def save_hsv(data: tuple):
	out = ""
	for v in data:
		out += str(v) + "a"
	out = out[:-1]

	return out
