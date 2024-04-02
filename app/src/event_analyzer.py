class EventAnalyzer():
    def get_joiners_multiple_meetings_method(self, events):
        d = {}
        res = []

        for e in events:
            for j in e.joiners:
                if d.get(j.name) is None:
                    d[j.name] = 1
                else:
                    d.update(j.name, d[j.name]+1)
                if d[j.name] == 2:
                    res.append(j)

        return res
