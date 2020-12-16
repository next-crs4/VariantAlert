# User Manual

## Home
The **VariantAlert** landing page shows a short description 
of the tool and a minimized menu bar, 
with options only for unregistered users.

![Home Page](images/home.png)

To access the full functionality of VariantAlert, 
users must sign up and then log in

## SignUp
![SignUp btn](images/signup_btn.png)

By clicking on the SignUp button, it will be shown SignUp form

![SignUp](images/signup.png)

## Login
![Login btn](images/login_btn.png)

By clicking on the Login button, it will be shown Login form

![Login](images/login.png)

## After Login
After login successfully, user is redirect on query form page.

![After Login](images/after_login.png)
Please note the changes in menu bar:
- An User menu to edit profile (green button) and to log out (red button) 

![User Menu](images/user_menu.png)

-  A new dropdown item in menu bar: **Variants**

![Variant Menu](images/variants_menu.png)

## Add New
This is the page where users are automatically redirected after login.
Variant Alert offers users two ways to submit their variants to keep under control:
- **Single** mode, by filling out the form one variant at a time
- **Multiple** mode, by uploading a csv file containing all the variants

In any case, 
for each query the user must enter the following mandatory fields, 
to identify the variant according the HGVS name based variant id
- **Label**
- **Chromosome**
- **Genomic Position**
- **Assembly**
- **Reference Variant**
- **Alternative Variant**
- **Sources**

### Single Mode
![Single Mode](images/add_new_single.png)
After successfully submitting, user will be redirect in a **Details** page, 
where is showed result of query.
### Multiple Mode
![Multple Mode](images/add_new_multiple.png)
In this case, the label will be the same for all variants.
An example csv file is available in the `files` folder
After successfully submitting, user will be redirect in a **History** page,
where is showed list of variants query.

### Sources
![Sources](images/add_new_sources.png)

## Show all
The page (shows a table listing all the variants submitted by the user.

![Show all](images/show_all.png)

For each variant the query parameters, 
the creation date and the date of the last change are shown. 
In case there has been a change since the last login, 
the variant is marked with an alert tick. In addition, 
each variant features 3 action buttons.

![Actions](images/show_all_actions.png)
- Green icon to show query results (**Detail** page)
- Red icon to delete the variant
- Blue icon to download query result as Excel file (`*.xlsx`)

Last but not least, 
a form located below the table allows you to filter 
and sort the list.

![Filters](images/show_all_filters.png)
## Alerts
In particular, users can choose to view only 
variants that have had a change since the last login.

![Only Alerts](images/only_alerts.png)

## Details
This page shows variant details and result query
![Details 1](images/details_1.png)
![Details 2](images/details_2.png)


## Download
as mentioned above, users can download query results as `*.xlsx` file 
![Download](images/download.png)
