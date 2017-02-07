import json
from analysis import DumpDirectory

dump = DumpDirectory("dump")

def safeSplit(string, delim):
    return filter(lambda x: x != "", string.split(delim))

def parseState(state):
    if state == "": return []
    annotations = safeSplit(state, ";")
    annotations = map(lambda a: [ a.split("|")[0], safeSplit(a.split("|")[1], ",") ], annotations)
    return annotations

for session in dump.sessions():
    print session["clientID"], session["sessionID"], session["timeCreated"], session["appVersion"]
    for timestamp, action, label in session["actions"]:
        if action.startswith("annotation") or action.startswith("export"):
            label = json.dumps(parseState(label))
        # print "  ", timestamp, action, label

for export in dump.exports():
    print export.keys()
    print export["sessionID"], export["timeCreated"]
