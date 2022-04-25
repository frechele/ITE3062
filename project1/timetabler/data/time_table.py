from collections import namedtuple
import pandas as pd
import json
from typing import List
import numpy as np


LectureTime = namedtuple('LectureTime', ['day', 'start', 'end'])


class TimedLecture:
    def __init__(self, lecture: str, professor: str, unit: int, start_times: List[str], end_times: List[str]):
        self.lecture = lecture
        self.professor = professor
        self.unit = unit
        self.start_times = start_times

        self.times = []
        for start_time, end_time in zip(start_times, end_times):
            day, st_hour, st_minute = map(int, start_time.split('/'))
            day, ed_hour, ed_minute = map(int, end_time.split('/'))

            def _time_convert(hour: int, minute: int) -> int:
                return minute // 30 + 2 * hour

            self.times.append(LectureTime(day=day, start=_time_convert(
                st_hour, st_minute), end=_time_convert(ed_hour, ed_minute)))

    def __hash__(self):
        return hash((self.lecture, self.professor, tuple(self.start_times)))

    def __eq__(self, other):
        return self.lecture == other.lecture and self.professor == other.professor and self.start_times == other.start_times


class TimeTable:
    def __init__(self):
        self.table = np.ones((5, 48)) * -1
        self.lectures: List[TimedLecture] = []

    def is_valid(self, lecture: TimedLecture) -> bool:
        for t in lecture.times:
            for i in range(t.start, t.end):
                if self.table[t.day, i] >= 0:
                    return False
        return True

    def add_lecture(self, lecture: TimedLecture) -> bool:
        if not self.is_valid(lecture):
            return False

        self.lectures.append(lecture)
        for t in lecture.times:
            for i in range(t.start, t.end):
                self.table[t.day, i] = len(self.lectures) - 1

        return True

    def remove_lecture(self, lecture: TimedLecture) -> bool:
        idx = self.table[lecture.times[0].day, lecture.times[0].start]
        if idx == -1:
            return False

        if self.lectures[idx].lecture != lecture.lecture or self.lectures[idx].professor != lecture.professor:
            return False

        del self.lectures[idx]

        for t in lecture.times:
            for i in range(t.start, t.end):
                self.table[t.day, i] = -1

        return True

    @property
    def total_lecture(self) -> int:
        return sum([lecture.unit for lecture in self.lectures])


class LectureTimeDB:
    def __init__(self):
        self.df = pd.DataFrame(
            columns=['lecture', 'professor', 'unit', 'start_time', 'end_time'])

        with open('database/lecture_time', 'rt') as f:
            lecture_times = json.load(f)
            for data in lecture_times:
                lecture = data['lecture']
                professor = data['professor']
                unit = data['unit']

                start_time = []
                end_time = []

                for t in data['time']:
                    start = t['start']
                    end = t['end']

                    date_mapping = {
                        '월': 0, '화': 1, '수': 2, '목': 3, '금': 4
                    }

                    for k, v in date_mapping.items():
                        start = start.replace(k, str(v))
                        end = end.replace(k, str(v))

                    start_time.append(start)
                    end_time.append(end)

                start_time = ';'.join(start_time)
                end_time = ';'.join(end_time)

                self.df = self.df.append({
                    'lecture': lecture,
                    'professor': professor,
                    'unit': unit,
                    'start_time': start_time,
                    'end_time': end_time
                }, ignore_index=True)

    def get_timed_lecture_professor(self, lecture: str, professor: str) -> List[TimedLecture]:
        df = self.df[(self.df['lecture'] == lecture) & (self.df['professor'] == professor)][['start_time', 'end_time']]

        result = []
        for start_time, end_time in df.itertuples(index=False):
            start_times = start_time.split(';')
            end_times= end_time.split(';')

            timed_lecture = TimedLecture(lecture, professor, start_times, end_times)
            result.append(timed_lecture)

        return result

    def get_timed_lecture(self, lecture: str) -> List[TimedLecture]:
        df = self.df[self.df['lecture'] == lecture][['professor', 'unit', 'start_time', 'end_time']]

        result = []
        for professor, unit, start_time, end_time in df.itertuples(index=False):
            start_times = start_time.split(';')
            end_times= end_time.split(';')

            timed_lecture = TimedLecture(lecture, professor, unit, start_times, end_times)
            result.append(timed_lecture)

        return result

    def get_all_timed_lectures(self) -> List[TimedLecture]:
        result = []
        for lecture in self.get_lectures():
            result += self.get_timed_lecture(lecture)
        return result

    def get_lectures(self) -> List[str]:
        result = set()

        for lecture in self.df['lecture']:
            result.add(lecture)

        return list(result)
