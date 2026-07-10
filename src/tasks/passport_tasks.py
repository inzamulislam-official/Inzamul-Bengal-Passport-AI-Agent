from crewai import Task

from src.agents.policy_guardian import policy_guardian
from src.agents.fee_calculator import fee_calculator
from src.agents.document_architect import document_architect


policy_task = Task(
    description="""
You are given a passport applicant profile.

Your responsibilities:

1. Determine whether the applicant is eligible.

2. Determine the passport validity.

Rules:

- Under 18 → Maximum 5 Years
- Age 18 to 65 → Eligible for 10 Years
- Above 65 → Maximum 5 Years

Determine required identification.

Rules:

- Under 18 → Birth Registration
- Adult → NID

If the applicant requests an invalid passport validity,
flag the inconsistency.

Return a structured response.
""",

    expected_output="""
Eligibility Status

Passport Validity

Required Identification

Policy Warning (if any)
""",

    agent=policy_guardian
)


fee_task = Task(
    description="""
Using the policy result,
calculate passport fee.

Use the official 2026 fee structure.

Include:

Passport Fee

VAT

Total Fee

Return all amounts in BDT.
""",

    expected_output="""
Passport Fee

VAT

Total Payable Amount
""",

    agent=fee_calculator,

    context=[policy_task]
)


document_task = Task(
    description="""
Generate the complete passport document checklist.

Examples:

Adult
Minor
Government Employee
Business Person
Student

Return only the required documents.
""",

    expected_output="""
Customized Passport Checklist
""",

    agent=document_architect,

    context=[policy_task]
)