"""
MCP Tools for Complaint Management
All tool implementations for the FastMCP server
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from .database import db
from .models import Complaint
from .config import config

logger = logging.getLogger(__name__)


def create_complaint(
    description: str,
    customer_name: str,
    order_id: str,
    priority: str = "Medium",
    remarks: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new complaint
    
    Args:
        description: Detailed description of the complaint
        customer_name: Name of the customer
        order_id: Order ID associated with the complaint
        priority: Priority level (Low, Medium, High, Critical)
        remarks: Optional remarks or notes
    
    Returns:
        Structured response with complaint details
    """
    try:
        # Validate priority
        if priority not in config.VALID_PRIORITIES:
            return {
                "operation": "create_complaint",
                "success": False,
                "error": f"Invalid priority. Must be one of: {', '.join(config.VALID_PRIORITIES)}",
                "result": None
            }
        
        with db.get_session() as session:
            complaint = Complaint(
                description=description,
                customer_name=customer_name,
                order_id=order_id,
                priority=priority,
                status="New",
                remarks=remarks
            )
            session.add(complaint)
            session.flush()
            
            result = complaint.to_dict()
            
            logger.info(f"Created complaint ID: {complaint.complaint_id}")
            
            return {
                "operation": "create_complaint",
                "success": True,
                "message": "Complaint created successfully",
                "result": result
            }
    
    except Exception as e:
        logger.error(f"Error creating complaint: {e}")
        return {
            "operation": "create_complaint",
            "success": False,
            "error": str(e),
            "result": None
        }


def get_complaint(complaint_id: int) -> Dict[str, Any]:
    """
    Get a complaint by ID
    
    Args:
        complaint_id: The complaint ID to retrieve
    
    Returns:
        Structured response with complaint details
    """
    try:
        with db.get_session() as session:
            complaint = session.query(Complaint).filter(
                Complaint.complaint_id == complaint_id
            ).first()
            
            if not complaint:
                return {
                    "operation": "get_complaint",
                    "success": False,
                    "error": f"Complaint with ID {complaint_id} not found",
                    "result": None
                }
            
            return {
                "operation": "get_complaint",
                "success": True,
                "result": complaint.to_dict()
            }
    
    except Exception as e:
        logger.error(f"Error getting complaint: {e}")
        return {
            "operation": "get_complaint",
            "success": False,
            "error": str(e),
            "result": None
        }


def update_complaint(
    complaint_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    remarks: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing complaint
    
    Args:
        complaint_id: The complaint ID to update
        status: New status (optional)
        priority: New priority (optional)
        remarks: New remarks (optional)
        description: New description (optional)
    
    Returns:
        Structured response with updated complaint details
    """
    try:
        # Validate status if provided
        if status and status not in config.VALID_STATUSES:
            return {
                "operation": "update_complaint",
                "success": False,
                "error": f"Invalid status. Must be one of: {', '.join(config.VALID_STATUSES)}",
                "result": None
            }
        
        # Validate priority if provided
        if priority and priority not in config.VALID_PRIORITIES:
            return {
                "operation": "update_complaint",
                "success": False,
                "error": f"Invalid priority. Must be one of: {', '.join(config.VALID_PRIORITIES)}",
                "result": None
            }
        
        with db.get_session() as session:
            complaint = session.query(Complaint).filter(
                Complaint.complaint_id == complaint_id
            ).first()
            
            if not complaint:
                return {
                    "operation": "update_complaint",
                    "success": False,
                    "error": f"Complaint with ID {complaint_id} not found",
                    "result": None
                }
            
            # Update fields if provided
            updated_fields = []
            if status:
                complaint.status = status
                updated_fields.append("status")
            if priority:
                complaint.priority = priority
                updated_fields.append("priority")
            if remarks is not None:
                complaint.remarks = remarks
                updated_fields.append("remarks")
            if description:
                complaint.description = description
                updated_fields.append("description")
            
            complaint.updated_at = datetime.utcnow()
            session.flush()
            
            logger.info(f"Updated complaint ID {complaint_id}: {', '.join(updated_fields)}")
            
            return {
                "operation": "update_complaint",
                "success": True,
                "message": f"Updated fields: {', '.join(updated_fields)}",
                "result": complaint.to_dict()
            }
    
    except Exception as e:
        logger.error(f"Error updating complaint: {e}")
        return {
            "operation": "update_complaint",
            "success": False,
            "error": str(e),
            "result": None
        }


def list_complaints(limit: int = 100) -> Dict[str, Any]:
    """
    List all complaints
    
    Args:
        limit: Maximum number of complaints to return (default: 100)
    
    Returns:
        Structured response with list of complaints
    """
    try:
        with db.get_session() as session:
            complaints = session.query(Complaint).order_by(
                Complaint.complaint_registration_date.desc()
            ).limit(limit).all()
            
            results = [complaint.to_dict() for complaint in complaints]
            
            return {
                "operation": "list_complaints",
                "success": True,
                "count": len(results),
                "result": results
            }
    
    except Exception as e:
        logger.error(f"Error listing complaints: {e}")
        return {
            "operation": "list_complaints",
            "success": False,
            "error": str(e),
            "result": None
        }


def filter_complaints(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    customer_name: Optional[str] = None,
    order_id: Optional[str] = None,
    limit: int = 100
) -> Dict[str, Any]:
    """
    Filter complaints by various criteria
    
    Args:
        status: Filter by status
        priority: Filter by priority
        customer_name: Filter by customer name (partial match)
        order_id: Filter by order ID
        limit: Maximum number of results (default: 100)
    
    Returns:
        Structured response with filtered complaints
    """
    try:
        with db.get_session() as session:
            query = session.query(Complaint)
            
            filters_applied = []
            
            if status:
                if status not in config.VALID_STATUSES:
                    return {
                        "operation": "filter_complaints",
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(config.VALID_STATUSES)}",
                        "result": None
                    }
                query = query.filter(Complaint.status == status)
                filters_applied.append(f"status={status}")
            
            if priority:
                if priority not in config.VALID_PRIORITIES:
                    return {
                        "operation": "filter_complaints",
                        "success": False,
                        "error": f"Invalid priority. Must be one of: {', '.join(config.VALID_PRIORITIES)}",
                        "result": None
                    }
                query = query.filter(Complaint.priority == priority)
                filters_applied.append(f"priority={priority}")
            
            if customer_name:
                query = query.filter(Complaint.customer_name.like(f"%{customer_name}%"))
                filters_applied.append(f"customer_name contains '{customer_name}'")
            
            if order_id:
                query = query.filter(Complaint.order_id == order_id)
                filters_applied.append(f"order_id={order_id}")
            
            complaints = query.order_by(
                Complaint.complaint_registration_date.desc()
            ).limit(limit).all()
            
            results = [complaint.to_dict() for complaint in complaints]
            
            return {
                "operation": "filter_complaints",
                "success": True,
                "filters": filters_applied,
                "count": len(results),
                "result": results
            }
    
    except Exception as e:
        logger.error(f"Error filtering complaints: {e}")
        return {
            "operation": "filter_complaints",
            "success": False,
            "error": str(e),
            "result": None
        }


def delete_complaint(complaint_id: int) -> Dict[str, Any]:
    """
    Delete a complaint by ID
    
    Args:
        complaint_id: The complaint ID to delete
    
    Returns:
        Structured response with deletion confirmation
    """
    try:
        with db.get_session() as session:
            complaint = session.query(Complaint).filter(
                Complaint.complaint_id == complaint_id
            ).first()
            
            if not complaint:
                return {
                    "operation": "delete_complaint",
                    "success": False,
                    "error": f"Complaint with ID {complaint_id} not found",
                    "result": None
                }
            
            complaint_data = complaint.to_dict()
            session.delete(complaint)
            session.flush()
            
            logger.info(f"Deleted complaint ID: {complaint_id}")
            
            return {
                "operation": "delete_complaint",
                "success": True,
                "message": f"Complaint {complaint_id} deleted successfully",
                "result": complaint_data
            }
    
    except Exception as e:
        logger.error(f"Error deleting complaint: {e}")
        return {
            "operation": "delete_complaint",
            "success": False,
            "error": str(e),
            "result": None
        }
