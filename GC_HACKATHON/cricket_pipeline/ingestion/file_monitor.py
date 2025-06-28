import pathway as pw

class FileMonitor:
    def __init__(self, directory: str):
        self.directory = directory

    def get_data_stream(self) -> pw.Table:
        return pw.io.fs.read(
            self.directory,
            format="binary",
            mode="streaming",
            with_metadata=True,
        )