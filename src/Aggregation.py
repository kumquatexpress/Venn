import json

def aggregate(input):
    data = json.loads(input)
    vals = dict()
    for r in data["relationships"]:
        pos_votes = votes.count(1)/float(len(r["votes"])) #percent
        
        ua1, ua2 = r["user1_answers"], r["user2_answers"]
        diff = [abs(ua1[i]-ua2[i]) for i in range(ua1) if ua1[i] > 0 and ua2[i] > 0]
        vals[r["id"]] = pos_votes * sum(diff)/float(len(diff)) #[0,1]
    return vals
