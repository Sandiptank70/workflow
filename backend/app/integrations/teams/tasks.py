"""
Microsoft Teams Integration
Supports sending messages and notifications to Teams channels via webhook
"""

import requests
from typing import Dict, Any
from datetime import datetime


def test_connection(credentials: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Test Microsoft Teams webhook connection
    
    Expected credentials:
    {
        "webhook_url": "https://outlook.office.com/webhook/..."
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        
        if not webhook_url:
            return {
                "success": False,
                "message": "Missing webhook_url in credentials"
            }
        
        # Validate webhook URL format
        if not webhook_url.startswith("https://") or "office.com/webhook" not in webhook_url:
            return {
                "success": False,
                "message": "Invalid Teams webhook URL format"
            }
        
        # Send a test message
        test_payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": "Connection Test",
            "themeColor": "0078D4",
            "title": "✅ Connection Test Successful",
            "text": "Your Microsoft Teams integration is working correctly!"
        }
        
        response = requests.post(
            webhook_url,
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Successfully connected to Microsoft Teams!",
                "data": {"status": "connected", "webhook_valid": True}
            }
        else:
            return {
                "success": False,
                "message": f"Connection failed with status {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "Connection timeout. Please check your webhook URL."
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Connection error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }


def send_simple_message(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a simple text message to Teams
    
    params:
    {
        "text": "Your message here"
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        text = params.get("text")
        
        if not text:
            return {
                "success": False,
                "message": "Missing 'text' parameter"
            }
        
        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "text": text
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Message sent successfully to Teams!",
                "data": {"text": text}
            }
        else:
            return {
                "success": False,
                "message": f"Failed to send message: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending message: {str(e)}"
        }


def send_card_message(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a formatted card message to Teams
    
    params:
    {
        "title": "Message Title",
        "text": "Message body text",
        "color": "0078D4" (hex color, optional, default is Teams blue)
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        title = params.get("title")
        text = params.get("text")
        color = params.get("color", "0078D4")  # Default Teams blue
        
        if not text:
            return {
                "success": False,
                "message": "Missing 'text' parameter"
            }
        
        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title or "Notification",
            "themeColor": color,
            "title": title,
            "text": text
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Card message sent successfully!",
                "data": {"title": title, "text": text}
            }
        else:
            return {
                "success": False,
                "message": f"Failed to send card: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending card message: {str(e)}"
        }


def send_notification(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a notification with status indicator
    
    params:
    {
        "title": "Notification Title",
        "message": "Notification message",
        "status": "success" | "warning" | "error" | "info",
        "subtitle": "Optional subtitle"
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        title = params.get("title", "Notification")
        message = params.get("message")
        status = params.get("status", "info").lower()
        subtitle = params.get("subtitle")
        
        if not message:
            return {
                "success": False,
                "message": "Missing 'message' parameter"
            }
        
        # Status color mapping
        status_colors = {
            "success": "28A745",  # Green
            "warning": "FFC107",  # Yellow
            "error": "DC3545",    # Red
            "danger": "DC3545",   # Red (alias)
            "info": "0078D4",     # Blue
            "default": "0078D4"   # Blue
        }
        
        # Status emoji mapping
        status_emojis = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "danger": "❌",
            "info": "ℹ️",
            "default": "📢"
        }
        
        color = status_colors.get(status, status_colors["default"])
        emoji = status_emojis.get(status, status_emojis["default"])
        
        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title,
            "themeColor": color,
            "title": f"{emoji} {title}",
            "text": message
        }
        
        if subtitle:
            payload["sections"] = [{
                "text": subtitle
            }]
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Notification sent successfully! (Status: {status})",
                "data": {"title": title, "status": status}
            }
        else:
            return {
                "success": False,
                "message": f"Failed to send notification: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending notification: {str(e)}"
        }


def send_rich_card(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a rich card with sections and facts
    
    params:
    {
        "title": "Card Title",
        "summary": "Brief summary",
        "sections": [
            {
                "title": "Section Title",
                "facts": [
                    {"name": "Field Name", "value": "Field Value"},
                    {"name": "Status", "value": "Active"}
                ],
                "text": "Additional text for this section"
            }
        ],
        "color": "0078D4" (optional)
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        title = params.get("title", "Notification")
        summary = params.get("summary", title)
        sections = params.get("sections", [])
        color = params.get("color", "0078D4")
        
        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": summary,
            "themeColor": color,
            "title": title
        }
        
        if sections:
            formatted_sections = []
            for section in sections:
                formatted_section = {}
                
                if section.get("title"):
                    formatted_section["activityTitle"] = section["title"]
                
                if section.get("text"):
                    formatted_section["text"] = section["text"]
                
                if section.get("facts"):
                    formatted_section["facts"] = section["facts"]
                
                formatted_sections.append(formatted_section)
            
            payload["sections"] = formatted_sections
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": "Rich card sent successfully!",
                "data": {"title": title, "sections_count": len(sections)}
            }
        else:
            return {
                "success": False,
                "message": f"Failed to send rich card: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending rich card: {str(e)}"
        }


def send_workflow_status(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send workflow execution status notification
    
    params:
    {
        "workflow_name": "My Workflow",
        "status": "success" | "failed" | "running",
        "execution_time": "2.5s" (optional),
        "details": "Additional details" (optional)
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        workflow_name = params.get("workflow_name", "Workflow")
        status = params.get("status", "running").lower()
        execution_time = params.get("execution_time")
        details = params.get("details")
        
        # Status configuration
        status_config = {
            "success": {
                "color": "28A745",
                "emoji": "✅",
                "text": "Completed Successfully"
            },
            "failed": {
                "color": "DC3545",
                "emoji": "❌",
                "text": "Failed"
            },
            "error": {
                "color": "DC3545",
                "emoji": "❌",
                "text": "Error"
            },
            "running": {
                "color": "0078D4",
                "emoji": "🔄",
                "text": "Running"
            },
            "pending": {
                "color": "FFC107",
                "emoji": "⏳",
                "text": "Pending"
            }
        }
        
        config = status_config.get(status, status_config["running"])
        
        facts = [
            {"name": "Workflow", "value": workflow_name},
            {"name": "Status", "value": f"{config['emoji']} {config['text']}"}
        ]
        
        if execution_time:
            facts.append({"name": "Execution Time", "value": execution_time})
        
        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": f"Workflow: {workflow_name}",
            "themeColor": config["color"],
            "title": f"{config['emoji']} Workflow Notification",
            "sections": [{
                "facts": facts
            }]
        }
        
        if details:
            payload["sections"][0]["text"] = details
        
        # Add timestamp
        payload["sections"][0]["facts"].append({
            "name": "Time",
            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Workflow status notification sent! (Status: {status})",
                "data": {"workflow": workflow_name, "status": status}
            }
        else:
            return {
                "success": False,
                "message": f"Failed to send workflow status: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending workflow status: {str(e)}"
        }


def send_alert(credentials: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send an alert/urgent notification
    
    params:
    {
        "title": "Alert Title",
        "message": "Alert message",
        "severity": "critical" | "high" | "medium" | "low",
        "source": "Source of alert" (optional)
    }
    """
    try:
        webhook_url = credentials.get("webhook_url")
        title = params.get("title", "Alert")
        message = params.get("message")
        severity = params.get("severity", "medium").lower()
        source = params.get("source", "Workflow Automation")
        
        if not message:
            return {
                "success": False,
                "message": "Missing 'message' parameter"
            }
        
        # Severity configuration
        severity_config = {
            "critical": {"color": "8B0000", "emoji": "🚨"},  # Dark Red
            "high": {"color": "DC3545", "emoji": "⚠️"},      # Red
            "medium": {"color": "FFC107", "emoji": "⚡"},    # Yellow
            "low": {"color": "17A2B8", "emoji": "ℹ️"}        # Cyan
        }
        
        config = severity_config.get(severity, severity_config["medium"])
        
        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title,
            "themeColor": config["color"],
            "title": f"{config['emoji']} ALERT: {title}",
            "text": message,
            "sections": [{
                "facts": [
                    {"name": "Severity", "value": severity.upper()},
                    {"name": "Source", "value": source},
                    {"name": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                ]
            }]
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Alert sent successfully! (Severity: {severity})",
                "data": {"title": title, "severity": severity}
            }
        else:
            return {
                "success": False,
                "message": f"Failed to send alert: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending alert: {str(e)}"
        }