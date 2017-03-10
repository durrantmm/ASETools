from collections import OrderedDict

class CustomConfigMarkDuplicates:

    def __init__(self):
        self.JAVA_PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
        self.JAVA_VERSION = "1.8.0_66"
        self.JAVA_VERSION_FLAG = "-version"

        self.PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java -jar " \
                    "/srv/gs1/software/picard-tools/2.8.0/picard.jar MarkDuplicates"
        self.VERSION = "2.8.0-SNAPSHOT"
        self.VERSION_FLAG = "--help"


        self.ARGS = OrderedDict([

            ("CREATE_INDEX", "true"),
            ("VALIDATION_STRINGENCY", "SILENT"),
            ("M", "output.metrics")

        ])