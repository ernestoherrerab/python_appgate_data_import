# Credentials to use.
provider "aws" {
    region = "eu-north-1" 
    profile = "appgate-prod"
}

data "aws_iam_policy_document" "Pol_SDP_NameResolver" {
  statement {
        sid = "VisualEditor0"
        effect = "Allow"
        actions = ["sts:AssumeRole"]
        resources = [for account_id in var.aws_account_ids:account_id]
  }
}

# Create the policy using the data structure above
resource "aws_iam_policy" "Pol_SDP_NameResolver"{
  name = "Pol_SDP_NameResolver"
  description = "SDP AWS Resolver Policy"
  policy = data.aws_iam_policy_document.Pol_SDP_NameResolver.json
}
