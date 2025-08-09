from struct import unpack, pack
from io import BytesIO


class Overlay:
	def __init__(self, file):
		with open(file, 'rb', buffering=128) as f:
			header, unk, segment_start, text_size, data_size, bss_size, static_init, static_init_end = unpack('<8I', f.read(4 * 8))
			self.filename = unpack('96s', f.read(96))[0].rstrip(b'\x00').decode('latin1')
			header_str = header.to_bytes(4, 'little').decode('latin-1')
			if header_str != 'MWo3':
				raise PermissionError(f'CANT EXECUTE OVERLAY MODULE {self.filename} ')
			self.text = f.read(text_size)
			self.data = BytesIO(f.read(data_size))
			self.bss = BytesIO(b'\x00' * bss_size)


if __name__ == '__main__':
	header = True
	o = Overlay('0000.mwo3')
	if o:
		print(f'{o.text}, {o.data.getvalue()}, {o.bss.getvalue()}')
	else:
		print('No file')
	with open(o.filename, 'wb') as f:
		if header is True:
			f.write(pack('4s', b'TEXT'))
			f.write(b'\x00' * 12)
			f.write(o.text)
			f.write(pack('4s', b'DATA'))
			f.write(b'\x00' * 12)
			f.write(o.data.getvalue())
			f.write(pack('4s', b'BSS'))
			f.write(b'\x00' * 12)
			f.write(o.bss.getvalue())
		else:
			f.write(o.text)
			f.write(o.data.getvalue())
			f.write(o.bss.getvalue())

		