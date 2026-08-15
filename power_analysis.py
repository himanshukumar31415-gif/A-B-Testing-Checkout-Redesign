"""
Sample size / power analysis -- done BEFORE collecting data.
WHY THIS MATTERS: this is the #1 thing fresher DS candidates skip. Running
a test then eyeballing the p-value without pre-computing sample size means
you don't know if a "no significant difference" result is a real null effect
or just an underpowered test that couldn't have detected the effect anyway.

Manual implementation (no statsmodels/no internet to install it) using the
standard two-proportion z-test sample size formula -- this is worth
understanding by hand, since interviewers sometimes ask you to derive it.
"""
import numpy as np
from scipy import stats

def sample_size_two_proportions(p1, mde, alpha=0.05, power=0.80):
    """
    p1: baseline conversion rate
    mde: minimum detectable effect (absolute, e.g. 0.02 = 2 percentage points)
    alpha: significance level (Type I error tolerance -- false positive rate)
    power: 1 - beta (Type II error tolerance -- probability of detecting a real effect)
    """
    p2 = p1 + mde
    p_bar = (p1 + p2) / 2

    z_alpha = stats.norm.ppf(1 - alpha / 2)   # two-tailed critical value
    z_beta = stats.norm.ppf(power)             # power critical value

    numerator = (z_alpha * np.sqrt(2 * p_bar * (1 - p_bar)) +
                 z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = mde ** 2
    n_per_group = numerator / denominator
    return int(np.ceil(n_per_group))

# Business context: current checkout conversion rate is 12%.
# The product team wants to detect at least a 2 percentage point lift
# (12% -> 14%) with standard alpha=0.05 and power=0.80
baseline = 0.12
mde = 0.02

n = sample_size_two_proportions(baseline, mde)
print(f"Baseline conversion rate: {baseline:.0%}")
print(f"Minimum detectable effect: {mde:.0%} (absolute)")
print(f"Required sample size per group: {n:,}")
print(f"Total sample size needed: {n*2:,}")
print(f"\nInterpretation for stakeholders:")
print(f"  'We need at least {n:,} visitors in EACH variant before we can")
print(f"   reliably detect a 2-point conversion lift. Running the test on")
print(f"   fewer visitors risks a false negative -- concluding \"no effect\"")
print(f"   when a real effect existed but the sample was too small to see it.'")
