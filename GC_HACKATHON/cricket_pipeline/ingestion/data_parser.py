from pathway.xpacks.llm import parsers

class DataParser:
    def __init__(self):
        self.text_parser = parsers.TextParser()
        self.image_parser = parsers.SlideParser(
            llm="gemini-pro-vision",
            parse_prompt="Extract cricket stats from images."
        )

    def parse_row(self, row):
        if row.data_type == "image":
            return self.image_parser.parse(row.content)
        elif row.data_type == "text":
            return self.text_parser.parse(row.content)
        else:
            raise ValueError("Unsupported data type")
