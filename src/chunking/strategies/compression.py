class CompressionStrategy:

    def compress(self, file):
        path = file.path.lower()

        if "lock" in path:
            return f"{file.path}\n[LOCKFILE TRUNCATED]"

        if ".test." in path:
            return f"{file.path}\n[Test file mirrors implementation changes]"

        return None
