import json

def qa(input):
    data = json.loads(input)
    vals = dict()
    crowd = dict()
    answers = dict()
    for r in data["questions"]:
        qid = r["question_id"]
        if qid not in vals:
            vals[qid] = True
        if qid not in answers:
            answers[qid] = 0
        if qid not in crowd:
            crowd[qid] = 0
        answers[qid] += r["answer"]
        crowd[qid] += 1

    questions = []
    for k in vals:
        question = dict()
        question["question_id"] = k
        question["crowd_num"] = crowd[k]
        question["answer"] = answers[k]/float(crowd[k])

        questions.append(question)

    return {"questions": questions}
