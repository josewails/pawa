import json
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.layouts import gridplot

from .models import (
    Survey,
    SurveyResult
)

def average(arr):

    if len(arr) > 0:
        return sum(arr) / len(arr)
    else:
        return 0


def get_groups_context(current_group):

    current_survey = Survey.objects.get(group=current_group)
    current_results = SurveyResult.objects.filter(survey=current_survey)
    current_group_infos = current_group.groupinfo_set.all()
    num_entries = current_results.count()

    dates = [current_result.created_on for current_result in current_results]

    current_ratings = [[average(arr) for arr in json.loads(current_result.result)]
                       for current_result in current_results]

    average_ratings = [[] for i in range(4)]

    total_ratings = [0, 0, 0, 0]

    for i in range(num_entries):
        for j in range(4):
            total_ratings[j] += current_ratings[i][j]
            average_ratings[j].append(total_ratings[j] / (i + 1))

    plot1 = figure(
        width=800, height=600,
        x_axis_label='Date Time', y_axis_label='Engagement',
        x_axis_type='datetime', y_range=(0, 6)
    )

    plot1.line(dates, average_ratings[0], legend='Reinforcement of needs')
    plot1.line(dates, average_ratings[1], legend='Membership', color='red'),
    plot1.line(dates, average_ratings[2], legend="Influence", color='orange'),

    activity_dates = [group_info.created_on for group_info in current_group_infos]
    activity_scores = [group_info.activity_score for group_info in current_group_infos]

    print(activity_dates, activity_scores)

    plot1.line(dates, average_ratings[3], legend="Shared Emotional Connections", color='green')

    plot2 = figure(width=800, height=600,
                   x_axis_label='Date Time', y_axis_label='Activity Score',
                   x_axis_type='datetime')

    plot2.line(activity_dates, activity_scores, legend='Activity Score')

    final_plot = gridplot([[plot1], [plot2]])

    script, div = components(final_plot)

    context = {
        'div': div,
        'script': script
    }

    return context