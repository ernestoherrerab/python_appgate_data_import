import csv
from decouple import config

# Function to Read CSV File
def read_csv(file):
    with open(file) as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        csv_data_list = []
        csv_data_final_list = []
        for row in csv_data:
            csv_data_list.append(row)
        for csv_final_list in csv_data_list:
            del csv_final_list[-1]
            csv_data_final_list.append(csv_final_list)
        return csv_data_final_list

"""
The goal of the script is to read the AWS account IDs from a CSV file and 
create a new file that will be used by Terraform to add the aws account IDs
to the Policies in the AWS SDP Prod account.
"""
def main():
    # Read CSV File and assing to a variable
    file_var = config('IMPORT_FILE')
    master_list = read_csv(file_var)
    aws_ids_arn_list = []
    aws_account_ids_list = []

    # Read Line by Line of CSV File
    for aws_ids_line in master_list:
        if aws_ids_line[8].upper().replace(" ", "") == "Y":
            aws_account_id_list = aws_ids_line[4].split(",")
            for aws_account_id in aws_account_id_list:
                if aws_account_id not in aws_account_ids_list:
                    aws_account_ids_list.append(aws_account_id)
                    aws_ids_arn_list.append('"arn:aws:iam::' + aws_account_id + ': role/SDP_NameResolver"')
                    arn_parameters = str(aws_ids_arn_list)
                else:
                    pass
        else:
            pass

    # Create the variables file and append line by line
    try:
        with open("./variables.tf", 'w') as var_file:
            var_file.write('variable "aws_account_ids" {\n')
            var_file.write('\tdescription = "Create Assumed roles"\n')
            var_file.write('\ttype = list\n')
            var_file.write('\tdefault = ')
            var_file.write(arn_parameters.replace("'", "").replace(" ",""))
            var_file.write('\n}')
    except NameError:
        arn_parameters = None
    
if __name__ == "__main__":
    main()
