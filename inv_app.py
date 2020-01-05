import streamlit as st
import os
import pandas as pd
import glob
import plotly.graph_objects as go


def get_root_dir():
    # Gets the path of the current directory
    ROOT_DIR = os.path.abspath(os.curdir)
    return str(ROOT_DIR)


def raw_data_exists(root_dir):
    data_path = root_dir+'\\raw_data.csv'
    if glob.glob(data_path):
        return True
    else:
        return False


@st.cache
def get_raw_data():
    root = get_root_dir()
    data_path = root+'\\raw_data.csv'
    try:
        df = pd.read_csv(data_path, index_col=['Year'])
    except FileNotFoundError:
        st.error('{file} cannot be found in the root directory'.format(
            file=data_path))
    return df


@st.cache
def plot_data(df, name):
    # Create traces
    fig = go.Figure(layout=go.Layout(
        title=go.layout.Title(
            text='Line plot for ticker: {} for chosen columns. '.format(name))
    ))
    options = list(df)
    for opt in options:
        fig.add_trace(go.Scatter(x=df.index, y=df[opt],
                                 mode='lines+markers',
                                 name=opt))
    fig.update_xaxes(ticks="inside")
    fig.update_yaxes(ticks="inside")
    fig.layout.template = 'presentation'
    # options include ggplot2, plotly_dark, seaborn, plotly, plotly_white, presentation, or xgridoff.
    return fig


def dfcol_select(df, name):
    options = st.multiselect(
        'Choose a column from the available data',
        list(df))
    st.write('Below is ticker info for: ', name)
    if options:
        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(df[options])
        fig = plot_data(df[options], name)
        st.plotly_chart(fig)
    else:
        st.warning('Awaiting your selection above......')


def get_year_info(df, name):
    # Dropped because there is not enough data per year
    years = df.Year.unique()
    year = st.sidebar.selectbox('select a year', years)
    st.write('You selected the ticker ', name, ' for the year ', year)
    df_yr = df[df.Year == year]
    st.write(df_yr)


def get_analytics():
    df = get_raw_data()
    tickers = df.Ticker.unique()
    sel = st.sidebar.selectbox('Select a Ticker', tickers)
    df_ticker = df[df.Ticker == sel]
    dfcol_select(df_ticker, sel)


def get_mission_statement():
    root = get_root_dir()
    file = root+'\\plan.txt'
    try:
        f = open(file, 'r').read()
    except FileNotFoundError:
        st.error('{file} cannot be found in the root directory'.format(
            file=file))
    st.markdown(f)


def main():
    st.sidebar.title('Welcome to Investment Group and Analytics')
    sel = st.sidebar.selectbox('Explore!', [
        'Our Mission Statement',
        'Investment and Portfolio Analytics'
    ])
    Dict = {'Investment and Portfolio Analytics': get_analytics,
            'Our Mission Statement': get_mission_statement
            }
    Dict.get(sel, lambda: None)()


if __name__ == '__main__':
    main()
