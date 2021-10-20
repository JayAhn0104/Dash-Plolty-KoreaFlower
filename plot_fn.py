from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

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
