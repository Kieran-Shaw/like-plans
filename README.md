# like-plans
A repo for medical plan similarity (and expressed similarity attributes) and recommendations


## Similarity Model

### v1 - Simple Similarity Model using Cost Sharing Details

### v2 - Layer in Networks / Actuarial Value


#### v3 - "Smart" - Using Networks & AV, Can we Recommend a Plan?


Brainstorming:
* Actuarial Value: https://www.chcf.org/wp-content/uploads/2017/12/PDF-HealthPlanActuarialValue.pdf
    * This honestly feels like a really important piece of the model. How might we think about the actuarial value - the proportion of the average individual calims covered by the insurance plan - in relation to the similarity of medical plans?
    * A standard metric for comparing across plans with a sample (can we call it standard?) population whose claims are simulated against the cost sharing of a medical plan
* Premiums vs. Actuarial Value
* Network Size vs. Premiums vs. Actuarial Value
* Interacting an Individual vs. Actuarial Value of a Medical Plan (can we fold in the concept of an HSA here / more specific features of the plan?)
* A medical plan is actually purchasing protection against risk (we can do our best to measure the "knowable" risk, and we should model in some efficient frontier of "unknowable" risk... does someone always want to be on the efficient frontier of risk? Maybe they will willingly choose to be inside of the efficient frontier...)
    * If one is purchasing protection against risk, there is absolutely an efficient frontier for each individual given their expected utilization (dependents included) and their risk tolerance
    * Maybe, we could suggest a risk tolerance level. You should be willing to take a risk because of x, y, and z demographic considerations

* Can we "predict" actuarial value?
    * Do I have to build an actuarial value calculator... or can I train a model on the characteristics of the plan to then predict what the AV would be?
    * Eh, I think the important thing here is that it is tied to the sample population


* Health Plan Provider Networks?
    * https://www.soa.org/resources/tables-calcs-tools/research-health-plan-provider-network-risk/
* Long Term Health Care Projection Costs
    * https://www.soa.org/research-reports/research-healthcare-trends/

* Network Data
    * Can we use and process network data from Ribbon to understand the number of providers and use that in the model?


