import os, sys
import json


def read_json_to_dict(path):
    return json.load(open(path))


class RunSTAR:

    @staticmethod
    def save(RunSTAR_o):
        out_config_dict = RunSTAR.encodeJSON(RunSTAR_o)

        with open(RunSTAR_o.run_star_json_path, 'w') as outfile:
            outfile.write(json.dumps(out_config_dict, indent=4))

    @staticmethod
    def encodeJSON(RunSTAR_o):
        keep = ["output_dir", "ARGS", "PATH", "readFilesIn", "outFileNamePrefix", "VERSION", "output_sam"]
        outdict = RunSTAR_o.__dict__.copy()
        outdict['readFilesIn'] = RunSTAR_o.readFilesIn._asdict()
        outdict['outFileNamePrefix'] = RunSTAR_o.outFileNamePrefix._asdict()

        outdict = {key: val for key, val in outdict.items() if key in keep}
        return outdict

    @staticmethod
    def decodeJSON():
        pass

class RunAddReadGroups:
    @staticmethod
    def save(RunAddReadGroups_o):
        out_config_dict = RunAddReadGroups.encodeJSON(RunAddReadGroups_o)

        with open(RunAddReadGroups_o.run_star_json_path, 'w') as outfile:
            outfile.write(json.dumps(out_config_dict, indent=4))

    @staticmethod
    def encodeJSON(RunAddReadGroups_o):
        keep = ["output_dir", "ARGS", "PATH", "input_file", "JAVA_PATH", "JAVA_VERSION", "VERSION", "output_file"]
        outdict = RunAddReadGroups_o.__dict__.copy()
        outdict['input_file'] = RunAddReadGroups_o.input_file._asdict()
        outdict['output_file'] = RunAddReadGroups_o.output_file._asdict()

        outdict = {key: val for key, val in outdict.items() if key in keep}
        return outdict

    @staticmethod
    def decodeJSON():
        pass
