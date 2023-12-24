import pandas as pd
import copy
import random
from enum import Enum
import json

def get_schedule(semester_parity):

    subDF = pd.read_csv("__mocks__/subjects.csv")
    grupDF = pd.read_csv("__mocks__/groups.csv")
    profDF = pd.read_csv("__mocks__/professors.csv")
    cabDF = pd.read_csv("__mocks__/cabinets.csv")

    class Subject:
        def __init__(self, id, unitate_curs, teorie, practica, lab, semester_parity):
            self.id = id
            self.unitate_curs = unitate_curs
            self.teorie = teorie
            self.practica = practica
            self.lab = lab
            self.semester_parity = semester_parity
        def __repr__(self):
            # return f"id - {self.id}, unitate_curs - {self.unitate_curs}, teorie - {self.teorie}, practica - {self.practica}, lab - {self.lab}, parity - {self.semester_parity}"
            return f"{self.id}"

    class Group:
        def __init__(self, id, name, language, nr_persons, subject_ids):
            self.id = id
            self.name = name
            self.language = language
            self.nr_persons = int(nr_persons)
            self.subject_ids = []
            for num in subject_ids.split(','):
                try:
                    self.subject_ids.append(int(num.strip()))
                except:
                    pass
        def __repr__(self):
            # return f"name - {self.name}, lang - {self.language}, nr - {self.nr_persons}, sub_ids - {self.subject_ids}"
            return f"{self.name}"

    class Professor:
        def __init__(self, id, name, subject, _type, availability):
            self.id = id
            self.name = name
            self.subject = subject
            self.is_lab = _type == "LAB"
            self.availability = availability
        def __repr__(self):
            # return f"id - {self.id}, name - {self.name}, sub - {self.subject}, type - {self.type}, availability - \n{self.availability}"
            return f"{self.name}"

    class Cab:
        def __init__(self, id, is_lab, capacity):
            self.id = id
            self.is_lab = is_lab
            self.capacity = capacity
            self.for_seminar = capacity <= 32 # max people in group
        def __repr__(self):
            return f"id - {self.id}, lab - {self.is_lab}, cap - {self.capacity}"

    list_of_subj1 = []
    list_of_subj2 = []
    list_of_groups = []
    list_of_profs = []
    list_of_cabs = []

    for _, row in subDF.iterrows():
        id = row["id"]
        unitate_curs = row["unitate_curs"]
        teorie = row["teorie"]
        practica = row["practica"]
        lab = row["lab"]
        try:
            semester_parity = int(row["semestru"]) % 2
        except:
            continue
        subj = Subject(id, unitate_curs, teorie, practica, lab, semester_parity)
        if semester_parity:
            list_of_subj2.append(subj)
        else:
            list_of_subj1.append(subj)


    for _, row in grupDF.iterrows():
        id = row["id"]
        name = row["speciality"]
        language = row["language"]
        nr_persoane = row["nr_persoane"]
        subject_ids = row["subject_ids"]
        grup = Group(id, name, language, nr_persoane, subject_ids)
        list_of_groups.append(grup)

    for _, row in profDF.iterrows():
        id = row["id"]
        name = row["name"]
        subject = row["subject"]
        _type = row["type"]
        availability = []
        weekdays = ["mon", "tue", "wed", "thu", "fri", "sat"]
        for day in weekdays:
            _temp = []
            for j in range(7):
                availability.append(row[f"{day}_per_{j+1}"])
        prof = Professor(id, name, subject, _type, availability)
        list_of_profs.append(prof)

    for _, row in cabDF.iterrows():
        id = row["id "]
        is_lab = row["is_lab_cab"]
        nr_persons = row["nr_persons"]
        cab = Cab(id, is_lab, nr_persons)
        list_of_cabs.append(cab)

    class PairType(Enum):
        LECTURE = 0
        SEMINAR = 1
        LAB = 2

    class ProfGrupPair:
        def __init__(self, prof, group, _type):
            self.prof = prof
            self.group = group
            self.type = _type
            self.possibilities = set()
            self.entropy = 0

    prof_grup_pairs1 = []
    lab_prof_grup_pairs1 = []
    seminar_prof_grup_pairs1 = []
    for prof in list_of_profs:
        for grup in list_of_groups:
            if prof.subject in grup.subject_ids:
                subject = None
                for i in list_of_subj1:
                    if prof.subject == i.id:
                        subject = i
                if subject:
                    if prof.is_lab:
                        for i in range((subject.lab) // 30):
                            lab_prof_grup_pairs1.append(ProfGrupPair(prof, grup, PairType.LAB))
                    else:
                        for i in range((subject.practica) // 30):
                            seminar_prof_grup_pairs1.append(ProfGrupPair(prof, grup, PairType.SEMINAR))
                        for i in range((subject.teorie) // 30):
                            prof_grup_pairs1.append(ProfGrupPair(prof, grup, PairType.LECTURE))


    prof_grup_pairs2 = []
    lab_prof_grup_pairs2 = []
    seminar_prof_grup_pairs2 = []
    for prof in list_of_profs:
        for grup in list_of_groups:
            if prof.subject in grup.subject_ids:
                subject = None
                for i in list_of_subj2:
                    if prof.subject == i.id:
                        subject = i
                if subject:
                    if prof.is_lab:
                        for i in range((subject.lab + 29) // 30):
                            lab_prof_grup_pairs2.append(ProfGrupPair(prof, grup, PairType.LAB))
                    else:
                        for i in range((subject.practica + 29) // 30):
                            seminar_prof_grup_pairs2.append(ProfGrupPair(prof, grup, PairType.SEMINAR))
                        for i in range((subject.teorie + 29) // 30):
                            prof_grup_pairs2.append(ProfGrupPair(prof, grup, PairType.LECTURE))

    class CabState:
        def __init__(self, cab):
            self.prof = None
            self.groups = []
            self.cab = cab
            self.type = None
        def __repr__(self):
            return f"{self.prof}, {self.groups}, {self.cab.id}, {self.cab.capacity}, {self.type}"

    def generate_(lab_prof_grup_pairs, seminar_prof_grup_pairs, prof_grup_pairs, spacetime_states):

        print(len(lab_prof_grup_pairs))
        print(len(seminar_prof_grup_pairs)) 
        print(len(prof_grup_pairs))

        group_sets = []
        prof_sets = []

        for time_index in range(42):
            _time = []
            for cab in list_of_cabs:
                _time.append(CabState(copy.deepcopy(cab)))
            spacetime_states.append(_time)
            group_sets.append(set())
            prof_sets.append(dict())

        def get_free_spacetime(prof, group):
            _list = []
            for time_index, _time in enumerate(spacetime_states):
                if prof.name in prof_sets[time_index]:
                    cab_index = prof_sets[time_index][prof.name]
                    if spacetime_states[time_index][cab_index].cab.capacity > group.nr_persons:
                        _list.append((time_index, cab_index))
                        break
            if _list:
                return _list
            for time_index, _time in enumerate(spacetime_states):
                if not prof.availability[time_index]:
                    continue
                if group.name in group_sets[time_index]:
                    continue
                for cab_index, cab in enumerate(_time):
                    cab_lab = cab.cab.is_lab
                    if cab_lab:
                        continue
                    if cab.prof == None:
                        _list.append((time_index, cab_index))
            return _list

        def get_free_seminar_spacetime(prof,group):
            _list = []
            for time_index, _time in enumerate(spacetime_states):
                if not prof.availability[time_index]:
                    continue
                if group.name in group_sets[time_index]:
                    continue
                if prof.name in prof_sets[time_index]:
                    continue
                for cab_index, cab in enumerate(_time):
                    if cab.cab.for_seminar:
                        if cab.prof == None:
                            _list.append((time_index, cab_index))
                        if cab.prof is prof:
                            if cab.cab.capacity > group.nr_persons:
                                _list.append((time_index, cab_index))
                            break
            return _list

        def get_free_lab_spacetime(prof, group):
            _list = []
            for time_index, _time in enumerate(spacetime_states):
                if not prof.availability[time_index]:
                    continue
                if group.name in group_sets[time_index]:
                    continue
                if prof.name in prof_sets[time_index]:
                    continue
                # if prof.name in prof_sets[time_index]:
                #     cab_index = prof_sets[time_index][prof.name]
                #     if spacetime_states[time_index][cab_index].cab.capacity > group.nr_persons:
                #         _list.append((time_index, cab_index))
                #         continue
                for cab_index, cab in enumerate(_time):
                    if cab.cab.is_lab:
                        if cab.prof == None:
                            _list.append((time_index, cab_index))
                        if cab.prof is prof:
                            if cab.cab.capacity > group.nr_persons:
                                _list.append((time_index, cab_index))
                            break
            return _list

        # could be very much optimized

        def reset_possibilities(prof_grup_pairs, method):
            for pair in prof_grup_pairs:
                prof = pair.prof
                group = pair.group
                spacetime_coords = method(prof, group)
                pair.possibilities = spacetime_coords
                pair.entropy = len(spacetime_coords)

        def end_scheduling():
            df = pd.DataFrame(
                spacetime_states,
                columns = list_of_cabs
            )

            df.to_excel("scheduler2.xlsx")
            exit(0)

        def calculate(pairs, method, pairtype=None):

            total = 0
            while pairs:
                min_entropy = float("inf")

                reset_possibilities(pairs, method)

                impossible = []
                for pair in pairs:
                    if pair.entropy == 0:
                        print("FOUND IMPOSSIBLE")
                        impossible.append(pair)
                        continue
                    if pair.entropy < min_entropy:
                        min_entropy = pair.entropy

                for imp_track in impossible:
                    pairs.remove(imp_track)

                if min_entropy == 0:
                    print("Impossible state reached")
                    end_scheduling()

                lowest_entropy = []
                for pair in pairs:
                    if pair.entropy == min_entropy:
                        lowest_entropy.append(pair)

                pair_choice = random.choice(lowest_entropy)
                prof = pair_choice.prof
                group = pair_choice.group
                # print("entropy -", min_entropy)
                # print(prof, group)
                possibility = random.choice(pair_choice.possibilities)
                time_index, cab_index = possibility
                # print(list_of_cabs[cab_index].id, list_of_cabs[cab_index].is_lab)
                # group_sets[time_index].add(group.name)
                if pairtype == PairType.LECTURE:
                    prof_sets[time_index][prof.name] = cab_index
                spacetime = spacetime_states[time_index][cab_index]
                spacetime.prof = prof
                spacetime.groups.append(group)
                spacetime.cab.capacity -= group.nr_persons
                # print(pairtype)
                spacetime.cab.type = pairtype
                pairs.remove(pair_choice)
                total += 1
            # print(total)

        calculate(lab_prof_grup_pairs, get_free_lab_spacetime, PairType.LAB)
        calculate(seminar_prof_grup_pairs, get_free_seminar_spacetime, PairType.SEMINAR)
        calculate(prof_grup_pairs, get_free_spacetime, PairType.LECTURE)

    if semester_parity == 1:        
        spacetime_states1 = []
        generate_(lab_prof_grup_pairs1, seminar_prof_grup_pairs1, prof_grup_pairs1, spacetime_states1)
    if semester_parity == 2:
        spacetime_states2 = []
        generate_(lab_prof_grup_pairs2, seminar_prof_grup_pairs2, prof_grup_pairs2, spacetime_states2) 
    # spacetime_states2 = []
    # generate_(lab_prof_grup_pairs2, seminar_prof_grup_pairs2, prof_grup_pairs2, spacetime_states2)

    schedule_details = {
        group.name : {} for group in list_of_groups
    }

    def get_day(day):
        if day == 0:
            return "Monday"
        if day == 1:
            return "Tuesday"
        if day == 2:
            return "Wednesday"
        if day == 3:
            return "Thursday"
        if day == 4:
            return "Friday"
        if day == 5:
            return "Saturday"
        
    def get_hour(hour):
        if hour == 0:
            return "8:00 - 9:30"
        if hour == 1:
            return "9:45 - 11:15"
        if hour == 2:
            return "11:30 - 13:00"
        if hour == 3:
            return "13:30 - 15:00"
        if hour == 4:
            return "15:15 - 16:45"
        if hour == 5:
            return "17:00 - 18:30"
        if hour == 6:
            return "18:30 - 20:15"

    def find_subject(id):
        for i in list_of_subj1:
            if id == i:
                return i.unitate_curs

    def get_type(type):
        if type == PairType.LAB:
            return "Lab"
        if type == PairType.SEMINAR:
            return "Sem"
        if type == PairType.LECTURE:
            return "Curs"

    for i, _time in enumerate(spacetime_states1):
        for cab in _time:
            if cab.prof != None:
                day = i // 7
                hour = i % 7
                
                for group in cab.groups:
                    schedule_details[group.name][f"{get_day(day)}-{get_hour(hour)}"] = {
                        "subject" : f"{find_subject(cab.prof.subject)} - {get_type(cab.cab.type)}",
                        "room" : cab.cab.id,
                        "professorName" : cab.prof.name
                    }


    return schedule_details

    # df = pd.DataFrame(
    #     spacetime_states1,
    #     columns = list_of_cabs
    # )

    # df.to_excel("parity1.xlsx")

    # df = pd.DataFrame(
    #     spacetime_states2,
    #     columns = list_of_cabs
    # )

    # df.to_excel("parity2.xlsx")