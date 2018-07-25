import json
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import Label

from .models import (
    Survey,
    SurveyResult
)


def response_with_x_frames(response, origin):

    if origin:
        response['X-FRAME-OPTIONS'] = 'ALLOW-FROM ' + origin

    return response


def average(arr):

    if len(arr) > 0:
        return sum(arr) / len(arr)
    else:
        return 0


def get_groups_context(current_group):

    context = dict()
    plots = []

    current_survey = Survey.objects.all()[0]
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
        width=400, height=400, title='Engagement over time',
        x_axis_label='Date Time', y_axis_label='Engagement',
        x_axis_type='datetime', y_range=(0, 6)
    )

    plot1.line(dates, average_ratings[0], legend='Reinforcement of needs')
    plot1.line(dates, average_ratings[1], legend='Membership', color='red')
    plot1.line(dates, average_ratings[2], legend="Influence", color='orange')


    plot1.line(dates, average_ratings[3], legend="Shared Emotional Connections", color='green')

    if len(dates) < 2:
        p1_label = Label(x=70, y=70, x_units='screen', y_units='screen',
                         text='There is not Engagement  Data', render_mode='css',
                         border_line_color='black', border_line_alpha=1.0,
                         background_fill_color='white', background_fill_alpha=1.0)

        plot1.add_layout(p1_label)

    plots.append([plot1])

    activity_dates = [group_info.created_on for group_info in current_group_infos]

    activity_scores = [group_info.activity_score for group_info in current_group_infos]


    plot2 = figure(width=400, height=400, title='Activity score over time',
                   x_axis_label='Date Time', y_axis_label='Activity Score',
                   x_axis_type='datetime')

    plot2.line(activity_dates, activity_scores, legend='Activity Score')

    plots.append([plot2])

    if len(activity_dates) < 2:
        p2_label = Label(x=70, y=70, x_units='screen', y_units='screen',
                         text='There is not Activity Score data', render_mode='css',
                         border_line_color='black', border_line_alpha=1.0,
                         background_fill_color='white', background_fill_alpha=1.0)

        plot2.add_layout(p2_label)

    final_plot = gridplot(plots)

    script, div = components(final_plot)

    context['div'] = div
    context['script'] = script

    return context
