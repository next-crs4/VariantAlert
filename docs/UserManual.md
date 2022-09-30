# User Manual

## Home
The **VariantAlert** landing page shows a short description 
of the tool and a minimized menu bar, 
with options only for unregistered users.

![Home Page]({{ 'assets/images/home.png' | site_relative }})

To access the full functionality of VariantAlert, 
users must sign up and then log in.

## SignUp

![SignUp btn]({{ 'assets/images/signup_btn.png' | site_relative }})

The SignUp button will open the SignUp form

![SignUp]({{ 'assets/images/signup.png' | site_relative }})

## Login

![Login btn]({{ 'assets/images/login_btn.png' | site_relative }})

By clicking on the Login button, the Login form will be displayed

![Login]({{ 'assets/images/login.png' | site_relative }})

## After Login
After login successfully, user is redirected to the query page.

![After Login]({{ 'assets/images/after_login.png' | site_relative }})

Please note the changes in menu bar:

- A User menu to edit your profile (green button) and to log out (red button) 

![User Menu]({{ 'assets/images/user_menu.png' | site_relative }})

-  A new dropdown item in menu bar: **Variants**

![Variant Menu]({{ 'assets/images/variants_menu.png' | site_relative }})

## Add New
This is the page where users are automatically redirected after login.
Variant Alert offers users two ways to submit their variants to keep under control:

- **Single** mode: the user can fill the form one variant at a time
- **Multiple** mode: upload of a VCF or CSV file containing multiple variants

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

![Single Mode]({{ 'assets/images/add_new_single.png' | site_relative }})

After successfully submitting the variant, the user will be redirected to
the **Details** page with the results of the query.

### Multiple Mode

####  From CSV file
![Multiple Mode from CSV]({{ 'assets/images/add_new_multiple_csv.png' | site_relative }})

In this case, the label will be the same for all the variants.
An example csv file is available [here]({{ 'assets/files/ex_multiple_mode.csv' | site_relative }}).

After successfully submitting, the user will be redirected to the **History** 
page with the list of the submitted variants.

####  From VCF file
![Multiple Mode from VCF]({{ 'assets/images/add_new_multiple_vcf.png' | site_relative }})

Again, the label will be the same for all the variants.
After successfully submitting, the user will be redirected to the **History** 
page with the list of the submitted variants.

## Show all
The page shows a table listing all the variants submitted by the user.

![Show all]({{ 'assets/images/show_all.png' | site_relative }})

For each variant the query parameters, 
the creation date and the date of the last change are shown. 
If a change in annotation was detected since the last login, 
the variant is marked with an alert tick. In addition, 
each variant features 3 action buttons:

![Actions]({{ 'assets/images/show_all_actions.png' | site_relative }})

- Green: show query results (**Detail** page)
- Red: delete the variant
- Blue: download the query results as Excel file (`*.xlsx`)

A form below the table allows the user to filter and sort the list of queries.

![Filters]({{ 'assets/images/show_all_filters.png' | site_relative }})

## Alerts
Display only variants with an updated annotation since the last login.

![Only Alerts]({{ 'assets/images/only_alerts.png' | site_relative }})

## Details
This page shows variant details and results of the query.

![Details 1]({{ 'assets/images/details_1.png' | site_relative }})

![Details 2]({{ 'assets/images/details_2.png' | site_relative }})


## Download
Users can download query results as `*.xlsx` file 

![Download]({{ 'assets/images/download.png' | site_relative }})
