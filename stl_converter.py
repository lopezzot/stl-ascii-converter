import struct
import argparse
import sys
import os

def convert_stl_binary_to_ascii(input_file, output_file):
    # Open input in binary read mode ('rb') and output in text write mode ('w')
    with open(input_file, 'rb') as infile, open(output_file, 'w') as outfile:
        
        # Read the 80-byte header
        header = infile.read(80)
        
        # Extract printable characters for the solid name (ignore null bytes)
        solid_name = "".join([chr(b) for b in header if 32 <= b < 127]).strip()
        if not solid_name:
            solid_name = "converted_mesh"
            
        outfile.write(f"solid {solid_name}\n")
        
        # Read the number of faces (4 bytes, unsigned int, little-endian)
        faces_bytes = infile.read(4)
        if not faces_bytes:
            print("Error: Empty file.")
            sys.exit(1)
            
        faces = struct.unpack('<I', faces_bytes)[0]
        
        print(f"Converting {faces} faces from '{input_file}' to '{output_file}'...")

        # Loop through each face
        for _ in range(faces):
            # Read 50 bytes per face: 
            # 12 (normal) + 36 (3 vertices * 12) + 2 (attribute byte count)
            face_data = infile.read(50)
            
            if len(face_data) < 50:
                print("Warning: Reached EOF unexpectedly. File might be corrupted.")
                break

            # Unpack 3 floats for the normal vector (<3f means little-endian, 3 floats)
            nx, ny, nz = struct.unpack('<3f', face_data[0:12])
            outfile.write(f"  facet normal {nx:e} {ny:e} {nz:e}\n")
            outfile.write("    outer loop\n")

            # Unpack 3 floats for Vertex 1
            v1x, v1y, v1z = struct.unpack('<3f', face_data[12:24])
            outfile.write(f"      vertex {v1x:e} {v1y:e} {v1z:e}\n")
            
            # Unpack 3 floats for Vertex 2
            v2x, v2y, v2z = struct.unpack('<3f', face_data[24:36])
            outfile.write(f"      vertex {v2x:e} {v2y:e} {v2z:e}\n")
            
            # Unpack 3 floats for Vertex 3
            v3x, v3y, v3z = struct.unpack('<3f', face_data[36:48])
            outfile.write(f"      vertex {v3x:e} {v3y:e} {v3z:e}\n")

            outfile.write("    endloop\n")
            outfile.write("  endfacet\n")

        outfile.write(f"endsolid {solid_name}\n")
        
    print("Conversion completed successfully!")

if __name__ == "__main__":
    # Set up argument parsing for command line execution
    parser = argparse.ArgumentParser(description="Convert a binary STL file to an ASCII STL file.")
    parser.add_argument("input_file", help="Path to the source binary STL file")
    parser.add_argument("output_file", help="Path to the destination ASCII STL file")
    
    args = parser.parse_args()
    
    # Check if the input file actually exists before proceeding
    if not os.path.exists(args.input_file):
        print(f"Error: The file '{args.input_file}' does not exist.")
        sys.exit(1)
        
    convert_stl_binary_to_ascii(args.input_file, args.output_file)
