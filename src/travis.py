from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests

DATE_MECHANISM_FIRST_ENABLED = datetime(year=2019, month=7, day=11)
PANTSBUILD_PANTS_REPO_ID = 402860

JobId = int


@dataclass(frozen=True)
class TravisJob:
    id_: JobId
    repo_id: int
    created_at: datetime

    @classmethod
    def get_from_api(cls, job_id: JobId) -> Optional[TravisJob]:
        travis_token = get_travis_token()
        if travis_token is None:
            return None
        travis_response = requests.get(
            f"https://api.travis-ci.org/job/{job_id}",
            headers={"Travis-API-Version": "3", "Authorization": f"token {travis_token}"},
        )
        data = travis_response.json()
        try:
            return TravisJob(
                id_=job_id,
                repo_id=data["repository"]["id"],
                created_at=datetime.fromisoformat(data["created_at"][:-5]),
            )
        except KeyError:
            return None

    def is_valid(self) -> bool:
        """Check that the job belongs to pantsbuild.pants and that it was created after we turned
          on this mechanism."""
        return (
            self.repo_id == PANTSBUILD_PANTS_REPO_ID
            and self.created_at >= DATE_MECHANISM_FIRST_ENABLED
        )


def get_travis_token() -> Optional[str]:
    return os.getenv("TRAVIS_TOKEN")
