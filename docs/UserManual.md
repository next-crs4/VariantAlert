# User Manual

## Home
The **VariantAlert** landing page shows a short description 
of the tool and a minimized menu bar, 
with options only for unregistered users.

![Home Page](images/home.png)

To access the full functionality of VariantAlert, 
users must sign up and then log in.

## SignUp
![SignUp btn](images/signup_btn.png)

The SignUp button will open the SignUp form

![SignUp](images/signup.png)

## Login
![Login btn](images/login_btn.png)

By clicking on the Login button, the Login form will be displayed

![Login](images/login.png)

## After Login
After login successfully, user is redirected to the query page.

![After Login](images/after_login.png)
Please note the changes in menu bar:
- A User menu to edit your profile (green button) and to log out (red button) 

![User Menu](images/user_menu.png)

-  A new dropdown item in menu bar: **Variants**

![Variant Menu](images/variants_menu.png)

## Add New
This is the page where users are automatically redirected after login.
Variant Alert offers users two ways to submit their variants to keep under control:
- **Single** mode: the user can fill the form one variant at a time
- **Multiple** mode: upload of a csv file containing multiple variants

In any case, for each query the user must enter the following mandatory fields in order  
to uniquely identify the variants:
- **Label**: a label for the query
- **Chromosome**
- **Genomic Position**
- **Assembly**: hg19 or hg38
- **Reference Variant**: the reference base 
- **Alternative Variant**: the alternate bases
- **Sources**: databases for annotation

### Single Mode
![Single Mode](images/add_new_single.png)
After successfully submitting the variant, the user will be redirected to
the **Details** page with the results of the query.

### Multiple Mode
![Multple Mode](images/add_new_multiple.png)
In this case, the label will be the same for all the variants.
An example csv file is available in the `files` folder.
After successfully submitting, the user will be redirected to the **History** 
page with the list of the submitted variants.

### Sources
![Sources](images/add_new_sources.png)

## Show all
The page shows a table listing all the variants submitted by the user.

![Show all](images/show_all.png)

For each variant the query parameters, 
the creation date and the date of the last change are shown. 
If a change in annotation was detected since the last login, 
the variant is marked with an alert tick. In addition, 
each variant features 3 action buttons:

![Actions](images/show_all_actions.png)
- Green: show query results (**Detail** page)
- Red: delete the variant
- Blue: download the query results as Excel file (`*.xlsx`)

A form below the table allows the user to filter and sort the list of queries.

![Filters](images/show_all_filters.png)
## Alerts
Display only variants with an updated annotation since the last login.

![Only Alerts](images/only_alerts.png)

## Details
This page shows variant details and results of the query.
![Details 1](images/details_1.png)
![Details 2](images/details_2.png)


## Download
Users can download query results as `*.xlsx` file 
![Download](images/download.png)
