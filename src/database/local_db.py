import json


DATABASE = "data/passport_data.json"


def load_database():

    with open(DATABASE, "r", encoding="utf-8") as f:

        return json.load(f)


def get_fee(page, validity, delivery):

    db = load_database()

    return db["fees_2026"][page][validity][delivery]


def get_documents(age, profession):

    db = load_database()

    docs = []

    if age < 18:

        docs.extend(
            db["required_docs"]["minor_under_18"]
        )

    else:

        docs.extend(
            db["required_docs"]["adult"]
        )

    if profession.lower() == "government":

        docs.extend(
            db["required_docs"]["government_staff"]
        )

    return list(set(docs))