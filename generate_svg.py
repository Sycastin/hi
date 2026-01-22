from __future__ import annotations

from html import escape


def build_svg(name: str, font_size: int = 96, padding: int = 20) -> str:
    safe_name = escape(name)
    width = max(300, len(name) * font_size * 0.6) + padding * 2
    height = font_size + padding * 2
    baseline = padding + font_size * 0.8

    return "\n".join(
        [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{int(width)}\" height=\"{int(height)}\">",
            f"  <rect width=\"100%\" height=\"100%\" fill=\"white\" />",
            (
                "  <text"
                f" x=\"{padding}\" y=\"{int(baseline)}\""
                f" font-size=\"{font_size}\""
                " font-family=\"Arial, sans-serif\""
                " fill=\"black\""
                ">"
                f"{safe_name}"
                "</text>"
            ),
            "</svg>",
            "",
        ]
    )


def main() -> None:
    name = input("Enter a name to render as SVG: ").strip()
    if not name:
        print("Please provide a non-empty name.")
        return

    svg = build_svg(name)
    output_path = "name.svg"
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(svg)

    print(f"Saved SVG to {output_path}")


if __name__ == "__main__":
    main()
