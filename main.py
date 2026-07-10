from pathlib import Path

from crewai import Crew

from src.agents.policy_guardian import policy_guardian
from src.agents.fee_calculator import fee_calculator
from src.agents.document_architect import document_architect

from src.tasks.passport_tasks import (
    policy_task,
    fee_task,
    document_task
)

from src.database.local_db import (
    get_fee,
    get_documents
)

from src.utils.helpers import (
    calculate_vat,
    calculate_total,
    validate_validity,
    generate_markdown_table
)

from src.tools.scraper import scrape_data


passport_crew = Crew(

    agents=[
        policy_guardian,
        fee_calculator,
        document_architect
    ],

    tasks=[
        policy_task,
        fee_task,
        document_task
    ],

    verbose=True
)


print("\n====== Amar Passport AI Agent ======\n")

age = int(input("Age: "))

profession = input(
    "Profession (private/government/student/business/freelancer/unemployed): "
).lower()

pages = input(
    "Passport Pages (48/64): "
)

delivery = input(
    "Delivery (regular/express/super_express): "
).lower()

requested_validity = input(
    "Requested Validity (5 Years/10 Years): "
)

district = input(
    "District: "
)

nid = input(
    "Do you have NID? (yes/no): "
).lower()


if pages == "48":

    pages = "48_pages"

else:

    pages = "64_pages"


scraper_result = scrape_data()


if scraper_result["status"]:

    print("\nWebsite Connected Successfully.\n")

else:

    print("\nScraping Failed.")
    print("Using Local Database.\n")


user = {

    "age": age,

    "profession": profession,

    "pages": pages,

    "delivery": delivery,

    "requested_validity": requested_validity,

    "district": district,

    "nid": nid

}


valid, allowed = validate_validity(

    age,

    requested_validity

)


if not valid:

    print("\nINVALID REQUEST\n")

    print(

        f"You can only apply for {allowed}"

    )

    raise SystemExit


fee = get_fee(

    pages,

    allowed,

    delivery

)


vat = calculate_vat(fee)

total = calculate_total(fee)

documents = get_documents(

    age,

    profession

)


crew_result = passport_crew.kickoff(

    inputs=user

)


report = {

    "Eligibility": "Eligible",

    "Passport Validity": allowed,

    "Pages": pages,

    "Delivery": delivery,

    "Base Fee": f"{fee} BDT",

    "VAT": f"{vat} BDT",

    "Total Fee": f"{total} BDT",

    "Data Source": scraper_result["source"],

    "Documents": ", ".join(documents)

}


markdown = generate_markdown_table(report)


print("\n")

print("=" * 60)

print("PASSPORT READINESS REPORT")

print("=" * 60)

print()

print(markdown)

print()

print("AI AGENT ANALYSIS")

print()

print(crew_result)

print()

print("বাংলা সারসংক্ষেপ\n")

print(

f"""

আবেদন অবস্থা: Eligible

পাসপোর্টের মেয়াদ: {allowed}

পৃষ্ঠা: {pages}

ডেলিভারি: {delivery}

মোট ফি: {total} টাকা

তথ্যের উৎস: {scraper_result["source"]}

প্রয়োজনীয় কাগজপত্র:

{", ".join(documents)}

"""

)


output_folder = Path("output")

output_folder.mkdir(exist_ok=True)

report_file = output_folder / "report.md"

with open(

    report_file,

    "w",

    encoding="utf-8"

) as file:

    file.write("# Passport Readiness Report\n\n")

    file.write(markdown)

    file.write("\n\n")

    file.write("## AI Agent Analysis\n\n")

    file.write(str(crew_result))

    file.write("\n\n")

    file.write("## Bangla Summary\n\n")

    file.write(

f"""

আবেদন অবস্থা: Eligible

পাসপোর্টের মেয়াদ: {allowed}

পৃষ্ঠা: {pages}

ডেলিভারি: {delivery}

মোট ফি: {total} টাকা

তথ্যের উৎস: {scraper_result["source"]}

প্রয়োজনীয় কাগজপত্র:

{", ".join(documents)}

"""

    )

print("\nReport Saved -> output/report.md")