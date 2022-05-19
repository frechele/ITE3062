import copy
import numpy as np
import random
from typing import List

from timetabler.data.lecture import LectureList, LectureReportDB
from timetabler.data.time_table import TimeTable, LectureTime, LectureTimeDB, TimedLecture
from timetabler.optimizer.scoring import Evaluator


class Solution:
    def __init__(self, eval_f):
        self.tt = TimeTable()
        self.lectures: List[TimedLecture] = []
        self.required: List[bool] = []

        self.score = -np.inf
        self.eval_f = eval_f

    def add_lecture(self, lecture: TimedLecture, required: bool) -> bool:
        if not self.tt.add_lecture(lecture):
            return False

        self.lectures.append(lecture)
        self.required.append(required)
        return True

    def build(self):
        self.score = self.eval_f(self.tt)

    def __hash__(self):
        return hash((hash(lec.lecture, lec.professor, hash(tuple(lec.start_times))) for lec in self.lectures))

    def __eq__(self, other):
        return frozenset(self.lectures) == frozenset(other.lectures)


class Solver:
    def __init__(self, difficulty: int, team: int, exam_difficulty: int, diversity: int, blank_level: int, min_lecture: int, max_lecture: int, must_include: List[str]):
        self.difficulty = difficulty
        self.team = team
        self.exam_difficulty = exam_difficulty
        self.diversity = diversity
        self.blank_level = blank_level
        self.min_lecture = min_lecture
        self.max_lecture = max_lecture
        self.must_include = must_include

        self.evaluator = Evaluator(LectureList(), LectureReportDB())
        self.eval_f = lambda x: self.evaluator.evaluate(x, self.difficulty, self.team, self.exam_difficulty, self.diversity, self.blank_level)

    def get_solutions(self) -> List[Solution]:
        time_db = LectureTimeDB()

        # build first bank
        bank: List[Solution] = []
        def _build_bank(i, arr=[]):
            if i == len(self.must_include):
                sol = Solution(self.eval_f)

                for lec in arr:
                    if not sol.add_lecture(lec, True):
                        return

                while sol.tt.total_lecture < (self.max_lecture * 0.8):
                    lec_strs = set([lecture.lecture for lecture in sol.lectures])
                    candidates = list(set(time_db.get_all_timed_lectures()).difference(set(sol.lectures)))
                    candidates = list(filter(lambda x: x.lecture not in lec_strs, candidates))
                    sol.add_lecture(random.choice(candidates), False)

                sol.build()
                bank.append(sol)
                return

            for lec in time_db.get_timed_lecture(self.must_include[i]):
                _build_bank(i+1, arr+[lec])

        _build_bank(0)

        if len(bank) == 0:
            return []

        def _remove_invalid(large_bank):
            removed = []
            for candi in large_bank:
                if self.min_lecture <= candi.tt.total_lecture <= self.max_lecture:
                    removed.append(candi)

            return removed
        
        for iteration in range(10):
            tmp_bank = copy.deepcopy(bank)

            for seed in bank:
                lec_strs = set([lecture.lecture for lecture in seed.lectures])
                replaceable = []
                for idx in range(len(seed.lectures)):
                    if not seed.required[idx]:
                        replaceable.append(idx)

                for i in range(10):
                    candidates = list(set(time_db.get_all_timed_lectures()).difference(seed.lectures))

                    if np.random.random() < 0.5 or len(replaceable) == 0 or seed.tt.total_lecture < self.min_lecture:
                        candidates = list(filter(lambda x: x.lecture not in lec_strs, candidates))
                        sol = copy.deepcopy(seed)
                        if sol.add_lecture(random.choice(candidates), False):
                            sol = None
                    else:
                        candidates = list(filter(lambda x: x.lecture not in lec_strs, candidates))
                        to_replace = random.choice([None] + candidates)
                        if to_replace is not None and to_replace.lecture in lec_strs:
                            replace_idx = [lec.lecture for lec in seed.lectures].index(to_replace.lecture)
                        else:
                            replace_idx = random.choice(replaceable)

                        lectures = seed.lectures[:]
                        lectures[replace_idx] = to_replace

                        sol = Solution(self.eval_f)
                        invalid = False
                        for lecture, req in filter(lambda x: x[0] is not None, zip(lectures, seed.required)):
                            if not sol.add_lecture(lecture, req):
                                invalid = True
                                break
                        if invalid:
                            sol = None

                    if sol is not None:
                        old_energy = seed.score
                        sol.build()
                        new_energy = sol.score

                        dE = -(new_energy - old_energy)
                        if dE <= 0 or np.random.random() <= np.exp(-dE / 1e-6):
                            tmp_bank.append(sol)

            tmp_bank = _remove_invalid(list(set(tmp_bank)))
            tmp_bank.sort(key=lambda x: x.score, reverse=True)
            bank = tmp_bank[:10]

        return bank[:5]
