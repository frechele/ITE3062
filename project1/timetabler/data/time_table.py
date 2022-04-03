from collections import namedtuple
import pandas as pd
import json
from typing import List


LectureTime = namedtuple('LectureTime', ['day', 'start', 'end'])


class TimedLecture:
    def __init__(self, lecture: str, professor: str, start_times: List[str], end_times: List[str]):
        self.lecture = lecture
        self.professor = professor

        self.times = []
        for start_time, end_time in zip(start_times, end_times):
            day, st_hour, st_minute = map(int, start_time.split('/'))
            day, ed_hour, ed_minute = map(int, end_time.split('/'))

            def _time_convert(hour: int, minute: int) -> int:
                return minute // 30 + 2 * hour

            self.times.append(LectureTime(day=day, start=_time_convert(
                st_hour, st_minute), end=_time_convert(ed_hour, ed_minute)))


class TimeTable:
    pass


class LectureTimeDB:
    def __init__(self):
        self.df = pd.DataFrame(
            columns=['lecture', 'professor', 'start_time', 'end_time'])

        with open('database/lecture_time', 'rt') as f:
            lecture_times = json.load(f)
            for data in lecture_times:
                lecture = data['lecture']
                professor = data['professor']

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
                    'start_time': start_time,
                    'end_time': end_time
                }, ignore_index=True)

    def get_timed_lecture(self, lecture: str, professor: str) -> List[TimedLecture]:
        df = self.df[(self.df['lecture'] == lecture) & (self.df['professor'] == professor)][['start_time', 'end_time']]

        result = []
        for start_time, end_time in df.itertuples(index=False):
            start_times = start_time.split(';')
            end_times= end_time.split(';')

            timed_lecture = TimedLecture(lecture, professor, start_times, end_times)
            result.append(timed_lecture)

        return result

    def get_timed_lecture(self, lecture: str) -> List[TimedLecture]:
        df = self.df[self.df['lecture'] == lecture][['professor', 'start_time', 'end_time']]

        result = []
        for professor, start_time, end_time in df.itertuples(index=False):
            start_times = start_time.split(';')
            end_times= end_time.split(';')

            timed_lecture = TimedLecture(lecture, professor, start_times, end_times)
            result.append(timed_lecture)

        return result


if __name__ == '__main__':
    db = LectureTimeDB()
    
    for lecture in db.get_timed_lecture('데이터베이스시스템및응용'):
        print(lecture.lecture)
        print(lecture.professor)
        print(lecture.times)
        print()
