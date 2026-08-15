"""
Simulate the A/B test running for the pre-computed sample size.
True effect baked in: Variant B genuinely lifts conversion by ~1.8 points
(close to, but not exactly, our 2-point MDE -- realistic, since true effects
rarely land exactly where planned).
"""
import numpy as np
import pandas as pd

np.random.seed(7)

n_per_group = 4600  # slightly above required 4,438, realistic (traffic doesn't stop exactly on target)

# Variant A (control, old checkout): 12% conversion
converted_a = np.random.binomial(1, 0.12, n_per_group)
# Variant B (new checkout): true 13.8% conversion (1.8pt lift)
converted_b = np.random.binomial(1, 0.138, n_per_group)

device_a = np.random.choice(['mobile', 'desktop'], n_per_group, p=[0.65, 0.35])
device_b = np.random.choice(['mobile', 'desktop'], n_per_group, p=[0.65, 0.35])

df = pd.concat([
    pd.DataFrame({'user_id': [f'A{i:05d}' for i in range(n_per_group)],
                  'variant': 'A', 'converted': converted_a, 'device': device_a}),
    pd.DataFrame({'user_id': [f'B{i:05d}' for i in range(n_per_group)],
                  'variant': 'B', 'converted': converted_b, 'device': device_b}),
], ignore_index=True)

df.to_csv('ab_test_data.csv', index=False)
print(f"Generated {len(df)} rows ({n_per_group} per variant)")
print(df.groupby('variant')['converted'].agg(['count', 'sum', 'mean']))
