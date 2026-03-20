from src.models.diff_models import DiffFile, Hunk

def parse_diff(diff_text: str):
    files = []
    current_file = None
    current_hunk = None

    for line in diff_text.split("\n"):

        if line.startswith("diff --git"):
            if current_file:
                files.append(current_file)

            path = line.split(" ")[-1]
            current_file = DiffFile(path=path, hunks=[])

        elif line.startswith("@@"):
            current_hunk = Hunk(header=line, lines=[])
            current_file.hunks.append(current_hunk)

        elif current_hunk:
            current_hunk.lines.append(line)

    if current_file:
        files.append(current_file)

    return files
