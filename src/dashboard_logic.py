# src/dashboard_logic.py
import pandas as pd

def calculate_all_kpis(df: pd.DataFrame) -> dict:
    """Calculates all requested KPIs from the dataframe."""
    if df.empty:
        return {
            "total_sales": 0, "no_of_agents": 0, "no_of_cancelled": 0,
            "no_of_contracted": 0, "no_of_reservation": 0, "no_of_deals": 0
        }
    
    # لم نعد بحاجة لـ .str.lower() لأن البيانات نظيفة
    total_sales = df.loc[df['deal_status'] != 'Cancelled', 'unit_price'].sum()
    
    # اسم العمود الصحيح هو 'sales_agent_name'
    no_of_agents = df['sales_agent_name'].nunique()
    
    no_of_deals = len(df)
    no_of_cancelled = (df['deal_status'] == 'Cancelled').sum()
    no_of_contracted = (df['deal_status'] == 'Contracted').sum()
    no_of_reservation = (df['deal_status'] == 'Reservation').sum()

    return {
        "total_sales": total_sales, "no_of_agents": no_of_agents,
        "no_of_deals": no_of_deals, "no_of_cancelled": no_of_cancelled,
        "no_of_contracted": no_of_contracted, "no_of_reservation": no_of_reservation,
    }

# --- الدوال الجديدة للرسوم البيانية ---

def get_deal_status_distribution(df: pd.DataFrame):
    """Counts the number of deals for each status for the donut chart."""
    if df.empty or 'deal_status' not in df.columns:
        return pd.Series()
    return df['deal_status'].value_counts()

def get_deals_by_salesperson_status(df: pd.DataFrame):
    """Groups data by salesperson and deal status for the stacked bar chart."""
    if df.empty or 'sales_agent_name' not in df.columns or 'deal_status' not in df.columns:
        return pd.DataFrame()
    
    # نقوم بتجميع البيانات وعمل unstack لتحويل الحالات إلى أعمدة
    chart_data = df.groupby(['sales_agent_name', 'deal_status']).size().unstack(fill_value=0)
    
    # نضيف عمود المجموع لفرز البيانات
    if 'Contracted' in chart_data.columns:
        chart_data['total_successful'] = chart_data['Contracted']
        return chart_data.sort_values('total_successful', ascending=False)
    
    return chart_data


def get_deals_by_month(df: pd.DataFrame):
    """Groups data by reservation month for the monthly deals bar chart."""
    if df.empty or 'reservation_date' not in df.columns:
        return pd.DataFrame()
    
    df_temp = df.dropna(subset=['reservation_date']).copy()
    df_temp['reservation_date'] = pd.to_datetime(df_temp['reservation_date'])
    df_temp['month_year'] = df_temp['reservation_date'].dt.to_period('M').astype(str)
    monthly_deals = df_temp.groupby('month_year').size().reset_index(name='no_of_deals')
    return monthly_deals.sort_values('month_year')

# --- الدالة الجديدة والمعدلة ---
def get_deals_aggregated_by_month(df: pd.DataFrame):
    """
    Aggregates deals by month name across all years for the seasonality line chart.
    """
    if df.empty or 'reservation_date' not in df.columns:
        return pd.DataFrame()
    
    df_temp = df.dropna(subset=['reservation_date']).copy()
    df_temp['reservation_date'] = pd.to_datetime(df_temp['reservation_date'])
    
    # 1. نستخرج رقم الشهر (للفرز) واسم الشهر (للعرض)
    df_temp['month_num'] = df_temp['reservation_date'].dt.month
    df_temp['month_name'] = df_temp['reservation_date'].dt.strftime('%B')
    
    # 2. نقوم بالتجميع حسب الشهر وعد الصفقات
    monthly_agg = df_temp.groupby(['month_num', 'month_name']).size().reset_index(name='no_of_deals')
    
    # 3. نفرز حسب رقم الشهر لضمان الترتيب الصحيح (يناير، فبراير، ...)
    return monthly_agg.sort_values('month_num')