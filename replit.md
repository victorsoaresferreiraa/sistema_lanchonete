# Overview

This is a comprehensive snack bar management system built in Python with a Tkinter GUI. The system provides complete control over inventory management, sales recording, data export, and visualization capabilities. It's designed as a standalone desktop application that uses SQLite for local data storage and offers features like stock control, sales history tracking, Excel exports, and interactive charts.

# User Preferences

Preferred communication style: Simple, everyday language.

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
- **Schema Design**: Two main tables - 'estoque' (inventory) and 'historico_vendas' (sales history)
- **Data Management**: DatabaseManager class handles all database operations with connection pooling
- **File Structure**: Organized data directory for database and exported files

## Key Components
- **Inventory Controller**: Manages product addition, updates, and stock queries
- **Sales History Controller**: Handles sales recording and history retrieval
- **Export Controller**: Generates Excel reports using pandas and openpyxl
- **Chart Controller**: Creates interactive visualizations with matplotlib
- **Utility Helpers**: Common functions for window centering, date formatting, and validation

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
- **Nuitka**: Executable packaging for Windows distribution

## Data Processing
- **tabulate**: Table formatting for console output and reports
- **datetime**: Built-in date and time handling for sales timestamps
- **os/sys**: File system operations and path management

## File Formats
- **Excel (.xlsx)**: Export format for inventory and sales reports
- **SQLite (.db)**: Local database storage format
- **PNG/JPG**: Chart export formats via matplotlib