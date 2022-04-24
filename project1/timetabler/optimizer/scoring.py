import numpy as np

from timetabler.data.lecture import LectureList, LectureReportDB
from timetabler.data.time_table import LectureTime, TimeTable


class Evaluator:
    def __init__(self, lecture_list: LectureList, report_db: LectureReportDB):
        self.lecture_list = lecture_list
        self.report_db = report_db

    def evaluate(self, tt: TimeTable, difficulty: int, team: int, exam_difficulty: int, diversity: int, blank_level: int) -> float:
        assignment_score = 0
        team_project_score = 0
        exam_score = 0
        grade_score = 0
        blank_score = 0
        total_range = 0
        category_dist = dict()

        for lecture in tt.lectures:
            report = self.report_db.get_report(lecture.lecture, lecture.professor)
            category = self.lecture_list.get_lecture_category(report.lecture)[0]

            assignment_score += report.assignment_counts * (report.assignment_level + 0.5)
            team_project_score += report.team_project
            exam_score += report.exam_counts * (report.exam_level + 0.5)
            grade_score += report.grade_level

            category_dist[category] = category_dist.get(category, 0) + 1

        for day in range(5):
            if np.sum(tt.table[day]) == 0:
                continue

            for first_idx in range(48):
                if tt.table[day, first_idx] >= 0:
                    break

            for last_idx in range(48):
                if tt.table[day, -last_idx - 1] >= 0:
                    break

            count = np.sum(tt.table[day, first_idx:-last_idx])
            total = 48 - first_idx - last_idx
            blank_score += total - count
            total_range += total

        jeongong_ratio = category_dist.get('전공', 0) / len(tt.lectures)
        category_dist = np.array(list(category_dist.values())) / len(tt.lectures)

        total_score = (difficulty - 1) * (assignment_score + grade_score) \
                      + (team - 1) * team_project_score \
                      + (exam_difficulty - 1) * exam_difficulty
        total_score /= len(tt.lectures)

        total_score -= blank_score / total_range * -(blank_level - 1)

        if diversity == 0:
            total_score += jeongong_ratio
        elif diversity >= 2:
            total_score -= jeongong_ratio * 0.5
        if diversity == 3:
            total_score += category_dist.var()

        return 1 / (1 + np.exp(-total_score)) * 100
