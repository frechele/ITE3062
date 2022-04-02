from collections import namedtuple
import pandas as pd
import os
import pickle
from typing import List


Lecture = namedtuple('Lecture', ['name', 'category'])
LECTURE_REPORT_ELEMENTS = ['lecture', 'professor', 'assignment_counts', 'assignment_level',
                           'team_project', 'exam_counts', 'exam_level', 'exam_type', 'grade_level']
LectureReport = namedtuple(
    'LectureReport', LECTURE_REPORT_ELEMENTS)


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


if __name__ == '__main__':
    lect_list = LectureList()
    print(lect_list.df)

    print(lect_list.get_professors_by_lecture('운영체제'))
