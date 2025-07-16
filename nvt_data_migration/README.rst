Data Migration Tool
===================

Overview
--------

The **Data Migration Tool** is a sophisticated module designed to assist developers in the seamless migration of data from any PostgreSQL database into Odoo. It provides a structured mechanism to define source databases, execute queries, map source columns to target Odoo fields, and sync data in an efficient manner.

Features
--------

- **Data Source Management**:
  Easily define and manage multiple PostgreSQL data sources with fields for host, port, database, user, and password.

- **Query Execution**:
  Execute SQL queries on the defined data source while ensuring that unsafe queries (e.g., `UPDATE`, `DELETE`) are forbidden.

- **Field Mapping**:
  Define how source database columns are mapped to Odoo fields, supporting various data types and transformation methods like fixed values, formulas, or direct column-to-field mapping.

- **Data Synchronization**:
  Sync data from the source database to the target Odoo model using the provided query and field mappings. The module also provides feedback and error handling for partial data transactions.

- **Query Result Visualization**:
  Visualize the results of the executed query in a neat table format, enabling developers to quickly verify and assess the fetched data.

Benefits
--------

- **Flexibility**: Handle a wide range of data transformation requirements, from simple column mappings to more complex formula-based transformations.

- **Security**: Ensure that unsafe SQL statements are not executed, maintaining the integrity of your databases.

- **Efficiency**: Speed up the data migration process by leveraging the structured tools and processes provided by this module.

- **Error Handling**: Receive immediate feedback on any errors encountered during data synchronization, ensuring that issues are quickly identified and addressed.

Installation and Usage
----------------------

To make use of this module:

1. Install the module in your Odoo instance.
2. Navigate to the module's main menu to define your data sources.
3. Set up your data target models and field mappings.
4. Execute your data synchronization processes as needed.

For more detailed instructions and examples, please refer to the module's main documentation.

