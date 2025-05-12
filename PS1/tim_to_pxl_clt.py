import struct
import sys
import os

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def split_tim_to_pxl_clt(tim_data):
    tim_id, tim_version, tim_reserved, tim_flags = struct.unpack('<BBHI', tim_data[:8])
    if tim_id != 0x10:
        raise ValueError("Invalid TIM file ID (expected 0x10)")
    
    has_clut = (tim_flags & 0x08) != 0
    pixel_type = tim_flags & 0x07
    
    pos = 8
    
    clut_data = None
    pixel_data = None
    
    if has_clut:
        clut_size = struct.unpack_from('<I', tim_data, pos)[0]
        clut_section = tim_data[pos:pos+clut_size]
        pos += clut_size
        
        clt_id = 0x11
        clt_version = 0x00
        clt_reserved = 0x0000
        clt_flags = 0x02
        
        clut_data = bytearray()
        clut_data.extend(struct.pack('<BBHI', clt_id, clt_version, clt_reserved, clt_flags))
        clut_data.extend(clut_section)
    
    pixel_section = tim_data[pos:]
    
    pxl_id = 0x12
    pxl_version = 0x00
    pxl_reserved = 0x0000
    pxl_flags = pixel_type
    
    pxl_data = bytearray()
    pxl_data.extend(struct.pack('<BBHI', pxl_id, pxl_version, pxl_reserved, pxl_flags))
    pxl_data.extend(pixel_section)
    
    return bytes(pxl_data), bytes(clut_data) if has_clut else None

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("tim_to_pxl_clt.py by Pio")
        print("Converts a PS1 tim texture to a pxl and clt file")
        print("\nUsage: tim_to_pxl_clt.py input.tim [output_basename]")
        print("If output_basename is not provided, input filename will be used as base")
        return
    
    tim_file = sys.argv[1]
    
    try:
        tim_data = read_file(tim_file)
        
        pxl_data, clut_data = split_tim_to_pxl_clt(tim_data)
        
        if len(sys.argv) == 2:
            base_name = os.path.splitext(tim_file)[0]
        else:
            base_name = sys.argv[2]
        
        pxl_file = f"{base_name}.pxl"
        clt_file = f"{base_name}.clt" if clut_data else None
        
        write_file(pxl_file, pxl_data)
        print(f"Created PXL file: {pxl_file}")
        
        if clut_data and clt_file:
            write_file(clt_file, clut_data)
            print(f"Created CLT file: {clt_file}")
        elif not clut_data:
            print("TIM file contained no CLUT data - only created PXL file")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()