from typing import Dict, List, Optional

from pydantic import BaseModel, root_validator


class LocalizedField(BaseModel):
    translations: Optional[Dict[str, str]] = None

    @root_validator(pre=True)
    def handle_plain_dict(cls, values):
        if isinstance(values, dict) and 'translations' not in values:
            return {'translations': values}
        return values

    def get(self, language: str) -> str:
        if self.translations:
            return self.translations.get(language, self.translations.get('en', ''))
        return ''


class Info(BaseModel):
    @classmethod
    def load(cls, info_dict: Dict):
        return cls(**info_dict)


class PersonalInfo(Info):
    title: Optional[LocalizedField] = None
    name: Optional[LocalizedField] = None
    experience: Optional[LocalizedField] = None
    email: Optional[str] = None
    birth: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[LocalizedField] = None
    github: Optional[str] = None
    website: Optional[str] = None


class Objective(Info):
    title: Optional[LocalizedField] = None
    description: Optional[LocalizedField] = None


class ResearchInterest(Info):
    title: Optional[LocalizedField] = None
    areas: Optional[List[LocalizedField]] = []


class Education(Info):
    school_name: Optional[LocalizedField] = None
    school_abbreviation: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    degree: Optional[LocalizedField] = None
    faculty: Optional[LocalizedField] = None
    honors: Optional[List[LocalizedField]] = []


class Educations(Info):
    title: Optional[LocalizedField] = None
    educations: Optional[List[Education]] = []


class SkillItem(Info):
    category: Optional[LocalizedField] = None
    description: Optional[LocalizedField] = None
    skills: Optional[List[str]] = []


class Skills(Info):
    title: Optional[LocalizedField] = None
    skill_items: Optional[List[SkillItem]] = []


class JobItemPoint(Info):
    key: Optional[LocalizedField] = None
    description: Optional[LocalizedField] = None


class JobItem(Info):
    item_name: Optional[LocalizedField] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[LocalizedField] = None
    note: Optional[LocalizedField] = None
    points: Optional[List[JobItemPoint]] = []


class JobDuties(Info):
    title: Optional[LocalizedField] = None
    description: Optional[LocalizedField] = None


class Job(Info):
    company_name: Optional[LocalizedField] = None
    job_title: Optional[LocalizedField] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    job_duties: Optional[JobDuties] = None
    items: Optional[List[JobItem]] = []


class Jobs(Info):
    title: Optional[LocalizedField] = None
    jobs: Optional[List[Job]] = []
