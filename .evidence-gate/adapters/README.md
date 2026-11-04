# Adapters

Adapter files tell the Gate which URL, button or field to use in this shop app.

- `api.yaml`: the HTTP adapter (quote an order through `POST /api/cart/quote`).
- `browser.yaml`: the browser adapter (add to cart, place an order, read the receipt by `data-testid`).

They started from the examples in the evidence-gate repo (`contract/examples/api.adapter.yaml` and `contract/examples/browser.adapter.yaml`) and were checked against `docs/API.md` and `app/static/`. A copy used by the evaluation lives in evidence-gate under `eval/adapters/`.

`api.yaml` has no `-q` in `tests_command` on purpose: this repo's `pytest.ini` already sets `-q`, and two of them hide the summary line the Gate reads.

Do not edit the shop code to fit the adapter; change the adapter instead.
