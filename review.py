import json
import sys
from ai_client import ask_json

SYSTEM = """You are a senior DevOps engineer reviewing a Terraform plan.
Return only JSON with these keys:
summary: one short paragraph,
risk_level: one of low, medium, high,
findings: a list of objects with resource, issue and recommendation.
Flag security weaknesses, cost risks, reliability risks and anything
that would be unsafe in production. Say clearly when something is
acceptable for a learning or test setup."""

plan_text = open(sys.argv[1]).read()
result = ask_json(SYSTEM, plan_text)
print(json.dumps(result, indent=2))
