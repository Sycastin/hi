from __future__ import annotations

from flask import Flask, jsonify, render_template, request
from matplotlib.path import Path
from matplotlib.textpath import TextPath

app = Flask(__name__)


def _path_to_equations(path: Path, scale: float = 0.05) -> list[dict[str, list[float] | str]]:
    vertices = path.vertices
    codes = path.codes
    if codes is None:
        return []

    equations: list[dict[str, list[float] | str]] = []
    current = None
    idx = 0

    while idx < len(codes):
        code = codes[idx]
        if code == Path.MOVETO:
            current = vertices[idx]
            idx += 1
        elif code == Path.LINETO and current is not None:
            start = current
            end = vertices[idx]
            equations.append(
                {
                    "type": "line",
                    "points": [
                        float(start[0]),
                        float(start[1]),
                        float(end[0]),
                        float(end[1]),
                    ],
                }
            )
            current = end
            idx += 1
        elif code == Path.CURVE3 and current is not None:
            control = vertices[idx]
            end = vertices[idx + 1]
            equations.append(
                {
                    "type": "quadratic",
                    "points": [
                        float(current[0]),
                        float(current[1]),
                        float(control[0]),
                        float(control[1]),
                        float(end[0]),
                        float(end[1]),
                    ],
                }
            )
            current = end
            idx += 2
        elif code == Path.CURVE4 and current is not None:
            control1 = vertices[idx]
            control2 = vertices[idx + 1]
            end = vertices[idx + 2]
            equations.append(
                {
                    "type": "cubic",
                    "points": [
                        float(current[0]),
                        float(current[1]),
                        float(control1[0]),
                        float(control1[1]),
                        float(control2[0]),
                        float(control2[1]),
                        float(end[0]),
                        float(end[1]),
                    ],
                }
            )
            current = end
            idx += 3
        else:
            idx += 1

    for eq in equations:
        eq["points"] = [p * scale for p in eq["points"]]

    return equations


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/api/equations")
def equations() -> tuple[str, int] | tuple[dict[str, list[dict[str, list[float] | str]]], int]:
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    if not name:
        return jsonify({"error": "Name is required."}), 400

    text_path = TextPath((0, 0), name, size=160)
    eqs = _path_to_equations(text_path)

    return jsonify({"equations": eqs}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
