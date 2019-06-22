COLOURS = {
    # text colour, bg-color
    "arsenal": ["#FFFFFF", "#EF0107"],
    "bournemouth": ["#b50e12", "#000000"],
    "brightonhovealbion": ["#FFFFFF", "#0057B8"],
    "burnley": ["#EDE939", "#6C1D45"],
    "chelsea": ["#FFFFFF", "#034694"],
    "crystalpalace": ["#123064", "#CF4157"],
    "everton": ["#003399", "#FFFFFF"],
    "leicester": ["#fdbe11", "#003090"],
"liverpool": ["#F6EB61", "#c8102E"],
"manchestercity": ["#1C2C5B", "#6CABDD"],
"newcastle": ["#FFFFFF", "#241F20"],
"southampton": ["#FFFFFF", "#d71920"],
"tottenham": ["#FFFFFF", "#132257"],
"westham": ["#1bb1e7", "#7A263A"],
"sheffieldutd": ["#ec2227", "#FFFFFF"],
"astonvilla": ["#850322", "#88bbff"],
"norwich": ["#ffee00", "#007020"],
    "manchesterutd": ["#FBE122", "#DA291C"],
    "watford": ["#ED2127", "#FBEE23"],
    "wolves": ["#231F20", "#FDB913"]
}


def main():
    lines = []
    for k, (color, bg_color) in COLOURS.items():
        lines.append(".%s{color: %s;background-color: %s;}"%(k, color, bg_color))

    for k1, (color1, bg_color1) in COLOURS.items():
        for k2, (color2, bg_color2) in COLOURS.items():
            lines.append(".{0}{1}{{background: linear-gradient(135deg,{2} 0%,{2} 50%,{3} 50%,{3} 100%);}}".format(
                k1, k2, bg_color1, bg_color2
            ))
    out = "\n".join(lines)
    with open("../static/footballteams.css", "w+") as f:
        f.write(out)


if __name__ == "__main__":
    main()
