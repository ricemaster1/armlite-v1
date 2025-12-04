### Special thanks to Peter Higginson for this amazing Programming Manual. Please refer to https://peterhigginson.co.uk/ARMlite/Programming%20reference%20manual_v1_3.pdf for details.
### Image to ARMLite Assembly Sprite Converter v1.0

from PIL import Image
import webcolors
import sys
import os
import math
import argparse

# Define ARMLite-supported HTML color names 
ARMLITE_COLORS = [
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'
]

ARMLITE_RGB = {name: webcolors.name_to_rgb(name) for name in ARMLITE_COLORS}

def closest_color(rgb):
    min_dist = float('inf') 
    closest = None
    for name, color_rgb in ARMLITE_RGB.items():
        dist = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, color_rgb)) # Euclidean distance squared
        if dist < min_dist:
            min_dist = dist
            closest = name
    return closest

def process_image(image_path, output_path):
    # parser = argparse.ArgumentParser(description='Convert an image to ARMLite assembly sprite.')
    # parser.add_argument('image', help='Path to input image')
    # parser.add_argument('-o', '--output', default='converted.s', help='Output assembly file path')
    # args = parser.parse_args()
    #### unused args ignore please 

    img = Image.open(image_path).convert('RGB')
    img = img.resize((128, 96))  # Resize to ARMLite high-res display
    pixels = list(img.getdata())

    # Begin generating the assembly code
    lines = []
    lines.append('; === Fullscreen Sprite ===')
    lines.append('    MOV R0, #2') # Set resolution to high-res. 
    lines.append('    STR R0, .Resolution')
    lines.append('    MOV R1, #.PixelScreen')
    lines.append('    MOV R6, #512 ; row stride (128 * 4)')

    for y in range(96):
        for x in range(128):
            offset = ((y * 128) + x) * 4
            addr_line = f'    MOV R5, #{offset}\n    ADD R4, R1, R5'
            rgb = pixels[y * 128 + x]
            color = closest_color(rgb)
            write_line = f'    MOV R0, #.{color}\n    STR R0, [R4]   ; Pixel ({x},{y})'
            lines.append(addr_line)
            lines.append(write_line) # keep in mind it will generate ~50K LoC

    lines.append('    HALT') # End of program. If you'd like to integrate it in a subroutine, replace with a 'RET' instruction and ensure the subroutine has a BL to return to.
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Assembly sprite file written to {output_path}")

if __name__ == '__main__':
     parser = argparse.ArgumentParser(description='Convert an image to ARMLite assembly sprite.')
     parser.add_argument('image', help='Path to input image')
     parser.add_argument('-o', '--output', default='converted.s', help='Output assembly file path')
     args = parser.parse_args()

     if not os.path.isfile(args.image):
        print("Image not found.")
        sys.exit(1)

     process_image(args.image, args.output)
