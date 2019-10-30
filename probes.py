import ctypes
import functools
import sys


class MemoryDigger:
    @classmethod
    def view_object(cls, obj):
        return cls(start=id(obj), length=sys.getsizeof(obj))

    def __init__(self, start, *, end=None, length=None, safety_checks=True):
        self.start = start
        if end is None:
            end = start + length
        self.end = end

        if end < start:
            raise ValueError("end before start")
        if safety_checks and end - start > 0xFFFF:
            raise ValueError("size greater than 64k, really?")

        self.mem = None
        self.load()

    def __len__(self) -> int:
        return self.end - self.start

    def load(self):
        mem = []
        for x in range(len(self)):
            mem.append(ctypes.c_char.from_address(self.start + x).value[0])
        mem = bytes(mem)
        self.mem = mem

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(start={self.start:#_x}, length={len(self):#_x})"
        )

    def hex_view(self, *args, **kwargs):
        kwargs.setdefault("offset", self.start)
        return hex_view(self.mem, *args, **kwargs)

    def hex_view_compact(self, *args, **kwargs):
        kwargs.setdefault("offset", self.start)
        return hex_view_compact(self.mem, *args, **kwargs)


def hex_view(mem, row_len=16, *, offset=0, inter_group=" ", inter_byte=" "):
    mem_prefix = (offset // 0x1_0000) % 0x1_0000_0000
    header = (inter_group + inter_byte).join(
        (
            inter_byte.join(format(c % 0x10, " 2x") for c in range(m, m + 8))
            for m in range(0, row_len, 8)
        )
    )
    print(f"0x{mem_prefix:09_X}_", "|", header)
    for n in range(0, len(mem), row_len):
        line_data = mem[n : n + row_len]
        line_segments = (inter_group + inter_byte).join(
            (
                inter_byte.join(format(c, "02x") for c in line_data[m : m + 8])
                for m in range(0, row_len, 8)
            )
        )
        offset_low = (offset + n) % 0x1_0000
        print(f"        {offset_low:04X}", "|", line_segments)


hex_view_compact = functools.partial(hex_view, inter_byte="", row_len=32)
# hex_view(mem, inter_byte="", row_len=32)
# hex_view(mem)
