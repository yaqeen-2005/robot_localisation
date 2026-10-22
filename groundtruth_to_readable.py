
import csv
import re

with open("ground_truth_raw.txt") as f:
    raw = f.read()

messages = re.split(r"(?=header\s*\{)", raw)

with open("ground_truth.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "x", "y"])

    for message in messages:
        stamp = re.search(
            r"stamp\s*\{\s*sec:\s*(\d+)\s*nsec:\s*(\d+)",
            message
        )
        robot = re.search(
            r'pose\s*\{\s*name:\s*"differential_robot"'
            r'[\s\S]*?position\s*\{([^}]*)\}',
            message
        )

        if not stamp or not robot:
            continue

        position = robot.group(1)
        x_match = re.search(r"\bx:\s*([-\d.eE+]+)", position)
        y_match = re.search(r"\by:\s*([-\d.eE+]+)", position)

        x = float(x_match.group(1)) if x_match else 0.0
        y = float(y_match.group(1)) if y_match else 0.0
        time = int(stamp.group(1)) + int(stamp.group(2)) * 1e-9

        writer.writerow([time, x, y])

