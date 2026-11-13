import os
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

# 1. CONNECT: Jev 1.13, free on OpenCode for a limited time
client = TypeSafeClient(
    api_key=os.environ["OPENCODE_API_KEY"],
    base_url="https://opencode.ai/inference/systemone",
    model="jev-1.13-free",
    compression=False)

# 2. ASK: typed questions, not a prompt
questions = {
    "team": Choice(
        instructions="Which team should handle this ticket",
        criteria={
            "billing": "Payments, refunds, invoices",
            "technical": "Bugs, the app, the pot not working",
            "shipping": "Delivery, late or damaged packages",
        }),
    "angry": Score(
        instructions="How frustrated the customer is",
        criteria=["Calm", "Frustrated but civil", "Very angry"]),
    "urgent": Noul(
        instructions="The ticket needs attention today"),
    "fits": Noul(
        instructions="The ticket is about billing, "
                     "a technical problem, or shipping"),
}

# 3. DECIDE: the model judges, your code acts
def triage(ticket):
    r = client.system_one(state=ticket, questions=questions)
    team = r.choices["team"]
    if r.nouls["fits"].noul < 0.3 or team.confidence < 0.5:
        return "human", r
    return team.choice, r

# 4. RUN it on every ticket
for ticket in open("tickets.txt", encoding="utf-8"):
    where, r = triage(ticket.strip())
    flag = "URGENT" if r.nouls["urgent"].noul > 0.7 else ""
    print(f"{where:10} {flag:7} {ticket.strip()[:40]}")
