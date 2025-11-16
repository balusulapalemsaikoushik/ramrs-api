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
    try:
        if (answer := clue.answer) is not None:
            return answer["category"]
        category_frequencies = {}
        for answer in clue.answers:
            if (category := answer["category"]) in category_frequencies:
                category_frequencies[category] += 1
            else:
                category_frequencies[category] = 1
        return max(category_frequencies, key=category_frequencies.get)
    except KeyError as e:
        print(f"WARNING: The {e.args[0]} for the clue \"{clue["clue"]}\" doesn't exist")
        return None

def _select_answers(clue):
    try:
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
    except KeyError:
        print(f'WARNING: The answers for clue "{clue["clue"]}" need attention')
        return None

def _get_ranked_clues():
    clues_ranked = pd.DataFrame(get_clues(db))
    clues_ranked.dropna(subset=["clue"], inplace=True)
    clues_ranked = clues_ranked[~clues_ranked["label"].isin(UNNECESSARY_LABELS)]
    clues_ranked = clues_ranked[clues_ranked["answers"].str.len() > 0]
    clues_ranked.loc[:, "category"] = clues_ranked.apply(_get_category, axis=1)
    clues_ranked.dropna(subset=["category"], inplace=True)
    clues_ranked.loc[:, "answers"] = clues_ranked.apply(_select_answers, axis=1)
    clues_ranked.dropna(subset=["answers"], inplace=True)
    clues_ranked.loc[:, "frequency"] = clues_ranked["answers"].apply(len)
    return clues_ranked.sort_values(by="frequency", ascending=False)

def get_grouped_clues():
    clues = _get_ranked_clues()
    return clues.groupby("category").apply(
        lambda category: category.to_dict(orient="records"), include_groups=False
    ).to_dict()

def get_category_clues(category):
    clues = _get_ranked_clues()
    return clues.loc[clues["category"] == category].to_dict(orient="records")
