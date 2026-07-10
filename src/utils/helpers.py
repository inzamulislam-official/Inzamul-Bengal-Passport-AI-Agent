from tabulate import tabulate


def calculate_vat(base_fee):
    return round(base_fee * 0.15)


def calculate_total(base_fee):
    return base_fee + calculate_vat(base_fee)


def validate_validity(age, requested_validity):
    requested_validity = requested_validity.lower().strip()

    if age < 18:
        allowed = "5_years"

    elif age > 65:
        allowed = "5_years"

    else:
        allowed = "10_years"

    request = requested_validity.replace(" ", "_")

    if request != allowed:

        return False, allowed

    return True, allowed


def generate_markdown_table(data):

    rows = []

    for key, value in data.items():
        rows.append([key, value])

    return tabulate(
        rows,
        headers=["Field", "Value"],
        tablefmt="github"
    )