from pylatex import Command, Itemize, NoEscape
from pylatex.base_classes import LatexObject
from pytexresume.infos import *
from pytexresume.resume import BasicResume, SContainer, format_link


class SItemize(Itemize):
    _latex_name = "itemize"

    def add_item(self, s):
        if isinstance(s, LatexObject):
            super().append(NoEscape("\item {}".format(s.dumps())))
        else:
            super().append(NoEscape("\item {}".format(s)))

    def add_avoid_none(self, fmt: str = "{}", value=""):
        if value is not None:
            self.add_item(fmt.format(value))


class EnSimple(BasicResume):
    lang: str = 'en'

    def gen_personal_info_block(self, personal_info: PersonalInfo) -> SContainer:
        container = SContainer()
        container.append(Command('resumeSection', arguments=NoEscape(personal_info.title.get(self.lang))))
        container.append(Command('resumeSubsection', arguments=[NoEscape(personal_info.name.get(self.lang)), ""]))
        with container.create(SItemize()) as itemize:
            itemize: SItemize
            itemize.add_avoid_none("Experience: {}", personal_info.experience.get(self.lang))
            itemize.add_avoid_none("Email: {}", format_link(personal_info.email))
            itemize.add_avoid_none("Birth: {}", personal_info.birth)
            itemize.add_avoid_none("Phone: {}", personal_info.phone)
            itemize.add_avoid_none("Location: {}", personal_info.location.get(self.lang))
            itemize.add_avoid_none("GitHub: {}", format_link(personal_info.github))
            itemize.add_avoid_none("Website: {}", format_link(personal_info.website))
        return container

    def gen_objective_block(self, objective: Objective) -> SContainer:
        container = SContainer()
        container.append(Command('resumeSection', arguments=NoEscape(objective.title.get(self.lang))))
        with container.create(SItemize()) as itemize:
            itemize: SItemize
            itemize.add_avoid_none(value=format_link(objective.description.get(self.lang)))
        return container

    def gen_research_interest_block(self, research_interest: ResearchInterest) -> SContainer:
        container = SContainer()
        container.append(Command('resumeSection', arguments=NoEscape(research_interest.title.get(self.lang))))
        with container.create(SItemize()) as itemize:
            itemize: SItemize
            for research_area in research_interest.areas:
                itemize.add_avoid_none(value=research_area.get(self.lang))
        return container

    def gen_educations_block(self, educations: Educations) -> SContainer:
        container = SContainer()
        container.append(Command('resumeSection', arguments=NoEscape(educations.title.get(self.lang))))
        for education in educations.educations:
            container.append(Command('resumeEducation',
                                     arguments=[NoEscape(education.degree.get(self.lang)),
                                                NoEscape(education.start_date + ' - ' + education.end_date),
                                                NoEscape(education.faculty.get(self.lang)),
                                                NoEscape(education.school_name.get(self.lang))]))

            if education.honors:
                with container.create(SItemize()) as itemize:
                    itemize: SItemize
                    for honor in education.honors:
                        itemize.add_avoid_none(value=format_link(honor.get(self.lang)))

        return container

    def gen_skills_block(self, skills: Skills) -> SContainer:
        container = SContainer()
        container.append(Command('resumeSection', arguments=skills.title.get(self.lang)))
        with container.create(SItemize()) as itemize:
            itemize: SItemize
            for skill in skills.skill_items:
                if skill.skills:
                    itemize.add_item(Command(command="resumeSingleHead", arguments=[
                        NoEscape(skill.category.get(self.lang)+":"),
                        NoEscape(", ".join(skill.skills))
                    ]))
                else:
                    itemize.add_item(Command(command="resumeSingle",
                                             arguments=NoEscape(skill.description.get(self.lang))))
        return container

    def gen_jobs_block(self, jobs: Jobs) -> SContainer:
        container = SContainer()
        container.append(Command('resumeSection', arguments=NoEscape(jobs.title.get(self.lang))))
        for job in jobs.jobs:
            container.append(Command('resumeSubsectionTime',
                                     arguments=[NoEscape(job.job_title.get(self.lang)),
                                                NoEscape(job.company_name.get(self.lang)),
                                                NoEscape(job.start_date + ' - ' + job.end_date)]))
            with container.create(SItemize()) as job_itemize:
                job_itemize: SItemize
                if job.job_duties:
                    job_itemize.add_item(Command('resumeSingleHead',
                                                 arguments=[NoEscape(job.job_duties.title.get(self.lang)),
                                                            NoEscape(job.job_duties.description.get(self.lang))]))
                if job.items:
                    for job_item in job.items:
                        job_itemize.add_item(Command('resumeSubsectionProject',
                                                     arguments=[NoEscape(job_item.item_name.get(self.lang)),
                                                                NoEscape(job_item.description.get(self.lang))]))
                    with job_itemize.create(SItemize()) as job_item_itemize:
                        job_item_itemize: SItemize
                        job_item_itemize.add_avoid_none(format_link(job_item.note.get(self.lang)))
                        for item_point in job_item.points:
                            if item_point.key:
                                job_item_itemize.add_item(Command(command="resumeSingleHead", arguments=[
                                    NoEscape(item_point.key.get(self.lang)+":"),
                                    NoEscape(item_point.description.get(self.lang))
                                ]))
                            else:
                                job_item_itemize.add_item(Command(command="resumeSingle", arguments=[
                                    NoEscape(item_point.description.get(self.lang))
                                ]))
                return container
