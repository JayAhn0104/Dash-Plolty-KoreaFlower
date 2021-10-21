from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


def df_top(df, var, top_limit):
    sorted_df = df.sort_values(by=var, ascending=False)
    target_df = sorted_df[:top_limit]
    target_other_df = pd.DataFrame(sorted_df[top_limit:].sum()).transpose()
    out_df = pd.concat([target_df, target_other_df], axis=0)
    out_df.rename({0:'Others'}, inplace=True)
    return out_df


def df_top_years(df, var, top_limit):
    df_list = []
    for year in df.unstack().index:
        year_df = df.xs(year)
        df_list.append(df_top(year_df, var, top_limit)[var])
    out_df = pd.concat(df_list, axis=1)
    out_df.set_axis(df.unstack().index, axis=1, inplace=True)
    out_df.drop('Others', axis=0, inplace=True)
    return out_df


def df_top_reduce(df, top_list, with_others):
    if with_others:
        out_df = df[df['pumName'].isin(top_list)]
    else:
        top_df = df[df['pumName'].isin(top_list)]
        other_df = df[df['pumName'].isin(top_list)].groupby('Year').sum()
        other_df['pumName'] = 'others'
        other_df['Year'] = other_df.index
        out_df = pd.concat([top_df, other_df], axis=0)
    return out_df


def bar_line_fn(target_df, time_unit):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=target_df[time_unit], y=target_df['totQty'], name="totQty"),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=target_df[time_unit], y=target_df['avgAmt'], name="avgAmt",
                   mode='lines'),
        secondary_y=True
    )
    fig.update_layout(
        title_text='totQty & avgAmt from {} to {}'.format(target_df[time_unit].iloc[0],
                                                          target_df[time_unit].iloc[-1])
    )
    fig.update_xaxes(title_text=time_unit)
    fig.update_yaxes(title_text="<b>totQty</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>avgAmt</b>", secondary_y=True)

    return fig


class target_fn:
    def __init__(self, df, name, time_unit, year):
        self.df = df
        self.name = name
        self.time_unit = time_unit
        self.year = year

    def df_target(self, year):
        if isinstance(year, int):
            target_df = self.df[(self.df['pumName'] == self.name) & (self.df['saleYear'] == year)]
            date_df = pd.DataFrame({self.time_unit: self.df[self.df['saleYear'] == year][self.time_unit].unique()})
            target_df = pd.merge(date_df, target_df, on=self.time_unit, how='outer')
        else:
            target_df = self.df[self.df['pumName'] == self.name]
            date_df = pd.DataFrame({self.time_unit: self.df[self.time_unit].unique()})
            target_df = pd.merge(date_df, target_df, on=self.time_unit, how='outer')

        return target_df.groupby(self.time_unit).sum()[['totQty', 'avgAmt', 'saleYear']].reset_index().sort_values(
            by=self.time_unit)

    def plot_target(self, target_df):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=target_df[self.time_unit], y=target_df['totQty'], name="totQty", marker_line_width=0),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=target_df[self.time_unit], y=target_df['avgAmt'], name="avgAmt",
                       mode='lines'),
            secondary_y=True
        )
        fig.update_layout(
            title_text='totQty & avgAmt of {} from {} to {}'.format(self.name, target_df[self.time_unit].iloc[0],
                                                                    target_df[self.time_unit].iloc[-1])
        )
        fig.update_xaxes(title_text=self.time_unit)
        fig.update_yaxes(title_text="<b>totQty</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>avgAmt</b>", secondary_y=True)

        return fig
