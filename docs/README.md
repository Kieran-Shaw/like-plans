# v1 model

### raw plans

- The raw_plans.csv file has all of the plans and all their attributes; in addition to some airbyte data that is unimportant

### raw pricings

- The raw_pricings.csv file has, for each plan, every premium by age. The format is "long" format.

### cleaning plans

- How should I be dealing with null values? For example, how should we deal with null values for HMO plans that don't have out of network coverage (so they have no deductible or coinsurance or anything like that?)
  - Potentially, we need to have a different similarity model for the different plan types.
  - Would we want to compare an HMO plan vs. a PPO plan? My gut is saying that that sort of comparison isn't worth it at finding similar plans. BUT, that level of comparison could be worth it / worthwhile when talking about looking at an employers package of plans - what is the average actuarial value of your offering to employees across the plans? How much do you contribute to those plans? What does plotting AV vs. average contribution do?

### model implementation

- To build an accurate similarity model, it is important to compare like plan types to one another. I am mostly thinking here about comparing HMO/EPO to HMO/EPO and then PPO/POS to PPO/POS.
- Building the model to compare HMO to PPO will both break the model (a bunch of nulls in out of network coverage) and it will also not result in accurate information.
- Tactically, this means that I should clean the columns (in network and out of network) with the knowledge that the in network fields will be used for all plan types (HMO, EPO, PPO, POS) and the out of network will be used for just PPO and POS

# data visualization

- I need to prepare a dataframe where we can visualize the things that we want (ex: premium vs. plan_level)
- Should this be in the pricings dataframe? Should I join everything to the plans dataframe?

# random notes

- A Tiered Healthcare Plan
  - A tiered healthcare plan is where the insurance carrier provides financial incentives for patients to get care within the first tier. In other words, I think there is a different level of costs that the insurance carrier has negotiated for providers within the first tier, where this level of costs is likely lower.
    - In Network Tier 1 -> Lowest $
    - In Network Tier 2 -> Middle $
    - Out of Network -> Highest $
- How should I handle this when building the similarity model?
  - In general, I don't actually think that this is super important. It mostly is the case with the Blues (Anthem, BlueShield) in California, and I haven't seen this much with the other carriers.
  - It is probably most instructive to have in network vs. out of network cost sharing, and this in network tier 1 vs. tier 2 doesn't seem as important.
- "Not Covered" or "Null" Values
  - Sometimes, there are "Not Covered" values in the moop or deductible or coinsurance - really, you can name any feature.
  - This isn't a bad thing, it is actually a feature of the plan.
    - ex: an HMO plan does not have out of network cost sharing (unless, for emergency services)
    - ex: a plan may not have coinsurance (this is different than a value of 0%). 0% implies that there still exists coinsurance on that plan, while nan (null value) really means that the plan doesn't have any.
