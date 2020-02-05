variable "aws_account_ids" {
	description = "Create Assumed roles"
	type = list
	default = ["arn:aws:iam::158578129438:role/SDP_NameResolver","arn:aws:iam::281341048624:role/SDP_NameResolver","arn:aws:iam::525311203628:role/SDP_NameResolver","arn:aws:iam::217999714305:role/SDP_NameResolver","arn:aws:iam::217999714388:role/SDP_NameResolver","arn:aws:iam::217999714389:role/SDP_NameResolver"]
}