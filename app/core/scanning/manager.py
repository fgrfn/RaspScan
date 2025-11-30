"""Scanning orchestration and backend abstraction."""
from __future__ import annotations
from typing import List
import uuid

from app.core.jobs.manager import JobManager
from app.core.jobs.models import JobRecord, JobStatus


class ScannerManager:
    """High-level entrypoint for scan operations."""

    def list_devices(self) -> List[dict]:
        # TODO: integrate SANE/eSCL discovery (Avahi + sane-airscan)
        # Example: subprocess.run(['scanimage', '-L'])
        # For now return empty list until SANE integration is complete
        return []

    def list_profiles(self) -> List[dict]:
        # TODO: pull from config storage (SQLite or config file)
        # For now return empty list until profile management is implemented
        return []

    def start_scan(self, device_id: str, profile_id: str, target_id: str, filename_prefix: str | None) -> str:
        job_id = str(uuid.uuid4())
        JobManager().create_job(
            job_id=job_id,
            job_type="scan",
            device_id=device_id,
            target_id=target_id,
            status=JobStatus.queued,
        )
        # TODO: dispatch actual scan execution to background worker
        return job_id

    def list_jobs(self) -> List[JobRecord]:
        return JobManager().list_jobs(job_type="scan")

    def get_job(self, job_id: str) -> JobRecord:
        return JobManager().get_job(job_id)
