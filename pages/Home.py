# pages/Home.py

import streamlit as st
import plotly.express as px

# استدعاء الدوال اللازمة، بما في ذلك الدالة الجديدة
from src.automation.automation_logic import load_automation_data
from src.dashboard_logic import calculate_all_kpis, get_deal_status_distribution, get_deals_by_salesperson_status, get_deals_aggregated_by_month

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="Main Dashboard")

# عنوان الداشبورد
st.title("📊Overview Dashboard")
st.markdown("---")

# تحميل البيانات
df = load_automation_data()

if df.empty:
    st.warning("Could not load data to display dashboard.")
else:
    # --- عرض مؤشرات الأداء الرئيسية (KPIs) ---
    kpis = calculate_all_kpis(df)
    # ... (كود الـ KPIs يبقى كما هو) ...
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales (Active Deals)", f"{kpis['total_sales']/1_000_000:,.2f} M")
    col2.metric("Total Deals", f"{kpis['no_of_deals']:,}")
    col3.metric("Active Sales Agents", f"{kpis['no_of_agents']:,}")
    col4, col5, col6 = st.columns(3)
    col4.metric("✅ Contracted", f"{kpis['no_of_contracted']:,}")
    col5.metric("📝 Reservation", f"{kpis['no_of_reservation']:,}")
    col6.metric("❌ Cancelled", f"{kpis['no_of_cancelled']:,}")
    
    st.markdown("---")
    st.subheader("Visual Insights")

    # --- الصف الأول من الرسوم البيانية ---
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        # ... (كود Donut Chart يبقى كما هو) ...
        status_dist = get_deal_status_distribution(df)
        if not status_dist.empty:
            fig_status = px.pie(status_dist, values=status_dist.values, names=status_dist.index, title="Deal Status Distribution", hole=.4)
            st.plotly_chart(fig_status, use_container_width=True)
            
    with col_chart2:
        # ... (كود Stacked Bar Chart يبقى كما هو) ...
        sales_data = get_deals_by_salesperson_status(df).head(10)
        if not sales_data.empty:
            if 'total_successful' in sales_data.columns:
                sales_data_to_plot = sales_data.drop(columns=['total_successful'])
            else:
                sales_data_to_plot = sales_data
            fig_sales = px.bar(sales_data_to_plot, x=sales_data_to_plot.columns, y=sales_data_to_plot.index, orientation='h', title="Deals Breakdown per Salesperson (Top 10)", barmode='stack')
            fig_sales.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_sales, use_container_width=True)

    st.divider()

    # --- الصف الثاني: الرسم الخطي المجمع حسب الشهر ---
    st.subheader("Total Deals per Month (Aggregated Across All Years)")
    # --- هذا هو التعديل: نستدعي الدالة الجديدة ---
    monthly_agg_deals = get_deals_aggregated_by_month(df)
    
    if not monthly_agg_deals.empty:
        # ونرسم البيانات الجديدة باستخدام اسم الشهر
        fig_monthly_agg = px.line(
            monthly_agg_deals, 
            x='month_name', 
            y='no_of_deals',
            title="Sales Seasonality: Total Deals for Each Month",
            labels={'month_name': 'Month', 'no_of_deals': 'Total Number of Deals'},
            markers=True
        )
        st.plotly_chart(fig_monthly_agg, use_container_width=True)