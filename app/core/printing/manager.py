"""CUPS printing integration."""
from __future__ import annotations
from typing import List
import uuid

from fastapi import UploadFile

from app.core.jobs.manager import JobManager
from app.core.jobs.models import JobRecord, JobStatus


class PrinterManager:
    """Wrapper around CUPS operations."""

    def list_printers(self) -> List[dict]:
        # TODO: query CUPS for printers via subprocess or pycups
        # Example: subprocess.run(['lpstat', '-p', '-d'])
        # For now return empty list until CUPS integration is complete
        return []

    def list_jobs(self, printer_id: str) -> List[JobRecord]:
        return JobManager().list_jobs(job_type="print", printer_id=printer_id)

    def submit_job(self, printer_id: str, upload: UploadFile, options: dict) -> str:
        job_id = str(uuid.uuid4())
        # TODO: stream uploaded file to temp storage and submit to CUPS
        JobManager().create_job(
            job_id=job_id,
            job_type="print",
            printer_id=printer_id,
            status=JobStatus.queued,
        )
        return job_id

    def print_test_page(self, printer_id: str) -> str:
        job_id = str(uuid.uuid4())
        # TODO: generate test page and submit to CUPS
        JobManager().create_job(
            job_id=job_id,
            job_type="print",
            printer_id=printer_id,
            status=JobStatus.queued,
        )
        return job_id

    def add_printer(self, uri: str, name: str, description: str | None = None) -> None:
        """Add a printer to CUPS via lpinfo/lpadmin."""
        # TODO: integrate with CUPS via subprocess or pycups
        # Example: subprocess.run(['lpadmin', '-p', name, '-v', uri, '-E'])
        pass
