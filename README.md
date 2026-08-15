# A/B Test: Checkout Redesign Impact on Conversion

**Business problem:** The product team redesigned the checkout flow and wants to know,
with statistical confidence, whether it should replace the current one — and what that's
worth in revenue if shipped.

## What this project demonstrates
- **Pre-test power analysis** — computing required sample size *before* collecting data,
  based on baseline rate, minimum detectable effect, alpha, and power
- **Two-proportion z-test** — properly testing whether the conversion rate difference is
  statistically significant, not just eyeballing two percentages
- **95% confidence interval on the effect size** — the number that actually matters for
  a business decision, not just the p-value
- **Segment consistency check** — verifying the effect holds across mobile/desktop
  (a lightweight Simpson's Paradox check)
- **Business impact translation** — converting a statistical result into projected
  annual revenue

## Results
| Metric | Value |
|---|---|
| Variant A (control) conversion | 12.20% |
| Variant B (new checkout) conversion | 14.22% |
| Observed lift | +2.02 percentage points |
| p-value | 0.0042 |
| 95% CI on lift | [+0.64%, +3.40%] |
| Decision | Statistically significant — ship Variant B |
| Projected annual revenue impact | ~$2.18M |

## Key interview talking points
- **p-value ≠ "probability B is better."** It's the probability of seeing a gap this
  large (or larger) if there were truly no difference between variants.
- **Why report the CI, not just the p-value**: the CI tells stakeholders the plausible
  *range* of the true effect, which is what they need to make a decision — "significant"
  alone doesn't tell you if the effect is worth acting on.
- **Why segment checks matter**: an aggregate lift could mask a loss in one subgroup
  offset by a bigger gain in another. Checking mobile vs. desktop confirms the effect
  is real and broad-based, not an artifact of one segment.
- **Why compute sample size first**: without it, a "no significant difference" result
  is ambiguous — is there truly no effect, or was the test just underpowered to detect
  a real one?

## Tech stack
- Python: numpy, pandas, scipy.stats (z-test implemented manually — no statsmodels
  dependency, so the underlying formula is fully visible in the code)

## Repo structure
```
power_analysis.py     # sample size calculation before running the test
generate_ab_data.py    # simulates the test running for the required sample size
run_ab_test.py           # z-test, CI, segment check, business impact
ab_test_data.csv           # raw simulated experiment data
```

## Run locally
```bash
pip install numpy pandas scipy
python power_analysis.py
python generate_ab_data.py
python run_ab_test.py
```

## What I'd do with a real experiment
- Use a proper experimentation platform (Optimizely, GrowthBook) for randomization
  and traffic allocation rather than simulated assignment
- Check for novelty effects by running longer and comparing week-over-week lift
- Add a guardrail metric (e.g., checkout error rate) to make sure the new flow
  isn't improving conversion while creating a different downstream problem
