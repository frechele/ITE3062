from collections import namedtuple
import pandas as pd
import os
import pickle
from typing import Dict, List


Lecture = namedtuple('Lecture', ['name', 'category'])
LECTURE_REPORT_ELEMENTS = ['lecture', 'professor', 'assignment_counts', 'assignment_level',
                           'team_project', 'exam_counts', 'exam_level', 'exam_type', 'grade_level']
LectureReport = namedtuple(
    'LectureReport', LECTURE_REPORT_ELEMENTS)

def _make_mapping_table(labels: List[str]) -> Dict[str, int]:
    return { k: i for i, k in enumerate(labels) }

ASSIGNMENT_COUNTS_LABELS = ['없음', '보통', '많음']
ASSIGNMENT_LEVEL_LABELS = ['쉬움', '보통', '어려움', '매우어려움']
TEAM_PROJECT_LABELS = ['없음', '있음']
EXAM_COUNTS_LABELS = ['없음', '1번', '2번', '3번+']
EXAM_LEVEL_LABELS = ['쉬움', '보통', '어려움', '매우어려움']
EXAM_TYPE_LABELS = ['객관식', '혼합형', '논술형']
GRADE_LEVEL_LABELS = ['너그러움', '보통', '깐깐함']

ASSIGNMENT_COUNTS_MAPPING = _make_mapping_table(ASSIGNMENT_COUNTS_LABELS)
ASSIGNMENT_LEVEL_MAPPING = _make_mapping_table(ASSIGNMENT_LEVEL_LABELS)
TEAM_PROJECT_MAPPING = _make_mapping_table(TEAM_PROJECT_LABELS)
EXAM_COUNTS_MAPPING = _make_mapping_table(EXAM_COUNTS_LABELS)
EXAM_LEVEL_MAPPING = _make_mapping_table(EXAM_LEVEL_LABELS)
EXAM_TYPE_MAPPING = _make_mapping_table(EXAM_TYPE_LABELS)
GRADE_LEVEL_MAPPING = _make_mapping_table(GRADE_LEVEL_LABELS)


class LectureList:
    def __init__(self):
        self.df = pd.DataFrame(columns=['lecture', 'professor', 'category'])

        with open('database/lecture_list', 'rt') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue

                lecture, prof, category = line.split('\t')
                self.df = self.df.append({
                    'lecture': lecture,
                    'professor': prof,
                    'category': category
                }, ignore_index=True)

    def get_lectures(self) -> List[str]:
        result = set()

        for name in self.df['lecture']:
            result.add(name)

        return list(result)

    def get_lectures_by_category(self, category: str) -> List[str]:
        result = set()

        for name in self.df[self.df['category'] == category]['name']:
            result.add(name)

        return list(result)

    def get_lectures_by_professor(self, professor: str) -> List[Lecture]:
        result = list()

        for name, _, category in self.df[self.df['professor'] == professor].itertuples(index=False):
            result.append(Lecture(name=name, category=category))

        return result

    def get_professors_by_lecture(self, lecture: str) -> List[str]:
        result = set()

        for prof in self.df[self.df['lecture'] == lecture]['professor']:
            result.add(prof)

        return list(result)


class LectureReportDB:
    def __init__(self):
        pass

    def add_report(self, report: LectureReport):
        def _impl(df: pd.DataFrame) -> pd.DataFrame:
            return df.append(report._asdict(), ignore_index=True)

        self.open(_impl)

    def get_report(self, lecture: str, professor: str) -> LectureReport:
        with open('database/report_summary.pkl', 'rb') as f:
            df = pickle.load(f)

        record = df[(df['professor'] == professor) & (df['lecture'] == lecture)].iloc[0]
        return LectureReport(**record.to_dict())

    def open(self, fn, read_only: bool = False):
        if os.path.exists('database/reports.pkl'):
            with open('database/reports.pkl', 'rb') as f:
                data: pd.DataFrame = pickle.load(f)
        else:
            data: pd.DataFrame = pd.DataFrame(columns=LECTURE_REPORT_ELEMENTS)

        data = fn(data)

        if not read_only:
            with open('database/reports.pkl', 'wb') as f:
                pickle.dump(data, f)

    def summary_reports(self, lecture_list: LectureList):
        with open('database/reports.pkl', 'rb') as f:
            df = pickle.load(f)

        df_result = pd.DataFrame(columns=LECTURE_REPORT_ELEMENTS)

        lectures = lecture_list.get_lectures()
        for lecture in lectures:
            professors = lecture_list.get_professors_by_lecture(lecture)

            for professor in professors:
                df_lec_prof = df[(df['lecture'] == lecture) &
                                 (df['professor'] == professor)]

                if len(df_lec_prof) == 0:
                    continue

                df_lec_prof.loc[:, 'assignment_counts'] = df_lec_prof.assignment_counts.apply(lambda x: ASSIGNMENT_COUNTS_MAPPING[x])
                df_lec_prof.loc[:, 'assignment_level'] = df_lec_prof.assignment_level.apply(lambda x: ASSIGNMENT_LEVEL_MAPPING[x])
                df_lec_prof.loc[:, 'team_project'] = df_lec_prof.team_project.apply(lambda x: TEAM_PROJECT_MAPPING[x])
                df_lec_prof.loc[:, 'exam_counts'] = df_lec_prof.exam_counts.apply(lambda x: EXAM_COUNTS_MAPPING[x])
                df_lec_prof.loc[:, 'exam_level'] = df_lec_prof.exam_level.apply(lambda x: EXAM_LEVEL_MAPPING[x])
                df_lec_prof.loc[:, 'exam_type'] = df_lec_prof.exam_type.apply(lambda x: EXAM_TYPE_MAPPING[x])
                df_lec_prof.loc[:, 'grade_level'] = df_lec_prof.grade_level.apply(lambda x: GRADE_LEVEL_MAPPING[x])

                result_dict = {
                    'lecture': lecture,
                    'professor': professor
                }
                for key in LECTURE_REPORT_ELEMENTS[2:]:
                    result_dict[key] = df_lec_prof[key].mean()

                df_result = df_result.append(result_dict, ignore_index=True)
                
        with open('database/report_summary.pkl', 'wb') as f:
            pickle.dump(df_result, f)


if __name__ == '__main__':
    lect_list = LectureList()
    report_db = LectureReportDB()

    report_db.summary_reports(lect_list)
    print(report_db.get_report('운영체제', '정형수'))
