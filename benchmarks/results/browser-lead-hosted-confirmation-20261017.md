# Hosted browser allowance confirmation — 2026-10-17

[The c5e00fa workflow](https://github.com/skulitom/Nestbolt/actions/runs/39076499315)
passes **all six jobs**, including both platform checks, both maker rebuilds,
benchmark smoke and the browser job. The saved browser log reports **86 passes
and four opt-in skips** after the lead test adopted the normal five-second
functional allowance. All test assertions and production source remain unchanged.

The earlier bf9e880 workflow ended cancelled after a later push while Windows
checks were still running. Its browser failure, complete diagnostics and terminal
state remain preserved; it is not an all-six success. This supplement leaves
the [original failure archive](browser-lead-budget-20261017.md) intact. It does
not establish the cause of the older c36baa8 Firefox failure.

The archive retains original and new workflow metadata, the successful browser
log, capture/review records and this sealing procedure. CRC and every member
hash/size verify. Published preview assets and gate limits are unchanged.
H2/H5 remain open; milestone completion stays 60%.
