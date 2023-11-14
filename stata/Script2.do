* Set the working directory to where your data file is located
cd "D:\Reposetories\Stress-and-Glassdoor-During-Covid\data\"

* Import the dataset
import delimited "stata_v1.csv", clear

* Parse review_date_time to Stata datetime format
gen date_str = substr(review_date_time, 1, 10)
gen date = date(date_str, "YMD")
gen year1 = year(date)
gen month = month(date)

gen year_month = ym(year1, month)
format year_month %tm

* Drop duplicates based on company_id and year_month, keeping the first observation only
duplicates drop company_id year1, force

* Set the panel data structure with company_id as panel variable and year_month as time variable
xtset company_id year1

* Run fixed-effects regression to assess the impact of COVID on stress levels
xtlogit has_stress rating_overall rating_work_life_balance length_of_employment count_helpful amount_of_funding_rounds_until_n total_funding_until_now during_covid post_covid, fe