# Surveillance Management System

## Overview

This is a web-based surveillance management system built with Flask that provides comprehensive monitoring and management capabilities for security cameras, alerts, and forensic analysis. The system features role-based access control, real-time monitoring, and analytics capabilities designed for security operations teams.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **JavaScript**: Vanilla JavaScript for interactive features and real-time updates
- **Styling**: Custom CSS with CSS variables for theming, integrated with Bootstrap
- **Icons**: Feather Icons for consistent iconography
- **Charts**: Chart.js for analytics and data visualization

### Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM
- **Database**: SQLAlchemy with support for SQLite (default) and PostgreSQL
- **Authentication**: Session-based authentication with role-based access control
- **Middleware**: ProxyFix for handling reverse proxy headers

### Data Storage
- **ORM**: SQLAlchemy with DeclarativeBase for database models
- **Database**: SQLite for development, configurable for PostgreSQL in production
- **Connection Management**: Connection pooling with automatic reconnection

## Key Components

### Models
- **User**: User authentication and role management (operations, it, executive)
- **Camera**: IP camera management with status tracking
- **Alert**: Security alert system with severity levels and acknowledgment
- **Event**: Object detection and motion events with metadata

### Routes and Views
- **Authentication**: Login/logout functionality with session management
- **Dashboard**: Overview with statistics and real-time monitoring
- **Camera Management**: Grid and list views for camera monitoring
- **Alert Management**: Alert filtering, acknowledgment, and resolution
- **Analytics**: Data visualization for security metrics
- **Forensic Search**: Historical event search and analysis

### Role-Based Access Control
- **Operations**: Basic monitoring and alert management
- **IT**: Camera management and system administration
- **Executive**: Full access including analytics and forensic tools

## Data Flow

1. **User Authentication**: Session-based login with role determination
2. **Camera Data**: Mock data generation for demonstration purposes
3. **Alert Processing**: Real-time alert generation and management
4. **Event Tracking**: Object detection events with confidence scoring
5. **Analytics**: Data aggregation for reporting and insights

## External Dependencies

### Frontend Libraries
- Bootstrap 5.3.0 for responsive design
- Feather Icons for iconography
- Chart.js for data visualization
- Google Fonts (Inter) for typography

### Backend Dependencies
- Flask web framework
- SQLAlchemy ORM
- Werkzeug for security utilities
- Flask-Login for user session management

## Deployment Strategy

### Development Environment
- SQLite database for local development
- Debug mode enabled with hot reload
- Default admin user creation (admin/admin123)

### Production Considerations
- PostgreSQL database support via DATABASE_URL environment variable
- Session secret configuration via SESSION_SECRET
- ProxyFix middleware for reverse proxy deployment
- Connection pooling with health checks

### Configuration
- Environment-based configuration for database and secrets
- Automatic database table creation on startup
- Default admin user provisioning for initial setup

### Security Features
- Password hashing with Werkzeug
- Role-based access control
- Session management with secure defaults
- Input validation and sanitization

The system is designed to be easily deployable on cloud platforms with minimal configuration changes, supporting both development and production environments through environment variables.