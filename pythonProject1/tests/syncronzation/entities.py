from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict

from typing import Annotated
from typing import Optional

from datetime import datetime
from datetime import timezone
from datetime import date


class Entity(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CRMTeacher(Entity):
    ID: Annotated[int | None, Field(alias="ID")] = None
    Prepod: Annotated[str, Field(alias="Prepod")]
    Email: Annotated[str, Field(alias="Email")]
    Napravlenie: Annotated[str, Field(alias="Napravlenie")]


class CRMLesson(Entity):
    ID: Annotated[int | None, Field(alias="ID")] = None
    Zanyatiya: Annotated[str, Field(alias="Zanyatiya")]
    ClassID: Annotated[Optional[int], Field(alias="ClassID")]
    LessonDate: Annotated[datetime, Field(alias="LessonDate")]
    StartTime: Annotated[datetime, Field(alias="StartTime")]
    FinalTime: Annotated[datetime, Field(alias="FinalTime")]
    PrepodId: Annotated[int, Field(alias="PrepodId")]
    ThemeWork: Annotated[str, Field(alias="ThemeWork")]
    GroupId: Annotated[int, Field(alias="GroupId")]
    Status: Annotated[str, Field(alias="Status")]
    Notes: Annotated[str, Field(alias="Notes")]
    Busy: Annotated[bool, Field(alias="Busy")]
    Dist: Annotated[bool, Field(alias="Dist")]
    UchGod: Annotated[str, Field(alias="UchGod")]


class CRMGroup(Entity):
    ID: Annotated[int, Field(alias="ID")]
    GroupName: Annotated[str, Field(alias="GroupName")]
    KursID: Annotated[int, Field(alias="KursID")]
    PrepodId: Annotated[Optional[int], Field(alias="PrepodId")]
    Kurs: Annotated[str, Field(alias="Kurs")]
    Napravlenie: Annotated[str, Field(alias="Napravlenie")]
    LearnForm: Annotated[str, Field(alias="LearnForm")]
    StartDate: Annotated[datetime, Field(alias="StartDate")]
    FinalDate: Annotated[datetime, Field(alias="FinalDate")]
    StatusGroup: Annotated[str, Field(alias="StatusGroup")]
    ClientFakt: Annotated[int, Field(alias="ClientFakt")]
    Notes2: Annotated[Optional[str], Field(alias="Notes2", default=None)]
    Dist: Annotated[bool, Field(alias="Dist")]
    School: Annotated[str, Field(alias="School")]


class CRMClassrooms(Entity):
    ID: Annotated[int | None, Field(alias="ID")] = None
    Class: Annotated[str, Field(alias="Class")]
    PrimechaniyHarakteristika: Annotated[
        Optional[str], Field(alias="PrimechaniyHarakteristika")
    ]


class CRMReports(Entity):
    ID: Optional[int]
    DogovorID: int
    Dopusk: bool
    Exist: bool
    Notes: str
    Ocenka: int
    MainID: int
    ZanyatiyaID: int
    PrepodId: int
    GroupId: int


class CRMSchedule(Entity):
    ID: Optional[int]
    Days: str
    StartTime: datetime
    FinalTime: datetime
    Notes: str
    GroupId: int
    ClassID: int
    Dist: bool


class CRMDirections(Entity):
    ID: Optional[int]
    Napravlenie: str


class CRMContracts(Entity):
    ID: Optional[int]
    MainID: int
    KursID: int
    GroupId: int


class CRMStudents(Entity):
    ID: Optional[int]
    Family: str
    Imya: str
    Otch: str


class CRMCourses(Entity):
    ID: Optional[int]
    Kurs: str
    ProgrammKurs: str
    Napravlenie: str
