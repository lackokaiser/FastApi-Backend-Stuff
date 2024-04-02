import json
import models


class EventFileManager():
    FILE_PATH = "event.json"

    def decode(self, dict):
        event = models.Event.model_validate(dict)
        return event

    def read_events_from_file(self):
        f = open(self.FILE_PATH, "r")
        dict = json.load(f)
        list = []
        for d in dict:
            list.append(self.decode(d))
        return list

    def write_events_to_file(self, events):
        resDict = []
        for e in events:
            resDict.append(e.model_dump())
        listStr = json.dumps(resDict, sort_keys=True, indent=4)

        f = open(self.FILE_PATH, "w")
        f.write(listStr)

event = EventFileManager()

event.write_events_to_file(event.read_events_from_file())
