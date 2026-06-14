import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as STO
from datetime import timedelta

con = sqlite3.connect('expenses.db', check_same_thread=False)
cursor = con.cursor()
res = cursor.execute('select * from expenses')
res = res.fetchall()

category_options = ['Food', 'Rent', 'Fun', 'Transport', 'Interest']

def loadcats():
    global category_options
    res = cursor.execute('select * from categories')
    res = res.fetchall()

def intodb():
    if timestamp is None or option is None or spent is None:
        STO.write('Not all of the values were entered.')
        return
    cursor.execute('insert into expenses (date, category, spent) VALUES (?, ?, ?)', (timestamp, option, spent))
    res = cursor.execute('select * from expenses')
    res = res.fetchall()
    con.commit()

def showstats():
    delta = period_end - period_start

    interval = []

    for i in range(delta.days + 1):
        day = period_start + timedelta(days=i)
        interval.append(str(day))

    res = cursor.execute('select * from expenses')
    res = res.fetchall()

    interval_res = [entry for entry in res if entry[0] in interval]

    interval_data = {
        'date': [entry[0] for entry in interval_res],
        'category': [entry[1] for entry in interval_res],
        'spent': [entry[2] for entry in interval_res]
    }

    data = {
        'date': [entry[0] for entry in res],
        'category': [entry[1] for entry in res],
        'spent': [entry[2] for entry in res]
    }

    fig = px.pie(interval_data, values='spent', names='category', title='Overall spending')

    container.plotly_chart(fig)

    container.bar_chart(interval_data, x='date', y='spent', color='category')

@STO.dialog('Add custom category')
def add_category():
    newcat = STO.text_input('Type new category...')
    if STO.button('Add'):
        category_options.append(newcat)
        STO.rerun()

STO.title('dailymoney')

with STO.bottom:
    lefto, righto, t3, t4 = STO.columns(4)
    DN = lefto.button('Edit/delete transactions', type='tertiary')
    DNT = righto.button('Add custom category', type='tertiary', on_click=add_category)
    # STO.caption("maximus.cool")

FToe = STO.container(border=False)

with FToe:
    left, middle, right = STO.columns(3)
    STO.button("Submit transaction", on_click=intodb)

JsoR = STO.container(border=False) # stats container

container = STO.container(border=False)

with JsoR:
    left1, middle1, right1 = STO.columns(3, vertical_alignment='top')

period_start = left1.date_input('Select first date:')
period_end = middle1.date_input('Select last date:')

left1.button('Show stats', on_click=showstats)

spent = left.number_input(
    'Insert amount spent:', value=None, placeholder='Type an amount...'
)

option = middle.selectbox(
    'Pick category:',
    category_options,
    index=None,
    placeholder='Select category...'
)

timestamp = right.date_input('Pick transaction date:')

loadcats()