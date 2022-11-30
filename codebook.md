# Codebook
## Original card structure
The interview is structured in 5 "cards", and each card has around 80 values.  
On the original file, there are 5 rows per person interviewed, one per card.  
As each column only comprises a single character, some answers use multiple columns.

## Variable names
`cis2080_to_csv.py` transforms the original file into csv format, with column names
indicating card number and original column number, as labelled on the original questionnaire.  
For answers comprising multiple characters, these have been merged. For example, `T5_26` means
column 26 on card 5. While `T1_1-4` means columns 1 to 4, both inclusive, on card 1.

| Coded column name | Long name      | Description |
|-------------------|----------------|-------------|
| T5_26             | sex            |             |
| T5_27-28          | age            |             |
| T5_29             | marital_status |             |
| T5_30-31          | num_children   |             |


## Inconsistencies
### City code
There aren't codes for every city or town in the provided documentation. Only for the largest
city in the _provincia_ and for every city with a population over 100.000. Although not specified
in the documentation, it seems that smaller areas are coded as `0`.

### Card 5 blank page
The number of columns in card 5 is far larger than the documented variables.  
On the last page that covers the last variables of this card, there are documented variables
for a general poll weight and also weights for some regions in Andalucía, which is the first region ordered by name. The next page is blank.  
It is a reasonable guess that the undocumented variables relate to other regions that should have been on the blank page.  
We import the variable for general weight and discard consecutive columns, including those relating to Andalucía.

**Therefore, for card 5, columns after 84 are discarded.**


## Zero
It's not specified in the documentation, but it seems that very often spaces
mean zero.

## NA values
Not specified in the documentation.

For people who never smoked, the answer for the number of cigarettes a day is `-8`.
We assume this as an NA value.

In amount of beverages, 9 is considered a NA.

## Other codes for "no"
In some questions, such as telling if they have taken a specific medicament, many answers have been
coded as `0`, although the questionnaire specifically codes them as `1`, `2` and `9`. We assume
that this means "No".


## UBEs
[USA National Institutes for Health](https://www.niaaa.nih.gov/alcohols-effects-health/overview-alcohol-consumption/what-standard-drink)
[Standard Drinks in Spain (UBEs)](https://doi.org/10.20882/adicciones.621)

### Standard Drinks Spanish
1 beer = 1 Standard Drink  
1 glass of wine = 1 Standard Drink  
1 glass of spirits = 2 Standard Drinks

Vermouth is considered as a spirit.

## Income
Original answers include ranges, but for numeric computation concrete values have been assigned as shown in this table.

| Original range            | Assigned value |
|---------------------------|----------------|
| Under 50.000 ptas         | 25000          |
| 50.001 to 100.000 ptas    | 75000          |
| 100.001 to 150.000 ptas   | 125000         |
| 150.001 to 200.000 ptas   | 175000         |
| 200.001 to 300.000 ptas   | 250000         |
| 300.001 to 400.000 ptas   | 350000         |
| 400.001 to 500.000 ptas   | 450000         |
| 500.001 to 750.000 ptas   | 625000         |
| 750.001 to 1.000.000 ptas | 875000         |
| Over 1.000.000 ptas       | 1250000        |
| No answer                 | Pandas NA      |`
