import os, sys
import json


class RunSTAR:

    @staticmethod
    def save(RunSTAR_o):
        out_config_dict = RunSTAR.encodeJSON(RunSTAR_o)

        with open(RunSTAR_o.run_star_config_path, 'w') as outfile:
            outfile.write(json.dumps(out_config_dict, indent=4))

    @staticmethod
    def encodeJSON(RunSTAR_o):
        keep = ["output_dir", "ARGS", "PATH", "readFilesIn", "outFileNamePrefix", "VERSION", "output_sam"]
        outdict = RunSTAR_o.__dict__.copy()
        del outdict['parse_version']
        outdict['readFilesIn'] = RunSTAR_o.readFilesIn._asdict()
        outdict['outFileNamePrefix'] = RunSTAR_o.outFileNamePrefix._asdict()

        outdict = {key: val for key, val in outdict.items() if key in keep}
        return outdict

    @staticmethod
    def decodeJSON():
        pass

