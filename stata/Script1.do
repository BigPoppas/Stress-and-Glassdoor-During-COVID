* Set the working directory to where your data file is located
cd "D:\Reposetories\Stress-and-Glassdoor-During-Covid\data\"

* Import the dataset
import delimited "stata_v1.csv", clear

* Convert review_date_time to Stata datetime format
gen datetime = clock(review_date_time, "YMDhms")
format datetime %tc

* Handling repeated time values within panel by averaging stress level and dropping duplicates
bysort company_id datetime: egen mean_has_stress = mean(has_stress)
by company_id datetime: gen N = _N
drop if N > 1
replace has_stress = mean_has_stress
drop mean_has_stress N

* Set the panel data structure with company_id as panel variable and datetime as time variable
* If datetime gives repeated time values within panel error, create a unique time variable or use only date
xtset company_id datetime

* Run fixed-effects regression to assess the impact of COVID on stress levels
xtreg has_stress rating_overall rating_work_life_balance length_of_employment count_helpful amount_of_funding_rounds_until_n total_funding_until_now during_covid post_covid, fe vce(robust)

