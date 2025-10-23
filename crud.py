import pandas as pd

from database import db, get_clues

UNNECESSARY_LABELS = [
    "CARDINAL",
    "ORDINAL",
    "TIME",
    "DATE",
    "LANGUAGE",
    "PERCENT",
    "MONEY",
    "NORP",
]

def _get_category(clue):
    if (answer := clue.answer) is not None:
        return answer["category"]
    category_frequencies = {}
    for answer in clue.answers:
        if (category := answer["category"]) in category_frequencies:
            category_frequencies[category] += 1
        else:
            category_frequencies[category] = 1
    return max(category_frequencies, key=category_frequencies.get)

def _select_answers(clue):
    selected_answers = []
    answer_frequencies = {}
    for answer in clue["answers"]:
        if answer["category"] == clue["category"]:
            if (answer_text := answer["answer"]) in answer_frequencies:
                answer_frequencies[answer_text] += 1
            else:
                answer_frequencies[answer_text] = 1
            selected_answers.append(answer)
    return sorted(selected_answers, key=lambda answer: answer_frequencies[answer["answer"]], reverse=True)

def _get_ranked_clues():
    clues_ranked = pd.DataFrame(get_clues(db))
    clues_ranked = clues_ranked[~clues_ranked["label"].isin(UNNECESSARY_LABELS)]
    clues_ranked = clues_ranked[clues_ranked["answers"].str.len() > 0]
    clues_ranked.loc[:, "category"] = clues_ranked.apply(_get_category, axis=1)
    clues_ranked.loc[:, "answers"] = clues_ranked.apply(_select_answers, axis=1)
    clues_ranked.loc[:, "frequency"] = clues_ranked["answers"].apply(len)
    return clues_ranked.sort_values(by="frequency", ascending=False)

def get_category(category):
    clues = _get_ranked_clues()
    return clues.loc[clues["category"] == category].to_dict(orient="records")
