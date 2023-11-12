# Raw Plans

- The raw_plans.csv file has all of the plans and all their attributes; in addition to some airbyte data that is unimportant

# Raw Pricings

- The raw_pricings.csv file has, for each plan, every premium by age. The format is "long" format.

# Data Visualization

- I need to prepare a dataframe where we can visualize the things that we want (ex: premium vs. plan_level)
- Should this be in the pricings dataframe? Should I join everything to the plans dataframe?

# Random Notes

- A Tiered Healthcare Plan
  - A tiered healthcare plan is where the insurance carrier provides financial incentives for patients to get care within the first tier. In other words, I think there is a different level of costs that the insurance carrier has negotiated for providers within the first tier, where this level of costs is likely lower.
    - In Network Tier 1 -> Lowest $
    - In Network Tier 2 -> Middle $
    - Out of Network -> Highest $
- How should I handle this when building the similarity model?
  - In general, I don't actually think that this is super important. It mostly is the case with the Blues (Anthem, BlueShield) in California, and I haven't seen this much with the other carriers.
  - It is probably most instructive to have in network vs. out of network cost sharing, and this in network tier 1 vs. tier 2 doesn't seem as important.
