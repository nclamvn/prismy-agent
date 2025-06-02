# analytics/dashboard_components.py
"""
Professional Dashboard UI Components
Advanced visualizations and analytics displays
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime, timedelta

class DashboardComponents:
    """Professional dashboard UI components with advanced visualizations"""
    
    @staticmethod
    def create_kpi_metrics(insights: Any):
        """Create professional KPI metrics display"""
        st.markdown("### 📊 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                       padding: 20px; border-radius: 16px; text-align: center; color: white;">
                <h2 style="margin: 0; font-size: 2.5rem; font-weight: 700;">{insights.total_translations}</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Total Translations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            success_color = "#28a745" if insights.success_rate > 0.9 else "#ffc107" if insights.success_rate > 0.7 else "#dc3545"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {success_color}, {success_color}dd); 
                       padding: 20px; border-radius: 16px; text-align: center; color: white;">
                <h2 style="margin: 0; font-size: 2.5rem; font-weight: 700;">{insights.success_rate:.1%}</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Success Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            quality_color = "#28a745" if insights.average_quality > 0.9 else "#17a2b8" if insights.average_quality > 0.8 else "#ffc107"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {quality_color}, {quality_color}dd); 
                       padding: 20px; border-radius: 16px; text-align: center; color: white;">
                <h2 style="margin: 0; font-size: 2.5rem; font-weight: 700;">{insights.average_quality:.2f}</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Avg Quality</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            time_color = "#28a745" if insights.average_processing_time < 2 else "#ffc107" if insights.average_processing_time < 5 else "#dc3545"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {time_color}, {time_color}dd); 
                       padding: 20px; border-radius: 16px; text-align: center; color: white;">
                <h2 style="margin: 0; font-size: 2.5rem; font-weight: 700;">{insights.average_processing_time:.1f}s</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Avg Time</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_language_analysis_chart(language_data: Dict[str, int]):
        """Create language pairs analysis chart"""
        if not language_data:
            st.info("No language data available yet")
            return
        
        st.markdown("### 🌍 Language Pairs Analysis")
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=list(language_data.keys()),
            values=list(language_data.values()),
            hole=0.4,
            marker_colors=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        )])
        
        fig.update_layout(
            title="Most Common Translation Pairs",
            font=dict(family="Inter", size=14),
            showlegend=True,
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod 
    def create_complexity_distribution(complexity_data: Dict[str, int]):
        """Create document complexity distribution chart"""
        if not complexity_data:
            st.info("No complexity data available yet")
            return
        
        st.markdown("### 🧠 Document Complexity Distribution")
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=list(complexity_data.keys()),
                y=list(complexity_data.values()),
                marker_color=['#667eea', '#764ba2', '#f093fb', '#4facfe']
            )
        ])
        
        fig.update_layout(
            title="Documents by Complexity Level",
            xaxis_title="Complexity Level",
            yaxis_title="Number of Documents",
            font=dict(family="Inter", size=12),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_quality_trends_chart(quality_trends: List[Dict[str, Any]]):
        """Create quality trends over time chart"""
        if not quality_trends:
            st.info("Not enough data for trends analysis yet")
            return
        
        st.markdown("### 📈 Quality Trends Over Time")
        
        # Convert to DataFrame
        df = pd.DataFrame(quality_trends)
        
        # Create line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['average_quality'],
            mode='lines+markers',
            name='Average Quality',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        # Add translation count as secondary y-axis
        fig.add_trace(go.Bar(
            x=df['date'],
            y=df['translation_count'],
            name='Translation Count',
            yaxis='y2',
            opacity=0.3,
            marker_color='#764ba2'
        ))
        
        fig.update_layout(
            title="Quality Trends and Volume Over Time",
            xaxis_title="Date",
            yaxis=dict(title="Quality Score", side="left"),
            yaxis2=dict(title="Translation Count", side="right", overlaying="y"),
            font=dict(family="Inter", size=12),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_smart_features_usage(feature_usage: Dict[str, int]):
        """Create smart features usage visualization"""
        if not feature_usage:
            st.info("No smart features usage data available")
            return
        
        st.markdown("### ✨ Smart Features Usage")
        
        # Create horizontal bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=list(feature_usage.values()),
                y=list(feature_usage.keys()),
                orientation='h',
                marker_color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
            )
        ])
        
        fig.update_layout(
            title="Smart Features Utilization",
            xaxis_title="Usage Count",
            yaxis_title="Smart Features",
            font=dict(family="Inter", size=12),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_performance_radar_chart(performance_data: Dict[str, float]):
        """Create performance radar chart"""
        if not performance_data:
            st.info("No performance data available")
            return
        
        st.markdown("### 🎯 Performance Analysis")
        
        # Normalize scores to 0-100 scale for radar chart
        categories = ['Quality Score', 'Speed', 'Success Rate', 'Efficiency', 'Smart Features']
        values = [
            performance_data.get('average_quality_score', 0) * 100,
            max(0, 100 - (performance_data.get('average_processing_time', 0) * 20)),  # Inverse for speed
            performance_data.get('success_rate', 0),
            min(100, performance_data.get('total_chunks_processed', 0) * 5),
            min(100, len(performance_data.get('smart_features_usage', {})) * 25)
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Performance Metrics',
            line_color='#667eea',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            title="Overall Performance Radar",
            font=dict(family="Inter", size=12),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_cost_analysis(cost_data: Dict[str, float]):
        """Create cost analysis visualization"""
        if not cost_data or cost_data.get('total_estimated_cost', 0) == 0:
            st.info("No cost data available")
            return
        
        st.markdown("### 💰 Cost Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Total cost metrics
            st.metric(
                "Total Estimated Cost",
                f"${cost_data.get('total_estimated_cost', 0):.4f}",
                help="Estimated cost based on model usage"
            )
            
            st.metric(
                "Average Cost per Translation",
                f"${cost_data.get('average_cost_per_translation', 0):.4f}",
                help="Average cost per document"
            )
        
        with col2:
            # Cost by model
            cost_by_model = cost_data.get('cost_by_model', {})
            if cost_by_model:
                fig = go.Figure(data=[go.Pie(
                    labels=list(cost_by_model.keys()),
                    values=list(cost_by_model.values()),
                    hole=0.3
                )])
                
                fig.update_layout(
                    title="Cost Distribution by Model",
                    height=300,
                    margin=dict(t=50, b=50, l=50, r=50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_recommendations_panel(recommendations: List[str]):
        """Create recommendations panel with actionable insights"""
        st.markdown("### 💡 Performance Recommendations")
        
        if not recommendations:
            st.success("🎉 No recommendations - your system is performing optimally!")
            return
        
        for i, rec in enumerate(recommendations, 1):
            # Color code recommendations by type
            if "optimal" in rec.lower() or "continue" in rec.lower():
                icon = "🎉"
                color = "#28a745"
            elif "consider" in rec.lower():
                icon = "💡"
                color = "#17a2b8"
            elif "warning" in rec.lower() or "below" in rec.lower():
                icon = "⚠️"
                color = "#ffc107"
            else:
                icon = "📋"
                color = "#6c757d"
            
            st.markdown(f"""
            <div style="background: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1); 
                       border-left: 4px solid {color}; 
                       padding: 15px; 
                       margin: 10px 0; 
                       border-radius: 8px;">
                <div style="font-weight: 600; color: {color};">
                    {icon} Recommendation #{i}
                </div>
                <div style="margin-top: 8px; line-height: 1.5;">
                    {rec}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_real_time_stats_panel(real_time_stats: Dict[str, Any]):
        """Create real-time statistics panel"""
        st.markdown("### ⏱️ Real-Time Session Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #43e97b, #38f9d7); 
                       padding: 15px; border-radius: 12px; text-align: center; color: white;">
                <h3 style="margin: 0;">{real_time_stats.get('translations_this_session', 0)}</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9rem;">This Session</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fa709a, #fee140); 
                       padding: 15px; border-radius: 12px; text-align: center; color: white;">
                <h3 style="margin: 0;">{real_time_stats.get('total_translations_all_time', 0)}</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9rem;">All Time</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #a8edea, #fed6e3); 
                       padding: 15px; border-radius: 12px; text-align: center; color: #333;">
                <h3 style="margin: 0;">{real_time_stats.get('session_duration', 'N/A')}</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 0.9rem;">Session Duration</p>
            </div>
            """, unsafe_allow_html=True)
