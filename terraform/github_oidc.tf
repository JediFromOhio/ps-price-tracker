resource "aws_iam_openid_connect_provider" "github" {
  url               = "https://token.actions.githubusercontent.com"
  client_id_list    = ["sts.amazonaws.com"]
  thumbprint_list   = ["6938fd4d98bab03faadb97b34396831e3780aea1",
"1c5824a80a62e7b763e9ea4ed25282e6d5067420"]
}

resource "aws_iam_role" "github_actions_deploy" {
  name = "ps-price-tracker-github-deploy-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" : "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" : "repo:jedifromohio/ps-price-tracker:ref:refs/heads/main"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "ssm_deploy" {
  name = "ssm-deploy-policy"
  role = aws_iam_role.github_actions_deploy.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:SendCommand",
          "ssm:GetCommandInvocation"
        ]
        Resource = "*"
      }
    ]
  })
}

output "github_actions_role_arn" {
  description = "The ARN of the role for GitHub Actions"
  value       = aws_iam_role.github_actions_deploy.arn
}