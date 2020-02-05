This project is a combination of python and terraform to update the SDP AWS Resolver policies in AWS and upload data into AppGate.
In order to update the SDP AWS resolver policies in AWS, a two step process is
required.


Create the Terraform Variables file containing the data to update by running
python script that will create a "variables.tf" file by reading the data from
CSV file where the AWS acocund ID is included.


After the Variables file is created, use terraform to apply the "main.tf"
script which will update the AWS Policy in the "SDP Pro account".


A variables file is included in his project to preview how the "variables.tf" file
will look.

This program imports data from a CSV file, converts it into a JSON data structure that is consumable by SDP's REST API.
It then performs REST API calls and feeds the JSON data for entitlements and policies into the SDP.

The CSV file needs to be written in the following format starting from the top line:
service name, "list of servers separated by a comma ", ports(no spaces allow if there's more than one), "okta application ids (if applicable)", a comma
and on the 7th column a "Y" to specify if the services are ready for export.

Once the data is read from the CSV file, a JSON data structure for entitlements and policies is created, and then the relevant fields are taken from the
CSV data to populate the relevant fields.

Once this data structure is created and stored in a list, the program creates the REST API calls to retrieve the tokens which will be used to POST entitlements
and policies.

************************************************************************************************************************************************************************************

Instructions:

0. Pull the repository and edit the .env file as per the example (this file is added in .gitignore). 
   Make sure your credentials for Appgate-Pro are stored for the AWS CLI.
   Make sure youre using Python3
   Install config library
   Install requests library

1. Download the CSV 

2.  Run the "var_format.py" program which will create a new file called "variables.tf" with all the required information to run the main terraform program.

3. Once the file is created, run the "main.tf" file: "terraform init" -> terraform plan" -> "terraform apply"   

4. After the AWS changes have been implemented, run the "appgate_heimdall_data_import.py dev/stage/prod" program.

5. Push the tfstate files back to the repository. 

6. Optional - the "appgate_cleanup.py dev/stage" program can be used to delete Heimdall Entitlements, Policies and Assumed Roles. Can be used to practice. Cannot be used in prod as there are no    prod option.  
