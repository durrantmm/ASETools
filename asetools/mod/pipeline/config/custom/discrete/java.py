import sys
from collections import OrderedDict


class CustomConfigJava():

    def __init__(self):
        self.path = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
        self.JAVA_VERSION = "1.8.0_66"
        self.JAVA_VERSION_FLAG = "-version"

        self.PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java -jar " \
                    "/srv/gs1/software/picard-tools/2.8.0/picard.jar AddOrReplaceReadGroups"
        self.VERSION = "2.8.0-SNAPSHOT"
        self.VERSION_FLAG = "--help"

        self.ARGS = OrderedDict([

            ("SO", "coordinate"),
            ("RGID", "id"),
            ("RGLB", "library"),
            ("RGPL", "platform"),
            ("RGPU", "machine"),
            ("RGSM", "sample")

        ])
