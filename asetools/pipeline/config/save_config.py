import os, sys
import json



class RunSTAR:

    def save_state(self, RunSTAR_o, suffix=".json"):
        out_config_dict = self.encodeJSON(RunSTAR_o)

        with open(os.path.join(RunSTAR_o.OUTPUT_DIR, RunSTAR_o.__name__+suffix), 'w') as outfile:
            outfile.write(json.dumps(out_config_dict, indent=4))

    def encodeJSON(self, RunSTAR_o):
        outdict = RunSTAR_o.__dict__.copy()
        del outdict[RunSTAR_o.PARSE_VERSION.__name__]
        outdict[RunSTAR_o.readFilesIn.__name__] = RunSTAR_o.readFilesIn._asdict()
        outdict[RunSTAR_o.outFileNamePrefix.__name__] = RunSTAR_o.outFileNamePrefix._asdict()
        return outdict

    def decodeJSON(self):
        pass

