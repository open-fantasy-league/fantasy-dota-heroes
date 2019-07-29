COLOURS = {
    # text colour, bg-color
    "alliance": ["#cdcbd0", "#08783e"],
    "evilgeniuses": ["#FFFFFF", "#202d5a"],
    "forwardgaming": ["#00a6cf", "#d60b66"],
    "newbee": ["#29a6de", "#271818"],
    "chaos": ["#f8a770", "#000000"],
    "fnatic": ["#f19e33", "#000000"],
    "infamous": ["#FFFFFF", "#a8120e"],
    "keengaming": ["#a3a2a2", "#7b4e94"],
    "mineski": ["#f0f3fa", "#3a3a3c"],
"navi": ["#000000", "#fff200"],
"ninjasinpyjamas": ["#000000", "#a88b65"],
"og": ["#FFFFFF", "#022554"],
"psglgd": ["#cb2026", "#2a8ec1"],
"rng": ["#b4926a", "#FFFFFF"],
"teamliquid": ["#0e2240", "#FFFFFF"],
"teamsecret": ["#FFFFFF", "#000000"],
"tncpredator": ["#000000", "#f26925"],
"vicigaming": ["#000000", "#c5c6c6"],
    "virtuspro": ["#fc5000", "#111821"],
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
    with open("../static/dotateams.css", "w+") as f:
        f.write(out)


if __name__ == "__main__":
    main()
