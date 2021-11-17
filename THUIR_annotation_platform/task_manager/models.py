#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from user_system.models import User

try:
    import simplejson as json
except ImportError:
    import json


class TaskAnnotation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )

    # user intent
    specificity = models.IntegerField(default=-1)  # 0 ==> 4, broad ==> clear
    trigger = models.IntegerField(default=-1)  # 0 ==> 4, interest-driven ==> task-driven
    expertise = models.IntegerField(default=-1)  # 0 ==> 4, unfamiliar ==> familiar

    # search scenario
    time_condition = models.IntegerField(default=-1)  # 0 ==> 4, relax ==> tense
    position_condition = models.IntegerField(default=-1)  # 0 ==> 4, quiet ==> noisy

    # search task experience
    satisfaction = models.IntegerField(default=-1)
    information_difficulty = models.IntegerField(default=-1)
    success = models.IntegerField(default=-1)

    annotation_status = models.BooleanField(default=False)


class Query(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    task_annotation = models.ForeignKey(
        TaskAnnotation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        )

    partition_status = models.BooleanField(default=False, null=True, blank=True)
    annotation_status = models.BooleanField(default=False, null=True, blank=True)
    current_status = models.BooleanField(default=False, null=True, blank=True)

    query_string = models.CharField(max_length=1000, null=True, blank=True)
    start_timestamp = models.IntegerField(null=True, blank=True)
    end_timestamp = models.IntegerField(null=True, blank=True)
    life_start = models.IntegerField(null=True, blank=True)
    life_end = models.IntegerField(null=True, blank=True)
    # reformulation interface
    # 1: SERP inputbox, 2: SERP related queries (query suggestion),
    # 3: SERP related entities, 4: top searched queries, 5: others (other pages, sponsored search, ads)
    interface = models.IntegerField(default=1, null=True, blank=True)

    # user expectation, pre-query
    useful_pages = models.IntegerField(default=-1, null=True, blank=True)
    clicking_results = models.IntegerField(default=-1, null=True, blank=True)
    spending_time = models.IntegerField(default=-1, null=True, blank=True)    
    # diversity = models.IntegerField(default=-1, null=True, blank=True)  # 0->4
    # habit = models.CharField(max_length=50, null=True, blank=True)  #
    # redundancy = models.IntegerField(default=-1, null=True, blank=True)  # 0->4
    # difficulty = models.IntegerField(default=-1, null=True, blank=True)  # 0->4
    # gain = models.IntegerField(default=-1, null=True, blank=True)  # 0->9
    # effort = models.IntegerField(default=-1, null=True, blank=True)  # 0->9

    # user expectation confirmation, post-query
    useful_information = models.IntegerField(default=-1, null=True, blank=True)
    effort = models.IntegerField(default=-1, null=True, blank=True)
    satisfaction = models.IntegerField(default=-1, null=True, blank=True)
    recommendation = models.IntegerField(default=-1, null=True, blank=True)
    problem = models.CharField(max_length=50, null=True, blank=True)
    # diversity_confirm = models.IntegerField(default=-1, null=True, blank=True)
    # habit_confirm = models.CharField(max_length=50, null=True, blank=True)
    # redundancy_confirm = models.IntegerField(default=-1, null=True, blank=True)
    # difficulty_confirm = models.IntegerField(default=-1, null=True, blank=True)
    # gain_confirm = models.IntegerField(default=-1, null=True, blank=True)
    # effort_confirm = models.IntegerField(default=-1, null=True, blank=True)


class PageLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    belong_query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        )
    page_type = models.CharField(max_length=50, null=True, blank=True)
    page_title = models.CharField(max_length=50, null=True, blank=True)
    origin = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=1000, null=True, blank=True)
    referrer = models.CharField(max_length=1000, null=True, blank=True)
    serp_link = models.CharField(max_length=1000, null=True, blank=True)
    html = models.CharField(max_length=1000000, null=True, blank=True)
    start_timestamp = models.IntegerField(null=True, blank=True)
    end_timestamp = models.IntegerField(null=True, blank=True)
    dwell_time = models.IntegerField(null=True, blank=True)
    page_timestamps = models.CharField(max_length=1000000, null=True, blank=True)
    query_string = models.CharField(max_length=1000, null=True, blank=True)
    page_id = models.IntegerField(null=True, blank=True)
    mouse_moves = models.CharField(max_length=1000000, null=True, blank=True)
    clicked_results = models.CharField(max_length=1000000, null=True, blank=True)
    clicked_others = models.CharField(max_length=1000000, null=True, blank=True)


class QueryAnnotation(models.Model):  # !!
    id = models.AutoField(primary_key=True)
    belong_query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE,
        )
    # 1--initial, 2--spec, 3--gen, 4--meronym 5--holonym, 6--synonym, 7--parallel moving, 8--intent shift, 0--others
    relation = models.IntegerField()
    # 1--initial query ,2--SERP search snippets, 3--SERP other components,
    # 4--landing pages, 5--others (not acquired during search)
    inspiration = models.IntegerField()
    satisfaction = models.IntegerField()
    ending_type = models.IntegerField()  # 4--sat, 3--dissat, 2--new, 1-intent shift, 0--others
    other_reason = models.CharField(max_length=1000)
    other_relation = models.CharField(max_length=1000)


class SERPAnnotation(models.Model):
    id = models.AutoField(primary_key=True)
    serp_log = models.ForeignKey(
        PageLog,
        on_delete=models.CASCADE,
        )
    usefulness_0 = models.CharField(max_length=1000)
    usefulness_1 = models.CharField(max_length=1000)
    usefulness_2 = models.CharField(max_length=1000)

    serendipity_0 = models.CharField(max_length=1000)
    serendipity_1 = models.CharField(max_length=1000)

