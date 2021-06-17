import os
import json

configuration = {}
port = 10001
conf2port = {}
host = "localhost"
rootdir = "models"

for dirname in os.listdir(rootdir):
    try:
        source, target = dirname.split('-')
        sources = source.split('+')
        targets = target.split('+')
        dirname = os.path.join(rootdir, dirname)
        sourcetok = None
        targettok = None
        if os.path.isfile(os.path.join(dirname, "source.spm")):
            sourcetok = ("sourcespm",
                         os.path.join(dirname, "source.spm"))
        elif os.path.isfile(os.path.join(dirname, "source.bpe")):
            sourcetok = ("sourcebpe",
                         os.path.join(dirname, "source.bpe"))
        if os.path.isfile(os.path.join(dirname, "target.spm")):
            targettok = ("targepspm",
                         os.path.join(dirname, "target.spm"))
        elif os.path.isfile(os.path.join(dirname, "target.bpe")):
            targettok = ("targetbpe",
                         os.path.join(dirname, "target.bpe"))
        assert sourcetok and targettok
        assert os.path.isfile(os.path.join(dirname, "decoder.yml"))
        assert len(sources) > 0
        assert len(targets) > 0
        assert all(map(lambda x: len(x) <= 3, sources))
        assert all(map(lambda x: len(x) <= 3, targets))
    except Exception as ex:
        raise ex
        continue
    for source in sources:
        for target in targets:
            vals = dict((sourcetok, targettok))
            vals["host"] = host
            model_conf = os.path.join(dirname, "decoder.yml")
            if model_conf not in conf2port:
                conf2port[model_conf] = str(port)
                port += 1
            vals["port"] = conf2port[model_conf]
            vals["configuration"] = model_conf
            if source not in configuration:
                configuration[source] = {target: vals}
            else:
                configuration[source][target] = vals
print(json.dumps(configuration, sort_keys = True, indent = 4))
