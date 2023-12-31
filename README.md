# like-plans

A repo for medical plan similarity (and expressed similarity attributes) and recommendations

## How to use this repository?

1. Google ADC file path in .env
2. Run `python src/data/get_data.py` to get the plans and pricings
3. Run `python src/data/clean_data.py` to clean the data
4. Run `python src/models/v1_model.py` to see results.csv table populated

## v1 - Simple Similarity Model using Cost Sharing Details (plan attributes)

- This is a basic model - one that purely builds a similarity across the plan attributes that are known
  - here are some of the plan attributes that will be in this simple model
    - level ✅
    - individual_in_network_deductible ✅
    - family_in_network_deductible ✅
    - individual_out_of_network_deductible ✅
    - family_out_of_network_deductible ✅
    - individual_medical_moop ✅
    - family_medical_moop ✅
    - primary_care_physician ✅
    - plan_coinsurance ✅
    - infertility ✅
    - hsa_eligible ✅
    - rx_deductible ✅
    - chiropractic_services
    - networks (?? difficult one, lol)
- **How?**

  1. After processing, normalizing, and cleaning the data, just find the similarity across attributes (we should change the weights to say that one feature or many feature/s are more important than another)
  2. We can enable some sort of filtering; I want to see similar plans from this carrier & this plan type
  3. We can cluster the plans (based off of plan type and metallic level), and then compute similarity within that cluster?

  - This feels like it actually helps answer the question of comparing an HMO vs. an HMO. But, it brings up the question... what do we compare a EPO or POS to? These are distinct plan types

  - How might we let a use "buy down" or "buy up" - I think that this will get closer to when we need actuarial value? How might we "slide up" on the scale of a deductible or copay or something like that? I think we should be using actuarial value for this. What is a slightly better plan / worse design - ie, the plan covers a higher proportion of the cost of healthcare or the plan covers a slightly less porportion of healthcare costs?

## v2 - How can we make this model "better"

- There are a few dimensions that I think it will be interesting to make the model better
  1. Layer in Networks (size of network as a feature?)
     - Is it possible to use the # of providers per network from a data provider (ex: Ribbon)?
     - A quick thought... could it be true that the size of network is already built into the model in the premium price?
       - What is the main driver of the premium... is a question we should answer.

## v3 - "Smart" - Using Networks & AV, Can we Recommend a Plan?

---

## Viz / Research Questions

1. What are the main drivers of the premium / cost of a plan?
2. Can we calculate the Actuarial Value of a plan? How does the actuarial value of the plan impact the cost?
3. Can we "individualize" the Actuarial Value of a plan? Is this what "decision support" could be?

---

## Notes

Brainstorming:

- Actuarial Value: https://www.chcf.org/wp-content/uploads/2017/12/PDF-HealthPlanActuarialValue.pdf
  - This honestly feels like a really important piece of the model. How might we think about the actuarial value - the proportion of the average individual calims covered by the insurance plan - in relation to the similarity of medical plans?
  - A standard metric for comparing across plans with a sample (can we call it standard?) population whose claims are simulated against the cost sharing of a medical plan
- Premiums vs. Actuarial Value
- Network Size vs. Premiums vs. Actuarial Value
- Interacting an Individual vs. Actuarial Value of a Medical Plan (can we fold in the concept of an HSA here / more specific features of the plan?)
- A medical plan is actually purchasing protection against risk (we can do our best to measure the "knowable" risk, and we should model in some efficient frontier of "unknowable" risk... does someone always want to be on the efficient frontier of risk? Maybe they will willingly choose to be inside of the efficient frontier...)

  - If one is purchasing protection against risk, there is absolutely an efficient frontier for each individual given their expected utilization (dependents included) and their risk tolerance
  - Maybe, we could suggest a risk tolerance level. You should be willing to take a risk because of x, y, and z demographic considerations

- Can we "predict" actuarial value?

  - Do I have to build an actuarial value calculator... or can I train a model on the characteristics of the plan to then predict what the AV would be?
  - Eh, I think the important thing here is that it is tied to the sample population

- Health Plan Provider Networks?
  - https://www.soa.org/resources/tables-calcs-tools/research-health-plan-provider-network-risk/
- Long Term Health Care Projection Costs

  - https://www.soa.org/research-reports/research-healthcare-trends/

- Network Data

  - Can we use and process network data from Ribbon to understand the number of providers and use that in the model?

- Do we need to be able to compare an HMO to a PPO and visa versa? Wouldn't it just be comparing in-network options for those plans?
