# OpsPilot

AI in DevOps, built step by step. OpsPilot connects AI to real delivery work: reviewing infrastructure changes, generating Terraform, triaging incidents and running agents on Kubernetes, with guardrails at every stage.

## Ground rules

1. Validate before accepting. AI output passes automated checks before anything uses it.
2. Humans approve risky actions. Reading is automatic, changing infrastructure waits for a person.
3. Log everything. Every prompt, response and approval is recorded.

## Status

This is complete: a Terraform plan reviewer that sends a plan to Gemini and returns a structured JSON risk report, with a daily call limit to stay inside the free tier.

## Sample project

The infrastructure being reviewed comes from my tooling project, an AKS deployment with Terraform, Helm, GitHub Actions and Prometheus: github.com/kristarking/tooling-project

## Run it

1. Create a Gemini API key in Google AI Studio.
2. Create a virtual environment and install google-genai.
3. Set GEMINI_API_KEY in your terminal.
4. Run: python review.py plan.txt

## Roadmap

Phase 1 AI in CI, Phase 2 AI in infrastructure as code, Phase 3 AI in operations, Phase 4 agents and MCP, Phase 5 security and cost, Phase 6 evaluation.
