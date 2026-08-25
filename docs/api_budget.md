# Claude API budget

The default workflow is designed for an $11 research budget.

| Stage | Spending ceiling | Purpose |
|---|---:|---|
| Pilot | $1 | Code and review up to 10 diverse statutes |
| Main batch | $7 | First-pass coding after the pilot passes |
| Resolution reserve | $3 | Re-code failed or ambiguous passages |

The repository defaults to a hard `$8` ceiling because the pilot and main run should never consume the resolution reserve automatically.

Claude Haiku 4.5 is pinned because its published standard price is $1 per million input tokens and $5 per million output tokens. Anthropic's Batch API discounts both by 50%. Pricing can change, so the runner refuses to use a model without a locally pinned price.

Official references:

- [Anthropic model pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

## Cost controls

- Retrieve relevant passages before sending text.
- Estimate a conservative maximum before the first call.
- Require an explicit per-run ceiling.
- Cache by statute text, prompt version, schema, and model.
- Store actual input and output tokens for each request.
- Use the same pinned response-token ceiling in cost estimates and live requests.
- Use the synchronous API only for the pilot.
- Use batch pricing for the frozen main sample.
- Never spend the reserve automatically.

API spending does not replace human review. The budget buys reproducible first-pass labels, not legal conclusions.
