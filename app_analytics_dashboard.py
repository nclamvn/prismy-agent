import streamlit as st
import asyncio
import time
from datetime import datetime
from sdip_integration import SDIPSystem as SDIPSmartSystem
from ui_components.modern_components import ModernUIComponents
from analytics.analytics_engine import AnalyticsEngine
from analytics.dashboard_components import DashboardComponents

# Initialize components
ui = ModernUIComponents()
ui.setup_page_config()

# Initialize analytics engine (with session state to persist data)
if 'analytics_engine' not in st.session_state:
    st.session_state.analytics_engine = AnalyticsEngine()

analytics = st.session_state.analytics_engine
dashboard = DashboardComponents()

# Hero Section
ui.create_hero_section()

# Navigation tabs
tab1, tab2, tab3 = st.tabs(["🧠 Smart Translation", "📊 Analytics Dashboard", "⚡ Performance Insights"])

with tab1:
    # Smart Translation Interface
    st.markdown("## 🧠 Smart Translation Interface")
    
    # Smart features info
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
               padding: 20px; border-radius: 16px; margin: 15px 0; border-left: 4px solid #667eea;">
        <h4 style="color: #333; margin: 0 0 10px 0;">🧠 AI Smart Features Active</h4>
        <p style="margin: 0; color: #666;">
            All translations are automatically tracked for analytics and performance insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Translation interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input Document")
        
        input_text = st.text_area(
            "Enter text to translate:",
            height=300,
            placeholder="Paste your document here for AI-powered smart translation with analytics...",
            help="All translations are tracked for performance analytics"
        )
        
        # Language selection
        target_language = st.selectbox(
            "🌍 Target Language",
            ["Vietnamese", "English", "French", "German", "Spanish", "Chinese", "Japanese"],
        )
        
        source_language = st.selectbox(
            "🔤 Source Language", 
            ["Auto-detect", "English", "Vietnamese", "French", "German", "Spanish"]
        )
    
    with col2:
        st.markdown("### 🎯 Smart Translation Result")
        
        if st.button("🧠 Smart Translate with Analytics", type="primary"):
            if input_text:
                # Initialize smart system
                smart_system = SDIPSmartSystem()
                
                # Create placeholders for real-time updates
                status_placeholder = st.empty()
                progress_placeholder = st.empty()
                
                # Step-by-step processing
                with status_placeholder.container():
                    ui.create_status_indicators({
                        "🧠 AI Analysis": "info",
                        "📊 Analytics Recording": "warning"
                    })
                
                with progress_placeholder.container():
                    ui.create_animated_progress_bar(25, "Smart Analysis")
                
                time.sleep(0.8)
                
                try:
                    # Perform smart translation using asyncio.run()
                    result = asyncio.run(smart_system.smart_translate_document(
                        input_text, target_language, 
                        "auto" if source_language == "Auto-detect" else source_language
                    ))
                    
                    # Record in analytics
                    if result['success']:
                        # Add source info to result for analytics
                        result['source_language'] = source_language
                        result['target_language'] = target_language
                        result['original_text'] = input_text
                        
                        # Record translation for analytics
                        record_id = analytics.record_translation(result)
                        
                        with progress_placeholder.container():
                            ui.create_animated_progress_bar(100, "Complete + Recorded")
                        
                        with status_placeholder.container():
                            ui.create_status_indicators({
                                "✅ Translation Complete": "success",
                                "✅ Analytics Recorded": "success",
                                "📊 Dashboard Updated": "success"
                            })
                        
                        time.sleep(1)
                        
                        # Clear progress
                        progress_placeholder.empty()
                        status_placeholder.empty()
                        
                        # Success message with analytics info
                        st.success(f"🧠 Smart Translation Completed! (Analytics ID: {record_id})")
                        
                        # Smart metrics
                        st.markdown("### 📊 Translation Metrics")
                        ui.create_modern_metrics(
                            result['quality_score'],
                            result['processing_time'],
                            result['chunk_count']
                        )
                        
                        # Translation result
                        st.markdown("### 🎯 Translation Result")
                        st.text_area(
                            "AI-Enhanced Translation:",
                            value=result['translated_text'],
                            height=250,
                            help="This translation has been recorded for analytics"
                        )
                        
                        # Quick analytics preview
                        with st.expander("📊 Quick Analytics Preview"):
                            real_time_stats = analytics.get_real_time_stats()
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Session Translations", real_time_stats['translations_this_session'])
                            with col_b:
                                st.metric("Total All Time", real_time_stats['total_translations_all_time'])
                            with col_c:
                                st.metric("Session Quality", f"{real_time_stats['average_quality_this_session']:.2f}")
                            
                            st.info("📊 Visit the Analytics Dashboard tab for detailed insights!")
                    
                    else:
                        progress_placeholder.empty()
                        status_placeholder.empty()
                        st.error(f"❌ Translation failed: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    progress_placeholder.empty()
                    status_placeholder.empty()
                    st.error(f"❌ System error: {e}")
            
            else:
                st.warning("⚠️ Please enter text to translate")

with tab2:
    # Analytics Dashboard
    st.markdown("## 📊 Professional Analytics Dashboard")
    
    # Get comprehensive insights
    insights = analytics.get_comprehensive_insights()
    
    if insights.total_translations == 0:
        st.info("📊 No analytics data yet. Start translating to see comprehensive insights!")
        
        # Show empty state with nice design
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; 
                   background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
                   border-radius: 16px; margin: 20px 0;">
            <h2 style="color: #667eea; margin-bottom: 20px;">📈 Analytics Coming Soon</h2>
            <p style="color: #666; font-size: 1.1rem; margin-bottom: 30px;">
                Translate your first document to unlock powerful analytics insights
            </p>
            <div style="font-size: 4rem; margin: 20px 0;">📊</div>
            <p style="color: #888;">Professional insights • Performance tracking • Quality analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Show full analytics dashboard
        st.success(f"📊 Analytics Dashboard - {insights.total_translations} translations analyzed")
        
        # KPI Metrics
        dashboard.create_kpi_metrics(insights)
        
        # Charts and visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            dashboard.create_language_analysis_chart(insights.most_common_languages)
            dashboard.create_complexity_distribution(insights.complexity_distribution)
        
        with col2:
            dashboard.create_quality_trends_chart(insights.quality_trends)
            
            # Real-time stats
            real_time_stats = analytics.get_real_time_stats()
            dashboard.create_real_time_stats_panel(real_time_stats)
        
        # Performance recommendations
        dashboard.create_recommendations_panel(insights.performance_recommendations)
        
        # Cost analysis
        dashboard.create_cost_analysis(insights.cost_analysis)

with tab3:
    # Performance Insights
    st.markdown("## ⚡ Performance Insights & Analytics")
    
    performance_metrics = analytics.get_performance_metrics()
    
    if not performance_metrics:
        st.info("⚡ No performance data available yet. Complete some translations to see insights!")
    else:
        st.success("⚡ Performance Analysis - Deep dive into system performance")
        
        # Performance radar chart
        dashboard.create_performance_radar_chart(performance_metrics)
        
        # Smart features usage
        smart_features_usage = performance_metrics.get('smart_features_usage', {})
        dashboard.create_smart_features_usage(smart_features_usage)
        
        # Detailed metrics
        with st.expander("📋 Detailed Performance Metrics", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.json({
                    "Documents Processed": performance_metrics.get('total_documents_processed', 0),
                    "Success Rate": f"{performance_metrics.get('success_rate', 0):.1f}%",
                    "Average Quality": f"{performance_metrics.get('average_quality_score', 0):.2f}",
                    "Average Processing Time": f"{performance_metrics.get('average_processing_time', 0):.2f}s"
                })
            
            with col2:
                st.json({
                    "Total Chunks Processed": performance_metrics.get('total_chunks_processed', 0),
                    "Smart Features Used": len(smart_features_usage),
                    "Most Used Feature": max(smart_features_usage.items(), key=lambda x: x[1])[0] if smart_features_usage else "None",
                    "System Efficiency": "Optimal" if performance_metrics.get('success_rate', 0) > 95 else "Good"
                })
        
        # Export functionality
        st.markdown("### 📤 Export Analytics Data")
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("📄 Export as JSON"):
                json_data = analytics.export_analytics_data("json")
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json_data,
                    file_name=f"sdip_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col_export2:
            if st.button("📊 Export as CSV"):
                try:
                    csv_data = analytics.export_analytics_data("csv")
                    st.download_button(
                        label="⬇️ Download CSV", 
                        data=csv_data,
                        file_name=f"sdip_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"CSV export requires pandas: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <h4 style="color: #333;">📊 SDIP Analytics Dashboard</h4>
    <p>Semantic Document Intelligence Platform with Professional Analytics</p>
    <p><small>Smart Translation • Real-time Analytics • Performance Insights • Export Capabilities</small></p>
</div>
""", unsafe_allow_html=True)
