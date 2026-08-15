"""
Two-proportion z-test with confidence interval -- the standard method for
comparing conversion rates between two groups.
"""
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('ab_test_data.csv')

a = df[df['variant'] == 'A']['converted']
b = df[df['variant'] == 'B']['converted']

n_a, n_b = len(a), len(b)
conv_a, conv_b = a.sum(), b.sum()
p_a, p_b = conv_a / n_a, conv_b / n_b

# ---- Two-proportion z-test ----
# H0 (null hypothesis): p_a = p_b, i.e. the new checkout has NO effect on conversion
# H1 (alternative): p_a != p_b, i.e. there IS a difference
p_pool = (conv_a + conv_b) / (n_a + n_b)
se_pool = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
z_stat = (p_b - p_a) / se_pool
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))  # two-tailed

# ---- 95% Confidence interval on the DIFFERENCE (not pooled -- use unpooled SE for CI) ----
se_diff = np.sqrt(p_a*(1-p_a)/n_a + p_b*(1-p_b)/n_b)
diff = p_b - p_a
ci_low = diff - 1.96 * se_diff
ci_high = diff + 1.96 * se_diff

print("="*65)
print("A/B TEST RESULT: Checkout Redesign (Variant B) vs Control (A)")
print("="*65)
print(f"Variant A (control): {conv_a:,} / {n_a:,} = {p_a:.2%} conversion")
print(f"Variant B (new):     {conv_b:,} / {n_b:,} = {p_b:.2%} conversion")
print(f"\nObserved lift: {diff:+.2%} (absolute)")
print(f"95% Confidence interval on lift: [{ci_low:+.2%}, {ci_high:+.2%}]")
print(f"\nz-statistic: {z_stat:.3f}")
print(f"p-value: {p_value:.4f}")
print(f"\nDecision at alpha=0.05: {'REJECT null hypothesis -- statistically significant' if p_value < 0.05 else 'FAIL to reject null -- not statistically significant'}")

print(f"\n{'='*65}\nWhat this means in plain English (this is the part interviewers")
print(f"actually care about -- can you translate stats into a decision):")
print(f"{'='*65}")
if p_value < 0.05 and ci_low > 0:
    print(f"We are 95% confident the true lift is between {ci_low:.1%} and {ci_high:.1%}.")
    print(f"Since the entire interval is positive, the new checkout genuinely")
    print(f"improves conversion -- this is not noise. RECOMMEND: ship Variant B.")
else:
    print(f"The confidence interval crosses zero or the result isn't significant --")
    print(f"we cannot confidently say Variant B is better. RECOMMEND: do not ship")
    print(f"yet; consider running longer or re-evaluating the design.")

# ---- Segment check: does the effect hold across devices? (Simpson's paradox check) ----
print(f"\n{'='*65}\nSegment check: does the lift hold across device types?")
print(f"{'='*65}")
for device in ['mobile', 'desktop']:
    sub = df[df['device'] == device]
    sa = sub[sub['variant']=='A']['converted']
    sb = sub[sub['variant']=='B']['converted']
    print(f"{device:8s}: A={sa.mean():.2%} (n={len(sa)})  B={sb.mean():.2%} (n={len(sb)})  lift={sb.mean()-sa.mean():+.2%}")

# ---- Business impact ----
print(f"\n{'='*65}\nBusiness impact projection")
print(f"{'='*65}")
monthly_visitors = 200000
avg_order_value = 45
incremental_conversions = monthly_visitors * diff
incremental_revenue = incremental_conversions * avg_order_value
print(f"At {monthly_visitors:,} monthly checkout visitors and ${avg_order_value} AOV:")
print(f"  Projected incremental conversions/month: {incremental_conversions:,.0f}")
print(f"  Projected incremental revenue/month: ${incremental_revenue:,.0f}")
print(f"  Projected incremental revenue/year: ${incremental_revenue*12:,.0f}")
