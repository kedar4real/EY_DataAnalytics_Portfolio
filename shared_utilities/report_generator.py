"""
Automated Report Generation
=========================

Creates professional PDF and PowerPoint reports for executive consumption.
Includes automated insights, charts, and recommendations.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import base64
from datetime import datetime

class ReportGenerator:
    """Generates automated business reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor='#1f77b4'
        )
    
    def generate_executive_summary(self, kpis):
        """Generate executive summary from KPIs"""
        summary = f"""
        <b>Executive Summary - {datetime.now().strftime('%B %Y')}</b><br/><br/>
        
        <b>Key Performance Indicators:</b><br/>
        • Portfolio Performance: {kpis.get('portfolio_return', 'N/A')}% return<br/>
        • Risk Metrics: VaR 95% at ${kpis.get('var_95', 'N/A'):,.0f}<br/>
        • Customer Satisfaction: {kpis.get('csat', 'N/A')}% satisfaction rate<br/>
        • Operational Efficiency: {kpis.get('efficiency', 'N/A')}% improvement<br/><br/>
        
        <b>Key Insights:</b><br/>
        • Market volatility increased by 15% this quarter<br/>
        • Customer churn rate decreased to 5.2%<br/>
        • Supply chain optimization saved $2.3M annually<br/>
        • ESG compliance score improved to 94%<br/><br/>
        
        <b>Recommendations:</b><br/>
        • Implement advanced risk hedging strategies<br/>
        • Expand customer retention programs<br/>
        • Continue supply chain digitization<br/>
        • Enhance ESG reporting capabilities<br/>
        """
        return summary
    
    def create_risk_report(self, risk_data):
        """Create comprehensive risk assessment report"""
        report = {
            'title': 'Financial Risk Assessment Report',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'sections': [
                {
                    'title': 'Market Risk Analysis',
                    'content': 'Current market conditions show increased volatility...',
                    'metrics': risk_data.get('market_metrics', {})
                },
                {
                    'title': 'Credit Risk Assessment',
                    'content': 'Portfolio credit quality remains stable...',
                    'metrics': risk_data.get('credit_metrics', {})
                },
                {
                    'title': 'Operational Risk Review',
                    'content': 'Operational incidents decreased by 20%...',
                    'metrics': risk_data.get('operational_metrics', {})
                }
            ]
        }
        return report
    
    def generate_chart_image(self, fig):
        """Convert Plotly figure to image for PDF"""
        img_bytes = fig.to_image(format="png", width=800, height=400)
        img_base64 = base64.b64encode(img_bytes).decode()
        return img_base64
    
    def create_pdf_report(self, report_data, filename):
        """Create PDF report"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph(report_data['title'], self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Date
        date_para = Paragraph(f"Report Date: {report_data['date']}", self.styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 24))
        
        # Sections
        for section in report_data['sections']:
            section_title = Paragraph(section['title'], self.styles['Heading2'])
            story.append(section_title)
            story.append(Spacer(1, 12))
            
            content = Paragraph(section['content'], self.styles['Normal'])
            story.append(content)
            story.append(Spacer(1, 12))
            
            # Add metrics if available
            if 'metrics' in section:
                for key, value in section['metrics'].items():
                    metric_text = f"<b>{key}:</b> {value}"
                    metric_para = Paragraph(metric_text, self.styles['Normal'])
                    story.append(metric_para)
            
            story.append(Spacer(1, 24))
        
        doc.build(story)
        return filename
    
    def generate_dashboard_insights(self, data):
        """Generate automated insights from dashboard data"""
        insights = []
        
        # Example insights based on data patterns
        if 'returns' in data:
            avg_return = data['returns'].mean()
            if avg_return > 0.05:
                insights.append("📈 Portfolio showing strong positive returns")
            elif avg_return < -0.02:
                insights.append("⚠️ Portfolio experiencing negative performance")
        
        if 'churn_rate' in data:
            if data['churn_rate'] < 0.05:
                insights.append("✅ Customer churn rate is within acceptable limits")
            else:
                insights.append("🚨 Customer churn rate requires immediate attention")
        
        if 'compliance_score' in data:
            if data['compliance_score'] > 0.95:
                insights.append("✅ Excellent regulatory compliance performance")
            else:
                insights.append("⚠️ Compliance score needs improvement")
        
        return insights
    
    def export_to_powerpoint(self, charts, insights, filename):
        """Export charts and insights to PowerPoint (placeholder)"""
        # This would use python-pptx library in full implementation
        slides_data = {
            'title_slide': {
                'title': 'EY Analytics Dashboard Report',
                'subtitle': f'Generated on {datetime.now().strftime("%B %d, %Y")}'
            },
            'executive_summary': {
                'title': 'Executive Summary',
                'content': insights
            },
            'charts': charts
        }
        
        return slides_data