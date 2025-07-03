"""
Generador de reportes para el simulador de Chaos Engineering.
Crea reportes en HTML, JSON y CSV con métricas y análisis.
"""

import json
import csv
import time
import os
from typing import Dict, List, Any
from datetime import datetime
import logging

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

logger = logging.getLogger(__name__)

class ReportGenerator:
    """
    Generador de reportes completos para Chaos Engineering.
    """
    DIV_CLOSE = '</div>'
    
    def __init__(self, output_directory: str = "./reports"):
        self.output_directory = output_directory
        self.ensure_output_directory()
        
        logger.info(f"ReportGenerator inicializado con directorio: {output_directory}")
    
    def ensure_output_directory(self):
        """Crea el directorio de salida si no existe"""
        os.makedirs(self.output_directory, exist_ok=True)
    
    def generate_comprehensive_report(self, chaos_system, 
                                    include_charts: bool = True,
                                    formats: List[str] = None) -> Dict[str, str]:
        """
        Genera un reporte completo del sistema de chaos engineering.
        """
        if formats is None:
            formats = ["html", "json"]
        
        # Recopilar todos los datos
        report_data = self._collect_system_data(chaos_system)
        
        # Generar análisis
        analysis = self._generate_analysis(report_data)
        report_data["analysis"] = analysis
        
        # Generar gráficos si está disponible plotly
        charts = {}
        if include_charts and PLOTLY_AVAILABLE:
            charts = self._generate_charts(report_data)
        
        # Generar reportes en diferentes formatos
        output_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if "html" in formats:
            html_file = self._generate_html_report(report_data, charts, timestamp)
            output_files["html"] = html_file
        
        if "json" in formats:
            json_file = self._generate_json_report(report_data, timestamp)
            output_files["json"] = json_file
        
        if "csv" in formats:
            csv_files = self._generate_csv_reports(report_data, timestamp)
            output_files["csv"] = csv_files
        
        logger.info(f"Reporte completo generado: {list(output_files.keys())}")
        return output_files
    
    def _collect_system_data(self, chaos_system) -> Dict[str, Any]:
        """Recopila todos los datos del sistema"""
        data = {
            "timestamp": time.time(),
            "system_info": {},
            "services": {},
            "load_balancer": {},
            "monitoring": {},
            "chaos_monkey": {},
            "experiments": {},
            "patterns": {}
        }
        
        try:
            # Información del sistema
            if hasattr(chaos_system, 'get_system_status'):
                data["system_info"] = chaos_system.get_system_status()
            
            # Servicios
            if hasattr(chaos_system, 'services'):
                for service_name, service in chaos_system.services.items():
                    data["services"][service_name] = service.get_service_metrics()
            
            # Load Balancer
            if hasattr(chaos_system, 'load_balancer'):
                data["load_balancer"] = chaos_system.load_balancer.get_load_balancer_metrics()
            
            # Sistema de monitoreo
            if hasattr(chaos_system, 'monitoring'):
                data["monitoring"] = {
                    "dashboard_data": chaos_system.monitoring.get_dashboard_data(),
                    "health_report": chaos_system.monitoring.generate_health_report(),
                    "active_alerts": chaos_system.monitoring.get_alerts(active_only=True)
                }
            
            # Chaos Monkey
            if hasattr(chaos_system, 'chaos_monkey'):
                data["chaos_monkey"] = chaos_system.chaos_monkey.get_statistics()
            
            # Experimentos
            if hasattr(chaos_system, 'experiment_runner'):
                data["experiments"] = chaos_system.experiment_runner.get_all_experiments_status()
            
        except Exception as e:
            logger.error(f"Error recopilando datos del sistema: {e}")
        
        return data
    
    def _generate_analysis(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera análisis y recomendaciones basadas en los datos"""
        analysis = {
            "summary": {},
            "resilience_score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "risk_assessment": {}
        }
        
        try:
            # Análisis de disponibilidad
            total_services = len(report_data.get("services", {}))
            healthy_services = 0
            total_availability = 0.0
            
            for service_name, service_data in report_data.get("services", {}).items():
                availability = service_data.get("availability", 0)
                total_availability += availability
                
                if availability > 90:
                    healthy_services += 1
                elif availability < 50:
                    analysis["weaknesses"].append(
                        f"Servicio {service_name} tiene baja disponibilidad ({availability:.1f}%)"
                    )
            
            avg_availability = total_availability / max(1, total_services)
            analysis["summary"]["average_availability"] = avg_availability
            analysis["summary"]["healthy_services_ratio"] = healthy_services / max(1, total_services)
            
            # Análisis de experimentos
            experiments_data = report_data.get("experiments", {})
            if experiments_data:
                stats = experiments_data.get("statistics", {})
                success_rate = stats.get("success_rate", 0)
                total_experiments = stats.get("total_experiments", 0)
                
                analysis["summary"]["experiment_success_rate"] = success_rate
                analysis["summary"]["total_experiments"] = total_experiments
                
                if success_rate > 80:
                    analysis["strengths"].append("Alta tasa de éxito en experimentos de chaos")
                elif success_rate < 50:
                    analysis["weaknesses"].append("Baja tasa de éxito en experimentos de chaos")
            
            # Análisis de alertas
            monitoring_data = report_data.get("monitoring", {})
            active_alerts = monitoring_data.get("active_alerts", [])
            critical_alerts = [a for a in active_alerts if a.get("severity") == "CRITICAL"]
            
            analysis["summary"]["active_alerts"] = len(active_alerts)
            analysis["summary"]["critical_alerts"] = len(critical_alerts)
            
            # Cálculo del Resilience Score
            resilience_score = self._calculate_resilience_score(report_data)
            analysis["resilience_score"] = resilience_score
            
            # Recomendaciones basadas en el análisis
            analysis["recommendations"] = self._generate_recommendations(report_data, analysis)
            
            # Evaluación de riesgos
            analysis["risk_assessment"] = self._assess_risks(report_data)
            
        except Exception as e:
            logger.error(f"Error generando análisis: {e}")
        
        return analysis
    
    def _calculate_resilience_score(self, report_data: Dict[str, Any]) -> float:
        """Calcula un score de resiliencia del sistema (0-100)"""
        try:
            # Disponibilidad de servicios (40% del score)
            services = report_data.get("services", {})
            if services:
                avg_availability = sum(s.get("availability", 0) for s in services.values()) / len(services)
                availability_score = (avg_availability / 100) * 40
            else:
                availability_score = 0
            
            # Alertas activas (20% del score)
            monitoring = report_data.get("monitoring", {})
            active_alerts = monitoring.get("active_alerts", [])
            critical_alerts = [a for a in active_alerts if a.get("severity") == "CRITICAL"]
            
            if len(critical_alerts) > 0:
                alerts_score = max(0, 20 - len(critical_alerts) * 5)
            elif len(active_alerts) > 5:
                alerts_score = max(0, 20 - (len(active_alerts) - 5) * 2)
            else:
                alerts_score = 20
            
            # Experimentos de chaos (20% del score)
            experiments = report_data.get("experiments", {})
            if experiments:
                stats = experiments.get("statistics", {})
                success_rate = stats.get("success_rate", 0)
                experiment_score = (success_rate / 100) * 20
            else:
                experiment_score = 10  # Score medio si no hay experimentos
            
            # Diversidad de instancias (10% del score)
            total_instances = 0
            healthy_instances = 0
            
            for service_data in services.values():
                total_instances += service_data.get("total_instances", 0)
                healthy_instances += service_data.get("healthy_instances", 0)
            
            if total_instances > 0:
                instance_health_ratio = healthy_instances / total_instances
                instance_score = instance_health_ratio * 10
            else:
                instance_score = 0
            
            # Recovery capability (10% del score)
            # Basado en tiempo de recuperación de experimentos
            recovery_score = 10  # Placeholder
            
            final_score = availability_score + alerts_score + experiment_score + instance_score + recovery_score
            return min(100, max(0, final_score))
            
        except Exception as e:
            logger.error(f"Error calculando resilience score: {e}")
            return 50.0  # Score neutro en caso de error
    
    def _generate_recommendations(self, report_data: Dict[str, Any], analysis: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        try:
            resilience_score = analysis.get("resilience_score", 0)
            
            # Recomendaciones basadas en resilience score
            if resilience_score < 50:
                recommendations.append("🚨 Score de resiliencia crítico - Revisar inmediatamente la arquitectura")
            elif resilience_score < 70:
                recommendations.append("⚠️ Score de resiliencia bajo - Implementar mejoras de estabilidad")
            
            # Recomendaciones basadas en disponibilidad
            services = report_data.get("services", {})
            low_availability_services = [
                name for name, data in services.items() 
                if data.get("availability", 0) < 90
            ]
            
            if low_availability_services:
                recommendations.append(
                    f"📈 Mejorar disponibilidad de servicios: {', '.join(low_availability_services)}"
                )
            
            # Recomendaciones basadas en instancias
            single_instance_services = [
                name for name, data in services.items()
                if data.get("total_instances", 0) == 1
            ]
            
            if single_instance_services:
                recommendations.append(
                    f"🔄 Añadir redundancia a servicios con instancia única: {', '.join(single_instance_services)}"
                )
            
            # Recomendaciones basadas en experimentos
            experiments = report_data.get("experiments", {})
            if experiments:
                stats = experiments.get("statistics", {})
                if stats.get("total_experiments", 0) == 0:
                    recommendations.append("🧪 Comenzar a ejecutar experimentos de chaos regularmente")
                elif stats.get("success_rate", 0) < 70:
                    recommendations.append("🔧 Investigar causas de falla en experimentos de chaos")
            
            # Recomendaciones basadas en alertas
            monitoring = report_data.get("monitoring", {})
            critical_alerts = [
                a for a in monitoring.get("active_alerts", [])
                if a.get("severity") == "CRITICAL"
            ]
            
            if critical_alerts:
                recommendations.append("🚨 Resolver alertas críticas inmediatamente")
            
            # Recomendaciones de buenas prácticas
            if not recommendations:
                recommendations.extend([
                    "✅ Sistema en buen estado - Continuar con experimentos regulares",
                    "📊 Considerar aumentar la frecuencia de experimentos de chaos",
                    "🔍 Implementar métricas adicionales de observabilidad"
                ])
            
        except Exception as e:
            logger.error(f"Error generando recomendaciones: {e}")
            recommendations.append("❌ Error generando recomendaciones - Revisar logs")
        
        return recommendations
    
    def _assess_risks(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evalúa riesgos del sistema"""
        risks = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "overall_risk_level": "LOW"
        }
        
        try:
            # Riesgos basados en disponibilidad
            services = report_data.get("services", {})
            for service_name, service_data in services.items():
                availability = service_data.get("availability", 0)
                instances = service_data.get("total_instances", 0)
                
                if availability < 50:
                    risks["high_risk"].append(f"Servicio {service_name} con disponibilidad crítica")
                elif availability < 80:
                    risks["medium_risk"].append(f"Servicio {service_name} con disponibilidad baja")
                
                if instances == 1:
                    risks["medium_risk"].append(f"Servicio {service_name} sin redundancia")
            
            # Riesgos basados en alertas
            monitoring = report_data.get("monitoring", {})
            critical_alerts = [
                a for a in monitoring.get("active_alerts", [])
                if a.get("severity") == "CRITICAL"
            ]
            
            if len(critical_alerts) > 3:
                risks["high_risk"].append("Múltiples alertas críticas activas")
            elif len(critical_alerts) > 0:
                risks["medium_risk"].append("Alertas críticas activas")
            
            # Determinar nivel de riesgo general
            if risks["high_risk"]:
                risks["overall_risk_level"] = "HIGH"
            elif len(risks["medium_risk"]) > 3:
                risks["overall_risk_level"] = "HIGH"
            elif risks["medium_risk"]:
                risks["overall_risk_level"] = "MEDIUM"
            
        except Exception as e:
            logger.error(f"Error evaluando riesgos: {e}")
        
        return risks
    
    def _generate_charts(self, report_data: Dict[str, Any]) -> Dict[str, str]:
        """Genera gráficos usando Plotly"""
        charts = {}
        
        try:
            # Gráfico de disponibilidad de servicios
            charts["availability"] = self._create_availability_chart(report_data)
            
            # Gráfico de métricas de tiempo de respuesta
            charts["response_time"] = self._create_response_time_chart(report_data)
            
            # Gráfico de alertas
            charts["alerts"] = self._create_alerts_chart(report_data)
            
            # Gráfico de experimentos
            charts["experiments"] = self._create_experiments_chart(report_data)
            
        except Exception as e:
            logger.error(f"Error generando gráficos: {e}")
        
        return charts
    
    def _create_availability_chart(self, report_data: Dict[str, Any]) -> str:
        """Crea gráfico de disponibilidad de servicios"""
        services = report_data.get("services", {})
        
        if not services:
            return ""
        
        service_names = list(services.keys())
        availabilities = [services[name].get("availability", 0) for name in service_names]
        
        fig = go.Figure(data=[
            go.Bar(x=service_names, y=availabilities, 
                  marker_color=['red' if a < 90 else 'yellow' if a < 95 else 'green' for a in availabilities])
        ])
        
        fig.update_layout(
            title="Disponibilidad de Servicios (%)",
            xaxis_title="Servicios",
            yaxis_title="Disponibilidad (%)",
            yaxis_range=[0, 100]
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_response_time_chart(self, report_data: Dict[str, Any]) -> str:
        """Crea gráfico de tiempos de respuesta"""
        services = report_data.get("services", {})
        
        if not services:
            return ""
        
        service_names = list(services.keys())
        response_times = [services[name].get("avg_response_time_ms", 0) for name in service_names]
        
        fig = go.Figure(data=[
            go.Scatter(x=service_names, y=response_times, mode='lines+markers')
        ])
        
        fig.update_layout(
            title="Tiempo de Respuesta Promedio por Servicio",
            xaxis_title="Servicios",
            yaxis_title="Tiempo de Respuesta (ms)"
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_alerts_chart(self, report_data: Dict[str, Any]) -> str:
        """Crea gráfico de alertas"""
        monitoring = report_data.get("monitoring", {})
        alerts = monitoring.get("active_alerts", [])
        
        if not alerts:
            return "<p>No hay alertas activas</p>"
        
        severity_counts = {}
        for alert in alerts:
            severity = alert.get("severity", "UNKNOWN")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        fig = go.Figure(data=[
            go.Pie(labels=list(severity_counts.keys()), 
                  values=list(severity_counts.values()),
                  marker_colors=['red', 'orange', 'yellow', 'blue'])
        ])
        
        fig.update_layout(title="Distribución de Alertas por Severidad")
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_experiments_chart(self, report_data: Dict[str, Any]) -> str:
        """Crea gráfico de experimentos"""
        experiments = report_data.get("experiments", {})
        stats = experiments.get("statistics", {})
        
        if not stats:
            return "<p>No hay datos de experimentos</p>"
        
        successful = stats.get("successful_experiments", 0)
        failed = stats.get("failed_experiments", 0)
        
        fig = go.Figure(data=[
            go.Pie(labels=['Exitosos', 'Fallidos'], 
                  values=[successful, failed],
                  marker_colors=['green', 'red'])
        ])
        
        fig.update_layout(title="Resultados de Experimentos de Chaos")
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _generate_html_report(self, report_data: Dict[str, Any], charts: Dict[str, str], timestamp: str) -> str:
        """Genera reporte en formato HTML"""
        html_content = self._create_html_template(report_data, charts)
        
        filename = f"chaos_engineering_report_{timestamp}.html"
        filepath = os.path.join(self.output_directory, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Reporte HTML generado: {filepath}")
        return filepath
    
    def _create_html_template(self, report_data: Dict[str, Any], charts: Dict[str, str]) -> str:
        """Crea el template HTML para el reporte"""
        analysis = report_data.get("analysis", {})
        timestamp = datetime.fromtimestamp(report_data.get("timestamp", time.time()))

        resilience_score = analysis.get('resilience_score', 0)
        if resilience_score > 80:
            score_class = 'good'
        elif resilience_score > 60:
            score_class = 'medium'
        else:
            score_class = ''

        html = self._html_header(timestamp, resilience_score, score_class, analysis)
        html += self._html_charts_section(charts)
        html += self._html_analysis_section(analysis)
        html += self._html_recommendations_section(analysis)
        html += self._html_risk_section(analysis)
        html += self._html_services_section(report_data)
        html += '''
</body>
</html>
'''
        return html

    def _html_header(self, timestamp, resilience_score, score_class, analysis):
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Chaos Engineering</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 8px; }}
        .section {{ background-color: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background-color: #ecf0f1; border-radius: 5px; }}
        .score {{ font-size: 48px; font-weight: bold; color: #e74c3c; }}
        .score.good {{ color: #27ae60; }}
        .score.medium {{ color: #f39c12; }}
        .recommendation {{ background-color: #e8f5e9; border-left: 4px solid #4caf50; padding: 10px; margin: 5px 0; }}
        .weakness {{ background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 5px 0; }}
        .strength {{ background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 10px; margin: 5px 0; }}
        .risk-high {{ color: #f44336; font-weight: bold; }}
        .risk-medium {{ color: #ff9800; font-weight: bold; }}
        .risk-low {{ color: #4caf50; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 Reporte de Chaos Engineering</h1>
        <p>Generado el: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    <div class="section">
        <h2>📊 Resumen Ejecutivo</h2>
        <div class="metric">
            <div class="score {score_class}">{resilience_score:.1f}</div>
            <div>Resilience Score</div>
        </div>
        <div class="metric">
            <div style="font-size: 24px;">{analysis.get('summary', {}).get('average_availability', 0):.1f}%</div>
            <div>Disponibilidad Promedio</div>
        </div>
        <div class="metric">
            <div style="font-size: 24px;">{analysis.get('summary', {}).get('total_experiments', 0)}</div>
            <div>Experimentos Ejecutados</div>
        </div>
        <div class="metric">
            <div style="font-size: 24px;">{analysis.get('summary', {}).get('active_alerts', 0)}</div>
            <div>Alertas Activas</div>
        </div>
    </div>
"""

    def _html_charts_section(self, charts):
        if not charts:
            return ''
        html = '<div class="section"><h2>📈 Métricas Visuales</h2>'
        for chart_html in charts.values():
            if chart_html:
                html += f'<div style="margin: 20px 0;">{chart_html}</div>'
        html += self.DIV_CLOSE
        return html
       

    def _html_analysis_section(self, analysis):
        strengths = analysis.get('strengths', [])
        weaknesses = analysis.get('weaknesses', [])
        if not (strengths or weaknesses):
            return ''
        html = '<div class="section"><h2>🔍 Análisis</h2>'
        if strengths:
            html += '<h3>💪 Fortalezas</h3>'
            for strength in strengths:
                html += f'<div class="strength">{strength}</div>'
        if weaknesses:
            html += '<h3>⚠️ Áreas de Mejora</h3>'
            for weakness in weaknesses:
                html += f'<div class="weakness">{weakness}</div>'
        html += '</div>'
        return html

    def _html_recommendations_section(self, analysis):
        recommendations = analysis.get('recommendations', [])
        if not recommendations:
            return ''
        html = '<div class="section"><h2>💡 Recomendaciones</h2>'
        for recommendation in recommendations:
            html += f'<div class="recommendation">{recommendation}</div>'
        html += '</div>'
        return html

    def _html_risk_section(self, analysis):
        risk_assessment = analysis.get('risk_assessment', {})
        if not risk_assessment:
            return ''
        html = '<div class="section"><h2>⚠️ Evaluación de Riesgos</h2>'
        html += f'<p>Nivel de Riesgo General: <span class="risk-{risk_assessment.get("overall_risk_level", "low").lower()}">{risk_assessment.get("overall_risk_level", "LOW")}</span></p>'
        for risk_level in ['high_risk', 'medium_risk', 'low_risk']:
            risks = risk_assessment.get(risk_level, [])
            if risks:
                level_name = risk_level.replace('_', ' ').title()
                html += f'<h4>{level_name}</h4><ul>'
                for risk in risks:
                    html += f'<li>{risk}</li>'
                html += '</ul>'
        html += '</div>'
        return html

    def _html_services_section(self, report_data):
        services = report_data.get('services', {})
        if not services:
            return ''
        html = '<div class="section"><h2>🔧 Estado de Servicios</h2>'
        html += '<table><tr><th>Servicio</th><th>Disponibilidad</th><th>Instancias</th><th>Tiempo Respuesta</th><th>Tasa de Error</th></tr>'
        for service_name, service_data in services.items():
            html += f"""
            <tr>
                <td>{service_name}</td>
                <td>{service_data.get('availability', 0):.1f}%</td>
                <td>{service_data.get('healthy_instances', 0)}/{service_data.get('total_instances', 0)}</td>
                <td>{service_data.get('avg_response_time_ms', 0):.1f}ms</td>
                <td>{service_data.get('error_rate', 0):.2f}%</td>
            </tr>
            """
        html += '</table></div>'
        return html
    
    def _generate_json_report(self, report_data: Dict[str, Any], timestamp: str) -> str:
        """Genera reporte en formato JSON"""
        filename = f"chaos_engineering_report_{timestamp}.json"
        filepath = os.path.join(self.output_directory, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Reporte JSON generado: {filepath}")
        return filepath
    
    def _generate_csv_reports(self, report_data: Dict[str, Any], timestamp: str) -> List[str]:
        """Genera reportes en formato CSV"""
        csv_files = []
        
        # CSV de servicios
        services = report_data.get('services', {})
        if services:
            filename = f"services_report_{timestamp}.csv"
            filepath = os.path.join(self.output_directory, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Servicio', 'Disponibilidad', 'Instancias_Totales', 'Instancias_Saludables', 
                               'Tiempo_Respuesta_ms', 'Tasa_Error_pct', 'Total_Requests'])
                
                for service_name, service_data in services.items():
                    writer.writerow([
                        service_name,
                        service_data.get('availability', 0),
                        service_data.get('total_instances', 0),
                        service_data.get('healthy_instances', 0),
                        service_data.get('avg_response_time_ms', 0),
                        service_data.get('error_rate', 0),
                        service_data.get('total_requests', 0)
                    ])
            
            csv_files.append(filepath)
        
        # CSV de experimentos
        experiments = report_data.get('experiments', {})
        if experiments and 'experiment_history' in experiments:
            filename = f"experiments_report_{timestamp}.csv"
            filepath = os.path.join(self.output_directory, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Nombre', 'Tipo', 'Estado', 'Servicio_Target', 'Duración_s', 
                               'Tiempo_Inicio', 'Tiempo_Fin', 'Mensaje_Error'])
                
                for experiment in experiments['experiment_history']:
                    writer.writerow([
                        experiment.get('name', ''),
                        experiment.get('type', ''),
                        experiment.get('status', ''),
                        experiment.get('target_service', ''),
                        experiment.get('runtime_seconds', 0),
                        experiment.get('started_at', ''),
                        experiment.get('completed_at', ''),
                        experiment.get('error_message', '')
                    ])
            
            csv_files.append(filepath)
        
        logger.info(f"Reportes CSV generados: {len(csv_files)} archivos")
        return csv_files
