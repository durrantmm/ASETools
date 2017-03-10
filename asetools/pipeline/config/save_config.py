import os, sys
import json


class RunSTAR:

    @staticmethod
    def save(RunSTAR_o, suffix=".json"):
        out_config_dict = RunSTAR.encodeJSON(RunSTAR_o)

        with open(os.path.join(RunSTAR_o.OUTPUT_DIR, 'RunSTAR'+suffix), 'w') as outfile:
            outfile.write(json.dumps(out_config_dict, indent=4))

    @staticmethod
    def encodeJSON(RunSTAR_o):
        outdict = RunSTAR_o.__dict__.copy()
        del outdict['PARSE_VERSION']
        outdict['readFilesIn'] = RunSTAR_o.readFilesIn._asdict()
        outdict['outFileNamePrefix'] = RunSTAR_o.outFileNamePrefix._asdict()
        return outdict

    @staticmethod
    def decodeJSON():
        pass

