#!/bin/python3
import sys
import os
import tomllib

def help():
    print(f"Usage: {sys.argv[0]} (path/to/colorscheme.toml) (template_name) (colors format) (optional: path/to/output)")
    exit()

def hex_to_rgb(hex: str) -> str:
    hex = hex.lstrip("#")
    r, g, b = int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)
    return f"{r},{g},{b}"

def fill_template(template_file, colors, desc, output_file):
    with open(template_file, "r") as f:
        template = f.read()

    print(desc)
    all_vars = {**colors, **desc}
    output = template.format_map(all_vars)

    with open(output_file, "w") as f:
        f.write(output)
    

def get_colorscheme(colorscheme_name):
    colorscheme_file = colorscheme_name
    if not os.path.isfile(colorscheme_file):
        print("colorscheme {colorscheme} not found")
        help()

    with open(colorscheme_file, "rb") as f:
        tot = tomllib.load(f)
        colorscheme = {}
        try:
            colorscheme = tot["colors"]
            found = True
        except KeyError as e:
            print(e)
            help()

    colorscheme["accent"] = colorscheme[colorscheme["primary"]]

    desc = {
        "scheme_name": colorscheme_name,
        "scheme_id": colorscheme_name,
    }

    colors = {
        "rgb": {
            "background":         hex_to_rgb(colorscheme["background"]),
            "background_alt":     hex_to_rgb(colorscheme["background_alt"]),
            "background-alt":     hex_to_rgb(colorscheme["background_alt"]),
            "foreground":         hex_to_rgb(colorscheme["foreground"]),
            "foreground_inactive":hex_to_rgb(colorscheme["foreground"]),
            "black":              hex_to_rgb(colorscheme["black"]),
            "red":                hex_to_rgb(colorscheme["red"]),
            "green":              hex_to_rgb(colorscheme["green"]),
            "yellow":             hex_to_rgb(colorscheme["yellow"]),
            "blue":               hex_to_rgb(colorscheme["blue"]),
            "purple":             hex_to_rgb(colorscheme["magenta"]),
            "magenta":            hex_to_rgb(colorscheme["magenta"]),
            "pink":               hex_to_rgb(colorscheme["magenta"]),
            "white":              hex_to_rgb(colorscheme["white"]),
            "cyan":               hex_to_rgb(colorscheme["cyan"]),
            "accent":             hex_to_rgb(colorscheme["accent"]),
            "hover":              hex_to_rgb(colorscheme["background_alt"]),
            "primary":            colorscheme["primary"],
            "secondary":          colorscheme["secondary"],
        },
        "hex": {
            "background":         colorscheme["background"],
            "background_alt":     colorscheme["background_alt"],
            "background-alt":     colorscheme["background_alt"],
            "foreground":         colorscheme["foreground"],
            "foreground_inactive":colorscheme["foreground"],
            "black":              colorscheme["black"],
            "red":                colorscheme["red"],
            "green":              colorscheme["green"],
            "yellow":             colorscheme["yellow"],
            "blue":               colorscheme["blue"],
            "purple":             colorscheme["magenta"],
            "magenta":            colorscheme["magenta"],
            "pink":            colorscheme["magenta"],
            "white":              colorscheme["white"],
            "cyan":               colorscheme["cyan"],
            "accent":             colorscheme["accent"],
            "hover":              colorscheme["background_alt"],
            "primary":            colorscheme["primary"],
            "secondary":          colorscheme["secondary"],
        }
    }
    return colors, desc

def get_template(template_name):
    templates_dir = "templates"
    for file in os.listdir(templates_dir):
        if file.startswith(template_name) and file.endswith(".template"):
            return os.path.join(templates_dir, file)
    print(f"Template '{template_name}' not found.")
    help()

def get_output_file(template_file):
    output_dir = "output"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    output_file = f"{output_dir}/{os.path.basename(template_file).replace('.template', '')}"
    
    if len(sys.argv) == 5:
        output_file = sys.argv[4]

    return output_file
     
def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        help()

    colorscheme_name = sys.argv[1]
    template_name = sys.argv[2]
    color_fmt = "hex"

    if sys.argv[3] == "rgb" or sys.argv[3] == "hex":
        color_fmt = sys.argv[3]
    else:
        help()

    colorscheme, desc = get_colorscheme(colorscheme_name)
    template_file = get_template(template_name)
    output_file = get_output_file(template_file)

    fill_template(template_file, colorscheme[color_fmt], desc, output_file)

if __name__ == '__main__':
    main()
