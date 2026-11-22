
from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field, ConfigDict, model_validator


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_name: str = Field(
        min_length=3,
        max_length=100
    )

    description: str = Field(
        min_length=10,
        max_length=2000
    )

    client_name: str = Field(
        min_length=2,
        max_length=100
    )

    manager_name: str = Field(
        min_length=2,
        max_length=100
    )

    budget: float = Field(gt=0)

    currency: str = Field(
        default="INR",
        pattern=r"^[A-Z]{3}$"
    )

    start_date: date
    end_date: date

    status: Literal[
        "planned",
        "active",
        "on_hold",
        "completed"
    ] = "planned"

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError(
                "End date cannot be earlier than start date"
            )
        return self


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=2000
    )

    client_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    manager_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    budget: Optional[float] = Field(
        default=None,
        gt=0
    )

    currency: Optional[str] = Field(
        default=None,
        pattern=r"^[A-Z]{3}$"
    )

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    status: Optional[
        Literal["planned", "active", "on_hold", "completed"]
    ] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date < self.start_date
        ):
            raise ValueError(
                "End date cannot be earlier than start date"
            )
        return self
