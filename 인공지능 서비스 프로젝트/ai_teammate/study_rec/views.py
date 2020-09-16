from django.shortcuts import render
from users.models import Customer, Domain, Score, Role, Study
from django.contrib import auth
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame
import numpy as np
import pandas as pd

###############################################################


def get_not_zero_hope_course(input_num, customer_study):
    # 스터디 과목중 하트를 하나라도 준 과목들 리스트 리턴하는 함수
    return customer_study.loc[input_num][
        customer_study.loc[input_num] != 0
    ].index.tolist()


def course_to_ability(course_list):
    # 스터디 과목 리스트를 받아 그에 맞는 성적으로 매칭, 리스트로 정리해 리턴하는 함수
    ablility = []
    for course in course_list:
        if course in [
            "voice_recog_hearts",
            "computer_vision_hearts",
            "rec_system_hearts",
            "reinforcement_hearts",
        ]:
            if "modeling_score" not in ablility:
                ablility.append("modeling_score")
        elif course == "basic_python_hearts":
            if "mean" not in ablility:
                ablility.append("mean")
        elif course == "data_analysis_hearts":
            if "data_score" not in ablility:
                ablility.append("data_score")
        else:
            if course not in ablility:
                ablility.append(course[:-7])
    return ablility


def get_grade_for_hope_course(input_num, customer_study, customer_score):
    # 사용자 번호를 받아 해당 사용자가 하트를 준 스터디과목만 골라
    # 전체 사용자의 해당 과목 성적을 리턴하는 함수
    necessary_ability_list = course_to_ability(
        get_not_zero_hope_course(input_num, customer_study)
    )
    return customer_score[necessary_ability_list]


def get_grade_sub_for_hope_course(input_num, customer_study, customer_score):
    # 사용자 번호를 받아 해당 사용자가 하트를 준 스터디과목만 골라 정리하고
    # 전체성적에서 사용자의 성적을 뺀 절대값을 리턴하는 함수
    hope_course = get_grade_for_hope_course(input_num, customer_study, customer_score)
    grade_sub_only_hope_course = np.abs(hope_course - hope_course.loc[input_num]).mean(
        axis=1
    )
    return grade_sub_only_hope_course


###############################################################

# 스터디메이트 추천시스템
def study_rec_list(request, customer_pk):
    customer_list = Customer.objects.all()
    score_list = Score.objects.all()
    study_list = Study.objects.all()
    df0 = read_frame(customer_list)
    df1 = read_frame(score_list)
    df2 = read_frame(study_list)
    customer_score = df1.loc[
        :,
        [
            "web",
            "design",
            "data_score",
            "modeling_score",
            "machine_learning",
            "statistics",
            "deep_learning",
            "algorithm",
            "nlp",
        ],
    ]

    customer_score_sum = customer_score.sum(axis=1)
    customer_score["mean"] = customer_score.mean(axis=1)
    customer_study = df2.loc[
        :,
        [
            "web_hearts",
            "design_hearts",
            "machine_learning_hearts",
            "statistics_hearts",
            "deep_learning_hearts",
            "algorithm_hearts",
            "nlp_hearts",
            "basic_python_hearts",
            "data_analysis_hearts",
            "voice_recog_hearts",
            "computer_vision_hearts",
            "rec_system_hearts",
            "reinforcement_hearts",
        ],
    ]

    my_num = df0[df0["user"] == customer_pk].index.tolist()[0]

    study_similarity = cosine_similarity(customer_study, customer_study)
    hope_course_score = get_grade_for_hope_course(
        my_num, customer_study, customer_score
    )
    grade_subs = (
        get_grade_sub_for_hope_course(my_num, customer_study, customer_score) * 0.1
    )
    score_similarity = cosine_similarity(hope_course_score, hope_course_score)
    evaluation_value = (
        grade_subs - study_similarity[my_num - 1] - score_similarity[my_num - 1]
    )

    recommend_id_list = evaluation_value.sort_values().index.tolist()

    if my_num in recommend_id_list:
        recommend_id_list.remove(my_num)
    recommend_pk_list = df0.iloc[recommend_id_list].id

    recommend_customer_list = []
    recommend_customer_score_list = []
    recommend_customer_study_list = []

    for i in recommend_pk_list:
        now_customer = Customer.objects.get(pk=int(i))
        recommend_customer_list.append(now_customer)
        recommend_customer_score_list.append(Score.objects.get(foreignkey=now_customer))
        recommend_customer_study_list.append(Study.objects.get(foreignkey=now_customer))

    context = {
        "recommend_customer_list": recommend_customer_list,
        "recommend_customer_score_list": recommend_customer_score_list,
        "recommend_customer_study_list": recommend_customer_study_list,
    }
    return render(request, "study_rec/study_rec_list.html", context)


# 추천회원 정보보기
def s_check_info(request, customer_pk):
    customer = Customer.objects.get(pk=customer_pk)
    score = Score.objects.get(foreignkey=customer)
    study = Study.objects.get(foreignkey=customer)

    context = {"customer": customer, "score": score, "study": study}
    return render(request, "study_rec/s_check_info.html", context)
