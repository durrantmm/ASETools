from pipeline.config.discrete.java import CustomConfigJava


class FixedConfigJava(CustomConfigJava):

    def __init__(self):
        super().__init__()
        self.name = "Java"

        self.input = None

        self.output = None