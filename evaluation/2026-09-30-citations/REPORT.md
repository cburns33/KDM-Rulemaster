# Citation fix verification

Date: 30 September 2026.

Removed original-PDF page metadata from Sol's source payload and added an API-level instruction to leave citation rendering to the application. The app retains its mapped clickable citations; existing saved answers are unchanged.

Two new automated tests failed before the fix and pass afterward. All 64 automated tests pass. Existing integration checks cover mapped citations and saved responses.

One live T01 retest returned the correct attacker-knockdown ruling with no page references. Usage: 1,637 input plus 54 output tokens, totaling 1,691. The raw answer and usage are in result.json. The one-call run.py harness refuses to overwrite that result.

This is a prompt-and-payload mitigation, verified by one live sample. It does not guarantee compliance for every possible model answer. No output-stripping filter or historical-answer rewrite was added.

The higher-priority instruction uses the Responses API behavior documented in [OpenAI's text-generation guide](https://developers.openai.com/api/docs/guides/text). Model, reasoning effort, and output cap are unchanged.
