import re
from typing import Optional

from pylatex.base_classes import Container
from pytexresume.doc import Doc
from pytexresume.infos import *


class SContainer(Container):
    def dumps(self): return self.dumps_content()


class BasicResume(Doc):
    lang: Optional[str] = None

    def gen_personal_info_block(self, personal_info: PersonalInfo) -> SContainer: raise NotImplementedError
    def gen_objective_block(self, objective: Objective) -> SContainer: raise NotImplementedError
    def gen_research_interest_block(self, research_interest: ResearchInterest) -> SContainer: raise NotImplementedError
    def gen_educations_block(self, educations: Educations) -> SContainer: raise NotImplementedError
    def gen_skills_block(self, skills: Skills) -> SContainer: raise NotImplementedError
    def gen_jobs_block(self, jobs: Jobs) -> SContainer: raise NotImplementedError


def format_link(text: Optional[str], url_icon: Optional[str] = None, email_icon: Optional[str] = None) -> Optional[str]:
    if text is None:
        return None
    url_pattern = re.compile(r'(https?://[^\s]+)')
    email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
    if url_icon is not None:
        text = url_pattern.sub(rf'\\href{{\1}}{{{url_icon}\ \1}}', text)
    else:
        text = url_pattern.sub(r'\\href{\1}{\1}', text)
    if email_icon is not None:
        text = email_pattern.sub(rf'\\href{{mailto:\1}}{{{email_icon}\ \1}}', text)
    else:
        text = email_pattern.sub(r'\\href{mailto:\1}{\1}', text)
    return text
