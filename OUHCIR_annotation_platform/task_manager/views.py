#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext

from user_system.utils import *

from .utils import *
from django.views.decorators.csrf import csrf_exempt
import time

try:
    import simplejson as json
except ImportError:
    import json


@csrf_exempt
def data(request):
    if request.method == 'POST':
        message = json.loads(request.POST['message'])
        store_data(message)
        return HttpResponse('nice')
    else:
        return HttpResponse('oh no')


@csrf_exempt
@require_login
def page_annotation_submit(user, request, page_id):
    if request.method == 'POST':
        message = request.POST['message']
        store_page_annotation(message, page_id)
        return HttpResponse('nice')
    else:
        return HttpResponse('oh no')


@require_login
def task_home(user, request):
    clear_expired_query(user)
    annotation_num = len(Query.objects.filter(user=user, annotation_status=True))
    partition_num = len(Query.objects.filter(user=user, partition_status=True, annotation_status=False))
    remain_num = len(Query.objects.filter(user=user, partition_status=False))
    return render(
        request,
        'task_home.html',
        {
            'cur_user': user,
            'annotation_num': annotation_num,
            'partition_num': partition_num,
            'remain_num': remain_num
        }
        )


@require_login
def task_partition(user, request):
    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        if action_type == "partition":
            query_ids = request.POST.getlist('unpartition_checkbox')
            if query_ids:
                partition(user, query_ids)

        if action_type == "delete":
            query_ids = request.POST.getlist('unpartition_checkbox')
            if query_ids:
                delete(user, query_ids)

        if action_type == "unpartition":
            task_ids = request.POST.getlist('partition_checkbox')
            if task_ids:
                unpartition(user, task_ids)
        return HttpResponseRedirect('/task/partition/')

    clear_expired_query(user)
    unpartition_queries = sorted(Query.objects.filter(user=user, partition_status=False), key=lambda item: item.start_timestamp)
    unpartition_queries_to_pages = []
    for query in unpartition_queries:
        unpartition_queries_to_pages.append((query, sorted(PageLog.objects.filter(user=user, belong_query=query, page_type='SERP'), key=lambda item: item.start_timestamp)))

    unannotated_tasks = TaskAnnotation.objects.filter(user=user, annotation_status=False)
    unannotated_tasks_to_queries = []
    for task in unannotated_tasks:
        unannotated_tasks_to_queries.append((task.id, sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task), key=lambda item: item.start_timestamp)))
    return render(
        request,
        'task_partition.html',
        {
            'cur_user': user,
            'unpartition_queries_to_pages': unpartition_queries_to_pages,
            'partition_tasks_to_queries': unannotated_tasks_to_queries
        }
        )


@require_login
def annotation_home(user, request):
    clear_expired_query(user)
    annotated_tasks = TaskAnnotation.objects.filter(user=user, annotation_status=True)
    unannotated_tasks = TaskAnnotation.objects.filter(user=user, annotation_status=False)
    annotated_tasks_to_queries = []
    unannotated_tasks_to_queries = []
    for task in unannotated_tasks:
        unannotated_tasks_to_queries.append((task.id, sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task), key=lambda item: item.start_timestamp)))
    for task in annotated_tasks:
        annotated_tasks_to_queries.append((task.id, sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task), key=lambda item: item.start_timestamp)))

    return render(
        request,
        'annotation_home.html',
        {
            'cur_user': user,
            'unannotated_tasks_to_queries': unannotated_tasks_to_queries,
            'annotated_tasks_to_queries': annotated_tasks_to_queries
        }
        )

@require_login
def pre_task_annotation(user, request):
    if request.method == 'POST':
        task_condition = request.POST.get('task_condition')
        familarity = request.POST.get('familarity')
        pre_experience = request.POST.get('pre_experience')
        difficulty = request.POST.get('difficulty')

        pre_survey = PreSurvey()
        pre_survey.user = user
        pre_survey.task_condition = task_condition
        pre_survey.familarity = familarity
        pre_survey.pre_experience = pre_experience
        pre_survey.difficulty = difficulty
        pre_survey.save()
        return HttpResponseRedirect('https://www.bing.com/')

    return render(
        request,
        'pre_task_annotation.html',
        {
        'cur_user': user,
        }
        )


@require_login
def task_annotation1(user, request, task_id):
    if request.method == 'POST':
        task_condition = request.POST.get('task_condition_' + str(task_id))
        task_response = request.POST.get('task_response_' + str(task_id))
        time_condition = request.POST.get('time_condition_' + str(task_id))
        position_condition = request.POST.get('position_condition_' + str(task_id))
        # specificity = request.POST.get('specificity_' + str(task_id))
        # trigger = request.POST.get('trigger_' + str(task_id))
        # expertise = request.POST.get('expertise_' + str(task_id))

        task_annotation = TaskAnnotation.objects.get(id=task_id, user=user, annotation_status=False)
        task_annotation.task_condition = task_condition
        task_annotation.task_response = task_response
        task_annotation.time_condition = time_condition
        task_annotation.position_condition = position_condition
        # task_annotation.specificity = specificity
        # task_annotation.trigger = trigger
        # task_annotation.expertise = expertise
        task_annotation.save()
        return HttpResponseRedirect('/task/query_annotation/'+str(task_id))

    task_annotation = TaskAnnotation.objects.filter(id=task_id, user=user, annotation_status=False)
    if len(task_annotation) == 0:
        return HttpResponseRedirect('/task/home/')
    task_annotation = task_annotation[0]
    queries = sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task_annotation), key=lambda item: item.start_timestamp)
    queries_to_pages = []
    bookmarked_pages = []
    for query in queries:
        queries_to_pages.append((query, sorted(PageLog.objects.filter(user=user, belong_query=query, page_type='SERP'), key=lambda item: item.start_timestamp)))
        bookmarked_pages.append((query, sorted(PageLog.objects.filter(user=user, belong_query=query, bookmark='1'), key=lambda item: item.start_timestamp)))
    return render(
        request,
        'task_annotation1.html',
        {
            'cur_user': user,
            'task': task_annotation,
            'queries_to_pages': queries_to_pages,
            'bookmarked_pages': bookmarked_pages
        }
        )


@require_login
def pre_query_annotation(user, request, timestamp):
    if request.method == 'POST':
        useful_pages = request.POST.get('useful_pages')
        clicking_results = request.POST.get('clicking_results')
        spending_time = request.POST.get('spending_time')
        # diversity = request.POST.get('diversity')
        # habit = request.POST.get('habit_str')
        # redundancy = request.POST.get('redundancy')
        # difficulty = request.POST.get('difficulty')
        # gain = request.POST.get('gain')
        # effort = request.POST.get('effort')
        # unique_timstamp = request.POST.get('timestamp')
        # print diversity, habit, redundancy, difficulty, gain, effort

        new_query = Query()
        new_query.task_annotation = TaskAnnotation.objects.filter(annotation_status=True).first()
        new_query.partition_status = False
        new_query.annotation_status = False
        new_query.current_status = True
        new_query.life_start = int(time.time())
        new_query.user = user
        new_query.useful_pages = useful_pages
        new_query.clicking_results = clicking_results
        new_query.spending_time = spending_time
        # new_query.diversity = diversity
        # new_query.habit = habit
        # new_query.redundancy = redundancy
        # new_query.difficulty = difficulty
        # new_query.gain = gain
        # new_query.effort = effort
        new_query.start_timestamp = timestamp
        new_query.save()
        # print 'new_query success!'
        return HttpResponse('<html><body><script>window.close()</script></body></html>')

    return render(
        request,
        'pre_query_annotation.html',
        {
            'cur_user': user,
        }
        )

@require_login
def post_query_annotation(user, request, timestamp):
    if request.method == 'POST':
        useful_information = request.POST.get('useful_information')
        effort = request.POST.get('effort')
        satisfaction = request.POST.get('satisfaction')
        recommendation = request.POST.get('recommendation')
        problem = request.POST.get('problem_str')

        query = sorted(Query.objects.filter(user=user, current_status=True), key=lambda item: item.start_timestamp, reverse=True)[0]
        query.current_status = False
        query.life_end = int(time.time())
        query.useful_information = useful_information
        query.effort = effort
        query.satisfaction = satisfaction
        query.recommendation = recommendation
        query.problem = problem

        query.end_timestamp = timestamp
        query.save()

        # print 'query success!'
        return HttpResponseRedirect('https://www.bing.com/')

    return render(
        request,
        'post_query_annotation.html',
        {
            'cur_user': user,
        }
        )

@require_login
def query_annotation(user, request, task_id):
    task_annotation = TaskAnnotation.objects.filter(id=task_id, user=user, annotation_status=False)
    if len(task_annotation) == 0:
        return HttpResponseRedirect('/task/home/')
    task_annotation = task_annotation[0]
    queries = sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task_annotation), key=lambda item: item.start_timestamp)
    items_list = get_items_list(user, queries)

    if request.method == 'POST':
        for query in queries:
            relation = request.POST.get('relation_ratio_'+str(query.id))
            inspiration = request.POST.get('inspiration_'+str(query.id))
            satisfaction = request.POST.get('satisfaction_ratio_'+str(query.id))
            ending_type = request.POST.get('ending_ratio_'+str(query.id))
            other_reason = request.POST.get('ending_text_'+str(query.id))
            other_relation = request.POST.get('relation_text_' + str(query.id))
            query__annotation = QueryAnnotation.objects.filter(belong_query=query)[0]
            for dup_query_annotation in QueryAnnotation.objects.filter(belong_query=query)[1:]:
                dup_query_annotation.delete()
            query__annotation.relation = relation
            query__annotation.inspiration = inspiration
            query__annotation.satisfaction = satisfaction
            query__annotation.ending_type = ending_type
            query__annotation.other_reason = other_reason
            query__annotation.other_relation = other_relation

            # 触发expectation标注
            # if query.diversity != -1:
            #     # print(request.POST.get('habit_str_' + str(query.id)))
            #     diversity_confirm = request.POST.get('diversity_confirm_'+str(query.id))
            #     habit_confirm = request.POST.get('habit_str_' + str(query.id))
            #     redundancy_confirm = request.POST.get('redundancy_confirm_' + str(query.id))
            #     difficulty_confirm = request.POST.get('difficulty_confirm_' + str(query.id))
            #     gain_confirm = request.POST.get('gain_confirm_' + str(query.id))
            #     effort_confirm = request.POST.get('effort_confirm_' + str(query.id))
            #     query.diversity_confirm = diversity_confirm
            #     query.habit_confirm = habit_confirm
            #     query.redundancy_confirm = redundancy_confirm
            #     query.difficulty_confirm = difficulty_confirm
            #     query.gain_confirm = gain_confirm
            #     query.effort_confirm = effort_confirm
            #     query.save()
            query__annotation.save()
        return HttpResponseRedirect('/task/task_annotation2/'+str(task_id))

    return render(
        request,
        'query_annotation.html',
        {
            'cur_user': user,
            'items_list': items_list
        }
        )


@require_login
def task_annotation2(user, request, task_id):
    task_annotation = TaskAnnotation.objects.filter(id=task_id, user=user, annotation_status=False)
    if len(task_annotation) == 0:
        return HttpResponseRedirect('/task/home/')
    task_annotation = task_annotation[0]
    queries = sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task_annotation), key=lambda item: item.start_timestamp)
    flag = check_serp_annotations(user, queries)

    queries_to_pages = []
    for query in queries:
        queries_to_pages.append((query, sorted(PageLog.objects.filter(user=user, belong_query=query, page_type='SERP'), key=lambda item: item.start_timestamp)))

    if request.method == 'POST':
        useful_information_task = request.POST.get('useful_information_task')
        effort_task = request.POST.get('effort_task')
        satisfaction_task = request.POST.get('satisfaction_task')
        recommendation_task = request.POST.get('recommendation_task')
        # information_difficulty = request.POST.get('information_difficulty')
        # success = request.POST.get('success')
        task_annotation.useful_information_task = int(useful_information_task)
        task_annotation.effort_task = int(effort_task)
        task_annotation.satisfaction_task = int(satisfaction_task)
        task_annotation.recommendation_task = int(recommendation_task)
        # task_annotation.information_difficulty = int(information_difficulty)
        # task_annotation.success= int(success)
        # task_annotation.other_reason = request.POST.get('ending_text_'+str(task_id))
        task_annotation.annotation_status = True
        task_annotation.save()
        for query in queries:
            query.annotation_status = True
            query.save()
        return HttpResponseRedirect('/task/annotation/')

    return render(
        request,
        'task_annotation2.html',
        {
            'cur_user': user,
            'task': task_annotation,
            'queries_to_pages': queries_to_pages,
            'flag': flag
        }
        )


@require_login
def show_page(user, request, page_id):
    serp = PageLog.objects.filter(id=page_id, user=user)
    if len(serp) == 0:
        return HttpResponseRedirect('/task/home/')
    serp = serp[0]
    return render(
        request,
        'show_query.html',
        {
            'query': serp.query_string,
            'html': serp.html,
        }
        )


@require_login
def page_annotation(user, request, page_id):
    page = PageLog.objects.filter(id=page_id, user=user)
    if len(page) == 0:
        return HttpResponseRedirect('/task/home/')
    page = page[0]
    clicked_results = json.loads(page.clicked_results)
    clicked_ids = []
    for result in clicked_results:
        if result['id'] not in clicked_ids:
            clicked_ids.append(result['id'])
    if page.origin == 'baidu':
        return render(
            request,
            'page_annotation_baidu.html',
            {
                'query': page.query_string,
                'html': page.html,
                'page_id': page_id,
                'clicked_ids': clicked_ids
            }
            )
    if page.origin == 'sogou':
        return render(
            request,
            'page_annotation_sogou.html',
            {
                'query': page.query_string,
                'html': page.html,
                'page_id': page_id,
                'clicked_ids': clicked_ids
            }
            )
    if page.origin == 'google':
         return render(
            request,
            'page_annotation_google.html',
            {
                'query': page.query_string,
                'html': page.html,
                'page_id': page_id,
                'clicked_ids': clicked_ids
            }
            )
    if page.origin == 'bing':
         return render(
            request,
            'page_annotation_bing.html',
            {
                'query': page.query_string,
                'html': page.html,
                'page_id': page_id,
                'clicked_ids': clicked_ids
            }
            )
       


@csrf_exempt
def show_me_serp(request, query_id):
    query = Query.objects.get(id=query_id)
    serp = PageLog.objects.filter(belong_query=query, page_id='1')
    serp = serp[0]
    print (serp.id)
    return render(
        request,
        'show_query.html',
        {
            'html': serp.html,
        }
        )
