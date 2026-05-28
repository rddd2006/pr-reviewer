class ContextManager:

    def __init__(self):
        self.summary = ""

    def update(self, chunk_result):
        if chunk_result:
            self.summary += "\n" + chunk_result

    def get_context(self):
        return self.summary[-2000:]
