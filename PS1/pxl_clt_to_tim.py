import struct
import sys
import os

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def create_tim_from_pxl_clt(pxl_data, clt_data):
    pxl_id, pxl_version, pxl_reserved, pxl_flags = struct.unpack('<BBHI', pxl_data[:8])
    if pxl_id != 0x12:
        raise ValueError("Invalid PXL file ID (expected 0x12)")
    
    clt_id, clt_version, clt_reserved, clt_flags = struct.unpack('<BBHI', clt_data[:8])
    if clt_id != 0x11:
        raise ValueError("Invalid CLT file ID (expected 0x11)")
    
    clut_section = clt_data[8:]
    pxl_section = pxl_data[8:]
    
    tim_id = 0x10
    tim_version = 0x00
    tim_reserved = 0x0000
    tim_flags = (pxl_flags & 0x07) | 0x08
    
    tim_data = bytearray()
    tim_data.extend(struct.pack('<BBHI', tim_id, tim_version, tim_reserved, tim_flags))
    tim_data.extend(clut_section)
    tim_data.extend(pxl_section)
    
    return bytes(tim_data)

def main():
    if len(sys.argv) < 3:
        print("pxl_clt_to_tim.py by Pio")
        print("Converts PS1 pxl and clt files to a tim texture")
        print("\nUsage: pxl_clt_to_tim.py <input.pxl> <input.clt> [output.tim]")
        print("If output_basename is not provided, input pxl filename will be used as base")
        return

    pxl_file = sys.argv[1]
    clt_file = sys.argv[2]
    tim_file = sys.argv[3] if len(sys.argv) >= 4 else os.path.splitext(pxl_file)[0] + ".tim"
    
    try:
        pxl_data = read_file(pxl_file)
        clt_data = read_file(clt_file)
        tim_data = create_tim_from_pxl_clt(pxl_data, clt_data)
        with open(tim_file, 'wb') as f:
            f.write(tim_data)
        print(f"Successfully created {tim_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
