"""
graph functions for medium post:
<ACTUAL LINK>
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

__BLUE, __GREEN, __RED, __VIOLET, __YELLOW = sns.color_palette()[:5]

def __format_currency(number):
    "return a pretty currecny string, eg: $1.000.000"
    amount = "{0:,}".format(number)
    return '$%s' % amount

def __get_quarter(dataframe, quarter):
    "get quarter data from given dataframe"
    return dataframe.query('Trimestre == %d' % quarter)

def __income_by_decile_for_quarter(income, title, color=__GREEN, offset=0, label=''):
    "income by decile bar plot"
    deciles = np.arange(1, 11, 1)
    plot = plt.subplot(1, 1, 1)
    plot.set_title(title, y=1.03)
    plot.bar(deciles + offset, income, color=color, width=0.5, label=label)

    # set axes limits.
    plot.set_xlim(0.5, 11)
    plot.set_ylim(0, max(income) * 1.05)

    # set axes ticks.
    yticks = range(0, max(income) + 5000, 5000)
    ylabels = [__format_currency(n) for n in yticks]
    plot.set_yticks(yticks)
    plot.set_yticklabels(ylabels)
    plot.set_xticks(deciles + 0.25)
    plot.set_xticklabels(deciles)
    return plot

def income_by_decile_third_quarter(dataframe):
    "3rd quarter income by decile bar plot"
    title = "Ingresos Medios por Decil - 3er Trimestre - 2016"
    quarter = __get_quarter(dataframe, 3)
    income = quarter['IngresoMedio'].values
    return __income_by_decile_for_quarter(income, title)

def income_by_decile_second_quarter(dataframe):
    "2nd quarter income by decile bar plot"
    title = "Ingresos Medios por Decil - 2do Trimestre - 2016"
    quarter = __get_quarter(dataframe, 2)
    income = quarter['IngresoMedio'].values
    return __income_by_decile_for_quarter(income, title, color=__BLUE)

def income_by_decile_both_quarters(dataframe):
    "2nd and 3rd quarters income by decile bar plot"
    title = "Ingresos Medios por Decil - 2016"

    # quarter data.
    quarter = __get_quarter(dataframe, 3)
    income3 = quarter['IngresoMedio'].values
    quarter = __get_quarter(dataframe, 2)
    income2 = quarter['IngresoMedio'].values

    __income_by_decile_for_quarter(income2, title, color=__BLUE, offset=0.2, label='2do Trimestre')
    plot = __income_by_decile_for_quarter(income3, title, color=__GREEN, label='3er Trimestre')
    plot.legend(loc='upper left')
    return plot

def income_by_decile_both_quarters_with_minimum_wage(dataframe):
    "2nd and 3rd quarters income by decile bar plot, with minimum wage"
    min_wage = 8080
    plot = income_by_decile_both_quarters(dataframe)
    plot.axhline(y=min_wage, color=__RED, linewidth=1, alpha=0.5)
    plot.annotate('Salario Minimo (Enero 2017)',
                  xy=(2, min_wage), xycoords='data',
                  xytext=(+10, +30), textcoords='offset points',
                  fontsize=10, color=__RED, alpha=0.7,
                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color=__RED))
    return plot

def difference_of_income_between_2nd_and_3rd_decile(dataframe):
    "difference of income by decile bar plot"
    quarter = __get_quarter(dataframe, 3)
    income3 = quarter['IngresoMedio'].values
    quarter = __get_quarter(dataframe, 2)
    income2 = quarter['IngresoMedio'].values
    difference = (income3 - income2)
    plot = __income_by_decile_for_quarter(difference, 'Diferencia de Ingresos - 2do y 3er Trimestre', color=__VIOLET)

    yticks = range(0, max(difference) + 500, 500)
    ylabels = [__format_currency(n) for n in yticks]
    plot.set_yticks(yticks)
    plot.set_yticklabels(ylabels)

def difference_of_income_between_2nd_and_3rd_decile_percent(dataframe):
    "percent difference of income by decile bar plot"
    quarter = __get_quarter(dataframe, 3)
    income3 = quarter['IngresoMedio'].values
    quarter = __get_quarter(dataframe, 2)
    income2 = quarter['IngresoMedio'].values
    percent = (income3 - income2) * 100 / income2
    plot = __income_by_decile_for_quarter(percent, 'Diferencia de Ingresos (%) - 2do y 3er Trimestre', color=__YELLOW)

    yticks = range(0, max(percent) + 5, 2)
    ylabels = ['%d%%' % n for n in yticks]
    plot.set_yticks(yticks)
    plot.set_yticklabels(ylabels)
    plot.set_ylim(0, max(percent) * 1.05)
    return plot

def difference_of_income_between_2nd_and_3rd_decile_percent_with_inflation(dataframe):
    plot = difference_of_income_between_2nd_and_3rd_decile_percent(dataframe)
    inflation = 5.1
    plot.axhline(y=inflation, color=__RED, linewidth=1, alpha=0.5)
    plot.annotate('Inflacion Julio - Septiembre',
                  xy=(2, inflation), xycoords='data',
                  xytext=(-50, +75), textcoords='offset points',
                  fontsize=10, color=__RED, alpha=0.7,
                  arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color=__RED))