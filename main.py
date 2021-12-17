import pandas as pd
from Levenshtein import ratio
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

df = pd.read_csv('works.csv', encoding='utf-8')
snowball = SnowballStemmer(language='russian')

""" ЗАДАНИЕ 1 """

""" Алгоритм: пробегаемся по каждому слову, устанавливая начальную форму,
    и с помощью расстояния Левенштайна смотрим отношение слов друг к другу (если слова одинаковы, то равно 1), 
    допуская опечатки или лишние буквы, поэтому 0.92.
    Алгоритм неточный, потому что достаточно 1 сходства, чтобы засчитать профессию, но что есть. """

# mismatch_count = 0
# unknown_count = 0
#
#
# def check_words(titles, qualifications):
#     match_count = 0
#     for title in titles:
#         for qual in qualifications:
#             if ratio(snowball.stem(title), snowball.stem(qual)) >= 0.92:
#                 match_count += 1
#     return match_count
#
#
# for row_index in df.index:
#     row = df.loc[row_index]
#     try:
#         new_titles = word_tokenize(row['jobTitle'], language='russian')
#         new_qualifications = word_tokenize(row['qualification'], language='russian')
#         if check_words(new_titles, new_qualifications) == 0:
#             mismatch_count += 1
#     except TypeError:
#         unknown_count += 1
#
# print(mismatch_count, unknown_count)


""" Вопрос 1:
    Профессия и должность не совпадают у 8891 людей (ещё у 22553 нет тех или иных данных) """

""" ЗАДАНИЕ 2 """

# edu = {}
#
#
# def find_word(titles, qualifications, educationType):
#     match_count = 0
#     for title in titles:
#         if ratio(snowball.stem(title), 'менеджер') >= 0.92:
#             match_count += 1
#     for qual in qualifications:
#         if ratio(snowball.stem(qual), 'менеджер') >= 0.92:
#             match_count += 1
#
#     if match_count >= 1:
#         if educationType in edu.keys():
#             edu[educationType] += 1
#         else:
#             edu[educationType] = 1
#
#
# for row_index in df.index:
#     row = df.loc[row_index]
#     try:
#         new_titles = word_tokenize(row['jobTitle'], language='russian')
#         new_qualifications = word_tokenize(row['qualification'], language='russian')
#         education_type = row['educationType']
#         find_word(new_titles, new_qualifications, education_type)
#     except TypeError:
#         pass
#
# print(edu)

""" Вопрос 2:
    Менеджерами становятся люди с образованием: {'Высшее': 908, 'Среднее профессиональное': 220, 'Незаконченное высшее': 9, 'Среднее': 11, nan: 2} """


""" ЗАДАНИЕ 3 """

jobs = {}
endings = ['ер', 'ед', 'ир', 'ец', 'ист', 'ик', 'ист']


def get_job(titles, qualifications):
    for qual in qualifications:
        if ratio(snowball.stem(qual), 'инженер') >= 0.92:

            for job in titles:
                for ending in endings:

                    if ending in job:
                        job_lower = job.lower()
                        if job_lower in jobs.keys():
                            jobs[job_lower] += 1
                        else:
                            jobs[job_lower] = 1


for row_index in df.index:
    row = df.loc[row_index]
    try:
        new_titles = word_tokenize(row['jobTitle'], language='russian')
        new_qualifications = word_tokenize(row['qualification'], language='russian')
        get_job(new_titles, new_qualifications)
    except TypeError:
        pass

print({k: v for k, v in sorted(jobs.items(), key=lambda item: item[1], reverse=True)})

""" Вопрос 3:
    Люди с дипломом инженера работают: {'специалист': 168, 'инженер': 121, 'менеджер': 90, 'начальник': 80, 'ведущий': 45} """