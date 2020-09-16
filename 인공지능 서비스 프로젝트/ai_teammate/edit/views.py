from django.shortcuts import render, redirect
from users.models import Customer, Domain, Score, Role, Study
from django.contrib.auth.models import User
from django.contrib import auth

#
def edit(request, customer_pk):
    return render(request, "edit/edit.html")


# 정보수정
def info_edit(request, customer_pk):
    if request.method == "POST":
        Customer.objects.filter(pk=customer_pk).update(
            name=request.POST["name"],
            email=request.POST["email"],
            phone_num=request.POST["phone_num"],
        )

        return redirect("home")

    customer = Customer.objects.get(pk=customer_pk)

    context = {"customer": customer}

    return render(request, "edit/info_edit.html", context)


# 설문조사정보수정
def domain_edit(request, customer_pk):
    customer = Customer.objects.get(pk=customer_pk)
    if request.method == "POST":

        health = request.POST["health"]
        economy = request.POST["economy"]
        culture_art = request.POST["culture_art"]
        education = request.POST["education"]
        society = request.POST["society"]
        technology = request.POST["technology"]

        Domain.objects.filter(foreignkey=customer).update(
            health=request.POST["health"],
            economy=request.POST["economy"],
            culture_art=request.POST["culture_art"],
            education=request.POST["education"],
            society=request.POST["society"],
            technology=request.POST["technology"],
            domain_sum=int(health)
            + int(economy)
            + int(culture_art)
            + int(education)
            + int(society)
            + int(technology),
        )

        return redirect("home")

    domain = Domain.objects.get(foreignkey=customer)

    context = {"customer": customer, "domain": domain}

    return render(request, "edit/domain_edit.html", context)


# 설문조사정보수정
def score_edit(request, customer_pk):
    customer = Customer.objects.get(pk=customer_pk)
    if request.method == "POST":
        web = request.POST["web"]
        design = request.POST["design"]
        machine_learning = request.POST["machine_learning"]
        statistics = request.POST["statistics"]
        deep_learning = request.POST["deep_learning"]
        algorithm = request.POST["algorithm"]
        nlp = request.POST["nlp"]
        data_score = round(int(statistics) * 0.5 + int(machine_learning) * 0.5)
        modeling_score = round(
            int(machine_learning) * 0.25
            + int(deep_learning) * 0.25
            + int(algorithm) * 0.25
            + int(nlp) * 0.25
        )

        Score.objects.filter(foreignkey=customer).update(
            web=request.POST["web"],
            design=request.POST["design"],
            machine_learning=request.POST["machine_learning"],
            statistics=request.POST["statistics"],
            deep_learning=request.POST["deep_learning"],
            algorithm=request.POST["algorithm"],
            nlp=request.POST["nlp"],
            data_score=data_score,
            modeling_score=modeling_score,
            score_sum=int(web)
            + int(design)
            + int(machine_learning)
            + int(statistics)
            + int(deep_learning)
            + int(algorithm)
            + int(nlp)
            + int(data_score)
            + int(modeling_score),
        )

        return redirect("home")

    score = Score.objects.get(foreignkey=customer)

    context = {"customer": customer, "score": score}

    return render(request, "edit/score_edit.html", context)


# 설문조사정보수정
def role_edit(request, customer_pk):
    customer = Customer.objects.get(pk=customer_pk)
    if request.method == "POST":
        analysis_hearts = request.POST["analysis_hearts"]
        web_hearts = request.POST["web_hearts"]
        design_hearts = request.POST["design_hearts"]
        modeling_hearts = request.POST["modeling_hearts"]

        Role.objects.filter(foreignkey=customer).update(
            analysis_hearts=request.POST["analysis_hearts"],
            web_hearts=request.POST["web_hearts"],
            design_hearts=request.POST["design_hearts"],
            modeling_hearts=request.POST["modeling_hearts"],
            role_sum=int(analysis_hearts)
            + int(web_hearts)
            + int(design_hearts)
            + int(modeling_hearts),
        )

        return redirect("home")

    role = Role.objects.get(foreignkey=customer)

    context = {"customer": customer, "role": role}

    return render(request, "edit/role_edit.html", context)


# 설문조사정보수정
def study_edit(request, customer_pk):
    customer = Customer.objects.get(pk=customer_pk)
    if request.method == "POST":
        web_hearts = request.POST["web_hearts"]
        design_hearts = request.POST["design_hearts"]
        machine_learning_hearts = request.POST["machine_learning_hearts"]
        statistics_hearts = request.POST["statistics_hearts"]
        deep_learning_hearts = request.POST["deep_learning_hearts"]
        algorithm_hearts = request.POST["algorithm_hearts"]
        nlp_hearts = request.POST["nlp_hearts"]
        basic_python_hearts = request.POST["basic_python_hearts"]
        data_analysis_hearts = request.POST["data_analysis_hearts"]
        voice_recog_hearts = request.POST["voice_recog_hearts"]
        computer_vision_hearts = request.POST["computer_vision_hearts"]
        rec_system_hearts = request.POST["rec_system_hearts"]
        reinforcement_hearts = request.POST["reinforcement_hearts"]

        Study.objects.filter(foreignkey=customer).update(
            web_hearts=web_hearts,
            design_hearts=design_hearts,
            machine_learning_hearts=machine_learning_hearts,
            statistics_hearts=statistics_hearts,
            deep_learning_hearts=deep_learning_hearts,
            algorithm_hearts=algorithm_hearts,
            nlp_hearts=nlp_hearts,
            basic_python_hearts=basic_python_hearts,
            data_analysis_hearts=data_analysis_hearts,
            voice_recog_hearts=voice_recog_hearts,
            computer_vision_hearts=computer_vision_hearts,
            rec_system_hearts=rec_system_hearts,
            reinforcement_hearts=reinforcement_hearts,
            study_sum=int(web_hearts)
            + int(design_hearts)
            + int(machine_learning_hearts)
            + int(statistics_hearts)
            + int(deep_learning_hearts)
            + int(algorithm_hearts)
            + int(nlp_hearts)
            + int(basic_python_hearts)
            + int(data_analysis_hearts)
            + int(voice_recog_hearts)
            + int(computer_vision_hearts)
            + int(rec_system_hearts)
            + int(reinforcement_hearts),
        )
        return redirect("home")

    study = Study.objects.get(foreignkey=customer)

    context = {"customer": customer, "study": study}

    return render(request, "edit/study_edit.html", context)