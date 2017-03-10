import os, sys
import json


class RunSTAR:

    @staticmethod
    def save(RunSTAR_o, suffix=".json"):
        out_config_dict = RunSTAR.encodeJSON(RunSTAR_o)

        with open(RunSTAR_o.STAR_ALIGN_READS_CONFIG_PATH, 'w') as outfile:
            outfile.write(json.dumps(out_config_dict, indent=4))

    @staticmethod
    def encodeJSON(RunSTAR_o):
        keep = ["OUTPUT_DIR", "ARGS", "PATH", "readFilesIn", "outFileNamePrefix", "VERSION"]
        outdict = RunSTAR_o.__dict__.copy()
        del outdict['PARSE_VERSION']
        outdict['readFilesIn'] = RunSTAR_o.readFilesIn._asdict()
        outdict['outFileNamePrefix'] = RunSTAR_o.outFileNamePrefix._asdict()

        outdict = {key: val for key, val in outdict.items() if key in keep}
        return outdict

    @staticmethod
    def decodeJSON():
        pass

