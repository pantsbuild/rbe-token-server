from __future__ import annotations

from google.cloud import iam_credentials_v1

RBE_EXECUTE_TEST_SCOPES = [
    "https://www.googleapis.com/auth/remotebuildexecution.actions.create",
    "https://www.googleapis.com/auth/remotebuildexecution.actions.get",
    "https://www.googleapis.com/auth/remotebuildexecution.blobs.create",
    "https://www.googleapis.com/auth/remotebuildexecution.blobs.get",
    "https://www.googleapis.com/auth/remotebuildexecution.logstreams.create",
    "https://www.googleapis.com/auth/remotebuildexecution.logstreams.get",
    "https://www.googleapis.com/auth/remotebuildexecution.logstreams.update",
]

credentials_client = iam_credentials_v1.IAMCredentialsClient()

# NB: The project name must be a wildcard `-`, per
# https://cloud.google.com/iam/credentials/reference/rest/v1/projects.serviceAccounts/generateAccessToken.
resource_name = credentials_client.service_account_path(
    project="-", service_account="travis-ci-rbe@pants-remoting-beta.iam.gserviceaccount.com"
)


def generate() -> str:
    access_token: str = credentials_client.generate_access_token(
        name=resource_name, scope=RBE_EXECUTE_TEST_SCOPES
    ).access_token
    return access_token
