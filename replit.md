# Overview

This is a comprehensive snack bar management system built in Python with a Tkinter GUI. The system provides complete control over inventory management, sales recording, data export, and visualization capabilities. It's designed as a standalone desktop application that uses SQLite for local data storage and offers features like stock control, sales history tracking, Excel exports, and interactive charts.

# User Preferences

Preferred communication style: Simple, everyday language.
System requirements: Executable (.exe) with future update capabilities, pricing system integration, comprehensive stock management.
Build issues: Nuitka download failures resolved with PyInstaller alternative and .bat execution scripts.
Priority: System must work immediately in real lanchonete environment.
Documentation: Complete technical documentation created for maintenance and future modifications.
Knowledge transfer: User needs detailed explanations to understand Python architecture for independent maintenance.
Financial Dashboard: Complete financial dashboard implemented with 8 metrics, 4 chart types, intelligent alerts, and Excel export capabilities (August 2025).
Training Manual: Comprehensive training manual created for optimal system usage, covering all features, daily workflows, best practices, and troubleshooting (August 2025).
Commercial Focus: User interested in real commercial viability and practical implementation. System must be production-ready for actual lanchonete businesses with realistic pricing and market analysis.
Database Issues Resolved: Fixed "no such column id" and "NOT NULL constraint failed" errors through database structure unification and automatic migration system (August 2025).
Universal Accessibility: System optimized for users from children to elderly with comprehensive keyboard shortcuts (F1-F10, Enter, ESC), large fonts (22pt titles, 14pt fields, 28pt totals), high contrast colors, oversized buttons, audio feedback, and intelligent navigation. Complete auto-installer .bat files created for automatic Python download and installation (August 2025).

# System Architecture

## Frontend Architecture
- **GUI Framework**: Tkinter with ttk for modern styling
- **Window Management**: Modular window system with separate windows for main interface, inventory management, and sales history
- **Layout Design**: Responsive design using frames and grid layouts, centralized positioning
- **User Interaction**: Form-based inputs with validation, button-driven navigation

## Backend Architecture
- **Language**: Python 3.10+ with object-oriented design
- **Architecture Pattern**: MVC (Model-View-Controller) separation
- **Module Organization**: Separated into distinct modules (interface, estoque, pedidos, utils)
- **Data Validation**: Robust input validation with error handling and user feedback
- **Business Logic**: Centralized controllers for inventory, sales history, exports, and charts

## Data Storage
- **Database**: SQLite with local file storage (data/banco.db)
- **Schema Design**: Enhanced tables with pricing and configuration support
  - 'estoque': inventory with pricing, categories, and timestamps
  - 'historico_vendas': sales history with financial tracking
  - 'configuracoes': system settings and version control
- **Data Management**: DatabaseManager class handles all database operations with connection pooling
- **File Structure**: Organized data directory for database and exported files
- **Migration System**: Automatic database schema updates for version upgrades

## Key Components
- **Inventory Controller**: Manages product addition, updates, stock queries, and pricing
- **Sales History Controller**: Handles sales recording, history retrieval, and financial tracking
- **Credit Sales System**: Complete customer debt tracking with payment status and due dates
- **Advanced Cash Control**: Opening/closing, withdrawals, reinforcements, and daily reports
- **Backup System**: Complete backup, data-only backup, and Excel export capabilities
- **Export Controller**: Generates Excel reports using pandas and openpyxl
- **Chart Controller**: Creates interactive visualizations with matplotlib
- **Utility Helpers**: Common functions for window centering, date formatting, and validation
- **Version Manager**: Handles system versioning and automatic updates
- **Update Checker**: Monitors for new versions and manages update process

## Testing Framework
- **Testing**: Unit tests using unittest framework
- **Coverage**: Tests for database operations, inventory management, and sales recording
- **Test Structure**: Temporary database creation for isolated testing

# External Dependencies

## Core Libraries
- **tkinter/ttk**: Built-in Python GUI framework for the user interface
- **sqlite3**: Built-in Python database interface for local data storage
- **pandas**: Data manipulation and analysis, used for export functionality
- **openpyxl**: Excel file generation and manipulation for data exports
- **matplotlib**: Chart and graph generation for sales visualization
- **Pillow (PIL)**: Image processing capabilities for GUI enhancements

## Development Tools
- **Poetry**: Dependency management and virtual environment handling
- **pytest**: Testing framework for unit tests
- **Black**: Code formatting and style consistency
- **Flake8**: Code linting and quality analysis
- **MyPy**: Static type checking
- **Nuitka**: Executable packaging for Windows distribution with custom build script
- **Build System**: Automated executable generation with icon and asset embedding

## Data Processing
- **tabulate**: Table formatting for console output and reports
- **datetime**: Built-in date and time handling for sales timestamps
- **os/sys**: File system operations and path management

## File Formats
- **Excel (.xlsx)**: Export format for inventory and sales reports
- **SQLite (.db)**: Local database storage format
- **PNG/JPG**: Chart export formats via matplotlib