from fastapi import FastAPI
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "System": "Dockerized with uv and boto3"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/aws-identity")
def get_aws_identity():
    """
    Checks the current AWS identity using STS.
    This is useful for verifying ECS Task Roles or local credentials.
    """
    try:
        sts_client = boto3.client("sts")
        identity = sts_client.get_caller_identity()
        return {
            "status": "success",
            "Account": identity.get("Account"),
            "Arn": identity.get("Arn"),
            "UserId": identity.get("UserId")
        }
    except NoCredentialsError:
        return {
            "status": "error",
            "message": "No AWS credentials found. If running locally, check your .aws/credentials or env vars. If in ECS, check Task Role."
        }
    except ClientError as e:
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }
